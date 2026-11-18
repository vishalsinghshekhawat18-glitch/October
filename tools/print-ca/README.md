# Current Affairs print edition builder

Builds a month's notes into a story-style print edition: A4, black and white only.

The builder only reads the month's notes file. It never changes it.

## What it makes

- A cover with the lead story, four "Also in this issue" lines and a strip naming the sections.
- A contents page with real page numbers and "The month in numbers".
- Sections 1–8. Each opens with an outlined section number and a mini contents, then:
  - chapters, with every ★ card printed as a story;
  - In brief: every ☆ card, grouped under its topic heading shown once, in the outline-box style.
- Section 9: the summary tables, then all revision questions, with numbered answers after them.

There are two story sizes:

- **Full story:** headline, paragraph, a strip of big numbers, a chart, a "Remember it like this" box, a "Trap" box and the fact file.
- **Short story:** headline, paragraph, the card's own Remember / Exam angle box, and the fact file.

The fact file is the card's own content, in the card's order. Numbers that the older notes printed in bold are not bold in print.

## How to make a month

1. Copy `content/oct2026.py` to `content/<mon><year>.py`.
2. In the new file, set `NOTES`, the path to the month's final notes file.
   - Archived months are in `archive/current-affairs/`.
   - The current month is in the project. Join its parts into one file first.
3. Write the story layer in the same file:
   - Section intros, chapter titles and chapter intros.
   - One `st(...)` line for every ★ card. Each line gives the key, a unique piece of the card's title, a tag and a headline. Full stories also get a paragraph, a number strip, charts and a trap.
   - Charts, made with `hbar`, `steps` or `table_chart`.
   - The cover, the cover lines, the contents lines and the "month in numbers" table.
4. Check the story layer without building:

   ```
   python3 build.py content/<file>.py --check-only
   ```

5. Build the edition:

   ```
   python3 build.py content/<file>.py --out ../../archive/current-affairs/print
   ```

## What the build stops for

- **A number not in the notes.** Every number written in the content file must appear in the notes' reading area. This covers headlines, paragraphs, number strips, chart labels, hooks, traps, intros, the cover and the contents.
- **A ★ card with no story,** a story placed twice, or a story pointing at a ☆ card.
- **A card match that is not exactly one card.**
- **A paragraph that talks about "this card".** These are "In plain words" lines that only make sense on the website; write your own paragraph instead.

## Layout fixes it makes by itself

- **Short tables split badly.** A table of 14 rows or fewer that would leave 1–2 rows on a page is kept whole.
- **Short section endings.** If a section's last page is under 45% full, that section's In brief spacing is tightened. If the page is still short, the next section starts lower on the same page instead of on a fresh page.
- **Timelines and two-column fact lists** are drawn so they can break across pages. In WeasyPrint, flex boxes and multi-column lists drag the whole story to the next page.

## Files

| File | What it is |
|---|---|
| `build.py` | The builder |
| `print.css` | The style; the month in the running header is filled in by the builder |
| `content/oct2026.py` | October 2026 (129 stories) |
| `content/nov2026.py`, `nov2026_charts.json`, `nov2026_dash.html` | November 2026, 1–17 Nov (72 stories) |

Output goes to `archive/current-affairs/print/` as `CA_<Month>_2026_print.pdf`. Each build overwrites the same file name.

Needs Python 3 with `weasyprint` and `beautifulsoup4`, plus the Inter, Inter Display and Lora fonts.
