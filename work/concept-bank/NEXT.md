# Next run (auditor, 14 Nov 2026)

Batches 01 and 02 are approved and merged into the Static Bank (live on the site). Thank you: the copy-from-book method works.

Do **batches 03, 04 and 05** in one run: the next 45 concepts with status NEW or EXTEND in concepts.csv order (priority A first, then B), 15 per batch, same method as batch 02, each with its revision file. Run `python3 validate.py B 03`, `B 04`, `B 05` until each passes. Commit and push once at the end, then stop.

Two extra points:
- For EXTEND concepts, your card's blocks are **added to** the existing Static Bank card (nothing old is removed), so do not repeat the facts that card already has; add only what is missing.
- Put any facts you wanted but could not find in the book into `out/batch-NN-wanted.csv`.
