'use strict';

// An exam's own page: syllabus coverage, the books added so far, and every paper with its state.
(async () => {
  const O = October;
  const $ = s => document.querySelector(s);
  const data = O.data;
  O.applyTheme();
  O.themeMenu();

  const fail = msg => { $('#examBody').innerHTML = `<p class="load-error">${msg} <a href="./">Back to the library</a></p>`; };
  let lib;
  try {
    lib = await O.library();
  } catch (e) {
    return fail('This page could not be loaded. Check your connection and refresh.');
  }

  const id = new URLSearchParams(location.search).get('exam');
  const x = ((lib.library && lib.library.series) || []).find(s => s.id === id);
  if (!x) {
    $('#examName').textContent = 'Not found';
    return fail('This exam isn’t in the library.');
  }

  const books = (lib.subjects || []).filter(s => s.series === x.id).sort((a, b) => (a.paper || 0) - (b.paper || 0));
  const papers = (x.papers || []).length ? x.papers : books.map(s => s.title);
  const word = x.item || 'paper';
  const plural = (n, w) => `${n} ${w}${n === 1 ? '' : 's'}`;
  const byPaper = new Map(books.map(s => [s.paper, s]));

  // A ready book covers its paper in full; one still being written counts by its "coverage" (0–1) in subjects.json.
  const share = s => !s ? 0 : typeof s.coverage === 'number' ? Math.max(0, Math.min(1, s.coverage)) : O.isReady(s) ? 1 : 0;
  const shares = papers.map((_, i) => share(byPaper.get(i + 1)));
  const covered = shares.reduce((a, v) => a + v, 0) / papers.length;
  const done = shares.filter(v => v >= 1).length;
  const read = books.reduce((a, s) => a + (O.progress(s.slug) || 0), 0) / papers.length;

  document.title = `${x.name} · October Library`;
  $('#examName').textContent = x.name;
  $('#examFull').textContent = x.full || '';
  $('#examStats').innerHTML = [
    `${done} of ${plural(papers.length, word)} have notes`,
    read >= .005 ? `${Math.round(read * 100)}% of the exam read` : 'Not started yet',
  ].map(O.esc).join(' · ');

  const segs = papers.map((name, i) => {
    const v = shares[i];
    return `<span class="cov-seg${v >= 1 ? ' is-done' : v > 0 ? ' is-part' : ''}" style="--fill:${(v * 100).toFixed(0)}%" title="${O.esc(name)}"></span>`;
  }).join('');

  const ready = books.filter(O.isReady);
  const rows = papers.map((name, i) => {
    const s = byPaper.get(i + 1);
    const v = shares[i];
    const no = `<span class="syl-no">${i + 1}</span>`;
    if (s && O.isReady(s)) {
      const b = data.books[s.slug];
      const pct = O.progress(s.slug) || 0;
      const where = pct > .005 && pct < .995 && b.pos.section ? ` · ${O.esc(b.pos.section)}` : '';
      return `<li><a class="syl-row is-ready" href="reader.html?book=${encodeURIComponent(s.slug)}">${no}
        <span class="syl-text"><b>${O.esc(name)}</b><small>${O.stateText(s)}${where}</small></span>
        <span class="syl-go" aria-hidden="true">›</span></a></li>`;
    }
    const state = v > 0 ? `Notes ${Math.round(v * 100)}% written` : 'Notes not created yet';
    return `<li><div class="syl-row">${no}<span class="syl-text"><b>${O.esc(name)}</b><small>${state}</small></span></div></li>`;
  }).join('');

  $('#examBody').innerHTML = `
    <div class="coverage">
      <div class="cov-head"><span>Syllabus covered by notes</span><b>${Math.round(covered * 100)}%</b></div>
      <div class="cov-bar" role="img" aria-label="${done} of ${plural(papers.length, word)} have notes">${segs}</div>
    </div>
    ${ready.length ? `<section class="exam-sec">
      <div class="section-head"><h2>Your books</h2><p>${plural(ready.length, 'book')} ready to read</p></div>
      <div class="shelf">${ready.map((s, i) => O.bookCard(s, null, i)).join('')}</div>
    </section>` : ''}
    <section class="exam-sec">
      <div class="section-head"><h2>Syllabus</h2><p>${plural(papers.length, word)}</p></div>
      <ol class="syl">${rows}</ol>
    </section>`;
})();
