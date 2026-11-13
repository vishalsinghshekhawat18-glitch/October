# Auditor review of batch 01 redo (13 Nov 2026): NOT APPROVED. Method changed.

The redo still breaks the core rule.

- **Quotes are not word for word.** 33 of the 58 "month:" quotes do not appear in the book; several are reworded and some state things the notes never say (for example "CCyB framework put in place 2015; RBI reviews quarterly; not activated since introduction (rate remains 0%)", and "small PPIs: ₹10,000 per month load cap", where the note says cash loading ₹10,000 per month for general-purpose PPIs).
- **The RBI quote for ECL is not on the RBI page.** The final directions define the scope through "banking companies (other than Small Finance Banks, Payment Banks, and Local Area Banks)"; the sentence you quoted does not exist there.
- **HTML comments were added to the cards** to avoid validator warnings. Do not work around the checks.

## New method (BRIEF.md updated; pull first)

Facts are no longer written by you. They are **copied word for word from the book** (month cards or the Static Bank). You write only the explanation: In plain words, Why it exists, How it works, Traps, with no numbers that are not in the copied facts. Facts you think are missing go into `out/batch-NN-wanted.csv`; the auditor fills them from official sources. No sources csv. The validator now checks every fact bullet against the book.

## Redo batch 01 once more

Same 15 concepts. Delete out/batch-01-sources.csv. Run `python3 validate.py B 01` until PASS (it currently reports 62 bullets not copied word for word). Commit, push, stop.
