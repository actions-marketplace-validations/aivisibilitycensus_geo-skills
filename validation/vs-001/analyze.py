"""VS-001 analysis: outcomes exactly as listed in the geo-skills VS-001 protocol.
Input: geo-skills validation/vs-001/data/results/1.5.4.csv and data/human/manifest.csv.
Usage: python3 analyze.py <geo-skills/validation/vs-001> > results.md
"""
import csv, math, sys, json, collections
root = sys.argv[1]
rows = list(csv.DictReader(open(f"{root}/data/results/1.5.4.csv")))
man = {r['id']: r for r in csv.DictReader(open(f"{root}/data/human/manifest.csv")) if r['outcome']=='accepted'}

def wilson(k, n, z=1.959964):
    if n == 0: return (float('nan'),)*2
    p = k/n; d = 1+z*z/n
    c = (p + z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return (c-h, c+h)
def pct(k, n):
    lo, hi = wilson(k, n)
    return f"{k} of {n} ({100*k/n:.1f}%, 95% CI {100*lo:.1f}% to {100*hi:.1f}%)"
def auroc(pos, neg):
    # P(score_ai > score_human) + 0.5 P(tie)
    s = 0.0
    for a in pos:
        for b in neg:
            s += 1 if a > b else 0.5 if a == b else 0
    return s/(len(pos)*len(neg))

H = [r for r in rows if r['corpus']=='human']
A = [r for r in rows if r['corpus']!='human']
out = {}
NAMES = {'d1':'1. Over-explanation','d2':'2. Real things, named','d3':'3. Rhythm and variety','d4':'4. Stock AI phrasing'}
print(f"# VS-001 results, checker 1.5.4 (sha256 {rows[0]['checker_sha256']})\n")
print(f"Articles: {len(H)} human, {len(A)} AI ({', '.join(sorted(set(r['corpus'] for r in A)))})\n")
fh = sum(int(r['flagged']) for r in H); fa = sum(int(r['flagged']) for r in A)
print("## Primary (flagged = 2 or more of the four checks FAIL)\n")
print(f"- False-positive rate (human flagged): {pct(fh,len(H))}")
print(f"- Detection rate (AI flagged): {pct(fa,len(A))}\n")
out['fp']=(fh,len(H),wilson(fh,len(H))); out['det']=(fa,len(A),wilson(fa,len(A)))
print("## Per check (FAIL = level 2, PASS WITH NOTES = level 1)\n\n| Check | Human FAIL | AI FAIL | Human notes | AI notes |\n|---|---|---|---|---|")
for d in ['d1','d2','d3','d4']:
    print(f"| {NAMES[d]} | {pct(sum(r[d]=='2' for r in H),len(H))} | {pct(sum(r[d]=='2' for r in A),len(A))} | {pct(sum(r[d]=='1' for r in H),len(H))} | {pct(sum(r[d]=='1' for r in A),len(A))} |")
print(f"\nArticles with at least one PASS WITH NOTES: human {sum(any(r[d]=='1' for d in ['d1','d2','d3','d4']) for r in H)}, AI {sum(any(r[d]=='1' for d in ['d1','d2','d3','d4']) for r in A)}")
print("\n## FAIL count distribution\n\n| FAILs | Human | AI |\n|---|---|---|")
for k in range(5):
    print(f"| {k} | {sum(int(r['fails'])==k for r in H)} | {sum(int(r['fails'])==k for r in A)} |")
au_f = auroc([int(r['fails']) for r in A],[int(r['fails']) for r in H])
print(f"\nAUROC of FAIL count (AI vs human): {au_f:.3f}")
# reading
H3=[r for r in H if int(r['words'])>=300]; A3=[r for r in A if int(r['words'])>=300]
hh=sum(r['ai_band']=='High' for r in H3); ah=sum(r['ai_band']=='High' for r in A3)
hm=sum(r['ai_band'] in('High','Medium') for r in H3); am=sum(r['ai_band'] in('High','Medium') for r in A3)
au_s = auroc([float(r['ai_score']) for r in A],[float(r['ai_score']) for r in H])
print("\n## AI reading (articles of 300 words or more)\n")
print(f"- Human reading High: {pct(hh,len(H3))}")
print(f"- AI reading High: {pct(ah,len(A3))}")
print(f"- Human reading Medium or High: {pct(hm,len(H3))}")
print(f"- AI reading Medium or High: {pct(am,len(A3))}")
print(f"- AUROC of the reading's score: {au_s:.3f}")
bands=collections.Counter((r['corpus'],r['ai_band']) for r in rows)
print(f"- Band counts: {dict(bands)}")
print("\n## By blog group (human)\n\n| Group | n | flagged | High |\n|---|---|---|---|")
g=collections.defaultdict(list)
for r in H: g[man[r['id']]['group']].append(r)
for k,v in g.items():
    print(f"| {k} | {len(v)} | {sum(int(r['flagged']) for r in v)} | {sum(r['ai_band']=='High' for r in v)} |")
print("\n## By length band\n\n| Words | Human n | Human flagged | AI n | AI flagged |\n|---|---|---|---|---|")
bands_=[(0,1000),(1000,1500),(1500,2000),(2000,10**6)]
for lo,hi in bands_:
    h=[r for r in H if lo<=int(r['words'])<hi]; a=[r for r in A if lo<=int(r['words'])<hi]
    print(f"| {lo} to {hi-1 if hi<10**6 else 'more'} | {len(h)} | {sum(int(r['flagged']) for r in h)} | {len(a)} | {sum(int(r['flagged']) for r in a)} |")
print("\n## By model\n\n| Model folder | n | flagged | reading High (300+ words) |\n|---|---|---|---|")
for m in sorted(set(r['corpus'] for r in A)):
    v=[r for r in A if r['corpus']==m]; v3=[r for r in v if int(r['words'])>=300]
    print(f"| {m} | {len(v)} | {pct(sum(int(r['flagged']) for r in v),len(v))} | {pct(sum(r['ai_band']=='High' for r in v3),len(v3))} |")
print("\n## Words\n")
for name,c in (('human',H),('AI',A)):
    w=sorted(int(r['words']) for r in c); print(f"- {name}: median {w[len(w)//2]}, min {w[0]}, max {w[-1]}")
