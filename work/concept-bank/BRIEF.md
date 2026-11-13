# Concept Bank: brief for Antigravity

You are drafting work for the Current Affairs book in this repo. Claude (the auditor) reviews everything you produce before it goes into the book. Follow this brief exactly. If something is unclear, write the question into `out/QUESTIONS.md` and continue with the rest. Never guess.

## Goal

The book has two layers:
- **Monthly parts** (`nov-2026`, `oct-2026`, `sep-2026`, `may-2026`, `apr-2026`, `jan-mar-2026`) hold the news: what happened, numbers, dates.
- **The Static Bank** (part `static`) becomes a **Concept Bank**. It holds the understanding behind the news: what a thing is, why it exists, how it works, the fixed facts that do not change month to month, how the rules changed over time, and the traps. It does not repeat news facts. It points to the months instead.

Your job is the heavy mechanical work: mapping the monthly cards to concepts, then drafting concept cards in batches.

## Inputs (in this folder)

- `month_cards.csv`: every card in the monthly parts (part, chapter, subheading, priority must/good, title, first three bullets as gist). 1,233 cards, 621 of them "must".
- `static_cards.csv`: the 189 current Static Bank cards (section, subheading, title, gist).
- The full book: `books/current-affairs/content.html` (read a card there when the gist is not enough).

## Phase A: concept map (do this first, then stop)

Write these three files into `work/concept-bank/out/`:

### 1. `concepts.csv`

Columns, in this order:
`concept_id,concept_name,static_section,status,static_match,priority,month_refs,learner_must_understand`

- `concept_id`: `c-` plus short kebab-case, unique, stable (e.g. `c-expected-credit-loss`, `c-repo-rate`, `c-fpi`).
- `concept_name`: the plain name (e.g. "Expected Credit Loss provisioning").
- `static_section`: the Static Bank section it belongs to. Use the existing section names from `static_cards.csv`. If none fits, write `NEW: <proposed section name>`.
- `status`: one of
  - `EXISTS`: a Static Bank card already explains it fully.
  - `EXTEND`: a Static Bank card covers part of it; it needs the missing parts.
  - `NEW`: no Static Bank card covers it.
- `static_match`: the exact Static Bank card title for EXISTS or EXTEND; empty for NEW.
- `priority`: `A` = banking, RBI, SEBI, IRDAI, PFRDA, payments, monetary policy, fiscal, external sector, economy data; `B` = government schemes, polity and law, international organisations, trade agreements; `C` = everything else (science, defence, environment, sports, awards).
- `month_refs`: every monthly card that depends on this concept, as `part|card title`, separated by ` ;; `. Copy titles exactly from `month_cards.csv`.
- `learner_must_understand`: one sentence: what someone must understand to make sense of the news cards. No numbers from the news.

Rules for Phase A:
- A concept is an idea that keeps its meaning across months: an instrument (repo rate, CRR, floating rate bond), a framework (ECL, Basel III, PCA), an institution and its role (FSDC, GST Council, NCLT), a law or scheme design (IBC, PMJDY), a measure (CPI, IIP, fiscal deficit), a recurring index or report (what it measures, who publishes it).
- **Not** a concept: a one-off event, an appointment, an award winner, a sports result, a single MoU. Those stay in the months only.
- One concept per idea. Merge near-duplicates (e.g. "WPI" and "wholesale inflation" are one concept). Several months touching the same idea go into the same row's `month_refs`.
- Aim for coverage, not volume: every **must** card in `month_cards.csv` must appear either in some row's `month_refs` or in `unmapped.csv`.

### 2. `unmapped.csv`

Columns: `part,title,reason`. One row for every **must** card that has no concept, with a short reason (e.g. "appointment", "award", "one-off event"). "Good" cards may be left out silently.

### 3. `static_dated.csv`

Columns: `static_card_title,dated_text,suggested_home`. List every place in the current Static Bank that carries dated news rather than lasting concept (e.g. a 2026 circular's details, a company event, a person currently holding a post, a figure for one year). `suggested_home` is the monthly part where it belongs, or `drop` if it is in no month.

Then run `python3 work/concept-bank/validate.py A` and fix every error it prints. Commit with message `Concept Bank Phase A: concept map` and **stop**. Tell the user Phase A is done.

## Phase B: draft concept cards (only after the auditor approves Phase A)

The auditor will name the batch (for example "Phase B batch 1: priority A, first 15 NEW/EXTEND concepts in concepts.csv order"). For each batch write two files into `work/concept-bank/out/`:

### `batch-NN.html`: the cards

One card per concept, exactly this shape (copy the markup; change only the text):

```html
<details class="card" open id="c-expected-credit-loss"><summary>★ Expected Credit Loss provisioning</summary><div class="body">
<div class="plain"><strong>In plain words:</strong> One or two simple sentences: what it is.</div>
<p><strong>Why it exists</strong></p>
<ul><li>The problem it solves, in plain words.</li></ul>
<p><strong>How it works</strong></p>
<ul><li>Step → step → result (arrows allowed).</li></ul>
<p><strong>Fixed facts</strong></p>
<ul><li>Law and section, year, body in charge, the formula or structure. Only facts that do not change month to month.</li></ul>
<p><strong>How it changed</strong></p>
<ul><li>Latest first: date: what changed. Only rule or framework changes, not market numbers.</li></ul>
<p><strong>Traps</strong></p>
<ul><li>Look-alike terms and common confusions.</li></ul>
<p><strong>In the news</strong></p>
<ul><li><a href="#apr-2026">April 2026</a>: card title as in month_cards.csv</li></ul>
</div></details>
```

- `★` and `class="card"` for priority A and B; `☆` and `class="card opt"` for priority C. A `☆` card has **no** "In plain words" line.
- For an EXTEND concept, write the **whole** card (old content kept and corrected, gaps filled); the auditor replaces the old card.
- "In the news" lists every `month_refs` entry, one line each, linking to the part id (`#nov-2026`, `#oct-2026`, `#sep-2026`, `#may-2026`, `#apr-2026`, `#jan-mar-2026`). Do **not** repeat the news numbers there.
- Omit a sub-block only if there is truly nothing for it (for example no rule changes yet); never write placeholders.

### Facts are copied, never written (rule from 13 Nov 2026)

- Every bullet in **Fixed facts** and **How it changed** must be copied word for word from the book (`books/current-affairs/content.html`: a month card or the Static Bank part). You may only add a date prefix like `27 Apr 2026: ` in How it changed. The validator checks every bullet against the book; a bullet it cannot find fails the batch.
- If a fact you think belongs is not in the book, do not write it. List it in `out/batch-NN-wanted.csv` (columns `concept_id,wanted_fact,where_to_look`); the auditor adds it from an official source.
- **Why it exists, How it works, Traps and In plain words** are your own explanation in plain words. They may not contain any number that is not already in the card's fact bullets (the validator checks this). Explain ideas, not figures.
- Copy **whole** bullets (one complete `<li>` or table row from the book, or one complete `;`-separated part of it). Fragments cut mid-sentence fail the validator.
- **How it changed** holds rule or framework changes only, each with its date prefix. Amounts for one period (a half-year limit, a monthly figure) stay in the month cards and do not go here.
- Pick the facts a learner needs most: for a framework, its core numbers (for example the stage floors for ECL) come before side details.
- No sources csv is needed any more; the book is the source. No HTML comments anywhere.

### `batch-NN-revision.html`: flashcards

At least one question for every ★ card, in exactly this markup (one per line):

```html
<details data-concept="c-expected-credit-loss"><summary>What are the minimum Stage 1 and Stage 2 provisions under ECL?</summary><div class="ans">0.4% and 5%.</div></details>
```

Every number in an answer must appear in that card. Prefer questions that test understanding (why, which stage, what triggers) plus one number question where the card has key numbers.

Writing rules (the user's standing rules):
- Plain, clear English; bullets and short phrases; arrows for processes.
- Do not bold numbers. Do not expand acronyms in the body (the card title may carry the full name).
- No card IDs, source names or "per source" wording in the card text.
- Light background design is already in the book; do not add styles or scripts.
- Never invent a fact, date, number, link or quote. Missing is better than wrong.
- Never generate cards with a script from memory; read the sources, then write.
- How it changed holds rule and framework changes only; news numbers (limits for one half-year, market shares, monthly figures) stay in the month cards.

Then run `python3 work/concept-bank/validate.py B NN` and fix every error. Commit with message `Concept Bank Phase B batch NN` and **stop**. Do not start the next batch until the auditor approves.

## What you must never do

- Never edit `books/current-affairs/content.html`, `subjects.json` or anything outside `work/concept-bank/out/`.
- Never push changes to the live book.
- Never start a phase or batch the auditor has not approved.
