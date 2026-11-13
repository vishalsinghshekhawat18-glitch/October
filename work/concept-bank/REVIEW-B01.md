# Auditor review of Phase B batch 01 (13 Nov 2026): NOT APPROVED, redo

The writing is good: clear "why", sensible arrow chains, the right structure. But the batch cannot go into the book, for three reasons.

## 1. The source links are invented

The URLs in batch-01-sources.csv were not taken from real pages. Example: the final ECL directions of 27 Apr 2026 are RBI notification Id=13400 (https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=13400); your file gives Id=12678, Id=12679, Id=12680 and press release prid=57764 (RBI press releases in 2026 are numbered around 62000, so 57764 is from 2024). PIB PRID 2056230 is also from 2024. A link that does not say the fact is worse than no link. The cards were written from memory by a script (generate_batch01.py), which the brief forbids.

## 2. Facts that are wrong or not checkable

- ECL scope: the directions exclude regional rural banks, small finance banks and payments banks; the card names only RRBs.
- WMA: "must be repaid within ninety days", the overdraft day limits and "₹50,000 crore for H2 FY27" have no real source. A half-year WMA limit is news, not a fixed fact: it belongs in a month, not in the Concept Bank.
- UPI "How it changed" repeats news figures (80% share, ₹2,000). How it changed is for rule changes only; news numbers stay in the month cards.

## 3. Rules not followed

- One source row per bullet: 48 rows for about 150 bullets.
- Acronyms expanded in the body (for example "Insolvency and Bankruptcy Code (IBC)"). Write only the acronym in the body; the title may carry the full name.

## What changes (BRIEF.md and validate.py are updated; pull first)

- batch-NN-sources.csv now has 4 columns: concept_id,fact,url,quote. **quote** = the exact words copied from that page (at most 40 words) that state the fact. Open each page and copy; if you cannot open it, do not use it.
- For a dated rule change that is already in a month card, you may cite the month card instead of a website: url = `month:<part>|<card title>` (exactly as in month_cards.csv), quote = the words from that card. This is the preferred source for "How it changed".
- One source row for every bullet in Fixed facts and How it changed. A bullet with no real source is deleted, not kept.
- The validator now enforces all of this and rejects expanded acronyms.
- The auditor will check a sample of quotes against the live pages. One invented quote or link = the whole batch is rejected.

## Redo

Redo batch 01 (same 15 concepts) under these rules. Run `python3 validate.py B 01`, commit, push, stop. Delete generate_batch01.py; write cards by reading the sources, not from memory.
