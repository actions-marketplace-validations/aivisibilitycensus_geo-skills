# SV-001: do GEO audit scores go with being named by AI?

Pre-registered 10 November 2026, before the Census100 project management collection (13 and 17 November 2026) and before any score was taken. The commit that added this file is the timestamp. Nothing below changes once scoring starts, except to correct an error, and any correction is logged at the end of this file with its date.

## Question

Open-source GEO audit tools give a page a score out of 100. Do brands whose pages score higher get named more often in AI answers?

A search of nine public GEO skill repositories on 10 November 2026 found no published test of that. It found one stated claim: the client report template in zubair-trabzada/geo-seo-claude (`skills/geo-report/SKILL.md`, commit `989cae0`) tells the assistant to base a dollar estimate on "A 10-point GEO score improvement typically correlates with a 15-25% increase in AI citation frequency", with no source given in that file. The same line appears in TheSmokeDev/geo-skills.

This study tests the general question on one category with live answer data. It does not test that sentence directly: the "GEO score" in it is a composite that an AI model assigns during the audit, and this study uses the repository's fixed citability script, one component of that audit, because it gives the same number on every run.

## What is being tested, and what is not

Two scoring scripts, chosen because they run without an AI model in the loop, so the same page gives the same score to anyone who runs them:

| Script | Repository | Commit | What its authors say it measures |
|---|---|---|---|
| `scripts/citability_scorer.py` | zubair-trabzada/geo-seo-claude | `989cae01e8ebbc42a9ec798eb9e7cb423f5ec89c` | "how likely AI models are to cite" a page's passages |
| `cli/geo-audit.mjs` | Fangx-AI/geo-doctor | `3c158973a9388b66cbb33a3c722ecf26a677b971` | whether AI crawlers can read the page. Its own output says "Technical audit only, not an AI ranking" |

The second script does not claim to predict anything. It is included because access scores are widely read as visibility scores, and its authors' caution is stated here so the result is not read as a failure of a claim they did not make.

Not tested: audits where an AI model assigns the score (the same page can get different scores on different runs, so there is no fixed number to test), and any paid tool.

Both scripts are run exactly as published at those commits, with default settings, by `validation/sv-001/run_scores.py` in the workflow `.github/workflows/sv-001.yml`, on a GitHub-hosted runner. No threshold, weight or line of either script is changed.

## Brands and pages

The 20 brands in the Census100 project management category, fixed on 30 October 2026 (`config/categories/project-management.yml` in aivisibilitycensus/census-index). One page per brand, listed in `validation/sv-001/urls.csv`: `https://<domain>/`, following redirects, except two brands whose Census entry is a product on a larger company site (Jira on atlassian.com, Zoho Projects on zoho.com), where the product page is used.

A brand site and a product page are not the same kind of page. That is a known weakness; the two are flagged in the readout and the primary result is also reported without them.

## Scores

Each script is run once per page, on one day between 13 and 17 November 2026. The score used is the number the script reports: `average_citability_score` and `score`. A page the script cannot fetch or score is recorded as missing with the reason, tried at most twice, and never scored by hand. Raw output for every page is committed with the scores.

## Outcome

From the Census100 collection for this category (ChatGPT, Gemini and Google AI Mode; 25 fixed questions; runs on 13 and 17 November 2026), for each brand:

- **Named share:** answers that name the brand, divided by all answers collected.
- **Cited share:** answers that cite a URL on the brand's domain, divided by all answers collected.

Brand and domain matching is the Census100's own, fixed in the category file before collection. The people running the scores do not see outcome counts before the scores are committed, and the collection does not use the scores.

## Analysis

`validation/sv-001/analyze.py`, committed with this protocol.

**Primary.** For each script, Spearman's rank correlation between score and named share pooled over the three engines. Two tests, each at alpha 0.025 (0.05 split between them), two-sided, p from 100,000 seeded permutations (seed 20261110).

**Decision rule, fixed now:**

| Result | Reported as |
|---|---|
| rho above 0 and p below 0.025 | The score goes with being named in this category |
| rho below 0 and p below 0.025 | The score goes against being named in this category |
| Anything else | No relationship detected |
| Fewer than 15 brands scored by a script | That script is not testable here |
| 15 or more of a script's 20 scores inside one closed 10-point band (checked after the 15-brand minimum and before the other rows; added by the correction of 16 November 2026) | The scores do not vary enough across these pages to test the question |

**Secondary, reported without verdicts:** the same correlation per engine; against cited share; with Ahrefs Domain Rating held fixed (partial rank correlation; DR read on the scoring day), because large brands may both score well and be named often for unrelated reasons; and the primary test without the two product pages.

## What 20 brands can and cannot show

Simulated with the analysis script before registration (2,000-permutation tests on 1,500 simulated samples of 20):

| True rank correlation | Chance this study detects it |
|---|---|
| 0.4 | 25% |
| 0.5 | 42% |
| 0.6 | 63% |
| 0.7 | 86% |
| 0 (no relationship) | 2% false alarms |

So this study can find a strong relationship and will usually miss a moderate one. "No relationship detected" will mean exactly that. It will not mean the scores are useless, and the write-up will not say so.

The geo-audit score checks whether AI crawlers can reach and read one brand-owned page at the moment of the check. The outcome counts how often the brand is named in AI answers, which often draw on other pages, including third-party ones. A null result for that script means its score does not track naming for these 20 brands, not that its checks are useless. (Added by the correction of 16 November 2026.)

It is one software category of large, well-known brands. A result here does not carry over to local firms or small sites.

## Prediction

Recorded before any data: neither script's score will show a detectable relationship with named share. Reason for the guess: the brands named most in this category are the largest, and page structure is unlikely to separate them. This is a guess, written down so it can be wrong in public.

## Replication

The same protocol runs on each later Census100 category (CRM is next) with the same two commits. Results are reported per category first, then pooled. If either repository's authors publish a test of their own score, it is linked from the write-up.

## Publication

The result is published on aivisibilitycensus.com/experiments/ whichever way it comes out, with scores, outcome counts and raw script output under CC BY 4.0. The authors of both scripts are sent the result before publication and their replies are linked or quoted with permission.

## Conflicts of interest

The AI Visibility Census publishes its own free GEO skills in this repository, including a page check (`geo-check`) that gives findings and no score. A result against scores would suit that design. This is why the scripts, commits, pages, outcome, test and decision rule are fixed here before any data exists.

## Corrections

- 10 November 2026, about 17:00 UTC, before any score or answer was collected: the Question section first said the review covered ten repositories and found no claim. It covered nine outside repositories, and a second search found the unsourced "10-point" claim quoted above. The wording was corrected. No script, page, outcome, test or rule changed.
- 16 November 2026, 13:25 UTC. This is an addition, not the correction of an error, so it departs from the rule at the top of this file that nothing changes after scoring starts except to fix an error. It is made anyway because the geo-doctor maintainer pointed out that the pre-registered analysis could read a correlation from scores with too little spread to carry one, and it is logged here so the departure is visible. It was made after scoring: both scripts scored the 20 pages on 14 November 2026 at 09:01 UTC (`sv-001/runs/2026-11-14/scores.csv`), so the scores already existed when these rules were written. It comes before any outcome is computed (collection dates 13 and 17 November 2026). The person who wrote it did not open the score file or the raw output first. It follows a comment by the geo-doctor maintainer on Fangx-AI/geo-doctor#53. The primary statistic, the permutation test, alpha and the existing rows of the decision rule are unchanged. `sv-001/analyze.py` and its tests are updated in the same commit to apply items 1 and 2.
  1. **Score spread first.** For each script, the readout shows the scores sorted, how many are 90 or above, and (for geo-audit) how many are at or below 60, the cap `cli/geo-audit.mjs` applies when a critical check fails. If 15 or more of a script's 20 scores fall inside one closed 10-point band (for example 85 to 95 inclusive; if fewer than 20 pages are scored: three quarters of those scored, rounded up), that script's result is reported as "the scores do not vary enough across these pages to test the question" and no correlation is read for it. This adds one row to the decision rule, checked after the 15-brand minimum and before every other row.
  2. **Ties.** Spearman's rho already uses average ranks for tied scores (`ranks()` in `analyze.py`, unchanged). The readout adds the share of tied scores for each script, and Kendall's tau-b beside rho as a secondary statistic, without a verdict.
  3. **What the geo-audit score measures.** A short version is added to "What 20 brands can and cannot show". In full: geo-audit checks whether AI crawlers can reach and read one brand-owned page at the moment of the check. Its critical checks are fetch and HTTP status, a readable robots.txt that allows AI search crawlers, responses to crawler user agents, noindex in header or meta, and extractable text; it also scores redirects, canonical, title, meta description, H1, language attribute, sitemap and JSON-LD validity. The outcome counts how often the brand is named in AI answers, and those answers often draw on other pages, including third-party ones. A null result means the score does not track naming for these 20 brands. It does not mean the checks are useless.
  4. **Version.** On 16 November 2026 the maintainer stated that `cli/geo-audit.mjs` is unchanged between the pinned commit `3c15897` and master. Checked the same day: `git diff 3c158973a9388b66cbb33a3c722ecf26a677b971 fc0349a -- cli/geo-audit.mjs` is empty (`fc0349a` was master on 16 November). No re-run is needed.
  Wording of this entry tightened at about 13:40 UTC the same day after an independent check: it now states the departure from the no-change rule, the order of the checks, the closed band and the full list of geo-audit checks. No rule, threshold or code changed in that edit.
