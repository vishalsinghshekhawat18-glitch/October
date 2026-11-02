'use strict';

// Shared helpers for the library and the reader: saved state, themes, subjects and covers.
const October = (() => {
  const KEY = 'october:v1';
  let data = read();

  function read() {
    let d;
    try { d = JSON.parse(localStorage.getItem(KEY)); } catch (e) { d = null; }
    d = d && typeof d === 'object' ? d : {};
    d.prefs = d.prefs || {};
    d.books = d.books || {};
    d.daily = d.daily || {};
    return d;
  }

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (e) { /* storage unavailable */ }
  }

  function book(slug) {
    const b = data.books[slug] || (data.books[slug] = {});
    b.bookmarks = b.bookmarks || [];
    b.highlights = b.highlights || [];
    b.seconds = b.seconds || 0;
    return b;
  }

  const THEMES = [
    { id: 'auto', label: 'Auto' },
    { id: 'paper', label: 'Paper' },
    { id: 'sepia', label: 'Sepia' },
    { id: 'sage', label: 'Sage' },
    { id: 'dusk', label: 'Dusk' },
    { id: 'night', label: 'Night' },
  ];

  const darkQuery = matchMedia('(prefers-color-scheme: dark)');

  function resolveTheme(t) {
    if (!t || t === 'auto') return darkQuery.matches ? 'dusk' : 'paper';
    return t;
  }

  function applyTheme() {
    document.documentElement.dataset.theme = resolveTheme(data.prefs.theme);
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = getComputedStyle(document.documentElement).getPropertyValue('--bg').trim();
  }

  darkQuery.addEventListener('change', () => {
    if (!data.prefs.theme || data.prefs.theme === 'auto') applyTheme();
  });

  async function library() {
    const res = await fetch('subjects.json', { cache: 'no-cache' });
    if (!res.ok) throw new Error('subjects.json ' + res.status);
    return res.json();
  }

  function dayKey(d = new Date()) {
    return d.toLocaleDateString('en-CA');
  }

  function addTime(slug, seconds) {
    book(slug).seconds += seconds;
    const k = dayKey();
    data.daily[k] = (data.daily[k] || 0) + seconds;
  }

  // Consecutive days with at least a minute of reading, counting today only once it qualifies.
  function streak() {
    const d = new Date();
    if (!(data.daily[dayKey(d)] >= 60)) d.setDate(d.getDate() - 1);
    let n = 0;
    while (data.daily[dayKey(d)] >= 60) {
      n++;
      d.setDate(d.getDate() - 1);
    }
    return n;
  }

  function fmtMinutes(minutes) {
    const m = Math.max(1, Math.round(minutes));
    if (m < 60) return m + ' min';
    const h = Math.floor(m / 60);
    const r = m % 60;
    return r ? `${h} h ${r} min` : `${h} h`;
  }

  function esc(s) {
    return String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }

  // Line emblems for covers; a subject picks one by name in subjects.json.
  const EMBLEMS = {
    book: '<path d="M8 11c6-2.5 12-1.5 16 2.5 4-4 10-5 16-2.5v27c-6-2.5-12-1.5-16 2.5-4-4-10-5-16-2.5z"/><path d="M24 13.5v27"/>',
    graph: '<path d="M9 7v32h32"/><path d="M13 13c9 3 15 11 24 22"/><path d="M13 35c9-3 15-11 24-22"/><circle cx="25" cy="24" r="1.6" fill="currentColor"/>',
    sigma: '<path d="M34 10H14l12 14-12 14h20"/>',
    atom: '<circle cx="24" cy="24" r="2.4" fill="currentColor"/><ellipse cx="24" cy="24" rx="18" ry="7"/><ellipse cx="24" cy="24" rx="18" ry="7" transform="rotate(60 24 24)"/><ellipse cx="24" cy="24" rx="18" ry="7" transform="rotate(120 24 24)"/>',
    flask: '<path d="M19 6h10M21 6v12L10 38a3 3 0 0 0 2.6 4.5h22.8A3 3 0 0 0 38 38L27 18V6"/><path d="M14.5 30h19"/>',
    leaf: '<path d="M10 38C10 18 22 8 40 8c0 18-10 30-30 30z"/><path d="M10 38 28 20"/>',
    globe: '<circle cx="24" cy="24" r="16"/><path d="M8 24h32M24 8c5 5 7 10 7 16s-2 11-7 16c-5-5-7-10-7-16s2-11 7-16z"/>',
    quill: '<path d="M38 8C24 10 14 20 12 36l-2 4"/><path d="M38 8c0 12-8 22-22 24"/><path d="M19 23h8"/>',
    scales: '<path d="M24 8v32M15 40h18M10 14h28"/><path d="m10 14-5 12h10zM38 14l-5 12h10z"/>',
    compass: '<circle cx="24" cy="24" r="16"/><path d="m30 18-4 8-8 4 4-8z"/>',
    columns: '<path d="M8 18 24 8l16 10M10 18h28M13 22v12M21 22v12M27 22v12M35 22v12M8 38h32"/>',
    code: '<path d="M18 14 8 24l10 10M30 14l10 10-10 10M27 10l-6 28"/>',
  };

  function emblem(name) {
    return `<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${EMBLEMS[name] || EMBLEMS.book}</svg>`;
  }

  function cover(s, number) {
    const c = s.cover || {};
    // Papers in an exam series are labelled by paper ("Paper 1") rather than by shelf number; "coverLabel" overrides it.
    const no = s.coverLabel ? s.coverLabel : s.paper ? `Paper ${s.paper}` : number != null ?`No. ${String(number).padStart(2, '0')}` : (s.kind === 'guide' ? 'Start here' : '');
    return `<div class="cover" style="--c1:${c.from || '#3b5570'};--c2:${c.to || '#1c2b3b'};--cink:${c.ink || '#f3ead8'}"><div class="cover-in">
      <span class="cover-no">${esc(no)}</span>
      <span class="cover-emblem">${emblem(c.emblem)}</span>
      <span class="cover-rule"></span>
      <span class="cover-title">${esc(s.title)}</span>
      ${s.subtitle ? `<span class="cover-sub">${esc(s.subtitle)}</span>` : ''}
    </div></div>`;
  }

  const isReady = s => s.status === 'ready';

  function progress(slug) {
    const b = data.books[slug];
    return b && b.pos ? b.pos.pct : null;
  }

  function stateText(s) {
    if (!isReady(s)) return 'Arriving soon';
    const pct = progress(s.slug);
    if (pct == null || pct < .005) return 'Not started';
    if (pct >= .995) return 'Finished';
    return `${Math.round(pct * 100)}% read`;
  }

  // A book on a shelf: cover, title, progress bar and state. i staggers the entrance animation.
  function bookCard(s, number, i = 0) {
    const pct = progress(s.slug) || 0;
    return `<a class="book${isReady(s) ? '' : ' is-soon'}" href="reader.html?book=${encodeURIComponent(s.slug)}" style="animation-delay:${i * 60}ms">
      <div class="book-cover-wrap">${isReady(s) ? '' : '<span class="tag">Soon</span>'}${cover(s, number)}</div>
      <div class="book-meta">
        <span class="book-title">${esc(s.title)}</span>
        ${isReady(s) ? `<div class="bar"><span style="width:${(pct * 100).toFixed(1)}%"></span></div>` : ''}
        <span class="book-state">${stateText(s)}</span>
      </div>
    </a>`;
  }

  function themeMenu() {
    const btn = document.getElementById('themeBtn');
    const pop = document.getElementById('themePop');
    const label = document.getElementById('themeLabel');
    const current = () => data.prefs.theme || 'auto';

    function render() {
      const cur = current();
      label.textContent = THEMES.find(t => t.id === cur).label;
      pop.innerHTML = THEMES.map(t => `<button class="theme-opt" data-theme-id="${t.id}" aria-pressed="${t.id === cur}">
        <span class="swatch" data-swatch="${t.id}">Aa</span>${t.label}</button>`).join('');
    }

    function close() {
      pop.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
    }

    render();
    btn.addEventListener('click', e => {
      e.stopPropagation();
      pop.hidden = !pop.hidden;
      btn.setAttribute('aria-expanded', String(!pop.hidden));
    });
    pop.addEventListener('click', e => {
      const opt = e.target.closest('[data-theme-id]');
      if (!opt) return;
      data.prefs.theme = opt.dataset.themeId;
      save();
      applyTheme();
      render();
    });
    document.addEventListener('click', e => { if (!e.target.closest('.theme-menu')) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  }

  return {
    get data() { return data; },
    save, book, THEMES, resolveTheme, applyTheme, library, dayKey, addTime, streak, fmtMinutes, esc, emblem, cover,
    isReady, progress, stateText, bookCard, themeMenu,
  };
})();
