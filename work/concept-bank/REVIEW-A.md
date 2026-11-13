# Auditor review of Phase A (13 Nov 2026)

Phase A is approved with the fixes below. Apply them first, re-run `python3 validate.py A` until it passes, then do Phase B batch 01. Commit, and this time **push to GitHub** (`git push origin main`); the auditor reviews only what is on GitHub. Your Phase A commit was never pushed.

## 1. Add these concepts (priority A, status NEW unless a Static Bank card matches; then EXTEND)

| concept_id | concept_name | map these cards (move them out of unmapped.csv) |
|---|---|---|
| c-npa-asset-classification | NPA recognition, asset classification and provisioning (IRAC) | may-2026 Public sector banks FY26: record profit, lowest NPAs; plus any month card on gross/net NPA or IRAC |
| c-bank-ownership-shareholding | Bank ownership: prior approval for major shareholding, voting caps, foreign bank subsidiaries | apr-2026 M&A: Emirates NBD-RBL Bank, Jio-Allianz, Federal Bank; may-2026 Emirates NBD gets all approvals for RBL Bank; may-2026 Bank and insurance stake deals; sep-2026 RBI approves LIC stake of up to 9.99% in ICICI Bank |
| c-share-buyback | Share buybacks: tender offer vs open-market route | apr-2026 SEBI: buyback and IPO norms; may-2026 SEBI proposals: GARUDA for AIFs and open-market buybacks |
| c-loan-recovery-fair-practices | Fair practices in lending and loan recovery (recovery agents, conduct rules) | may-2026 RBI draft: loan recovery conduct and locking of financed phones |
| c-acquisition-finance | Bank finance for acquisitions | jan-mar-2026 RBI final acquisition finance framework for banks |
| c-currency-management | Currency management: note issue, design, clean note policy | oct-2026 Polymer banknotes: RBI proposal (merge with the existing clean note policy concept if you prefer: then just add the ref there) |
| c-index-providers | Market indices and their regulation | may-2026 SEBI: "Significant Indices" and registration of index providers |

Also map: may-2026 RBI Payment Systems Report (December 2025) → c-upi (or a payment systems concept); oct-2026 RBI Master Circular: credit facilities to SCs and STs → priority sector lending concept; jan-mar-2026 SEBI: merchant banker net worth overhaul → add a concept c-market-intermediaries (merchant bankers, brokers, registration); oct-2026 High Level Committee on Banking for Viksit Bharat → keep unmapped (committee), fine.

## 2. static_dated.csv: change these decisions

Rule: "drop" only when the fact is already in a monthly part or is of no exam value. Lasting framework facts and rule histories stay in the Concept Bank as "How it changed" or "Fixed facts".

- Keep (change to `keep`): Governors since 1997; Integrated Ombudsman Scheme 2026; GST 2.0 slab overhaul of 2025; Banking Laws (Amendment) Act 2025; Regional Rural Banks (RRBs) count history; How India's disaster law came about; NBFC layers, capital and loan rules; Bank capital, exposure and co-operative tiers; Recent RBI and SEBI rules: key numbers.
- Heads of bodies (Finance regulators and financial bodies; Banks in news: founding, HQ and heads; Central agencies and defence bodies; Financial and UN-family bodies): `keep` — they will become one "Who heads what (as of date)" reference section. Do not drop.
- Static one-liners from June–July 2026 and Scheme facts from the last six months: `hold` — June and July are not built yet; these may be the only copy.
- `validate.py` now accepts `keep` and `hold` as suggested_home values.

## 3. Phase B batch 01

Priority A concepts with status NEW or EXTEND, the first 15 in concepts.csv order (start with c-expected-credit-loss). Follow BRIEF.md Phase B exactly. For EXTEND cards, read the matching Static Bank card in books/current-affairs/content.html (part `static`) and keep its correct content. Run `python3 validate.py B 01`, commit, push, stop.
