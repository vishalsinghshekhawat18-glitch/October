# Auditor review of batch 01, third version (13 Nov 2026): accepted after small fixes

Good progress: every fact is now real and comes from the notes, the explanations are clear, no invented numbers, no comments. The method works. Fix these, then go straight on to batch 02 in the same run.

## Fix in batch 01

1. **Whole bullets only.** The validator now rejects fragments (10 bullets, for example "they apply from 1 Apr 2027 ..." and "total with CCB = 11.5%"). Replace each with the whole bullet it came from, or a better whole bullet.
2. **ECL:** Fixed facts must carry the core of the framework: the three stages and their minimum provisions (0.4% Stage 1, 5% Stage 2, Stage 3 full lifetime loss: whole bullets or table rows from the April card) and the start date 1 April 2027.
3. **WMA:** remove "Period Oct 2026 – Mar 2027 ..." and "₹37,500 crore" from How it changed (half-year amounts are news; they stay in the September card). How it changed may stay empty if there is no rule change; then omit that block.
4. **PPI Traps:** remove "and cash withdrawals"; the notes do not say that.
5. **Revision:** write out/batch-01-revision.html (markup in BRIEF.md), at least one question per card.

Run `python3 validate.py B 01` until PASS.

## Then batch 02

Next 15 priority A concepts with status NEW or EXTEND, in concepts.csv order, after the 15 of batch 01. Same method, including batch-02-revision.html. Run `python3 validate.py B 02` until PASS. Commit both, push, stop.
