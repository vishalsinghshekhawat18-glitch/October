# Next run (auditor, 14 Nov 2026)

Batches 03–05 are approved and merged (live on the site). Do **batches 06, 07 and 08** the same way: the next 45 concepts with status NEW or EXTEND in concepts.csv order, 15 per batch, each with its revision file. Validate each until PASS, commit and push once at the end, then stop.

One fix: every card body must stay inside `<div class="body">` and the card must end with `</ul>\n</div></details>`. In batches 04 and 05 the body div was closed early (right after the first blocks), so Fixed facts and later blocks sat outside it. The validator now checks this.
