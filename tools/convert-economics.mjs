// Convert "The Economics Book with Revision File" HTML into the reader's book format.
// Usage: node convert-economics.mjs <source.html> <outDir>
// Writes <outDir>/content.html and <outDir>/img/fig-NN.<ext>; prints a summary.
import * as cheerio from 'cheerio';
import { readFileSync, writeFileSync, mkdirSync, rmSync } from 'fs';
import { join } from 'path';

const [src, outDir] = process.argv.slice(2);
const $ = cheerio.load(readFileSync(src, 'utf8'));
const text = el => $(el).text().replace(/\s+/g, ' ').trim();
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

rmSync(join(outDir, 'img'), { recursive: true, force: true });
mkdirSync(join(outDir, 'img'), { recursive: true });

const stats = { parts: 0, chapters: 0, sections: 0, boxes: 0, questions: 0, recall: 0, images: 0, agentNotesRemoved: 0, revisionChapters: 0 };
const BOX_LABELS = {
  why: 'Why it matters', defn: 'Definition', example: 'Example', exam: 'Exam tip',
  trap: 'Common trap', data: 'Data', formula: 'Formula',
};

// Images: move embedded data URIs into files so they load lazily.
let figNo = 0;
function extractImage(img, ctx) {
  const s = ctx(img).attr('src') || '';
  const m = s.match(/^data:image\/(png|jpe?g|gif|webp|svg\+xml);base64,(.+)$/s);
  if (!m) return;
  const ext = m[1] === 'jpeg' ? 'jpg' : m[1] === 'svg+xml' ? 'svg' : m[1];
  const name = `fig-${String(++figNo).padStart(2, '0')}.${ext}`;
  const buf = Buffer.from(m[2], 'base64');
  writeFileSync(join(outDir, 'img', name), buf);
  ctx(img).attr('src', `img/${name}`);
  // Intrinsic size (PNG header) lets the browser reserve space before a lazy image loads.
  if (ext === 'png' && buf.length > 24) {
    ctx(img).attr('width', String(buf.readUInt32BE(16)));
    ctx(img).attr('height', String(buf.readUInt32BE(20)));
  }
  const w = (ctx(img).attr('style') || '').match(/width:\s*([\d.]+)%/);
  ctx(img).removeAttr('style');
  if (w) ctx(img).attr('style', `width:${Math.round(+w[1])}%`);
  stats.images++;
}

// Wrap loose inline content of a box in a paragraph.
function boxBody(inner, ctx) {
  const html = ctx(inner).html().trim();
  const hasBlock = ctx(inner).children('p, ul, ol, table, div, figure, h3, h4').length > 0;
  return hasBlock ? html : `<p>${html}</p>`;
}

const out = [];

// ---------- Main parts ----------
let chapterNo = 0;
$('div.partwrap').each((pi, pw) => {
  const part = $(pw);

  // Drop the editor-only "Agent Notes" and everything after it in this part.
  const agent = part.find('h1.unlisted');
  if (agent.length) {
    stats.agentNotesRemoved += agent.nextAll().length + 1;
    agent.nextAll().remove();
    agent.remove();
  }

  const cover = part.find('div.cover');
  const titleHtml = cover.find('h1.parttitle').html() || '';
  const [partNo, partName] = titleHtml.split(/<br\s*\/?>/i).map(s => cheerio.load(s).text().trim());
  const partLead = text(cover.find('p.lead'));
  const partId = part.attr('id') || `part${pi + 1}`;
  cover.remove();
  part.find('nav').remove();
  part.find('hr.start').remove();
  stats.parts++;

  out.push(`<h1 class="rd-part" id="${partId}" data-toc="${esc(`${partNo} · ${partName}`)}"><span class="rd-part-no">${esc(partNo)}</span>${esc(partName)}</h1>`);
  if (partLead) out.push(`<p class="rd-part-lead">${esc(partLead)}</p>`);

  // Chapters: kicker + h1 become a chapter heading; section levels shift down by one.
  part.find('h1').each((ci, h) => {
    const kick = $(h).prev('p.kicker');
    const num = (text(kick).match(/Chapter\s+(\d+)/) || [])[1] || String(chapterNo + 1);
    chapterNo = +num;
    kick.remove();
    const title = text(h);
    $(h).replaceWith(`<h2 class="rd-chapter" id="${$(h).attr('id') || 'chapter-' + num}" data-toc="${esc(`${num}. ${title}`)}"><span class="rd-ch-no">Chapter ${num}</span>${esc(title)}</h2>`);
    stats.chapters++;
  });
  part.find('p.kicker').remove();
  part.find('h3').each((i, h) => { h.tagName = 'h4'; });
  part.find('h2:not(.rd-chapter)').each((i, h) => { h.tagName = 'h3'; stats.sections++; });
  part.find('p.lead').attr('class', 'rd-lead');

  // Callout boxes
  part.find('div.box').each((i, b) => {
    const kind = Object.keys(BOX_LABELS).find(k => $(b).hasClass(k)) || 'why';
    const inner = $(b).children('.bx').length ? $(b).children('.bx') : $(b);
    $(b).replaceWith(`<aside class="rd-box rd-box-${kind}"><span class="rd-box-label">${BOX_LABELS[kind]}</span>${boxBody(inner, $)}</aside>`);
    stats.boxes++;
  });

  // Multiple-choice options written as line blocks become lists.
  part.find('div.line-block').each((i, lb) => {
    const lines = ($(lb).html() || '').split(/<br\s*\/?>/i).map(s => s.trim()).filter(Boolean);
    $(lb).replaceWith(`<ul class="rd-options">${lines.map(l => `<li>${l}</li>`).join('')}</ul>`);
  });

  // Options written as an (a)-(d) list. The source's converter misread "(a) (i) & (ii) only"
  // as a list nested in a list, so rebuild the "(i)" prefix from the inner list's start number.
  const ROMAN = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii'];
  part.find('ol[type="a"]').each((i, ol) => {
    const items = $(ol).children('li').map((j, li) => {
      const kids = $(li).contents().filter((k, n) => n.type !== 'text' || n.data.trim());
      let html = $(li).html().trim();
      if (kids.length === 1 && kids.first().is('ol')) {
        const inner = kids.first();
        const start = +(inner.attr('start') || 1);
        html = `(${ROMAN[start] || start}) ${inner.children('li').first().html().trim()}`;
      }
      stats.optionListsRebuilt = (stats.optionListsRebuilt || 0) + (j === 0 ? 1 : 0);
      return `<li>(${String.fromCharCode(97 + j)}) ${html}</li>`;
    }).get();
    $(ol).replaceWith(`<ul class="rd-options">${items.join('')}</ul>`);
  });

  // Lists of self-contained questions ("stem … Options: (a) … (b) … Answer: (b).") become one card each.
  part.find('ol, ul').each((i, list) => {
    const lis = $(list).children('li');
    if (!lis.length || !lis.toArray().every(li => /Answer:/.test(text(li)))) return;
    const start = +($(list).attr('start') || 1);
    const cards = lis.map((j, li) => {
      const html = $(li).html().replace(/<\/?p>/g, ' ').trim();
      const ai = html.search(/<strong>\s*Answer:/);
      const stemAndOpts = html.slice(0, ai).trim();
      const answer = html.slice(ai).trim();
      const [stem, optText] = stemAndOpts.split(/\s*Options:\s*/);
      const opts = optText ? optText.split(/\s+(?=\([a-e]\)\s)/).map(o => o.trim()).filter(Boolean) : [];
      stats.questions++;
      stats.inlineQuestions = (stats.inlineQuestions || 0) + 1;
      return `<div class="rd-q"><p><strong>Q${start + j}.</strong> ${stem}</p>${opts.length ? `<ul class="rd-options">${opts.map(o => `<li>${o}</li>`).join('')}</ul>` : ''}<details class="rd-answer"><summary>Show answer</summary><p>${answer}</p></details></div>`;
    }).get();
    $(list).replaceWith(cards.join(''));
  });

  // A question written as a numbered list item becomes a "Q<n>." paragraph. When the source
  // merged the question's statements into the same list, they become an (i), (ii)… list.
  part.find('ol').each((i, ol) => {
    const lis = $(ol).children('li');
    if (!lis.length || $(ol).attr('type') === 'i' || !/\[[^\]]*\b(19|20)\d{2}\b[^\]]*\]/.test(text(lis.first()))) return;
    // Loose list items wrap their text in <p>; unwrap so the stem stays one paragraph.
    const inner = li => {
      const kids = $(li).children();
      return kids.length && kids.length === kids.filter('p').length && !$(li).contents().filter((k, n) => n.type === 'text' && n.data.trim()).length
        ? kids.map((k, p) => $(p).html().trim()).get().join(' ')
        : $(li).html().trim();
    };
    const rest = lis.slice(1).map((j, li) => `<li>${inner(li)}</li>`).get().join('');
    $(ol).replaceWith(`<p><strong>Q${$(ol).attr('start') || 1}.</strong> ${inner(lis.first())}</p>${rest ? `<ol type="i">${rest}</ol>` : ''}`);
    if (rest) stats.mergedStatementsSplit = (stats.mergedStatementsSplit || 0) + 1;
  });

  // Questions: anchor on each "Answer" paragraph, walk back to the question stem,
  // and turn the group into a card whose answer stays hidden until tapped.
  const isStem = el => /\[[^\]]*\b(19|20)\d{2}\b[^\]]*\]|^Q\d+\.?\s/.test(text(el));
  part.find('p').filter((i, p) => /^Answer\b/.test(text(p)) && !$(p).closest('details').length).each((i, p) => {
    const ans = $(p);
    const group = [];
    let node = ans.prev();
    let stemFound = false;
    while (node.length && group.length < 5 && node.is('p, ol, ul, table') && !node.is('.rd-q') && !/^Answer\b/.test(text(node))) {
      group.unshift(node);
      if (isStem(node)) { stemFound = true; break; }
      node = node.prev();
    }
    const details = `<details class="rd-answer"><summary>Show answer</summary><p>${ans.html()}</p></details>`;
    if (stemFound) {
      const card = $('<div class="rd-q"></div>');
      group[0].before(card);
      group.forEach(g => card.append(g));
      card.append(details);
      ans.remove();
      stats.questions++;
    } else {
      ans.replaceWith(details);
      stats.answersWithoutCard = (stats.answersWithoutCard || 0) + 1;
    }
  });

  part.find('figure img, img').each((i, img) => extractImage(img, $));
  part.find('colgroup').remove();
  part.find('tr').removeAttr('class');

  out.push(part.html());
});

// ---------- Revision file (stored inside a declarative shadow root) ----------
const tplHtml = $('template').first().html() || '';
const R = cheerio.load(tplHtml);
const revCover = $('div.revcover');
out.push(`<h1 class="rd-part rd-appendix" id="revision" data-toc="Revision File"><span class="rd-part-no">Revision</span>Revision File</h1>`);
const revLead = text(revCover.find('p.lead'));
if (revLead) out.push(`<p class="rd-part-lead">${esc(revLead)}</p>`);
R('div.ch').each((i, ch) => {
  const c = R(ch);
  const kick = text(c.children('.k'));
  const num = (kick.match(/Chapter\s+(\d+)/) || [])[1] || String(i + 1);
  c.children('.k').remove();
  const h1 = c.children('h1').first();
  const title = text(h1);
  h1.replaceWith(`<h2 class="rd-chapter rd-rev" id="rev-ch-${num}" data-toc="${esc(`${num}. ${title}`)}"><span class="rd-ch-no">Revision · Chapter ${num}</span>${esc(title)}</h2>`);
  c.find('h2:not(.rd-chapter)').each((j, h) => { h.tagName = 'h3'; });
  c.find('div.core').each((j, d) => R(d).replaceWith(`<aside class="rd-box rd-box-core">${boxBody(d, R)}</aside>`));
  c.find('div.d').each((j, d) => R(d).replaceWith(`<aside class="rd-box rd-box-defn">${boxBody(d, R)}</aside>`));
  c.find('div.f').each((j, d) => R(d).replaceWith(`<aside class="rd-box rd-box-formula rd-box-tight">${boxBody(d, R)}</aside>`));
  c.find('p.src').attr('class', 'rd-src');
  c.find('div.two').attr('class', 'rd-two');
  c.find('div.q').each((j, q) => {
    R(q).find('li').each((k, li) => {
      const a = R(li).children('span.a');
      const ans = a.html();
      a.remove();
      R(li).html(`<span class="rd-recall-q">${R(li).html().trim()}</span>${ans ? `<details class="rd-answer"><summary>Show answer</summary><p>${ans.replace(/^\s*Answer:\s*/, '')}</p></details>` : ''}`);
      stats.recall++;
    });
    R(q).replaceWith(`<div class="rd-recall">${R(q).html()}</div>`);
  });
  c.find('img').each((j, img) => extractImage(img, R));
  out.push(`<section class="rd-rev-ch">${c.html()}</section>`);
  stats.revisionChapters++;
});

// Typographic arrows in text (not inside code).
const body = out.join('\n').replace(/(>[^<]*)/g, seg => seg.replace(/ -&gt; /g, ' → ').replace(/ &lt;- /g, ' ← ').replace(/ -> /g, ' → '));
const doc = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>The Economics Book</title>
</head>
<body>
${body}
</body>
</html>
`;
writeFileSync(join(outDir, 'content.html'), doc);

// Sanity checks on the output
const check = cheerio.load(doc);
stats.outputKB = Math.round(Buffer.byteLength(doc) / 1024);
stats.leftoverAgentText = /Agent Notes|Codex Ch/.test(doc);
stats.leftoverDataUris = (doc.match(/src="data:/g) || []).length;
stats.h1 = check('h1').length;
stats.h2 = check('h2').length;
stats.h3 = check('h3').length;
stats.h4 = check('h4').length;
stats.tables = check('table').length;
stats.details = check('details').length;
stats.duplicateIds = (() => {
  const seen = new Map();
  check('[id]').each((i, e) => seen.set(e.attribs.id, (seen.get(e.attribs.id) || 0) + 1));
  return [...seen].filter(([, n]) => n > 1).map(([k]) => k);
})();
stats.questionsWithoutAnswer = check('.rd-q').filter((i, e) => !check(e).find('details').length).length;
console.log(JSON.stringify(stats, null, 2));
