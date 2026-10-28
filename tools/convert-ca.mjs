// Build the Current Affairs book from its source files (Static Bank and monthly compilations).
// Usage: node convert-ca.mjs <outDir> <file.html> [<file.html> …]
// Static Bank comes first, then months newest first. Writes <outDir>/content.html and prints a summary.
import * as cheerio from 'cheerio';
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const [outDir, ...files] = process.argv.slice(2);
const MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
const SMALL = /^(and|of|the|in|to|for|on|with|by|or|a|an|at|vs)$/i;
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const cap = w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase();
const titleCase = s => s.split(/(\s+)/).map((w, i) => (i > 0 && SMALL.test(w) ? w.toLowerCase() : w)).join('');

function partInfo($, file) {
  const t = e => $(e).text().replace(/\s+/g, ' ').trim();
  const h = t($('.cover h1').first()) || t($('title'));
  const ps = $('.cover > p').map((i, p) => t(p)).get();
  if (/static/i.test(h)) {
    return { kind: 'static', slug: 'static', title: 'Static Bank', kicker: 'Static', lead: ps.find(p => !/must-learn/.test(p)) || '', sort: Infinity };
  }
  // "CURRENT AFFAIRS: OCTOBER 2026", or a range like "JANUARY–MARCH 2026" / "JAN–MAR 2026"
  const name = h.replace(/^current affairs\s*:?\s*/i, '');
  const monthOf = w => MONTHS.find(m => w.length >= 3 && m.startsWith(w.toLowerCase()));
  const found = (name.match(/[A-Za-z]+/g) || []).map(monthOf).filter(Boolean);
  const year = +((name.match(/\b(20\d{2})\b/) || [])[1] || 0);
  if (!found.length || !year) throw new Error(`Can't tell which month ${file} covers (heading: "${h}")`);
  const last = Math.max(...found.map(m => MONTHS.indexOf(m)));
  const title = name.replace(/[A-Za-z]+/g, w => (monthOf(w) ? cap(monthOf(w)) : w));
  const coverage = (ps.join(' | ').match(/Coverage[^|]*/i) || [''])[0].trim();
  const slug = `${found.map(m => m.slice(0, 3)).join('-')}-${year}`;
  return { kind: 'month', slug, title, kicker: 'Current Affairs', lead: coverage, sort: year * 12 + last };
}

const stats = { parts: [], sections: 0, cards: 0, must: 0, good: 0, recall: 0, boxes: 0, agentNotesRemoved: 0 };
const parts = files.map(file => {
  const $ = cheerio.load(readFileSync(file, 'utf8'));
  return { $, file, info: partInfo($, file) };
}).sort((a, b) => b.info.sort - a.info.sort);

const out = [];
for (const { $, info } of parts) {
  const t = e => $(e).text().replace(/\s+/g, ' ').trim();
  const P = info.slug;
  const pstat = { title: info.title, sections: 0, cards: 0, must: 0, recall: 0 };

  // Section names: the source's own contents links have the nicest capitalisation.
  const tocNames = new Map($('.toc a').map((i, a) => [[($(a).attr('href') || '').slice(1), t(a)]]).get());

  // Drop editor notes, navigation, scripts, cover and the hint line.
  $('section.notes').each((i, s) => { stats.agentNotesRemoved++; $(s).remove(); });
  $('h1.sec').filter((i, h) => /agent notes/i.test(t(h))).each((i, h) => { stats.agentNotesRemoved++; $(h).nextAll().remove(); $(h).remove(); });
  $('nav, script, style, .cover, .toc, p.hint').remove();
  $('*').contents().filter((i, n) => n.type === 'comment').remove();

  // Prefix ids so several months can live in one book.
  $('[id]').each((i, e) => { $(e).attr('id', `${P}-${$(e).attr('id')}`); });
  $('a[href^="#"]').each((i, a) => { $(a).attr('href', `#${P}-${$(a).attr('href').slice(1)}`); });

  const main = $('main').length ? $('main') : $('body');

  // Counts, as the source shows them: cards numbered within each section, and each section's totals.
  const isMust = d => /^\s*★/.test(t($(d).children('summary'))) && !$(d).hasClass('opt');
  main.find('h1.sec').each((i, h) => {
    // A section, plus anything left between it and the next one (some files have stray Q&A there).
    const own = $(h).closest('section');
    const sec = own.length ? own.add(own.nextUntil('section, h1.sec, :has(h1.sec)')) : $(h).nextUntil('h1.sec').addBack();
    const details = sec.find('details').add(sec.filter('details'));
    const cards = details.filter('.card').toArray();
    cards.forEach((d, j) => $(d).attr({ 'data-no': j + 1, 'data-of': cards.length }));
    const questions = details.not('.card').filter((j, d) => $(d).parent().is('.rev') || $(d).find('.ans').length).length;
    $(h).attr({ 'data-n': cards.length, 'data-m': cards.filter(isMust).length, 'data-q': questions });
  });

  // Revision quizzes: group headings stay as sections; each Q&A becomes a recall item with a hidden answer.
  main.find('.rev').each((i, rev) => {
    const html = [];
    let items = [];
    const flush = () => { if (items.length) html.push(`<div class="rd-recall"><ol>${items.join('')}</ol></div>`); items = []; };
    $(rev).children().each((j, el) => {
      if ($(el).is('details')) {
        const q = $(el).children('summary').html() || '';
        const a = $(el).find('.ans').html() || $(el).children(':not(summary)').html() || '';
        items.push(`<li><span class="rd-recall-q">${q.trim()}</span><details class="rd-answer"><summary>Show answer</summary><p>${a.trim()}</p></details></li>`);
        pstat.recall++;
      } else {
        flush();
        if ($(el).is('h3')) $(el).attr('data-keep', '3');
        html.push($.html(el));
      }
    });
    flush();
    $(rev).replaceWith(html.join(''));
  });

  // Stray Q&A blocks outside the quiz: consecutive ones become one recall list.
  main.find('details:not(.card)').filter((i, d) => $(d).find('.ans').length && !$(d).closest('.rd-recall').length).each((i, d) => {
    const item = `<li><span class="rd-recall-q">${($(d).children('summary').html() || '').trim()}</span><details class="rd-answer"><summary>Show answer</summary><p>${($(d).find('.ans').html() || '').trim()}</p></details></li>`;
    const prev = $(d).prev();
    if (prev.is('.rd-recall')) {
      prev.children('ol').append(item);
      $(d).remove();
    } else {
      $(d).replaceWith(`<div class="rd-recall"><ol>${item}</ol></div>`);
    }
    pstat.recall++;
  });

  // Headings: sections → chapters, subheads → sections.
  main.find('h3:not([data-keep])').each((i, h) => { h.tagName = 'h4'; });
  main.find('h3[data-keep]').removeAttr('data-keep');
  main.find('h2').each((i, h) => { h.tagName = 'h3'; });
  main.find('h1.sec').each((i, h) => {
    const id = $(h).attr('id') || `${P}-s${i + 1}`;
    const raw = tocNames.get(id.slice(P.length + 1)) || t(h);
    const m = raw.match(/^(\d+)\.\s*(.*)$/);
    const num = m ? m[1] : String(i + 1);
    const name = titleCase(m ? m[2] : raw);
    const [n, mu, q] = ['data-n', 'data-m', 'data-q'].map(a => +$(h).attr(a) || 0);
    const count = [n && `${n} item${n === 1 ? '' : 's'}`, q && `${q} question${q === 1 ? '' : 's'}`].filter(Boolean).join(' · ');
    const mustCount = [n && `${mu} ★`, q && `${q} question${q === 1 ? '' : 's'}`].filter(Boolean).join(' · ');
    const tally = n ? `<span class="rd-ch-count">${n} items · ${mu} ★ must-learn · ${n - mu} ☆ good to know</span>` : q ? `<span class="rd-ch-count">${q} questions</span>` : '';
    $(h).replaceWith(`<h2 class="rd-chapter" id="${id}" data-toc="${esc(`${num}. ${name}`)}"${count ? ` data-count="${count}" data-count-must="${mustCount}"` : ''}><span class="rd-ch-no">${esc(info.title)} · Section ${num}</span>${esc(name)}${tally}</h2>`);
    pstat.sections++;
  });

  // News and fact cards: headline with a must-learn / good-to-know marker, body expanded for reading.
  main.find('details.card').each((i, d) => {
    const sum = $(d).children('summary');
    const title = (sum.html() || '').trim();
    const must = isMust(d);
    const clean = title.replace(/^\s*[★☆]\s*/, '');
    const body = $(d).children('.body').length ? $(d).children('.body').html() : $(d).children(':not(summary)').toArray().map(e => $.html(e)).join('');
    const no = $(d).attr('data-no') ? `<span class="rd-card-no" title="Item ${$(d).attr('data-no')} of ${$(d).attr('data-of')} in this section">${$(d).attr('data-no')}<small>/${$(d).attr('data-of')}</small></span>` : '';
    $(d).replaceWith(`<article class="rd-card ${must ? 'is-must' : 'is-good'}"><h4 class="rd-card-title">${no}<span class="rd-star">${must ? '★ Must-learn' : '☆ Good to know'}</span>${clean}</h4>${body}</article>`);
    pstat.cards++;
    if (must) pstat.must++;
  });

  // Study notes: exam angles, memory hooks and mnemonics become labelled callouts.
  const box = (sel, kind, label, prefix) => main.find(sel).each((i, el) => {
    let html = $(el).html().trim().replace(prefix, '').trim();
    $(el).replaceWith(`<aside class="rd-box rd-box-${kind}"><span class="rd-box-label">${label}</span><p>${html}</p></aside>`);
    stats.boxes++;
  });
  box('.angle', 'exam', 'Exam angle', /^<(strong|b)>\s*Exam angle:?\s*<\/\1>\s*/i);
  box('.hook', 'remember', 'Remember', /^<(strong|b)>\s*Remember:?\s*<\/\1>\s*/i);
  box('p.mn', 'mnemonic', 'Mnemonic', /^<(strong|b)>\s*Mnemonic:?\s*<\/\1>\s*/i);
  box('.plain', 'plain', 'In plain words', /^<(strong|b)>\s*In plain words:?\s*<\/\1>\s*/i);

  main.find('div.tw').each((i, w) => { $(w).replaceWith($(w).html()); });

  const total = [pstat.cards && `${pstat.cards} items`, pstat.recall && `${pstat.recall} questions`].filter(Boolean).join(' · ');
  const totalMust = [pstat.cards && `${pstat.must} ★`, pstat.recall && `${pstat.recall} questions`].filter(Boolean).join(' · ');
  out.push(`<h1 class="rd-part" id="${P}" data-toc="${esc(info.title)}"${total ? ` data-count="${total}" data-count-must="${totalMust}"` : ''}><span class="rd-part-no">${esc(info.kicker)}</span>${esc(info.title)}</h1>`);
  if (info.lead) out.push(`<p class="rd-part-lead">${esc(info.lead)}</p>`);
  if (pstat.cards) out.push(`<p class="rd-part-tally"><span><b>${pstat.cards}</b> items</span><span><b>${pstat.must}</b> ★ must-learn</span><span><b>${pstat.cards - pstat.must}</b> ☆ good to know</span>${pstat.recall ? `<span><b>${pstat.recall}</b> revision questions</span>` : ''}</p>`);
  out.push(main.html());

  stats.sections += pstat.sections;
  stats.cards += pstat.cards;
  stats.must += pstat.must;
  stats.good += pstat.cards - pstat.must;
  stats.recall += pstat.recall;
  stats.parts.push(`${pstat.title}: ${pstat.sections} sections, ${pstat.cards} cards (${pstat.must} ★), ${pstat.recall} recall`);
}

const doc = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Current Affairs</title>
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
stats.leftoverAgentText = /Agent Notes|Sources ingested/i.test(doc);
stats.leftoverDetailsCards = check('details.card').length;
stats.brokenLinks = check('a[href^="#"]').filter((i, a) => !seen.has(check(a).attr('href').slice(1))).length;
stats.outputKB = Math.round(Buffer.byteLength(doc) / 1024);
console.log(JSON.stringify(stats, null, 2));
