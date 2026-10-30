// Build an IIBF DBF paper from its notes file ("DBF design system": modules › units › ★/☆ topics).
// Usage: node convert-dbf.mjs <source.html> <outDir>
// Modules become parts, units become chapters, and each topic a numbered card. Sections after the
// modules (Recent Developments, Summary Tables, Quick Facts, Revision) close the book. Writes <outDir>/content.html.
import * as cheerio from 'cheerio';
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const [src, outDir] = process.argv.slice(2);
const $ = cheerio.load(readFileSync(src, 'utf8'));
const t = e => $(e).text().replace(/\s+/g, ' ').trim();
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const plural = (n, w) => `${n} ${w}${n === 1 ? '' : 's'}`;

// Some unit headings are in capitals; give them title case but keep acronyms.
const SMALL = /^(and|of|the|in|to|for|on|with|by|or|a|an|at|vs|including)$/i;
const ACRONYMS = new Set(['NITI', 'MSME', 'RBI', 'NBFC', 'GDP', 'SDG', 'IMF', 'WTO', 'FDI', 'FPI', 'SEBI', 'IRDAI', 'PFRDA', 'GST', 'FRBM', 'BOP', 'MFI', 'DFI', 'UPI', 'NPA', 'IBC']);
const titleCase = s => (s === s.toUpperCase()
  ? s.toLowerCase().split(/(\s+)/).map((w, i) => {
    const bare = w.replace(/[^a-z]/gi, '').toUpperCase();
    if (ACRONYMS.has(bare)) return w.toUpperCase();
    if (bare.endsWith('S') && ACRONYMS.has(bare.slice(0, -1))) return w.toUpperCase().replace(/S(\W*)$/, 's$1');
    return i > 0 && SMALL.test(w) ? w : w.charAt(0).toUpperCase() + w.slice(1);
  }).join('')
  : s);

const stats = {
  modules: 0, extras: 0, units: 0, topics: 0, must: 0, good: 0, unmarked: [],
  plain: 0, examples: 0, mcq: 0, remember: 0, flashcards: 0, practiceMcqs: 0, figures: 0, agentNotesRemoved: 0,
};

$('#agent-notes, .agent-notes').each((i, s) => { stats.agentNotesRemoved++; $(s).remove(); });
$('script, style, nav').remove();
$('*').contents().filter((i, n) => n.type === 'comment').remove();

// Book-wide note ("Nov 2026 cycle · facts as on …") leads the first module.
const docNote = t($('.doc-sub')).replace(/^IIBF Diploma in Banking (&|and) Finance\s*·\s*/i, '');
$('.doc-title, .doc-sub, .key').remove();

const starOf = h => {
  const s = t($(h).find('.star'));
  return s === '★' ? 'must' : s === '☆' ? 'good' : '';
};

// Callout notes become labelled reader boxes.
const box = (body, sel, kind, label, stat) => body.find(sel).add(body.filter(sel)).each((i, el) => {
  $(el).find('b.tag').first().remove();
  $(el).replaceWith(`<aside class="rd-box rd-box-${kind}"><span class="rd-box-label">${label}</span><p>${$(el).html().trim()}</p></aside>`);
  stats[stat]++;
});

// Revision: a Question | Answer table becomes flashcards; a numbered list of "(A)…(D)" questions
// followed by "Answers: 1-B, 2-C …" becomes question cards with hidden answers.
function revision(body) {
  body.find('table').each((i, tb) => {
    const heads = $(tb).find('thead th').map((j, th) => t(th).toLowerCase()).get();
    if (heads.length !== 2 || heads[0] !== 'question' || !/^answer/.test(heads[1])) return;
    const items = $(tb).find('tbody tr').map((j, tr) => {
      const [q, a] = $(tr).children('td').toArray();
      stats.flashcards++;
      return `<li><span class="rd-recall-q">${$(q).html().trim()}</span><details class="rd-answer"><summary>Show answer</summary><p>${$(a).html().trim()}</p></details></li>`;
    }).get();
    $(tb).replaceWith(`<div class="rd-recall"><ol>${items.join('')}</ol></div>`);
  });
  body.find('ol').each((i, ol) => {
    const key = $(ol).nextAll('p').first();
    const m = t(key).match(/^Answers?:\s*(.*)$/i);
    if (!m) return;
    const answers = Object.fromEntries([...m[1].matchAll(/(\d+)\s*[-–:.]\s*([A-E])\b/gi)].map(x => [+x[1], x[2].toUpperCase()]));
    const cards = $(ol).children('li').map((j, li) => {
      const [stem, ...rest] = $(li).html().split(/<br\s*\/?>/i);
      const opts = rest.join(' ').replace(/&nbsp;| /g, ' ').split(/\s*(?=\([A-E]\)\s)/).map(o => o.trim()).filter(Boolean);
      const letter = answers[j + 1];
      const right = letter && opts.find(o => o.startsWith(`(${letter})`));
      stats.practiceMcqs++;
      return `<div class="rd-q"><p><strong>Q${j + 1}.</strong> ${stem.trim()}</p>${opts.length ? `<ul class="rd-options">${opts.map(o => `<li>${o}</li>`).join('')}</ul>` : ''}${letter ? `<details class="rd-answer"><summary>Show answer</summary><p>${right || `(${letter})`}</p></details>` : ''}</div>`;
    }).get();
    $(ol).replaceWith(cards.join(''));
    key.remove();
  });
}

// Sections after the modules have no units; their kicker names what they are for.
const EXTRA_KICKER = [[/recent|development|update/i, 'Updates'], [/table|fact/i, 'At a glance'], [/revision|practice|mcq/i, 'Practice']];

const out = [];
let unitNo = 0;
$('section').each((mi, sec) => {
  const s = $(sec);
  const h1 = s.children('h1.module').first();
  if (!h1.length) return;
  const mm = t(h1).match(/^Module\s+([A-Z])\s*[—–-]\s*(.*)$/i);
  const letter = mm ? mm[1] : null;
  const name = mm ? mm[2] : t(h1);
  const id = s.attr('id') || (letter ? `module-${letter.toLowerCase()}` : `extra-${mi}`);
  const note = t(s.children('.module-note')) || (mi === 0 ? docNote : '');
  if (letter) stats.modules++;
  else stats.extras++;

  // Units: everything from one unit heading to the next. A section without units is one run of topics.
  const units = [];
  s.children('h2.unit').each((ui, h) => {
    units.push({ h, body: $(h).nextUntil('h2.unit') });
  });
  if (!units.length) units.push({ h: null, body: s.children().not('h1.module, .module-note') });

  const mod = { topics: 0, must: 0, good: 0, mcq: 0 };
  units.forEach(({ h, body }) => {
    let num = 0, title = '';
    if (h) {
      const raw = t(h);
      const m = raw.match(/^Unit\s+(\d+)\s*[·:.—–-]\s*(.*)$/i);
      num = m ? +m[1] : unitNo + 1;
      unitNo = num;
      title = titleCase(m ? m[2] : raw).replace(/\s+[—–]\s+/g, ': ');
      stats.units++;
    }

    const blocks = body.filter('.topic-block').add(body.find('.topic-block'));
    const tally = { must: 0, good: 0 };
    blocks.each((bi, b) => {
      const k = starOf($(b).find('h3.topic').first());
      if (k) tally[k]++;
    });

    // Callouts, tables and revision inside this unit, then the topic cards.
    const mcqBefore = stats.mcq;
    box(body, '.plain', 'plain', 'In plain words', 'plain');
    box(body, '.eg', 'example', 'Example', 'examples');
    box(body, '.mcq', 'exam', 'MCQ', 'mcq');
    box(body, '.remember', 'remember', 'Remember', 'remember');
    mod.mcq += stats.mcq - mcqBefore;
    body.find('.table-wrap').add(body.filter('.table-wrap')).each((i, w) => { $(w).replaceWith($(w).html()); });
    revision(body);
    stats.figures += body.find('figure.fig').add(body.filter('figure.fig')).length;

    const topics = blocks.toArray();
    const where = h ? 'unit' : 'section';
    topics.forEach((b, j) => {
      const th = $(b).find('h3.topic').first();
      const kind = starOf(th);
      th.find('.star').remove();
      const html = th.html().trim();
      const plain = t(th);
      const tid = th.attr('id') || (h ? `u${num}-t${j + 1}` : `${id}-t${j + 1}`);
      th.remove();
      if (!kind) stats.unmarked.push(`${h ? `Unit ${num}` : name}: ${plain}`);
      const chip = kind === 'must' ? '<span class="rd-star">★ Must-learn</span>' : kind === 'good' ? '<span class="rd-star">☆ Good to know</span>' : '';
      const no = `<span class="rd-card-no" title="Topic ${j + 1} of ${topics.length} in this ${where}">${j + 1}<small>/${topics.length}</small></span>`;
      $(b).replaceWith(`<article class="rd-card ${kind === 'good' ? 'is-good' : 'is-must'}"><h3 class="rd-card-title" id="${tid}" data-toc="${esc(`${kind === 'good' ? '☆ ' : kind === 'must' ? '★ ' : ''}${plain}`)}">${no}${chip}${html}</h3>${$(b).html().trim()}</article>`);
    });

    const n = topics.length;
    mod.topics += n;
    mod.must += tally.must;
    mod.good += tally.good;
    stats.topics += n;
    stats.must += tally.must;
    stats.good += tally.good;
    if (!h) return;
    const count = plural(n, 'topic');
    const line = `<span class="rd-ch-count">${count} · ${tally.must} ★ must-learn${tally.good ? ` · ${tally.good} ☆ good to know` : ''}</span>`;
    $(h).replaceWith(`<h2 class="rd-chapter" id="unit-${num}" data-toc="${esc(`${num}. ${title}`)}" data-count="${count}" data-count-must="${tally.must} ★"><span class="rd-ch-no">Module ${letter} · Unit ${num}</span>${esc(title)}${line}</h2>`);
  });
  h1.remove();
  s.children('.module-note').remove();

  const hasUnits = !!units[0].h;
  const kicker = letter ? `Module ${letter}` : (EXTRA_KICKER.find(([re]) => re.test(name)) || [0, 'Extra'])[1];
  const label = letter ? `Module ${letter} · ${name}` : name;
  out.push(`<h1 class="rd-part${letter ? '' : ' rd-appendix'}" id="${id}" data-toc="${esc(label)}" data-count="${plural(mod.topics, 'topic')}" data-count-must="${mod.must} ★"><span class="rd-part-no">${esc(kicker)}</span>${esc(name)}</h1>`);
  if (note) out.push(`<p class="rd-part-lead">${esc(note)}</p>`);
  out.push(`<p class="rd-part-tally">${hasUnits ? `<span><b>${units.length}</b> units</span>` : ''}<span><b>${mod.topics}</b> topics</span><span><b>${mod.must}</b> ★ must-learn</span>${mod.good ? `<span><b>${mod.good}</b> ☆ good to know</span>` : ''}${mod.mcq ? `<span><b>${mod.mcq}</b> MCQ pointers</span>` : ''}</p>`);
  out.push(s.html());
});

const doc = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>${esc(t($('title')) || 'DBF paper')}</title>
</head>
<body>
${out.join('\n')}
</body>
</html>
`;
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'content.html'), doc);

const check = cheerio.load(doc);
const seen = new Map();
check('[id]').each((i, e) => seen.set(e.attribs.id, (seen.get(e.attribs.id) || 0) + 1));
stats.duplicateIds = [...seen].filter(([, n]) => n > 1).map(([k]) => k);
stats.brokenLinks = check('a[href^="#"]').filter((i, a) => !seen.has(check(a).attr('href').slice(1))).length;
stats.leftoverAgentText = /Agent Notes|not for reading/i.test(doc);
stats.leftoverSourceBlocks = check('.topic-block, .mcq, .remember, .plain, .eg').length;
stats.practiceWithoutAnswer = check('.rd-q').filter((i, e) => !check(e).find('details').length).length;
stats.outputKB = Math.round(Buffer.byteLength(doc) / 1024);
console.log(JSON.stringify(stats, null, 2));
