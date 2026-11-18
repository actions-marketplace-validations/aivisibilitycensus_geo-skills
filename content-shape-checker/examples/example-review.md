# Example review: draft-before.md

Synthetic example. See [README.md](README.md) for where the numbers come from and who wrote the drafts.

Draft: "Why month-end close matters for growing businesses", 327 words in 5 sections (top heading not counted).

## 1. Results

| Check | Result | Behind it (web tool code, hsc 1.5.4, where checks 3 and 4 are called "Rhythm and variety" and "Stock AI phrasing") |
|---|---|---|
| Over-explanation | FAIL | 2 strikes, 6.1 per 1,000 words (fails above 3) |
| Real things, named | FAIL | 0 anchors per 100 words; 5 of 5 sections have no number, name, date or place |
| Scaffold variance | FAIL | 6 strikes: section length variation 0.09; paragraph length variation 0.23; sentence spread 3.6 words; no sentence of 30 words or more; no asides; 5 lists of three |
| Profundity inflation | FAIL | 7 strikes, 21.4 per 1,000 words; 2 "not just X, but Y" |

Eight flags below come from the skill's written rules rather than the web tool's four checks. They are marked "(skill rules)", so you can see where the two differ. Two of those sentences ("Overall..." and "In short...") the tool does flag, for other reasons, under Profundity inflation.

## 2. The strongest habit

**Nothing in the post is specific.** No company, number, date, person or place appears anywhere, so every section has to make its point with adjectives and a closing summary. Fix that and most of the other flags go with it: a sentence with a real number in it rarely needs "This means that" after it.

## 3. Flagged sentences

### Over-explanation

- "Ultimately, a process that does not scale will hold the business back." Section-closing summary. Fix: cut it; the section has already said this.
- "Technology plays a key role in a modern close." Significance claim. Fix: name the one tool or step that saved time, and how much.
- "In other words, the close is where clarity begins." (skill rules: interprets the line before it) Fix: cut.
- "This means that leaders are often flying blind." (skill rules: interprets the line before it) Fix: cut, or replace with what actually went wrong, e.g. "[the report that went out late, and when]".
- "This shows that growth and complexity go hand in hand." (skill rules: interprets the line before it) Fix: cut.
- "Overall, a modern close is not just faster, but more strategic." (skill rules: section-closing summary) Fix: cut.
- "In short, small changes can lead to transformative results." (skill rules: section-closing summary) Fix: replace with the one result the reader can check, e.g. "[days to close before and after]".

### Real things, named

- No anchors in any of the 5 sections: "The challenge", "Why it gets harder as you grow", "What a better close looks like", "The role of technology", "How to get started". Fix: give each section one fact the writer actually knows: a day count, a number of accounts, a team, a month.
- "For businesses of all sizes, it is not just an accounting task, but a powerful opportunity to understand the health of the company." Category language. Fix: say which business: "[your company, its size]".
- "Teams everywhere find that the spreadsheets that worked at the start no longer keep up." (skill rules: category language) Fix: "[which spreadsheet broke, and when]".

### Scaffold variance

- All 5 sections open on a general claim (skill rules: more than 40% of sections open the same way) and run to about the same length (web tool: section length variation 0.09). Fix: open one section on a number or a dated incident, and let one section run long and another be two sentences.
- Five lists of three, where the content has no reason to come in threes:
  - "More customers, more suppliers and more systems all add complexity to the process."
  - "A better close is seamless, predictable and transparent."
  - "It brings together the right people, the right tools and the right habits."
  - "The right tools can automate repetitive tasks, reduce errors and free up time for analysis."
  - "When people, process and technology work together, the results can be remarkable."
  Fix: use the number of items the content has. If there are really two causes, list two.

### Profundity inflation

- "For businesses of all sizes, it is not just an accounting task, but a powerful opportunity to understand the health of the company." Not just X, but Y. Fix: "The close tells you [the one thing it told you last month]."
- "Overall, a modern close is not just faster, but more strategic." Not just X, but Y. Fix: cut (also a closing summary).
- Intensity words with nothing behind them: "powerful" (skill rules; "For businesses of all sizes, it is not just an accounting task, but a powerful opportunity to understand the health of the company."), "crucial" ("Month-end close is one of the most crucial processes in any finance team."), "robust" ("Without a robust process, decisions are made on incomplete information."), "seamless" ("A better close is seamless, predictable and transparent."), "plays a key role" ("Technology plays a key role in a modern close."), "transformative" ("In short, small changes can lead to transformative results."). Fix: drop the word and say what happened.

## 4. Change first

Replace the opening section with the one close that went wrong, with its date and how many days it took; the rest of the rewrite follows from having a real case.

---

## After the rewrite: draft-after.md

349 words in 5 sections. Web tool code, same version: Over-explanation PASS (0 strikes), Real things, named PASS (8.3 anchors per 100 words, no section without one), Scaffold variance PASS (one note: section lengths still fairly even, variation 0.14), Profundity inflation PASS (1 strike: the "rather than" in the checklist section).

What changed: the post is now about one company's close, with the days, the accounts, the purchase order count and the month each change was made, and it keeps a section on what did not work. No new facts were needed beyond what the writer of a real version of this post would know.

The web tool's AI-style reading puts this rewrite at **Medium**, and both drafts were written by a model. The shape checks measure how a draft is built, not who built it.
