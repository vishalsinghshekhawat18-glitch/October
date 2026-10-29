// Build an IIBF DBF paper from its notes file ("DBF design system": modules › units › ★/☆ topics).
// Usage: node convert-dbf.mjs <source.html> <outDir>
// Modules become parts, units become chapters, and each topic a numbered card. Writes <outDir>/content.html.
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

const stats = { modules: 0, units: 0, topics: 0, must: 0, good: 0, unmarked: [], mcq: 0, remember: 0, figures: 0, agentNotesRemoved: 0 };

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

const out = [];
let unitNo = 0;
$('section').each((mi, sec) => {
  const s = $(sec);
  const h1 = s.children('h1.module').first();
  if (!h1.length) return;
  const [, letter, name] = t(h1).match(/^Module\s+([A-Z])\s*[—–-]\s*(.*)$/i) || [null, String.fromCharCode(65 + mi), t(h1)];
  const id = s.attr('id') || `module-${letter.toLowerCase()}`;
  const note = t(s.children('.module-note')) || (mi === 0 ? docNote : '');
  stats.modules++;

  // Units: everything from one unit heading to the next.
  const units = [];
  s.children('h2.unit').each((ui, h) => {
    const body = $(h).nextUntil('h2.unit');
    units.push({ h, body });
  });

  const mod = { topics: 0, must: 0, good: 0, mcq: 0 };
  units.forEach(({ h, body }) => {
    const raw = t(h);
    const m = raw.match(/^Unit\s+(\d+)\s*[·:.—–-]\s*(.*)$/i);
    const num = m ? +m[1] : unitNo + 1;
    unitNo = num;
    const title = titleCase(m ? m[2] : raw).replace(/\s+[—–]\s+/g, ': ');
    stats.units++;

    const blocks = body.filter('.topic-block').add(body.find('.topic-block'));
    const tally = { must: 0, good: 0 };
    blocks.each((bi, b) => {
      const k = starOf($(b).find('h3.topic').first());
      if (k) tally[k]++;
    });

    // Callouts and topic cards inside this unit.
    body.find('.mcq').add(body.filter('.mcq')).each((i, el) => {
      $(el).find('b.tag').remove();
      $(el).replaceWith(`<aside class="rd-box rd-box-exam"><span class="rd-box-label">MCQ</span><p>${$(el).html().trim()}</p></aside>`);
      stats.mcq++;
      mod.mcq++;
    });
    body.find('.remember').add(body.filter('.remember')).each((i, el) => {
      $(el).find('b.tag').remove();
      $(el).replaceWith(`<aside class="rd-box rd-box-remember"><span class="rd-box-label">Remember</span><p>${$(el).html().trim()}</p></aside>`);
      stats.remember++;
    });
    body.find('.table-wrap').add(body.filter('.table-wrap')).each((i, w) => { $(w).replaceWith($(w).html()); });
    stats.figures += body.find('figure.fig').add(body.filter('figure.fig')).length;

    // Re-select the topic blocks (callout replacement kept them, but refresh the set).
    const topics = body.filter('.topic-block').add(body.find('.topic-block')).toArray();
    topics.forEach((b, j) => {
      const th = $(b).find('h3.topic').first();
      const kind = starOf(th);
      th.find('.star').remove();
      const name = th.html().trim();
      const plain = t(th);
      const tid = th.attr('id') || `u${num}-t${j + 1}`;
      th.remove();
      if (!kind) stats.unmarked.push(`Unit ${num}: ${plain}`);
      const chip = kind === 'must' ? '<span class="rd-star">★ Must-learn</span>' : kind === 'good' ? '<span class="rd-star">☆ Good to know</span>' : '';
      const no = `<span class="rd-card-no" title="Topic ${j + 1} of ${topics.length} in this unit">${j + 1}<small>/${topics.length}</small></span>`;
      $(b).replaceWith(`<article class="rd-card ${kind === 'good' ? 'is-good' : 'is-must'}"><h3 class="rd-card-title" id="${tid}" data-toc="${esc(`${kind === 'good' ? '☆ ' : kind === 'must' ? '★ ' : ''}${plain}`)}">${no}${chip}${name}</h3>${$(b).html().trim()}</article>`);
    });

    const n = topics.length;
    mod.topics += n;
    mod.must += tally.must;
    mod.good += tally.good;
    stats.topics += n;
    stats.must += tally.must;
    stats.good += tally.good;
    const count = plural(n, 'topic');
    const countMust = `${tally.must} ★`;
    const line = `<span class="rd-ch-count">${count} · ${tally.must} ★ must-learn${tally.good ? ` · ${tally.good} ☆ good to know` : ''}</span>`;
    const head = `<h2 class="rd-chapter" id="unit-${num}" data-toc="${esc(`${num}. ${title}`)}" data-count="${count}" data-count-must="${countMust}"><span class="rd-ch-no">Module ${letter} · Unit ${num}</span>${esc(title)}${line}</h2>`;
    $(h).replaceWith(head);
  });
  h1.remove();
  s.children('.module-note').remove();

  out.push(`<h1 class="rd-part" id="${id}" data-toc="${esc(`Module ${letter} · ${name}`)}" data-count="${plural(mod.topics, 'topic')}" data-count-must="${mod.must} ★"><span class="rd-part-no">Module ${letter}</span>${esc(name)}</h1>`);
  if (note) out.push(`<p class="rd-part-lead">${esc(note)}</p>`);
  out.push(`<p class="rd-part-tally"><span><b>${units.length}</b> units</span><span><b>${mod.topics}</b> topics</span><span><b>${mod.must}</b> ★ must-learn</span>${mod.good ? `<span><b>${mod.good}</b> ☆ good to know</span>` : ''}<span><b>${mod.mcq}</b> MCQ pointers</span></p>`);
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
stats.leftoverTopicBlocks = check('.topic-block, .mcq, .remember').length;
stats.outputKB = Math.round(Buffer.byteLength(doc) / 1024);
console.log(JSON.stringify(stats, null, 2));
