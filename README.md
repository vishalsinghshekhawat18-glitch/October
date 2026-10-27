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

The reader keeps the notes' structure (headings, lists, tables, images, formulas, footnotes) and replaces their colours and fonts with the reader's own. `<h2>` headings (or whichever level is highest) become chapters in the contents.

Cover emblems available in `subjects.json`: `book`, `graph`, `sigma`, `atom`, `flask`, `leaf`, `globe`, `quill`, `scales`, `compass`, `columns`, `code`.

## Privacy

The site is public. Reading progress, highlights, bookmarks and settings are stored only in the reader's own browser.
