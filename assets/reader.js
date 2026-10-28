'use strict';

(async () => {
  const O = October;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = O.esc;
  const root = document.documentElement;
  const body = document.body;

  const content = $('#content');
  const titlepage = $('#titlepage');
  const endmatter = $('#endmatter');
  const drawer = $('#drawer');
  const scrim = $('#scrim');
  const settings = $('#settings');
  const selPop = $('#selPop');
  const notePop = $('#notePop');
  const searchBar = $('#searchBar');
  const searchInput = $('#searchInput');
  const track = $('#track');

  const WPM = 230;
  // The reading line: the block crossing it is "where you are". Kept constant so positions don't shift when bars hide.
  const READ_TOP = () => 76;
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasHighlightApi = typeof CSS !== 'undefined' && 'highlights' in CSS && typeof Highlight !== 'undefined';

  // ---------- Preferences ----------
  const prefs = O.data.prefs;
  const DEFAULTS = {
    font: 'literata', size: 19, leading: 'comfy', measure: 'medium', align: 'left', para: 'spaced',
    brightness: 100, tapTurn: true, dropcaps: true, showTime: true, mustOnly: false,
  };
  const FONTS = {
    literata: { label: 'Book', stack: "'Literata', Georgia, serif" },
    garamond: { label: 'Classic', stack: "'EB Garamond', Garamond, Georgia, serif", scale: 1.1 },
    sans: { label: 'Modern', stack: "'Inter', system-ui, sans-serif", scale: .93 },
    legible: { label: 'Legible', stack: "'Atkinson Hyperlegible', Verdana, sans-serif", scale: .97 },
  };
  const SIZES = [15, 16, 17, 18, 19, 20, 22, 24, 26, 28, 30];
  const LEADING = { compact: 1.52, comfy: 1.72, airy: 1.95 };
  const MEASURE = { narrow: '30em', medium: '36em', wide: '44em' };
  for (const k in DEFAULTS) if (prefs[k] === undefined) prefs[k] = DEFAULTS[k];

  function applyPrefs() {
    const f = FONTS[prefs.font] || FONTS.literata;
    root.style.setProperty('--rd-font', f.stack);
    root.style.setProperty('--rd-size', (prefs.size * (f.scale || 1)).toFixed(2) + 'px');
    root.style.setProperty('--rd-leading', LEADING[prefs.leading] || LEADING.comfy);
    root.style.setProperty('--rd-measure', MEASURE[prefs.measure] || MEASURE.medium);
    root.dataset.align = prefs.align;
    root.dataset.para = prefs.para;
    root.dataset.dropcaps = prefs.dropcaps ? 'on' : 'off';
    root.dataset.mustonly = prefs.mustOnly ? 'on' : 'off';
    $('#dim').style.opacity = ((100 - prefs.brightness) / 100 * .78).toFixed(3);
    $('#locTime').hidden = !prefs.showTime;
    O.applyTheme();
  }
  applyPrefs();

  // ---------- Load the book ----------
  const slug = new URLSearchParams(location.search).get('book') || '';
  let lib;
  try {
    lib = await O.library();
  } catch (e) {
    return fail('The library could not be loaded', 'Check your connection and try again.');
  }
  const subjects = lib.subjects || [];
  const subject = [...subjects, ...(lib.guide ? [lib.guide] : [])].find(s => s.slug === slug);
  if (!subject) return fail('This book isn’t on the shelf', 'It may have been renamed or moved.');

  const B = O.book(slug);
  const number = subject.kind === 'guide' ? null : subjects.indexOf(subject) + 1;
  document.title = `${subject.title} · October Library`;
  $('#barTitle').textContent = subject.title;

  titlepage.innerHTML = `
    <div class="rd-tp-cover">${O.cover(subject, number)}</div>
    <p class="rd-tp-eyebrow">${subject.kind === 'guide' ? 'Start here' : `Subject ${number ? 'No. ' + String(number).padStart(2, '0') : ''}`}</p>
    <h1 class="rd-tp-title">${esc(subject.title)}</h1>
    ${subject.subtitle ? `<p class="rd-tp-sub">${esc(subject.subtitle)}</p>` : ''}
    <p class="rd-tp-meta" id="tpMeta"></p>
    <div class="rd-ornament" aria-hidden="true">❦</div>`;

  // Runs once every declaration below exists (called at the end of this file).
  async function start() {
    let html = null;
    if (subject.status === 'ready' && subject.file) {
      try {
        const res = await fetch(subject.file, { cache: 'no-cache' });
        if (res.ok) html = await res.text();
      } catch (e) { /* handled below */ }
    }

    if (!html) return awaiting();

    ingest(html, new URL(subject.file, location.href));
    await renderMath();
    structure();
    O.data.last = slug;
    O.save();
  }

  // ---------- Ingest the subject's HTML ----------
  function ingest(source, base) {
    const doc = new DOMParser().parseFromString(source, 'text/html');
    const articles = doc.querySelectorAll('article');
    const src = doc.querySelector('main') || (articles.length === 1 ? articles[0] : doc.body);

    src.querySelectorAll('script, style, link, meta, noscript, iframe, object, embed, form, input, button, select, textarea, template, base, title, nav').forEach(n => n.remove());

    const keepStyle = /^(text-align|font-style|font-weight|text-decoration(-line)?|vertical-align|list-style-type)$/;
    src.querySelectorAll('*').forEach(el => {
      for (const attr of [...el.attributes]) {
        const name = attr.name.toLowerCase();
        if (name.startsWith('on')) {
          el.removeAttribute(attr.name);
        } else if (name === 'style') {
          const keep = p => keepStyle.test(p) || (el.tagName === 'IMG' && p === 'width');
          const kept = [...el.style].filter(keep).map(p => `${p}:${el.style.getPropertyValue(p)}`).join(';');
          if (kept) el.setAttribute('style', kept); else el.removeAttribute('style');
        } else if (name === 'href' || name === 'src' || name === 'xlink:href') {
          const v = attr.value.trim();
          if (/^javascript:/i.test(v)) el.removeAttribute(attr.name);
          else if (v && !v.startsWith('#') && !/^(data:|mailto:|tel:)/i.test(v)) {
            try { el.setAttribute(attr.name, new URL(v, base).href); } catch (e) { /* leave as is */ }
          }
        }
      }
      if (el.tagName === 'A') {
        const href = el.getAttribute('href') || '';
        if (href && !href.startsWith('#')) {
          el.target = '_blank';
          el.rel = 'noopener';
        }
      }
    });

    // The title page already shows the subject's name, so drop a single leading h1.
    const h1s = src.querySelectorAll('h1');
    const firstHeading = src.querySelector('h1, h2, h3, h4, h5, h6');
    if (h1s.length === 1 && firstHeading === h1s[0] && !h1s[0].classList.contains('rd-part')) h1s[0].remove();

    content.replaceChildren(...src.childNodes);

    $$('table', content).forEach(t => {
      if (t.parentElement.classList.contains('rd-table')) return;
      const wrap = document.createElement('div');
      wrap.className = 'rd-table';
      t.before(wrap);
      wrap.append(t);
    });
    $$('img', content).forEach(img => {
      img.loading = 'lazy';
      img.decoding = 'async';
    });
  }

  async function renderMath() {
    const text = content.textContent;
    if (!/\$\$|\\\(|\\\[/.test(text)) return;
    try {
      await loadCss('https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css');
      await loadScript('https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js');
      await loadScript('https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js');
      window.renderMathInElement(content, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '\\[', right: '\\]', display: true },
          { left: '\\(', right: '\\)', display: false },
        ],
        throwOnError: false,
        ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
      });
    } catch (e) { /* formulas stay as plain text */ }
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = reject;
      document.head.append(s);
    });
  }

  function loadCss(href) {
    return new Promise(resolve => {
      const l = document.createElement('link');
      l.rel = 'stylesheet';
      l.href = href;
      l.onload = l.onerror = resolve;
      document.head.append(l);
    });
  }

  // ---------- Structure: headings, blocks, word counts ----------
  let heads = [], tocHeads = [], chapters = [], parts = [], topLevel = 2, chapterLevel = 2, hasParts = false;
  let blocks = [], cum = [], words = [], totalWords = 0;
  let rawWords = [], hideable = [], vis = [], hasStars = false;
  let sectionOf = [], chapterOf = [], chapterEnd = [];
  let tocDepth = [], tocParent = [];
  // Books with "partPages" in subjects.json show one part at a time: each part scrolls on its own and ends with a link to the next.
  let partPages = false, partOf = [], pageEls = [], partStart = [], curPart = -1, bookEnd = '';
  const partNav = document.createElement('nav');
  partNav.className = 'rd-partnav';
  partNav.hidden = true;
  const tocOpen = new Set();
  const tocUserOpen = new Set();

  // A heading's name in contents, bars and lists; data-toc lets a book give a cleaner label.
  const label = h => (h.dataset.toc || h.textContent).replace(/\s+/g, ' ').trim();
  // What a book calls its chapters ("unit" in subjects.json, e.g. "section").
  const units = n => `${n} ${subject.unit || 'chapter'}${n === 1 ? '' : 's'}`;

  function slugify(s) {
    return s.toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60);
  }

  function structure() {
    const used = new Set($$('[id]', content).map(e => e.id));
    heads = $$('h1, h2, h3, h4', content).filter(h => h.textContent.trim());
    heads.forEach(h => {
      if (h.id) return;
      const baseId = slugify(h.textContent) || 'section';
      let id = baseId;
      for (let i = 2; used.has(id); i++) id = `${baseId}-${i}`;
      h.id = id;
      used.add(id);
    });
    // Books split into parts (headings marked .rd-part) have chapters one level below them.
    const levels = heads.map(h => +h.tagName[1]);
    topLevel = levels.length ? Math.min(...levels) : 2;
    hasParts = heads.some(h => h.classList.contains('rd-part'));
    chapterLevel = hasParts ? topLevel + 1 : topLevel;
    parts = hasParts ? heads.filter(h => +h.tagName[1] === topLevel) : [];
    tocHeads = heads.filter(h => +h.tagName[1] <= chapterLevel + 1);
    chapters = heads.filter(h => +h.tagName[1] === chapterLevel);
    chapters.forEach(h => h.classList.add('rd-ch'));

    const BLOCK = 'p, li, h1, h2, h3, h4, h5, h6, pre, blockquote, figure, img, .rd-table, hr, dt, dd, .katex-display, details, aside';
    const all = $$(BLOCK, content);
    const set = new Set(all);
    blocks = all.filter(el => {
      for (let p = el.parentElement; p && p !== content; p = p.parentElement) if (set.has(p)) return false;
      return true;
    });
    if (!blocks.length) blocks = [...content.children];
    if (!blocks.length) blocks = [content];

    rawWords = blocks.map(b => (b.textContent.match(/\S+/g) || []).length);
    hideable = blocks.map(b => !!b.closest('.rd-card.is-good'));
    hasStars = !!content.querySelector('.rd-card');

    let s = -1, c = -1;
    const tocSet = new Map(tocHeads.map((h, i) => [h, i]));
    const chSet = new Map(chapters.map((h, i) => [h, i]));
    blocks.forEach((b, i) => {
      const hs = b.matches('h1, h2, h3, h4') ? [b] : $$('h1, h2, h3, h4', b);
      for (const h of hs) {
        if (tocSet.has(h)) s = tocSet.get(h);
        if (chSet.has(h)) c = chSet.get(h);
      }
      sectionOf[i] = s;
      chapterOf[i] = c;
    });

    partPages = !!subject.partPages && parts.length > 1;
    if (partPages) {
      let k = 0;
      partOf = blocks.map(b => {
        const h = parts.find(p => p === b || b.contains(p));
        if (h) k = parts.indexOf(h);
        return k;
      });
      k = 0;
      pageEls = [...content.children].map(el => {
        if (parts.includes(el)) k = parts.indexOf(el);
        return [el, k];
      });
      root.dataset.partpages = 'on';
      content.before(partNav);
    }
    measure();
    partStart = parts.map(h => cum[Math.max(0, blocks.indexOf(h))]);

    const mainParts = parts.filter(h => !h.classList.contains('rd-appendix'));
    const appendices = parts.filter(h => h.classList.contains('rd-appendix'));
    const mainChapters = chapters.filter(h => !h.classList.contains('rd-rev'));
    $('#tpMeta').innerHTML = [
      mainParts.length > 1 ? `<span>${mainParts.length} parts</span>` : '',
      mainChapters.length ? `<span>${units(mainChapters.length)}</span>` : '',
      appendices.map(h => `<span>${esc(label(h))}</span>`).join(''),
      `<span>about ${O.fmtMinutes(totalWords / WPM)} of reading</span>`,
      subject.updated ? `<span>updated ${esc(new Date(subject.updated).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }))}</span>` : '',
    ].join('');

    bookEnd = `
      <div class="rd-ornament" aria-hidden="true">❦</div>
      <h2>The end of ${esc(subject.title)}</h2>
      <p>You've reached the last page. Your highlights and bookmarks are waiting in the contents panel whenever you want to revisit them.</p>
      <a class="rd-cta" href="./">Back to the library</a>`;
    endmatter.innerHTML = bookEnd;
    if (partPages) showPart(0);

    buildTextMap();
    renderToc();
    renderTicks();
    renderDrawerHead();
    renderMarks();
    renderHighlights();
    buildSettings();
    wire();

    body.classList.remove('rd-loading');
    document.fonts.ready.then(() => {
      restoreSaved();
      update();
    });
  }

  // Word counts and the list of visible blocks. With "must-learn only" on, good-to-know
  // cards are hidden: they count as zero words and are skipped when finding the reader's place.
  function isHidden(i) {
    return prefs.mustOnly && hasStars && hideable[i];
  }

  function measure() {
    vis = [];
    totalWords = 0;
    blocks.forEach((b, i) => {
      cum[i] = totalWords;
      words[i] = isHidden(i) ? 0 : rawWords[i];
      totalWords += words[i];
      if (!isHidden(i) && !(partPages && partOf[i] !== curPart)) vis.push(i);
    });
    totalWords = Math.max(totalWords, 1);
    if (!vis.length) vis = blocks.map((b, i) => i);
    chapterEnd = chapters.map((h, ci) => {
      const next = blocks.findIndex((b, i) => chapterOf[i] === ci + 1);
      return next === -1 ? totalWords : cum[next];
    });
  }

  // ---------- One part per page ----------
  // Shows part k alone (title page only with the first). Returns true if the page changed.
  function showPart(k) {
    if (!partPages || k === curPart || k < 0 || k >= parts.length) return false;
    curPart = k;
    pageEls.forEach(([el, p]) => { el.hidden = p !== k; });
    titlepage.hidden = k > 0;
    measure();
    const prev = parts[k - 1], next = parts[k + 1], here = parts[k];
    partNav.hidden = !prev;
    partNav.innerHTML = prev ? `<button class="rd-partnav-btn" data-go-part="${k - 1}">‹ ${esc(label(prev))}</button>` : '';
    endmatter.innerHTML = next ? `
      <div class="rd-ornament" aria-hidden="true">❦</div>
      <p class="rd-end-kicker">End of</p>
      <h2>${esc(label(here))}</h2>
      ${here.dataset.count ? `<p>${esc(here.dataset.count)}</p>` : ''}
      <button class="rd-cta" data-go-part="${k + 1}">Continue to ${esc(label(next))} ›</button>` : bookEnd;
    return true;
  }

  // Which part an element or text node is in.
  function partOfNode(n) {
    let k = 0;
    parts.forEach((h, i) => { if (h === n || h.compareDocumentPosition(n) & Node.DOCUMENT_POSITION_FOLLOWING) k = i; });
    return k;
  }

  function showPartOf(n) {
    return partPages && showPart(partOfNode(n));
  }

  function openPart(k) {
    if (showPart(k)) window.scrollTo({ top: 0, behavior: 'instant' });
    else goToEl(parts[k]);
    update();
  }

  // ---------- Positions ----------
  function blockAt(y) {
    let lo = 0, hi = vis.length - 1, ans = vis.length - 1;
    while (lo <= hi) {
      const mid = (lo + hi) >> 1;
      if (blocks[vis[mid]].getBoundingClientRect().bottom > y) { ans = mid; hi = mid - 1; } else lo = mid + 1;
    }
    return vis[ans];
  }

  function capturePos() {
    const top = READ_TOP();
    const i = blockAt(top);
    const r = blocks[i].getBoundingClientRect();
    const frac = Math.min(1, Math.max(0, (top - r.top) / Math.max(r.height, 1)));
    return { block: i, frac };
  }

  function restorePos(p, smooth) {
    if (!blocks[p.block]) return;
    if (partPages && showPart(partOf[p.block])) smooth = false;
    let i = p.block, frac = p.frac;
    if (isHidden(i)) {
      i = vis.find(v => v >= i) ?? vis[vis.length - 1];
      frac = 0;
    }
    const r = blocks[i].getBoundingClientRect();
    window.scrollTo({ top: scrollY + r.top + frac * r.height - READ_TOP(), behavior: smooth && !reduceMotion ? 'smooth' : 'instant' });
  }

  function atEnd() {
    return scrollY + innerHeight >= document.documentElement.scrollHeight - 4;
  }

  function wordsRead(p) {
    return cum[p.block] + p.frac * words[p.block];
  }

  function posFromPct(pct) {
    const target = pct * totalWords;
    let i = 0;
    while (i < blocks.length - 1 && cum[i + 1] <= target) i++;
    return { block: i, frac: words[i] ? Math.min(1, (target - cum[i]) / words[i]) : 0 };
  }

  function beforeContent() {
    if (partPages && curPart > 0) return false;
    return content.getBoundingClientRect().top > READ_TOP() + 1;
  }

  function currentPct(p = capturePos()) {
    if (atEnd()) return partPages && curPart < parts.length - 1 ? partStart[curPart + 1] / totalWords : 1;
    if (beforeContent()) return 0;
    return Math.min(1, wordsRead(p) / totalWords);
  }

  function goToEl(el, smooth = true) {
    if (showPartOf(el)) smooth = false;
    const r = el.getBoundingClientRect();
    window.scrollTo({ top: scrollY + r.top - READ_TOP() - 8, behavior: smooth && !reduceMotion ? 'smooth' : 'instant' });
  }

  // Keep the reader's place when the layout changes (font, size, spacing).
  function keepPlace(fn) {
    const p = beforeContent() ? null : capturePos();
    fn();
    if (p) {
      restorePos(p);
      document.fonts.ready.then(() => { restorePos(p); update(); });
    }
    update();
  }

  function restoreSaved() {
    const pos = B.pos;
    if (!pos || !(pos.pct > .005) || pos.block == null || !blocks[pos.block]) return;
    restorePos(pos);
    if (pos.pct < .995) {
      toast(`Resumed at ${Math.round(pos.pct * 100)}%`, 'Start over', () => {
        if (partPages && curPart !== 0) return openPart(0);
        window.scrollTo({ top: 0, behavior: reduceMotion ? 'instant' : 'smooth' });
      });
    }
  }

  // ---------- Live position updates ----------
  let saveTimer = 0;

  function update() {
    if (!blocks.length) return;
    const p = capturePos();
    const pct = currentPct(p);
    const pctText = `${Math.round(pct * 100)}%`;
    $('#trackFill').style.width = (pct * 100).toFixed(2) + '%';
    $('#thinFill').style.width = (pct * 100).toFixed(2) + '%';
    $('#locPct').textContent = pctText;
    track.setAttribute('aria-valuenow', Math.round(pct * 100));

    const before = beforeContent();
    const si = before ? -1 : sectionOf[p.block];
    const sectionName = si >= 0 ? label(tocHeads[si]) : '';
    const chIdx = before ? -1 : chapterOf[p.block];
    $('#locSection').textContent = sectionName || (before ? 'Title page' : subject.title);
    $('#barSection').textContent = chIdx >= 0 ? label(chapters[chIdx]) : sectionName;

    const read = before ? 0 : wordsRead(p);
    const bookLeft = Math.max(0, totalWords - read) / WPM;
    let timeText;
    if (pct >= .999) timeText = 'Finished';
    else {
      const ci = before ? -1 : chapterOf[p.block];
      timeText = ci >= 0 ? `${O.fmtMinutes(Math.max(0, chapterEnd[ci] - read) / WPM)} left in chapter` : `${O.fmtMinutes(bookLeft)} left`;
    }
    $('#locTime').textContent = timeText;

    if (si !== currentToc) markTocPosition(si);
    $('#dhPct') && ($('#dhPct').textContent = pctText);
    $('#dhBar') && ($('#dhBar').style.width = (pct * 100).toFixed(1) + '%');

    $('#btnBookmark').setAttribute('aria-pressed', String(!!visibleBookmark()));

    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      B.pos = { block: p.block, frac: +p.frac.toFixed(4), pct: +pct.toFixed(4), section: sectionName, minutesLeft: Math.round(bookLeft), at: Date.now() };
      O.save();
    }, 400);
  }

  let ticking = false;
  let lastY = scrollY;

  function onScroll() {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(() => {
        ticking = false;
        const dy = scrollY - lastY;
        if (Math.abs(dy) > 6) {
          if (dy > 0 && scrollY > 160 && !anyOverlayOpen()) setChrome(false);
          else if (dy < 0) setChrome(true);
          lastY = scrollY;
        }
        if (atEnd() || scrollY < 40) setChrome(true);
        update();
      });
    }
    if (!selPop.hidden) hidePop(selPop);
    if (!notePop.hidden) hidePop(notePop);
  }

  function setChrome(show) {
    body.classList.toggle('rd-chrome-hidden', !show);
  }

  function toggleChrome() {
    setChrome(body.classList.contains('rd-chrome-hidden'));
  }

  function turn(dir) {
    const hidden = body.classList.contains('rd-chrome-hidden') || body.classList.contains('rd-focus');
    const step = Math.max(200, innerHeight - (hidden ? 72 : 150));
    window.scrollBy({ top: dir * step, behavior: reduceMotion ? 'instant' : 'smooth' });
  }

  // ---------- Contents, ticks, drawer ----------
  // The contents is a collapsible tree: parts › chapters › sections, opened along the reader's position.
  let currentToc = -2;

  function renderToc() {
    const list = $('#tocList');
    if (!tocHeads.length) {
      list.innerHTML = '<li class="rd-empty">This book has no chapters yet.</li>';
      return;
    }
    const base = Math.min(...tocHeads.map(h => +h.tagName[1]));
    tocDepth = tocHeads.map(h => +h.tagName[1] - base);
    const stack = [];
    tocParent = tocHeads.map((h, i) => {
      while (stack.length && tocDepth[stack[stack.length - 1]] >= tocDepth[i]) stack.pop();
      const parent = stack.length ? stack[stack.length - 1] : -1;
      stack.push(i);
      return parent;
    });
    const hasKids = new Set(tocParent.filter(p => p >= 0));

    const blockIndex = new Map(blocks.map((b, i) => [b, i]));
    const startOf = h => {
      if (blockIndex.has(h)) return cum[blockIndex.get(h)];
      const i = blocks.findIndex(b => b.contains(h));
      return i >= 0 ? cum[i] : 0;
    };
    const starts = chapters.map(startOf);
    const chapterMins = new Map(chapters.map((h, ci) => [h, ((ci + 1 < starts.length ? starts[ci + 1] : totalWords) - starts[ci]) / WPM]));
    const chev = icon('<path d="m9 6 6 6-6 6"/>', 16);

    list.innerHTML = tocHeads.map((h, i) => {
      let meta = '';
      if (chapterMins.has(h)) meta = O.fmtMinutes(chapterMins.get(h));
      else if (parts.includes(h)) {
        const n = tocParent.filter(p => p === i).length;
        if (n) meta = units(n);
      }
      // Books that count their items (Current Affairs) show the tally too; in must-learn mode, the ★ count.
      const count = prefs.mustOnly && hasStars ? h.dataset.countMust : h.dataset.count;
      if (count) meta = meta ? `${count} · ${meta}` : count;
      return `<li data-i="${i}"${tocDepth[i] > 0 ? ' hidden' : ''}>
        <div class="rd-toc-row" style="--d:${tocDepth[i]}">
          ${hasKids.has(i) ? `<button class="rd-toc-tog" data-tog="${i}" aria-expanded="false" aria-label="Show contents of ${esc(label(h))}">${chev}</button>` : '<span class="rd-toc-tog"></span>'}
          <button class="rd-toc-item lvl-${Math.min(2, tocDepth[i])}${parts.includes(h) ? ' is-part' : ''}" data-i="${i}"><span class="rd-toc-text">${esc(label(h))}</span>${meta ? `<span class="rd-toc-min">${meta}</span>` : ''}</button>
        </div>
      </li>`;
    }).join('');
  }

  function applyTocOpen() {
    const visible = [];
    $$('#tocList > li[data-i]').forEach(li => {
      const i = +li.dataset.i;
      const p = tocParent[i];
      visible[i] = p < 0 || (visible[p] && tocOpen.has(p));
      li.hidden = !visible[i];
      const tog = li.querySelector('[data-tog]');
      if (tog) tog.setAttribute('aria-expanded', String(tocOpen.has(i)));
    });
  }

  // Open the branches leading to the reader's place, plus any the reader opened by hand.
  function openTocTo(si) {
    tocOpen.clear();
    tocUserOpen.forEach(i => tocOpen.add(i));
    for (let p = si; p >= 0; p = tocParent[p]) tocOpen.add(p);
    applyTocOpen();
  }

  function markTocPosition(si) {
    currentToc = si;
    const path = new Set();
    for (let p = si; p >= 0; p = tocParent[p]) path.add(p);
    $$('#tocList .rd-toc-item').forEach(b => {
      const i = +b.dataset.i;
      b.classList.toggle('is-current', i === si);
      b.classList.toggle('is-path', path.has(i) && i !== si);
      b.classList.toggle('is-read', si >= 0 && i < si && !path.has(i));
    });
  }

  function renderTicks() {
    $('#ticks').innerHTML = (hasParts ? parts : chapters).slice(1).map(h => {
      const i = blocks.findIndex(b => b === h || b.contains(h));
      return i >= 0 ? `<i style="left:${(cum[i] / totalWords * 100).toFixed(2)}%"></i>` : '';
    }).join('');
  }

  function renderDrawerHead() {
    $('#drawerHead').innerHTML = `${O.cover(subject, number)}
      <div><p class="rd-dh-title">${esc(subject.title)}</p>
      <div class="rd-dh-meta"><div class="rd-dh-bar"><span id="dhBar"></span></div><span id="dhPct">0%</span></div></div>`;
  }

  function openDrawer(tab) {
    closePanels();
    if (tab) selectTab(tab);
    drawer.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
    scrim.classList.add('is-on');
    if (currentToc >= 0) openTocTo(currentToc);
    // Scroll only the list (scrollIntoView would also move the page and the drawer sideways).
    const cur = $('.rd-toc-item.is-current', drawer);
    const list = $('.rd-drawer-body', drawer);
    if (cur && !$('#tocList').hidden) {
      list.scrollTop += cur.getBoundingClientRect().top - list.getBoundingClientRect().top - list.clientHeight / 2;
    }
  }

  function closeDrawer() {
    drawer.classList.remove('is-open');
    drawer.setAttribute('aria-hidden', 'true');
    if (settings.hidden) scrim.classList.remove('is-on');
  }

  function selectTab(tab) {
    $$('.rd-tab', drawer).forEach(t => t.setAttribute('aria-selected', String(t.dataset.tab === tab)));
    $$('[data-panel]', drawer).forEach(p => { p.hidden = p.dataset.panel !== tab; });
  }

  // ---------- Bookmarks ----------
  function visibleRange() {
    const top = READ_TOP();
    return [blockAt(top), blockAt(innerHeight - 70)];
  }

  function visibleBookmark() {
    if (!blocks.length || beforeContent()) return null;
    const [a, b] = visibleRange();
    return B.bookmarks.find(m => m.block >= a && m.block <= b) || null;
  }

  function toggleBookmark() {
    if (!blocks.length) return;
    const existing = visibleBookmark();
    if (existing) {
      B.bookmarks = B.bookmarks.filter(m => m !== existing);
      toast('Bookmark removed');
    } else {
      if (beforeContent()) { toast('Scroll into the book to bookmark a page'); return; }
      const p = capturePos();
      const si = sectionOf[p.block];
      B.bookmarks.push({
        id: Date.now().toString(36),
        block: p.block,
        frac: +p.frac.toFixed(4),
        pct: +currentPct(p).toFixed(4),
        section: si >= 0 ? label(tocHeads[si]) : subject.title,
        snippet: blocks[p.block].textContent.trim().replace(/\s+/g, ' ').slice(0, 140),
        created: Date.now(),
      });
      B.bookmarks.sort((x, y) => x.block - y.block || x.frac - y.frac);
      toast('Page bookmarked');
    }
    O.save();
    renderMarks();
    update();
  }

  function renderMarks() {
    $('#markCount').textContent = B.bookmarks.length || '';
    $('#markList').innerHTML = B.bookmarks.length
      ? B.bookmarks.map(m => `<li>
          <button class="rd-item" data-mark="${m.id}">
            <span class="rd-item-sec">${esc(m.section)} · ${Math.round(m.pct * 100)}%</span>
            <span class="rd-item-text">${esc(m.snippet)}${m.snippet.length >= 140 ? '…' : ''}</span>
            <span class="rd-item-meta">${new Date(m.created).toLocaleDateString(undefined, { day: 'numeric', month: 'short' })}</span>
          </button>
          <button class="rd-btn rd-sm rd-del" data-del-mark="${m.id}" aria-label="Remove bookmark">${xIcon()}</button>
        </li>`).join('')
      : '<li class="rd-empty">No bookmarks yet.<br>Tap the ribbon icon or press <b>B</b> to mark a page.</li>';
  }

  // ---------- Text map: character offsets for highlights and search ----------
  let TM = null;

  function buildTextMap() {
    const nodes = [], starts = [];
    let off = 0;
    const walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT, {
      acceptNode: n => (n.parentElement.closest('.katex-mathml') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT),
    });
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      nodes.push(n);
      starts.push(off);
      off += n.data.length;
    }
    TM = { nodes, starts, length: off, index: new Map(nodes.map((n, i) => [n, i])), text: nodes.map(n => n.data).join(''), lower: null };
  }

  function pointToOffset(node, offset) {
    const idx = TM.index.get(node);
    if (idx !== undefined) return TM.starts[idx] + offset;
    const r = document.createRange();
    r.setStart(node, offset);
    r.collapse(true);
    let lo = 0, hi = TM.nodes.length - 1, ans = TM.nodes.length;
    while (lo <= hi) {
      const mid = (lo + hi) >> 1;
      if (r.comparePoint(TM.nodes[mid], 0) >= 0) { ans = mid; hi = mid - 1; } else lo = mid + 1;
    }
    return ans < TM.nodes.length ? TM.starts[ans] : TM.length;
  }

  function offsetToPoint(off, isEnd) {
    let lo = 0, hi = TM.nodes.length - 1, ans = 0;
    while (lo <= hi) {
      const mid = (lo + hi) >> 1;
      const s = TM.starts[mid];
      if (isEnd ? s < off : s <= off) { ans = mid; lo = mid + 1; } else hi = mid - 1;
    }
    const n = TM.nodes[ans];
    return [n, Math.min(n.data.length, Math.max(0, off - TM.starts[ans]))];
  }

  function rangeFor(start, end) {
    const r = document.createRange();
    r.setStart(...offsetToPoint(start, false));
    r.setEnd(...offsetToPoint(end, true));
    return r;
  }

  // ---------- Highlights ----------
  const COLORS = ['yellow', 'green', 'blue', 'pink'];

  function locateHighlight(h) {
    if (TM.text.slice(h.start, h.end) === h.text) return true;
    const i = TM.text.indexOf(h.text);
    if (i === -1) return false;
    h.start = i;
    h.end = i + h.text.length;
    return true;
  }

  function paintHighlights() {
    if (!hasHighlightApi) return;
    for (const c of COLORS) {
      const ranges = B.highlights.filter(h => h.color === c && h.found !== false).map(h => rangeFor(h.start, h.end));
      CSS.highlights.set(`rd-hl-${c}`, new Highlight(...ranges));
    }
  }

  function renderHighlights() {
    B.highlights.forEach(h => { h.found = locateHighlight(h); });
    B.highlights.sort((a, b) => a.start - b.start);
    paintHighlights();
    $('#hlCount').textContent = B.highlights.length || '';
    $('#hlList').innerHTML = B.highlights.length
      ? B.highlights.map(h => `<li>
          <button class="rd-item" data-hl="${h.id}">
            <span class="rd-item-sec">${esc(h.section || subject.title)}</span>
            <span class="rd-item-text rd-item-hl" data-c="${h.color}">${esc(h.text.length > 280 ? h.text.slice(0, 280) + '…' : h.text)}</span>
            ${h.found === false ? '<span class="rd-item-meta">This passage has changed since you highlighted it.</span>' : ''}
          </button>
          <button class="rd-btn rd-sm rd-del" data-del-hl="${h.id}" aria-label="Remove highlight">${xIcon()}</button>
        </li>`).join('')
      : `<li class="rd-empty">No highlights yet.<br>Select any passage and pick a colour.${hasHighlightApi ? '' : '<br><br>This browser can’t show highlights on the page. Try a recent Chrome, Edge, Safari or Firefox.'}</li>`;
  }

  function addHighlight(sel, color) {
    let { start, end } = sel;
    const raw = TM.text.slice(start, end);
    start += raw.length - raw.trimStart().length;
    end -= raw.length - raw.trimEnd().length;
    if (end <= start) return;
    B.highlights = B.highlights.filter(h => h.end <= start || h.start >= end);
    const [node] = offsetToPoint(start, false);
    const bi = blocks.findIndex(b => b.contains(node));
    const si = bi >= 0 ? sectionOf[bi] : -1;
    B.highlights.push({
      id: Date.now().toString(36), start, end, text: TM.text.slice(start, end), color,
      section: si >= 0 ? label(tocHeads[si]) : '', created: Date.now(),
    });
    O.save();
    renderHighlights();
  }

  function highlightAtPoint(x, y) {
    let node, offset;
    if (document.caretPositionFromPoint) {
      const c = document.caretPositionFromPoint(x, y);
      if (!c) return null;
      node = c.offsetNode;
      offset = c.offset;
    } else if (document.caretRangeFromPoint) {
      const c = document.caretRangeFromPoint(x, y);
      if (!c) return null;
      node = c.startContainer;
      offset = c.startOffset;
    } else return null;
    if (!content.contains(node)) return null;
    const off = pointToOffset(node, offset);
    return B.highlights.find(h => h.found !== false && off >= h.start && off < h.end) || null;
  }

  // ---------- Selection popup ----------
  let pendingSel = null;

  function checkSelection() {
    const sel = getSelection();
    if (!sel.rangeCount || sel.isCollapsed) {
      if (selPop.dataset.mode === 'sel') hidePop(selPop);
      return;
    }
    const r = sel.getRangeAt(0);
    if (!content.contains(r.commonAncestorContainer)) return;
    const start = pointToOffset(r.startContainer, r.startOffset);
    const end = pointToOffset(r.endContainer, r.endOffset);
    const text = TM.text.slice(start, end);
    if (!text.trim()) return;
    pendingSel = { start, end, text };
    const word = text.trim();
    const single = /^[\p{L}][\p{L}'’-]{0,30}$/u.test(word);
    selPop.dataset.mode = 'sel';
    selPop.innerHTML = `${COLORS.map(c => `<button class="rd-dot" data-c="${c}" aria-label="Highlight ${c}"><i></i></button>`).join('')}
      <span class="rd-sep"></span>
      ${single ? '<button class="rd-act" data-act="define">Define</button>' : ''}
      <button class="rd-act" data-act="copy">Copy</button>
      <button class="rd-act" data-act="find">Search</button>`;
    showPop(selPop, r.getBoundingClientRect());
  }

  function showHighlightPop(h, x, y) {
    pendingSel = h;
    selPop.dataset.mode = 'hl';
    selPop.innerHTML = `${COLORS.map(c => `<button class="rd-dot${c === h.color ? ' is-on' : ''}" data-c="${c}" aria-label="Change to ${c}"><i></i></button>`).join('')}
      <span class="rd-sep"></span>
      <button class="rd-act" data-act="copy">Copy</button>
      <button class="rd-act" data-act="remove">Remove</button>`;
    const r = rangeFor(h.start, h.end).getClientRects();
    const rect = [...r].find(b => y >= b.top - 2 && y <= b.bottom + 2) || r[0] || { top: y, bottom: y, left: x, right: x, width: 0 };
    showPop(selPop, rect);
  }

  function showPop(pop, rect) {
    pop.hidden = false;
    const w = pop.offsetWidth, h = pop.offsetHeight;
    let top = rect.top - h - 12;
    if (top < 64) top = rect.bottom + 12;
    if (top + h > innerHeight - 8) top = Math.max(8, innerHeight - h - 8);
    let left = rect.left + (rect.width || 0) / 2 - w / 2;
    left = Math.max(8, Math.min(innerWidth - w - 8, left));
    pop.style.top = top + 'px';
    pop.style.left = left + 'px';
  }

  function hidePop(pop) {
    pop.hidden = true;
    if (pop === selPop) {
      pop.dataset.mode = '';
      pendingSel = null;
    }
  }

  async function onSelAction(e) {
    const dot = e.target.closest('.rd-dot');
    const act = e.target.closest('[data-act]');
    const sel = pendingSel;
    if (!sel) return;
    if (dot) {
      if (selPop.dataset.mode === 'hl') {
        sel.color = dot.dataset.c;
        O.save();
        renderHighlights();
      } else {
        addHighlight(sel, dot.dataset.c);
        getSelection().removeAllRanges();
        toast('Highlighted');
      }
      hidePop(selPop);
      return;
    }
    if (!act) return;
    const a = act.dataset.act;
    if (a === 'copy') {
      try { await navigator.clipboard.writeText(sel.text); toast('Copied'); } catch (err) { toast('Copy failed'); }
      hidePop(selPop);
    } else if (a === 'remove') {
      B.highlights = B.highlights.filter(h => h !== sel);
      O.save();
      renderHighlights();
      hidePop(selPop);
      toast('Highlight removed');
    } else if (a === 'find') {
      const q = sel.text.trim().slice(0, 80);
      getSelection().removeAllRanges();
      hidePop(selPop);
      openSearch(q);
    } else if (a === 'define') {
      const rect = selPop.getBoundingClientRect();
      const word = sel.text.trim();
      hidePop(selPop);
      define(word, rect);
    }
  }

  async function define(word, rect) {
    notePop.innerHTML = `<span class="rd-np-label">Dictionary</span><p class="rd-np-word">${esc(word)}</p><p class="rd-np-phon">Looking it up…</p>`;
    showPop(notePop, rect);
    try {
      const res = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word.toLowerCase())}`);
      if (!res.ok) throw new Error('not found');
      const entry = (await res.json())[0];
      const phon = entry.phonetic || (entry.phonetics || []).map(p => p.text).find(Boolean) || '';
      const meanings = (entry.meanings || []).slice(0, 3).map(m =>
        `<p><span class="rd-np-pos">${esc(m.partOfSpeech)}</span> ${esc((m.definitions[0] || {}).definition || '')}</p>`).join('');
      notePop.innerHTML = `<span class="rd-np-label">Dictionary</span><p class="rd-np-word">${esc(entry.word)}</p>${phon ? `<p class="rd-np-phon">${esc(phon)}</p>` : ''}${meanings}`;
    } catch (e) {
      notePop.innerHTML = `<span class="rd-np-label">Dictionary</span><p class="rd-np-word">${esc(word)}</p><p class="rd-np-phon">No definition found${navigator.onLine ? '' : ' (you’re offline)'}.</p>`;
    }
    showPop(notePop, rect);
  }

  // ---------- Search ----------
  let hits = [], hitIdx = -1;

  function openSearch(q) {
    closePanels();
    closeDrawer();
    setChrome(true);
    searchBar.hidden = false;
    if (q != null) searchInput.value = q;
    searchInput.focus();
    searchInput.select();
    runSearch(searchInput.value);
  }

  function closeSearch() {
    searchBar.hidden = true;
    hits = [];
    hitIdx = -1;
    if (hasHighlightApi) {
      CSS.highlights.delete('rd-search');
      CSS.highlights.delete('rd-search-cur');
    }
  }

  function runSearch(q) {
    hits = [];
    hitIdx = -1;
    q = q.trim().toLowerCase();
    if (q.length >= 2) {
      TM.lower = TM.lower || TM.text.toLowerCase();
      for (let i = TM.lower.indexOf(q); i !== -1 && hits.length < 1000; i = TM.lower.indexOf(q, i + q.length)) hits.push([i, i + q.length]);
      if (prefs.mustOnly && hasStars) hits = hits.filter(h => !offsetToPoint(h[0], false)[0].parentElement.closest('.rd-card.is-good'));
      if (hits.length) {
        const here = beforeContent() ? 0 : pointToOffset(...firstTextAt(capturePos()));
        hitIdx = Math.max(0, hits.findIndex(h => h[0] >= here));
      }
    }
    paintSearch(true);
  }

  function firstTextAt(p) {
    const el = blocks[p.block];
    const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const n = w.nextNode();
    return n ? [n, 0] : [el, 0];
  }

  function stepSearch(dir) {
    if (!hits.length) return;
    hitIdx = (hitIdx + dir + hits.length) % hits.length;
    paintSearch(true);
  }

  function paintSearch(scroll) {
    const q = searchInput.value.trim();
    $('#searchCount').textContent = q.length < 2 ? '' : hits.length ? `${hitIdx + 1} of ${hits.length}${hits.length >= 1000 ? '+' : ''}` : 'No matches';
    if (hasHighlightApi) {
      CSS.highlights.set('rd-search', new Highlight(...hits.map(h => rangeFor(h[0], h[1]))));
      CSS.highlights.set('rd-search-cur', hitIdx >= 0 ? new Highlight(rangeFor(...hits[hitIdx])) : new Highlight());
    }
    if (scroll && hitIdx >= 0) {
      const switched = showPartOf(rangeFor(...hits[hitIdx]).startContainer);
      const r = rangeFor(...hits[hitIdx]);
      const rect = r.getBoundingClientRect();
      const details = r.startContainer.parentElement.closest('details');
      if (details && !details.open) details.open = true;
      if (rect.top < 120 || rect.bottom > innerHeight - 120) {
        window.scrollTo({ top: scrollY + rect.top - innerHeight / 3, behavior: reduceMotion || switched ? 'instant' : 'smooth' });
      }
      if (!hasHighlightApi) {
        const sel = getSelection();
        sel.removeAllRanges();
        sel.addRange(r);
      }
    }
  }

  // ---------- Footnotes and images ----------
  function isFootnote(target, link) {
    return !!(target.closest('.footnotes, .footnote, [role="doc-endnotes"], [role="doc-footnote"], [role="doc-endnote"]')
      || /^(fn|footnote|note)[-_:]?\w*/i.test(target.id)
      || link.closest('sup'));
  }

  function showFootnote(link, target) {
    const clone = target.cloneNode(true);
    clone.querySelectorAll('a[href^="#fnref"], .footnote-back, .footnote-backref, [role="doc-backlink"]').forEach(a => a.remove());
    clone.removeAttribute('id');
    notePop.innerHTML = `<span class="rd-np-label">Note</span>${clone.tagName === 'LI' ? clone.innerHTML : clone.outerHTML}`;
    showPop(notePop, link.getBoundingClientRect());
  }

  function openLightbox(img) {
    const lb = $('#lightbox');
    lb.innerHTML = `<img src="${esc(img.currentSrc || img.src)}" alt="${esc(img.alt)}">`;
    lb.hidden = false;
  }

  // ---------- Settings ----------
  function icon(paths, size = 22) {
    return `<svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true">${paths}</svg>`;
  }

  function xIcon() {
    return icon('<path d="M7 7l10 10M17 7 7 17"/>', 16);
  }

  function buildSettings() {
    const seg = (key, opts, cls = '') => `<div class="rd-seg ${cls}">${opts.map(o =>
      `<button data-set="${key}" data-val="${o.v}" aria-label="${esc(o.label)}" title="${esc(o.label)}"${o.style ? ` style="${o.style}"` : ''}>${o.html}</button>`).join('')}</div>`;
    const lines = gap => icon(`<path d="M5 ${12 - gap * 2}h14M5 12h14M5 ${12 + gap * 2}h14"/>`);
    const margins = w => icon(`<path d="M${12 - w} 6h${w * 2}M${12 - w} 10h${w * 2}M${12 - w} 14h${w * 2}M${12 - w} 18h${w * 2}"/><path d="M3 4v16M21 4v16" opacity=".4"/>`);

    settings.innerHTML = `
      <div class="rd-set">
        <p class="rd-set-label">Theme</p>
        <div class="rd-swatches">${O.THEMES.map(t =>
          `<button class="rd-swatch" data-set="theme" data-val="${t.id}"><span class="swatch" data-swatch="${t.id}">Aa</span>${t.label}</button>`).join('')}</div>
      </div>
      <div class="rd-set">
        <p class="rd-set-label">Brightness</p>
        <div class="rd-range">${icon('<circle cx="12" cy="12" r="3"/><path d="M12 5v1.5M12 17.5V19M5 12h1.5M17.5 12H19"/>', 18)}
          <input type="range" id="brightness" min="35" max="100" step="1" value="${prefs.brightness}" aria-label="Brightness">
          ${icon('<circle cx="12" cy="12" r="4.5"/><path d="M12 2.5v2.5M12 19v2.5M2.5 12H5M19 12h2.5M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8"/>', 20)}</div>
      </div>
      <div class="rd-set">
        <p class="rd-set-label">Typeface</p>
        ${seg('font', Object.entries(FONTS).map(([v, f]) => ({ v, label: f.label, html: f.label, style: `font-family:${f.stack.replace(/"/g, "'")}` })), 'rd-fonts')}
      </div>
      <div class="rd-set">
        <p class="rd-set-label">Text size</p>
        <div class="rd-size">
          <button data-step="-1" aria-label="Smaller text">A</button>
          <div class="rd-pips" id="pips">${SIZES.map(() => '<i></i>').join('')}</div>
          <button data-step="1" aria-label="Larger text">A</button>
        </div>
      </div>
      <div class="rd-set rd-two">
        <div><p class="rd-set-label">Spacing</p>${seg('leading', [
          { v: 'compact', label: 'Compact spacing', html: lines(1.6) },
          { v: 'comfy', label: 'Comfortable spacing', html: lines(2.4) },
          { v: 'airy', label: 'Airy spacing', html: lines(3.2) }])}</div>
        <div><p class="rd-set-label">Margins</p>${seg('measure', [
          { v: 'narrow', label: 'Wide margins', html: margins(4) },
          { v: 'medium', label: 'Medium margins', html: margins(6) },
          { v: 'wide', label: 'Narrow margins', html: margins(8) }])}</div>
      </div>
      <div class="rd-set rd-two">
        <div><p class="rd-set-label">Alignment</p>${seg('align', [
          { v: 'left', label: 'Align left', html: icon('<path d="M4 6h16M4 10h11M4 14h16M4 18h9"/>') },
          { v: 'justify', label: 'Justify', html: icon('<path d="M4 6h16M4 10h16M4 14h16M4 18h16"/>') }])}</div>
        <div><p class="rd-set-label">Paragraphs</p>${seg('para', [
          { v: 'spaced', label: 'Spaced paragraphs', html: icon('<path d="M4 5h16M4 9h12M4 15h16M4 19h10"/>') },
          { v: 'indented', label: 'Indented paragraphs', html: icon('<path d="M8 5h12M4 9h16M4 13h12M8 17h12M4 21h14"/>') }])}</div>
      </div>
      <div class="rd-set">
        ${hasStars ? '<label class="rd-toggle rd-toggle-star">★ Must-learn only<input type="checkbox" data-toggle="mustOnly"></label>' : ''}
        <label class="rd-toggle">Tap page edges to turn pages<input type="checkbox" data-toggle="tapTurn"></label>
        <label class="rd-toggle">Drop caps at chapter openings<input type="checkbox" data-toggle="dropcaps"></label>
        <label class="rd-toggle">Show time left<input type="checkbox" data-toggle="showTime"></label>
        <button class="rd-reset" id="resetPrefs">Reset to defaults</button>
        <p class="rd-keys"><kbd>←</kbd> <kbd>→</kbd> turn pages · <kbd>T</kbd> contents · <kbd>/</kbd> search · <kbd>B</kbd> bookmark · <kbd>A</kbd> display · <kbd>F</kbd> focus · <kbd>+</kbd> <kbd>−</kbd> size</p>
      </div>`;
    refreshSettings();
  }

  function refreshSettings() {
    $$('[data-set]', settings).forEach(b => {
      const key = b.dataset.set;
      const cur = key === 'theme' ? (prefs.theme || 'auto') : prefs[key];
      b.setAttribute('aria-pressed', String(String(cur) === b.dataset.val));
    });
    $$('[data-toggle]', settings).forEach(i => { i.checked = !!prefs[i.dataset.toggle]; });
    const si = SIZES.indexOf(prefs.size);
    $$('#pips i', settings).forEach((p, i) => {
      p.classList.toggle('on', i <= si);
      p.classList.toggle('cur', i === si);
    });
    $('#brightness').value = prefs.brightness;
  }

  function setPref(key, val) {
    keepPlace(() => {
      prefs[key] = val;
      applyPrefs();
      if (key === 'mustOnly') {
        measure();
        renderToc();
        renderTicks();
        currentToc = -2;
      }
    });
    O.save();
    refreshSettings();
    if (key === 'mustOnly') toast(val ? 'Showing ★ must-learn items only' : 'Showing all items');
  }

  function stepSize(dir) {
    let i = SIZES.indexOf(prefs.size);
    if (i === -1) i = SIZES.indexOf(DEFAULTS.size);
    const next = SIZES[Math.max(0, Math.min(SIZES.length - 1, i + dir))];
    if (next !== prefs.size) setPref('size', next);
    toast(`Text size ${SIZES.indexOf(next) + 1} of ${SIZES.length}`);
  }

  function toggleSettings() {
    if (settings.hidden) {
      closeDrawer();
      settings.hidden = false;
      setChrome(true);
    } else settings.hidden = true;
  }

  function closePanels() {
    settings.hidden = true;
  }

  function anyOverlayOpen() {
    return drawer.classList.contains('is-open') || !settings.hidden || !searchBar.hidden;
  }

  function closeAll() {
    closeDrawer();
    closePanels();
    hidePop(selPop);
    hidePop(notePop);
    $('#lightbox').hidden = true;
    scrim.classList.remove('is-on');
  }

  // ---------- Toast ----------
  let toastTimer = 0;

  function toast(msg, actionLabel, action) {
    const t = $('#toast');
    t.innerHTML = `<span>${esc(msg)}</span>${actionLabel ? `<button>${esc(actionLabel)}</button>` : ''}`;
    if (actionLabel) t.querySelector('button').onclick = () => { action(); t.classList.remove('is-on'); };
    t.classList.add('is-on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove('is-on'), actionLabel ? 5000 : 1800);
  }

  // ---------- Events ----------
  function wire() {
    addEventListener('scroll', onScroll, { passive: true });
    addEventListener('resize', () => update());

    $('#btnToc').onclick = () => (drawer.classList.contains('is-open') ? closeDrawer() : openDrawer('toc'));
    $('#btnSearch').onclick = () => (searchBar.hidden ? openSearch() : closeSearch());
    $('#btnBookmark').onclick = toggleBookmark;
    $('#btnAa').onclick = e => { e.stopPropagation(); toggleSettings(); };
    $('#btnFull').onclick = () => {
      if (document.fullscreenElement) document.exitFullscreen();
      else root.requestFullscreen && root.requestFullscreen().catch(() => {});
    };
    document.addEventListener('fullscreenchange', () => $('#btnFull').classList.toggle('is-on', !!document.fullscreenElement));
    scrim.onclick = closeAll;
    [partNav, endmatter].forEach(el => el.addEventListener('click', e => {
      const b = e.target.closest('[data-go-part]');
      if (b) openPart(+b.dataset.goPart);
    }));

    drawer.addEventListener('click', e => {
      const tab = e.target.closest('.rd-tab');
      if (tab) return selectTab(tab.dataset.tab);
      const tog = e.target.closest('[data-tog]');
      if (tog) {
        const i = +tog.dataset.tog;
        if (tocOpen.has(i)) { tocOpen.delete(i); tocUserOpen.delete(i); } else { tocOpen.add(i); tocUserOpen.add(i); }
        applyTocOpen();
        return;
      }
      const item = e.target.closest('.rd-toc-item');
      if (item) {
        closeDrawer();
        goToEl(tocHeads[+item.dataset.i]);
        return;
      }
      const delMark = e.target.closest('[data-del-mark]');
      if (delMark) {
        B.bookmarks = B.bookmarks.filter(m => m.id !== delMark.dataset.delMark);
        O.save();
        renderMarks();
        update();
        return;
      }
      const delHl = e.target.closest('[data-del-hl]');
      if (delHl) {
        B.highlights = B.highlights.filter(h => h.id !== delHl.dataset.delHl);
        O.save();
        renderHighlights();
        return;
      }
      const mark = e.target.closest('[data-mark]');
      if (mark) {
        const m = B.bookmarks.find(x => x.id === mark.dataset.mark);
        closeDrawer();
        if (m) restorePos(m, true);
        return;
      }
      const hl = e.target.closest('[data-hl]');
      if (hl) {
        const h = B.highlights.find(x => x.id === hl.dataset.hl);
        closeDrawer();
        if (h && h.found !== false) {
          const switched = showPartOf(rangeFor(h.start, h.end).startContainer);
          const rect = rangeFor(h.start, h.end).getBoundingClientRect();
          window.scrollTo({ top: scrollY + rect.top - innerHeight / 3, behavior: reduceMotion || switched ? 'instant' : 'smooth' });
        }
      }
    });

    settings.addEventListener('click', e => {
      e.stopPropagation();
      const b = e.target.closest('[data-set]');
      if (b) return setPref(b.dataset.set, b.dataset.val);
      const s = e.target.closest('[data-step]');
      if (s) return stepSize(+s.dataset.step);
      if (e.target.closest('#resetPrefs')) {
        keepPlace(() => {
          Object.assign(prefs, DEFAULTS);
          prefs.theme = 'auto';
          applyPrefs();
        });
        O.save();
        refreshSettings();
        toast('Display settings reset');
      }
    });
    settings.addEventListener('input', e => {
      if (e.target.id === 'brightness') {
        prefs.brightness = +e.target.value;
        applyPrefs();
        O.save();
      }
    });
    settings.addEventListener('change', e => {
      const t = e.target.closest('[data-toggle]');
      if (t) setPref(t.dataset.toggle, t.checked);
    });

    searchInput.addEventListener('input', () => runSearch(searchInput.value));
    $('#searchNext').onclick = () => stepSearch(1);
    $('#searchPrev').onclick = () => stepSearch(-1);
    $('#searchClose').onclick = closeSearch;

    selPop.addEventListener('pointerdown', e => e.preventDefault());
    selPop.addEventListener('click', onSelAction);
    $('#lightbox').onclick = () => { $('#lightbox').hidden = true; };

    // Track: click or drag to jump; arrow keys nudge.
    const pctFromEvent = e => {
      const r = track.getBoundingClientRect();
      return Math.min(1, Math.max(0, (e.clientX - r.left) / r.width));
    };
    let dragging = false;
    track.addEventListener('pointerdown', e => {
      dragging = true;
      track.setPointerCapture(e.pointerId);
      restorePos(posFromPct(pctFromEvent(e)));
    });
    track.addEventListener('pointermove', e => {
      const pct = pctFromEvent(e);
      const p = posFromPct(pct);
      const si = sectionOf[p.block];
      const tip = $('#trackTip');
      tip.textContent = `${Math.round(pct * 100)}%${si >= 0 ? ' · ' + label(tocHeads[si]) : ''}`;
      tip.style.left = (pct * 100) + '%';
      if (dragging) restorePos(p);
    });
    track.addEventListener('pointerup', () => { dragging = false; });
    track.addEventListener('keydown', e => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      e.preventDefault();
      e.stopPropagation();
      restorePos(posFromPct(Math.min(1, Math.max(0, currentPct() + (e.key === 'ArrowRight' ? .02 : -.02)))));
    });

    // Selection
    let hadSelection = false;
    document.addEventListener('pointerdown', e => {
      hadSelection = !getSelection().isCollapsed;
      if (!e.target.closest('.rd-notepop')) hidePop(notePop);
      if (!e.target.closest('.rd-panel, #btnAa') && !settings.hidden) settings.hidden = true;
    });
    document.addEventListener('pointerup', e => {
      if (e.target.closest('.rd-pop, .rd-bar, .rd-drawer, .rd-panel, .rd-search')) return;
      setTimeout(checkSelection, 10);
    });
    let selTimer = 0;
    document.addEventListener('selectionchange', () => {
      clearTimeout(selTimer);
      selTimer = setTimeout(() => {
        const sel = getSelection();
        if (sel.isCollapsed) { if (selPop.dataset.mode === 'sel') hidePop(selPop); return; }
        if (matchMedia('(pointer: coarse)').matches) checkSelection();
      }, 350);
    });

    // Links, footnotes, images, highlights and page-turn taps
    $('#main').addEventListener('click', e => {
      const link = e.target.closest('a[href^="#"]');
      if (link && content.contains(link)) {
        const id = decodeURIComponent(link.getAttribute('href').slice(1));
        const target = id && document.getElementById(id);
        if (target && content.contains(target)) {
          e.preventDefault();
          if (isFootnote(target, link) && !target.matches('h1, h2, h3, h4, h5, h6')) showFootnote(link, target);
          else goToEl(target);
        }
        return;
      }
      if (e.target.closest('a, button, input, summary, .rd-table, pre, .katex, .rd-cta')) return;
      const img = e.target.closest('.rd-content img');
      if (img) return openLightbox(img);
      if (hadSelection || !getSelection().isCollapsed) return;
      const h = highlightAtPoint(e.clientX, e.clientY);
      if (h) return showHighlightPop(h, e.clientX, e.clientY);
      if (!selPop.hidden || !notePop.hidden) { hidePop(selPop); hidePop(notePop); return; }
      if (anyOverlayOpen() && searchBar.hidden) { closeAll(); return; }
      const x = e.clientX / innerWidth;
      if (prefs.tapTurn && x < .2) turn(-1);
      else if (prefs.tapTurn && x > .8) turn(1);
      else toggleChrome();
    });

    addEventListener('mousemove', e => {
      if (e.clientY < 48 || e.clientY > innerHeight - 48) {
        if (!body.classList.contains('rd-focus')) setChrome(true);
      }
    }, { passive: true });

    document.addEventListener('keydown', e => {
      if (e.target.closest('input, textarea, [contenteditable]')) {
        if (e.key === 'Escape') { closeSearch(); e.target.blur(); }
        else if (e.key === 'Enter' && e.target === searchInput) { e.preventDefault(); stepSearch(e.shiftKey ? -1 : 1); }
        return;
      }
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const k = e.key;
      if (k === 'ArrowRight' || k === 'PageDown' || (k === ' ' && !e.shiftKey)) { e.preventDefault(); turn(1); }
      else if (k === 'ArrowLeft' || k === 'PageUp' || (k === ' ' && e.shiftKey)) { e.preventDefault(); turn(-1); }
      else if (k === 't' || k === 'T') drawer.classList.contains('is-open') ? closeDrawer() : openDrawer('toc');
      else if (k === '/' || k === 's' || k === 'S') { e.preventDefault(); openSearch(); }
      else if (k === 'b' || k === 'B') toggleBookmark();
      else if (k === 'a' || k === 'A') toggleSettings();
      else if (k === 'f' || k === 'F') {
        body.classList.toggle('rd-focus');
        toast(body.classList.contains('rd-focus') ? 'Focus mode · press F to leave' : 'Focus mode off');
      }
      else if (k === '+' || k === '=') stepSize(1);
      else if (k === '-' || k === '_') stepSize(-1);
      else if (k === 'Escape') { closeAll(); if (!searchBar.hidden) closeSearch(); }
    });

    // Reading time: count while the page is visible and the reader was active recently.
    let lastActive = Date.now();
    ['scroll', 'pointermove', 'keydown', 'touchstart'].forEach(ev => addEventListener(ev, () => { lastActive = Date.now(); }, { passive: true }));
    setInterval(() => {
      if (document.visibilityState === 'visible' && Date.now() - lastActive < 120000) {
        O.addTime(slug, 5);
        O.save();
      }
    }, 5000);

    addEventListener('pagehide', () => {
      clearTimeout(saveTimer);
      if (blocks.length) {
        const p = capturePos();
        const pct = currentPct(p);
        const si = beforeContent() ? -1 : sectionOf[p.block];
        B.pos = {
          block: p.block, frac: +p.frac.toFixed(4), pct: +pct.toFixed(4),
          section: si >= 0 ? label(tocHeads[si]) : '',
          minutesLeft: Math.round(Math.max(0, totalWords - (beforeContent() ? 0 : wordsRead(p))) / WPM), at: Date.now(),
        };
      }
      O.save();
    });
  }

  // ---------- Empty and error states ----------
  function awaiting() {
    content.innerHTML = `<div class="rd-await">
      <h2>This volume is still being written</h2>
      <p>The notes for <em>${esc(subject.title)}</em> haven't been added yet. When they arrive they'll appear right here, with contents, search, highlights and everything else.</p>
      <a class="rd-cta" href="./">Back to the library</a>
    </div>`;
    disableTools();
  }

  function fail(title, msg) {
    titlepage.innerHTML = '';
    content.innerHTML = `<div class="rd-await"><div class="rd-ornament" aria-hidden="true">❦</div><h2>${esc(title)}</h2><p>${esc(msg)}</p><a class="rd-cta" href="./">Back to the library</a></div>`;
    disableTools();
  }

  function disableTools() {
    $$('#tools .rd-btn').forEach(b => { if (b.id !== 'btnAa') b.disabled = true; });
    $('#bottombar').hidden = true;
    body.classList.remove('rd-loading');
    buildSettings();
    $('#btnAa').onclick = e => { e.stopPropagation(); settings.hidden = !settings.hidden; };
    settings.addEventListener('click', e => {
      e.stopPropagation();
      const b = e.target.closest('[data-set]');
      if (b) { prefs[b.dataset.set] = b.dataset.val; applyPrefs(); O.save(); refreshSettings(); }
    });
    document.addEventListener('click', e => { if (!e.target.closest('.rd-panel, #btnAa')) settings.hidden = true; });
  }

  await start();
})();
