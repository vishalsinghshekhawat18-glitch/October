# October Library

A quiet reading room for my study notes: a shelf of subjects on the home page, and a book-style reader for each one.

**Live site:** https://vishalsinghshekhawat18-glitch.github.io/October/

## How it's organised

| Path | What it is |
|---|---|
| `index.html` | Library home: greeting, reading stats, continue-reading card and the shelf |
| `reader.html?book=<slug>` | The reader that opens any subject |
| `subjects.json` | The list of subjects: titles, cover colours, status and where each notes file lives |
| `books/<slug>/content.html` | The notes for one subject |
| `assets/` | Shared styles and scripts |

There is no build step. GitHub Pages serves the files as they are.

## Adding a subject's notes

1. Save the subject's finished HTML file as `books/<slug>/content.html`.
2. In `subjects.json`, add or update the subject's entry and set `"status": "ready"` and `"updated"` to today's date.
3. Commit and push. The site updates in about a minute.

The reader keeps the notes' structure (headings, lists, tables, images, formulas, footnotes) and replaces their colours and fonts with the reader's own. The highest heading level becomes chapters in the contents. In a book split into parts, mark part headings with `class="rd-part"`; chapters are then the next level down, and the contents shows parts › chapters › sections.

### Exam series

Papers for one exam sit together in their own labelled row on the shelf. The series is listed under `library.series` in `subjects.json` (id, name, full name and the list of paper names); each paper's entry adds `"series": "<id>"` and `"paper": <n>`. Papers not yet added show as empty slots with their names, and the row shows how much of the exam has been read.

Cover emblems available in `subjects.json`: `book`, `graph`, `sigma`, `atom`, `flask`, `leaf`, `globe`, `quill`, `scales`, `compass`, `columns`, `code`.

## Privacy

The site is public. Reading progress, highlights, bookmarks and settings are stored only in the reader's own browser.

## Re-importing a book from its source HTML

`tools/convert-economics.mjs` turns the Economics source file into `books/economics/` (content plus extracted images). It drops the editor-only "Agent Notes", unpacks the Revision File, turns callout boxes into reader callouts, and makes every exam and quick-recall question a card with a hidden answer. It needs Node.js and `cheerio`:

```
npm install cheerio@1.0.0
node tools/convert-economics.mjs <source.html> books/economics
```

`tools/convert-ca.mjs` builds the Current Affairs book from any set of its source files (Static Bank and monthly compilations). Pass every file that should be in the book; Static Bank goes first and months are ordered newest first by the month named in each file's heading:

```
node tools/convert-ca.mjs books/current-affairs CA_Jan-Mar_2026.html [more files…]
```

`tools/convert-dbf.mjs` builds an IIBF DBF paper from its notes file: modules become parts, units become chapters, and each ★/☆ topic becomes a numbered card with its MCQ and Remember notes. Editor notes are left out:

```
node tools/convert-dbf.mjs Paper1_IE_IFS.html books/dbf-paper-1
```
