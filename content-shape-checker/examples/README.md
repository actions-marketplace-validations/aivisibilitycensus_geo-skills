# Content shape checker: worked example

Two synthetic drafts of the same short blog post for a fictional company, and the review the skill gives the first one. Nothing here is a real business or a real close.

| File | What it is |
|---|---|
| [draft-before.md](draft-before.md) | A 327-word draft built the way generated text often is: category language, a summary at the end of every section, no names or numbers |
| [draft-after.md](draft-after.md) | The same post rewritten around specifics (349 words) |
| [example-review.md](example-review.md) | The skill's report on `draft-before.md`, with a short note on `draft-after.md` |

## Where the numbers come from

The PASS / FAIL levels and the counts in the review are the real output of the web tool's code, run on these two files: `validation/vs-001/checkers/hsc-1.5.4.cjs` (SHA-256 `27941ab5...`, the same file the live tool served on 18 November 2026), called the way `validation/vs-001/check.mjs` calls it (top-level heading removed, then `parseText` and `analyze`). To rerun:

```
cd validation/vs-001
node -e 'const h=require("./checkers/hsc-1.5.4.cjs"),fs=require("fs");for(const f of ["draft-before","draft-after"]){const r=h.analyze(h.parseText(fs.readFileSync("../../content-shape-checker/examples/"+f+".md","utf8").replace(/^# .*\n+/,"")));console.log(f,r.words,[r.d1,r.d2,r.d3,r.d4].map(d=>d.level).join(" "))}'
```

Expected output: `draft-before 327 2 2 2 2` and `draft-after 349 0 0 0 0` (0 = PASS, 1 = PASS WITH NOTES, 2 = FAIL).

The quoted sentences, the strongest habit and the fixes are the review the skill asks for in Step 4, written for this example.

## Who wrote the drafts

Both drafts were written by the Census agent, which is a Claude model, as test material. That matters for one reason: the rewritten draft passes all four checks, and the web tool's separate AI-style reading still puts it at **Medium**. Passing the shape checks is not proof that a person wrote something, and failing them is not proof that a model did. The skill says so in "What this skill does not do", and this example shows it.

## License

Text of the drafts and the review: CC BY 4.0, like the rest of the skill text ([LICENSE-docs](../../LICENSE-docs)).
