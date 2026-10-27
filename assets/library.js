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

  setupThemeMenu();

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

  function progressOf(slug) {
    const b = data.books[slug];
    return b && b.pos ? b.pos.pct : null;
  }

  function stateText(s) {
    if (!isReady(s)) return 'Arriving soon';
    const pct = progressOf(s.slug);
    if (pct == null || pct < .005) return 'Not started';
    if (pct >= .995) return 'Finished';
    return `${Math.round(pct * 100)}% read`;
  }

  // Shelf
  const cards = subjects.map((s, i) => {
    const pct = progressOf(s.slug) || 0;
    return `<a class="book${isReady(s) ? '' : ' is-soon'}" href="reader.html?book=${encodeURIComponent(s.slug)}" style="animation-delay:${i * 60}ms">
      <div class="book-cover-wrap">${isReady(s) ? '' : '<span class="tag">Soon</span>'}${O.cover(s, i + 1)}</div>
      <div class="book-meta">
        <span class="book-title">${O.esc(s.title)}</span>
        ${isReady(s) ? `<div class="bar"><span style="width:${(pct * 100).toFixed(1)}%"></span></div>` : ''}
        <span class="book-state">${stateText(s)}</span>
      </div>
    </a>`;
  });
  // Empty slots fill out the last row of the shelf, so it never ends with a lone gap.
  const shelf = $('#shelf');
  function renderShelf() {
    shelf.innerHTML = cards.join('');
    const cols = getComputedStyle(shelf).gridTemplateColumns.split(' ').length;
    const n = subjects.length;
    let empty = (cols - (n % cols)) % cols;
    if (n < cols) empty = cols - n;
    empty = Math.min(empty, Math.max(0, capacity - n));
    for (let i = 0; i < empty; i++) {
      shelf.insertAdjacentHTML('beforeend', `<div class="book is-empty" aria-hidden="true" style="animation-delay:${(n + i) * 60}ms">
        <div class="empty-slot"><b>+</b>Room for a new subject</div>
      </div>`);
    }
    shelf.dataset.cols = cols;
  }
  renderShelf();
  addEventListener('resize', () => {
    if (+shelf.dataset.cols !== getComputedStyle(shelf).gridTemplateColumns.split(' ').length) renderShelf();
  });
  const readyCount = subjects.filter(isReady).length;
  $('#shelfCount').textContent = `${subjects.length} ${subjects.length === 1 ? 'subject' : 'subjects'} · ${readyCount} ready to read`;

  // Continue reading
  const all = [...subjects, ...(lib.guide ? [lib.guide] : [])];
  const last = all.find(s => s.slug === data.last && isReady(s));
  const lastBook = last && data.books[last.slug];
  if (lastBook && lastBook.pos && lastBook.pos.pct > .005 && lastBook.pos.pct < .995) {
    const pct = lastBook.pos.pct;
    const left = lastBook.pos.minutesLeft;
    const el = $('#continue');
    el.outerHTML = `<a class="continue" id="continue" href="reader.html?book=${encodeURIComponent(last.slug)}">
      ${O.cover(last, last.kind === 'guide' ? null : subjects.indexOf(last) + 1)}
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
    </a>`;
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

  function setupThemeMenu() {
    const btn = $('#themeBtn');
    const pop = $('#themePop');
    const label = $('#themeLabel');
    const current = () => data.prefs.theme || 'auto';

    function render() {
      const cur = current();
      label.textContent = O.THEMES.find(t => t.id === cur).label;
      pop.innerHTML = O.THEMES.map(t => `<button class="theme-opt" data-theme-id="${t.id}" aria-pressed="${t.id === cur}">
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
      O.save();
      O.applyTheme();
      render();
    });
    document.addEventListener('click', e => { if (!e.target.closest('.theme-menu')) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  }
})();
