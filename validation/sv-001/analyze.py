#!/usr/bin/env python3
"""SV-001 analysis: do GEO audit scores go with being named by AI engines?

  python3 analyze.py scores.csv outcomes.csv --out-md readout.md

scores.csv    domain, scorer, score            (written by run_scores.py)
outcomes.csv  domain, engine, answers, named, cited   (exported from the Census100 collection)
covars.csv    domain, dr                       (optional, --covars; Ahrefs Domain Rating)

For each scorer it first reports the spread of the scores (correction of 16 Nov 2026 in the
protocol), then, for each scorer and outcome, Spearman's rank correlation with a p-value from
seeded permutations and Kendall's tau-b beside it. Standard library only. The decision rule is fixed in
../SV-001-protocol.md and is not a parameter here.
"""
import argparse
import csv
import math
import random
import sys
from collections import defaultdict

SEED = 20261110
PERMUTATIONS = 100000
ALPHA = 0.025            # two primary tests, Bonferroni from 0.05
MIN_N = 15               # fewer scored brands than this: arm reported as not testable
BAND = 10                # correction 16 Nov 2026: spread check band width, in score points
BAND_SHARE = 0.75        # 15 of 20: this share of scores (rounded up) inside one band = too little spread
HIGH = 90                # reported: scores at or above this
GEO_AUDIT_CAP = 60       # geo-audit caps the score at 60 when a critical check fails (cli/geo-audit.mjs)


def ranks(values):
    """Average ranks, ties shared."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[order[k]] = r
        i = j + 1
    return out


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0:
        return float("nan")
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(sxx * syy)


def spearman(x, y):
    return pearson(ranks(x), ranks(y))


def perm_p(x, y, n_perm=PERMUTATIONS, seed=SEED):
    """Two-sided permutation p-value for Spearman's rho."""
    rx, ry = ranks(x), ranks(y)
    obs = pearson(rx, ry)
    if math.isnan(obs):
        return obs, float("nan")
    rng = random.Random(seed)
    hits = 0
    ry = list(ry)
    for _ in range(n_perm):
        rng.shuffle(ry)
        if abs(pearson(rx, ry)) >= abs(obs) - 1e-12:
            hits += 1
    return obs, (hits + 1) / (n_perm + 1)


def kendall_tau_b(x, y):
    """Kendall's tau-b, ties corrected. Secondary statistic (correction of 16 Nov 2026)."""
    n = len(x)
    conc = disc = tx = ty = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy = x[i] - x[j], y[i] - y[j]
            if dx == 0 and dy == 0:
                continue
            if dx == 0:
                tx += 1
            elif dy == 0:
                ty += 1
            elif (dx > 0) == (dy > 0):
                conc += 1
            else:
                disc += 1
    den = math.sqrt((conc + disc + tx) * (conc + disc + ty))
    return float("nan") if den == 0 else (conc - disc) / den


def tied_share(values):
    """Share of scores that equal at least one other score."""
    if not values:
        return float("nan")
    counts = defaultdict(int)
    for v in values:
        counts[v] += 1
    return sum(c for c in counts.values() if c > 1) / len(values)


def max_in_band(values, width=BAND):
    """Largest number of scores that fit inside one closed band of the given width."""
    v = sorted(values)
    best = j = 0
    for i in range(len(v)):
        while v[i] - v[j] > width:
            j += 1
        best = max(best, i - j + 1)
    return best


def spread(scorer, values):
    """Spread check fixed by the 16 Nov 2026 correction. Read before any correlation."""
    n = len(values)
    need = math.ceil(BAND_SHARE * n) if n else 0
    in_band = max_in_band(values)
    return {"scorer": scorer, "n": n, "sorted": sorted(values),
            "high": sum(1 for v in values if v >= HIGH),
            "capped": sum(1 for v in values if v <= GEO_AUDIT_CAP) if "geo-doctor" in scorer else None,
            "in_band": in_band, "need": need, "tied_share": tied_share(values),
            "too_narrow": n > 0 and in_band >= need}


def partial_spearman(x, y, z):
    """Spearman correlation of x and y with z held fixed (first-order partial on ranks)."""
    rxy, rxz, ryz = spearman(x, y), spearman(x, z), spearman(y, z)
    den = math.sqrt((1 - rxz ** 2) * (1 - ryz ** 2))
    return float("nan") if den == 0 else (rxy - rxz * ryz) / den


def power(n, rho, alpha=ALPHA, sims=2000, n_perm=2000, seed=SEED):
    """Share of simulated samples (bivariate normal, correlation rho) where the permutation
    test rejects at alpha. Used once, to state in the protocol what n can detect."""
    rng = random.Random(seed)
    wins = 0
    for s in range(sims):
        x = [rng.gauss(0, 1) for _ in range(n)]
        y = [rho * a + math.sqrt(1 - rho ** 2) * rng.gauss(0, 1) for a in x]
        _, p = perm_p(x, y, n_perm=n_perm, seed=seed + s)
        if p < alpha:
            wins += 1
    return wins / sims


def read_scores(path):
    out = defaultdict(dict)
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (r.get("score") or "").strip() == "":
                continue
            out[r["scorer"]][r["domain"].strip().lower()] = float(r["score"])
    return out


def read_outcomes(path):
    """Return {domain: {engine: (answers, named, cited)}} plus an 'all' engine pooled over engines."""
    out = defaultdict(dict)
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = r["domain"].strip().lower()
            out[d][r["engine"].strip().lower()] = (int(r["answers"]), int(r["named"]), int(r["cited"]))
    for d, eng in out.items():
        eng["all"] = tuple(sum(v[i] for v in eng.values()) for i in range(3))
    return out


def read_covars(path):
    with open(path, newline="", encoding="utf-8") as f:
        return {r["domain"].strip().lower(): float(r["dr"]) for r in csv.DictReader(f) if (r.get("dr") or "").strip()}


NARROW = "the scores do not vary enough across these pages to test the question"


def verdict(n, rho, p, too_narrow=False):
    if n < MIN_N:
        return "not testable (fewer than %d scored brands)" % MIN_N
    if too_narrow:
        return NARROW
    if math.isnan(rho):
        return "not testable (no variation)"
    if p < ALPHA and rho > 0:
        return "score goes with the outcome"
    if p < ALPHA and rho < 0:
        return "score goes against the outcome"
    return "no relationship detected"


def analyze(scores, outcomes, covars=None, n_perm=PERMUTATIONS):
    rows = []
    engines = sorted({e for v in outcomes.values() for e in v})
    engines = ["all"] + [e for e in engines if e != "all"]
    for scorer in sorted(scores):
        narrow = spread(scorer, list(scores[scorer].values()))["too_narrow"]
        for engine in engines:
            for measure, idx in (("named", 1), ("cited", 2)):
                doms = [d for d in sorted(scores[scorer]) if engine in outcomes.get(d, {}) and outcomes[d][engine][0] > 0]
                x = [scores[scorer][d] for d in doms]
                y = [outcomes[d][engine][idx] / outcomes[d][engine][0] for d in doms]
                if len(doms) < 3:
                    rho, p, tau = float("nan"), float("nan"), float("nan")
                else:
                    rho, p = perm_p(x, y, n_perm=n_perm)
                    tau = kendall_tau_b(x, y)
                part = float("nan")
                if covars and len(doms) >= 4 and all(d in covars for d in doms):
                    part = partial_spearman(x, y, [covars[d] for d in doms])
                primary = engine == "all" and measure == "named"
                rows.append({"scorer": scorer, "engine": engine, "measure": measure, "n": len(doms),
                             "rho": rho, "p": p, "tau_b": tau, "partial_rho_dr": part, "primary": primary,
                             "verdict": verdict(len(doms), rho, p, narrow) if primary else ""})
    return rows


def fmt(v, nd=2):
    return "n/a" if v is None or (isinstance(v, float) and math.isnan(v)) else f"{v:.{nd}f}"


def render(rows, spreads=()):
    out = ["# SV-001 readout", ""]
    if spreads:
        out += ["## Score spread (read first)", "",
                f"If {int(BAND_SHARE * 100)}% or more of a script's scores (15 of 20) sit inside one {BAND}-point band, "
                "no correlation is read for that script.", "",
                "| Scorer | Pages scored | Scores, sorted | 90 or above | At or below the 60 cap | "
                f"Most inside one {BAND}-point band | Tied scores | Too little spread |",
                "|---|---|---|---|---|---|---|---|"]
        for s in spreads:
            cap = "n/a" if s["capped"] is None else str(s["capped"])
            out.append(f"| {s['scorer']} | {s['n']} | {', '.join(f'{v:g}' for v in s['sorted'])} | {s['high']} | {cap} | "
                       f"{s['in_band']} (limit {s['need']}) | {fmt(s['tied_share'] * 100, 0)}% | {'yes' if s['too_narrow'] else 'no'} |")
        out.append("")
    out += [
           "Spearman rank correlation between each audit score and the share of Census100 answers "
           f"that name (or cite) the brand. p from {PERMUTATIONS:,} seeded permutations, two-sided. "
           f"Primary tests: pooled engines, named share, one per scorer, alpha {ALPHA} each.", "",
           "## Primary tests", "", "| Scorer | Brands | rho | p | Verdict |", "|---|---|---|---|---|"]
    for r in rows:
        if r["primary"]:
            out.append(f"| {r['scorer']} | {r['n']} | {fmt(r['rho'])} | {fmt(r['p'], 3)} | {r['verdict']} |")
    out += ["", "\"No relationship detected\" is not \"the score does not work\". With about 20 brands "
            "this test only finds strong relationships; see the protocol for what it can detect.", "",
            "## All comparisons (secondary, no verdicts)", "",
            "| Scorer | Engine | Outcome | Brands | rho | p | Kendall tau-b | rho with DR held fixed |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['scorer']} | {r['engine']} | {r['measure']} | {r['n']} | {fmt(r['rho'])} | "
                   f"{fmt(r['p'], 3)} | {fmt(r['tau_b'])} | {fmt(r['partial_rho_dr'])} |")
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scores")
    ap.add_argument("outcomes")
    ap.add_argument("--covars")
    ap.add_argument("--out-md")
    a = ap.parse_args(argv)
    scores = read_scores(a.scores)
    spreads = [spread(k, list(v.values())) for k, v in sorted(scores.items())]
    rows = analyze(scores, read_outcomes(a.outcomes), read_covars(a.covars) if a.covars else None)
    md = render(rows, spreads)
    if a.out_md:
        with open(a.out_md, "w", encoding="utf-8") as f:
            f.write(md)
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
