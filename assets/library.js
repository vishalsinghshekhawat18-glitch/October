'use strict';

(async () => {
  const O = October;
  const $ = s => document.querySelector(s);
  const data = O.data;
  O.applyTheme();

  // Greeting and reading stats
  const hour = new Date().getHours();
  $('#greeting').textContent =
    hour < 5 ? 'Reading by lamplight.' :
    hour < 12 ? 'Good morning.' :
    hour < 17 ? 'Good afternoon.' : 'Good evening.';
  $('#today').textContent = new Date().toLocaleDateString(undefined, { weekday: 'long', day: 'numeric', month: 'long' });

  const todaySec = data.daily[O.dayKey()] || 0;
  const totalSec = Object.values(data.books).reduce((a, b) => a + (b.seconds || 0), 0);
  const streak = O.streak();
  const stats = [todaySec >= 60 ? `${O.fmtMinutes(todaySec / 60)} read today` : 'A fresh page today'];
  if (streak > 1) stats.push(`${streak}-day streak`);
  if (totalSec >= 60) stats.push(`${O.fmtMinutes(totalSec / 60)} in the library`);
  $('#stats').innerHTML = stats.map(s => `<span>${O.esc(s)}</span>`).join('');

  O.themeMenu();

  let lib;
  try {
    lib = await O.library();
  } catch (e) {
    $('#shelf').innerHTML = '<p class="load-error">The shelf could not be loaded. Check your connection and refresh.</p>';
    return;
  }

  const subjects = lib.subjects || [];
  const capacity = (lib.library && lib.library.capacity) || 12;
  const isReady = s => s.status === 'ready';

  // Shelf: general subjects first, then one labelled row per exam series (subjects.json "series").
  let delay = 0;
  const progressOf = O.progress;
  const card = (s, number) => O.bookCard(s, number, delay++);
  const slot = (html, extra = '') => `<div class="book is-empty${extra}" aria-hidden="true" style="animation-delay:${delay++ * 60}ms"><div class="empty-slot">${html}</div></div>`;

  const series = (lib.library && lib.library.series) || [];
  const general = subjects.filter(s => !s.series || !series.some(x => x.id === s.series));
  const groups = [{ books: general }, ...series.map(x => ({ series: x, books: subjects.filter(s => s.series === x.id) }))];
  const grouped = groups.length > 1;

  // What a series calls its slots ("item" in subjects.json, e.g. "subject"); papers by default.
  const itemOf = x => x.item || 'paper';
  const plural = (n, word) => `${n} ${word}${n === 1 ? '' : 's'}`;

  function seriesHead(x, books) {
    const total = (x.papers || []).length || books.length;
    const pct = books.reduce((a, s) => a + (progressOf(s.slug) || 0), 0) / Math.max(total, 1);
    return `<a class="shelf-group-head" href="exam.html?exam=${encodeURIComponent(x.id)}">
      <h3>${O.esc(x.name)}${x.full ? ` <span>${O.esc(x.full)}</span>` : ''}</h3>
      <p>${books.length} of ${plural(total, itemOf(x))} added${pct >= .005 ? ` · ${Math.round(pct * 100)}% of the exam read` : ''}<b>Syllabus ›</b></p>
    </a>`;
  }

  // Empty slots fill out the last row of the general shelf, so it never ends with a lone gap.
  // Each exam row links to its own page with the syllabus and coverage.
  const shelf = $('#shelf');
  // Tabs above a grouped shelf: All, the general subjects, or one exam. The choice is remembered.
  const keyOf = g => g.series ? g.series.id : 'general';
  let tab = groups.some(g => keyOf(g) === data.prefs.shelfTab) ? data.prefs.shelfTab : 'all';
  const tabs = $('#shelfTabs');
  if (grouped) {
    tabs.innerHTML = [['all', 'All', subjects.length], ...groups.filter(g => g.books.length || g.series).map(g => [keyOf(g), g.series ? g.series.name : 'My subjects', g.books.length])]
      .map(([k, name, n]) => `<button class="shelf-tab" role="tab" data-tab="${k}" aria-selected="${k === tab}">${O.esc(name)} <span>${n}</span></button>`).join('');
    tabs.hidden = false;
    tabs.addEventListener('click', e => {
      const b = e.target.closest('[data-tab]');
      if (!b || b.dataset.tab === tab) return;
      tab = b.dataset.tab;
      data.prefs.shelfTab = tab;
      O.save();
      tabs.querySelectorAll('[data-tab]').forEach(t => t.setAttribute('aria-selected', String(t.dataset.tab === tab)));
      renderShelf();
    });
  }
  function renderShelf() {
    delay = 0;
    shelf.classList.toggle('is-grouped', grouped);
    const shown = groups.filter(g => tab === 'all' || keyOf(g) === tab);
    const html = shown.map((g, gi) => {
      if (!g.series) return `<div class="shelf">${g.books.map((s, i) => card(s, i + 1)).join('')}</div>`;
      return `<section class="shelf-group">${seriesHead(g.series, g.books)}<div class="shelf">${
        g.books.sort((a, b) => (a.paper || 0) - (b.paper || 0)).map(s => card(s)).join('')
      }</div></section>`;
    });
    shelf.innerHTML = grouped ? html.join('') : html[0].replace(/^<div class="shelf">|<\/div>$/g, '');
    const first = grouped ? shelf.querySelector('.shelf') : shelf;
    const cols = getComputedStyle(first).gridTemplateColumns.split(' ').length;
    shelf.dataset.cols = cols;
    if (!shown.some(g => !g.series)) return;
    const n = general.length;
    let empty = (cols - (n % cols)) % cols;
    if (n < cols) empty = cols - n;
    empty = Math.min(empty, grouped ? 1 : Infinity, Math.max(0, capacity - subjects.length));
    for (let i = 0; i < empty; i++) first.insertAdjacentHTML('beforeend', slot('<b>+</b>Room for a new subject'));
  }
  renderShelf();
  addEventListener('resize', () => {
    const first = shelf.classList.contains('is-grouped') ? shelf.querySelector('.shelf') : shelf;
    if (+shelf.dataset.cols !== getComputedStyle(first).gridTemplateColumns.split(' ').length) renderShelf();
  });
  const readyCount = subjects.filter(isReady).length;
  $('#shelfCount').textContent = `${subjects.length} ${subjects.length === 1 ? 'subject' : 'subjects'} · ${readyCount} ready to read`;

  // Jump back in: the book read last as a large card, then up to two other books in progress, newest first.
  const all = [...subjects, ...(lib.guide ? [lib.guide] : [])];
  const coverNo = s => s.kind === 'guide' ? null : general.indexOf(s) + 1 || null;
  const reading = all
    .filter(s => isReady(s) && data.books[s.slug] && data.books[s.slug].pos && data.books[s.slug].pos.pct > .005 && data.books[s.slug].pos.pct < .995)
    .sort((a, b) => (b.slug === data.last) - (a.slug === data.last) || (data.books[b.slug].pos.at || 0) - (data.books[a.slug].pos.at || 0));
  const last = reading[0];
  if (last) {
    const lastBook = data.books[last.slug];
    const pct = lastBook.pos.pct;
    const left = lastBook.pos.minutesLeft;
    const also = reading.slice(1, 3).map(s => {
      const p = data.books[s.slug].pos;
      return `<a class="also-row" href="reader.html?book=${encodeURIComponent(s.slug)}">
        ${O.cover(s, coverNo(s))}
        <span class="also-text"><b>${O.esc(s.title)}</b><span>${O.esc(p.section || 'Where you left off')}</span></span>
        <span class="also-pct">${Math.round(p.pct * 100)}%</span>
      </a>`;
    }).join('');
    const el = $('#continue');
    el.outerHTML = `<div class="jump${also ? ' has-also' : ''}"><a class="continue" id="continue" href="reader.html?book=${encodeURIComponent(last.slug)}">
      ${O.cover(last, coverNo(last))}
      <div>
        <p class="eyebrow">Continue reading</p>
        <h2 class="continue-title">${O.esc(last.title)}</h2>
        <p class="continue-sec">${O.esc(lastBook.pos.section || 'Where you left off')}</p>
        <div class="continue-foot">
          <div class="bar"><span style="width:${(pct * 100).toFixed(1)}%"></span></div>
          <span class="continue-pct">${Math.round(pct * 100)}%${left ? ` · ${O.fmtMinutes(left)} left` : ''}</span>
          <span class="resume">Resume <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
        </div>
      </div>
    </a>${also ? `<div class="also"><p class="eyebrow">Also reading</p>${also}</div>` : ''}</div>`;
  }

  // Reader's guide
  if (lib.guide) {
    const g = $('#guide');
    g.outerHTML = `<a class="guide" id="guide" href="reader.html?book=${encodeURIComponent(lib.guide.slug)}">
      ${O.cover(lib.guide)}
      <span class="guide-text"><b>${O.esc(lib.guide.title)}</b><span>${O.esc(lib.guide.blurb || 'How to get the most out of this library')}</span></span>
      <svg class="guide-arrow" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
    </a>`;
  }
})();
