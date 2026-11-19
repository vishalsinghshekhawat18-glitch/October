"""Current Affairs print edition builder (story style, A4, black and white).

Usage:  python3 build.py content/<month>.py [--out DIR]

The month file (content/<month>.py) holds only the authored story layer: headlines, story paragraphs,
number strips, charts, chapter titles, cover. Every fact comes from the month's notes file; every number
written in the month file is checked against the notes and the build stops if one is missing.
The notes file is only read, never changed. See README.md.
"""
import re, html, sys, os, json, argparse
from bs4 import BeautifulSoup
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- notes
ap = argparse.ArgumentParser(); ap.add_argument('content'); ap.add_argument('--out', default='.')
ap.add_argument('--check-only', action='store_true')
ARGS = ap.parse_args()
C = {'__file__': os.path.abspath(ARGS.content)}
exec(open(ARGS.content, encoding='utf-8').read(), C)
NOTES_PATH = C['NOTES'] if os.path.isabs(C['NOTES']) else os.path.join(os.path.dirname(os.path.abspath(ARGS.content)), C['NOTES'])
NOTES = open(NOTES_PATH, encoding='utf-8').read()
soup = BeautifulSoup(NOTES, 'html.parser')
reading = NOTES[:NOTES.index('id="notes"')]

def nums_in(t):
    t = re.sub(r'<[^>]+>', ' ', t)
    return {x.replace(',', '').rstrip('.') for x in re.findall(r'\d[\d,]*(?:\.\d+)?', t)}
SRC = nums_in(reading)
WL = {str(n) for n in range(0, 13)} | {f'{n:02d}' for n in range(0, 10)} | {f'{a}.{b}' for a in range(1, 10) for b in range(1, 10)}
problems = []
def check(where, text):
    bad = nums_in(text) - SRC - WL
    if bad: problems.append(f'{where}: {sorted(bad)}')

def unbold_numbers(h):
    """Older notes bold their figures; the print never does (v3.1 section 7)."""
    return re.sub(r'<(strong|b)>([^<]*\d[^<]*)</\1>', r'\2', h)

# ---------------------------------------------------------------- charts
PAT = ('<defs><pattern id="{id}" width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
       '<rect width="3" height="3" fill="#fff"/><line x1="0" y1="0" x2="0" y2="3" stroke="#000" stroke-width="1.1"/></pattern>'
       '<pattern id="{id}d" width="2.4" height="2.4" patternUnits="userSpaceOnUse"><rect width="2.4" height="2.4" fill="#fff"/><circle cx="1.2" cy="1.2" r=".55" fill="#000"/></pattern></defs>')
FILLS = ['#000', 'url(#{p})', 'url(#{p}d)', '#fff', '#fff']
_pid = [0]
def hbar(title, rows, maxv, h=None, hi=None):
    """Horizontal bars. rows = [(label, value, shown_text)]; hi = index of the one black bar (others white)."""
    _pid[0] += 1; p = f'p{_pid[0]}'; n = len(rows); H = n * 20 + 4
    o = [f'<p class="chartlab">{title}</p><svg style="width:100%;height:{h or round(H*0.40,1)}mm;display:block" viewBox="0 0 200 {H}" font-family="Inter" font-size="6.8">', PAT.format(id=p)]
    for i, (lab, v, shown) in enumerate(rows):
        y = i * 20; w = 140 * v / maxv
        f = ('#000' if i == hi else '#fff') if hi is not None else FILLS[min(i, 4)].format(p=p)
        fw = ' font-weight="800"' if i == hi else ''
        o.append(f'<text x="0" y="{y+7}"{fw}>{html.escape(lab)}</text>'
                 f'<rect x="0" y="{y+9}" width="{w:.1f}" height="6.5" fill="{f}" stroke="#000" stroke-width=".5"/>'
                 f'<text x="{w+3:.1f}" y="{y+15}" font-weight="800">{html.escape(shown)}</text>')
    return ''.join(o) + '</svg>'
def steps(title, items, on_last=True):
    """Timeline. items = [(big text, small caption)]. Drawn as a one-row table: flex boxes cannot break in WeasyPrint."""
    cls = 'tl' + (' many' if len(items) > 6 else '') + (' vmany' if len(items) > 8 else '')
    o = [f'<p class="chartlab">{title}</p><table class="{cls}"><tr>']
    for i, (v, d) in enumerate(items):
        on = ' on' if (i == len(items) - 1 and on_last) else ''
        o.append(f'<td class="step{on}"><div class="v">{v}</div><div class="d">{d}</div></td>')
    return ''.join(o) + '</tr></table>'
def table_chart(title, head, rows, big_cols=()):
    """A small figure table. rows = list of cells; columns in big_cols are set large."""
    th = ''.join(f'<th>{x}</th>' for x in head)
    tr = ''.join('<tr>' + ''.join(f'<td{" class=\"big\"" if j in big_cols else ""}>{c}</td>' for j, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<p class="chartlab">{title}</p><table class="score"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
C.update(hbar=hbar, steps=steps, table_chart=table_chart)
CHARTS = C['make_charts'](hbar, steps, table_chart) if 'make_charts' in C else {}
CHARTS.update(C.get('RAW_CHARTS', {}))

# ---------------------------------------------------------------- cards
CARDS = soup.select('details.card')
SECEL = {}
for el in soup.select('section'):
    h = el.find(['h1', 'h2'])
    m = re.match(r'\s*(\d+)\.', h.get_text(strip=True)) if h else None
    if m and 1 <= int(m.group(1)) <= 9: SECEL[int(m.group(1))] = el
def find(sub):
    hits = [d for d in CARDS if sub in d.summary.get_text()]
    if len(hits) != 1: sys.exit(f'card match {len(hits)} for: {sub}')
    return hits[0]
def md_split(li):
    """Split a list item that carries a pipe (markdown) table into text before it and an HTML table."""
    if '|---' not in li.replace(' ', ''): return li, None
    lines = li.split('\n'); text = [l for l in lines if not l.strip().startswith('|')]
    rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in lines if l.strip().startswith('|') and not re.match(r'^\|?\s*-', l.strip().strip('|'))]
    head, body_ = rows[0], rows[1:]
    t = '<table><thead><tr>' + ''.join(f'<th>{c}</th>' for c in head) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in body_) + '</tbody></table>'
    return ' '.join(text).strip(), t
def read(d):
    b = d.select_one('.body')
    g = lambda c: (re.sub(r'^\s*(In plain words|Remember|Exam angle):\s*', '', b.select_one('.' + c).get_text(' ', strip=True)) if b.select_one('.' + c) else '')
    parts = []
    for ch in b.find_all(recursive=False):
        cls = (ch.get('class') or [''])[0]
        if cls in ('plain', 'hook', 'angle'): continue
        if ch.name == 'ul':
            buf = []
            for li in ch.find_all('li', recursive=False):
                txt, tb = md_split(unbold_numbers(li.decode_contents()))
                if tb:
                    if txt: buf.append(txt)
                    if buf: parts.append(('ul', buf)); buf = []
                    parts.append(('t', tb))
                else: buf.append(txt)
            if buf: parts.append(('ul', buf))
        elif ch.name == 'p': parts.append(('p', unbold_numbers(ch.decode_contents())))
        elif cls == 'tw' and ch.table: parts.append(('t', unbold_numbers(str(ch.table))))
    title = re.sub(r'^[★☆]\s*', '', d.summary.get_text(' ', strip=True))
    sub = d.find_previous('h2')
    return dict(title=title, must=d.get('class') == ['card'], plain=g('plain'), hook=g('hook'), angle=g('angle'), parts=parts,
                sub=sub.get_text(strip=True) if sub else '')

TID = [0]
def table(t, cls='score ff'):
    TID[0] += 1
    return t.replace('<table', f'<table class="{cls}" data-tid="t{TID[0]}"', 1)
def fact_file(c):
    o = []
    for k, v in c['parts']:
        if k == 'ul':
            if len(v) < 4: o.append('<ul class="one">' + ''.join(f'<li>{x}</li>' for x in v) + '</ul>')
            else:   # pairs side by side, row by row (a multi-column list cannot break and drags the whole story)
                rows = [v[i:i + 2] for i in range(0, len(v), 2)]
                o.append('<div class="ffg">' + ''.join('<div class="ffr">' + ''.join(f'<div class="ffc">{x}</div>' for x in r)
                         + ('<div class="ffc"></div>' if len(r) == 1 else '') + '</div>' for r in rows) + '</div>')
        elif k == 'p': o.append(f'<p class="ffp">{v}</p>')
        else: o.append(table(v))
    return f'<div class="ff"><b>Fact file</b>{"".join(o)}</div>' if o else ''

S = C['S']
def story(key, pre=''):
    s = S[key]; c = read(find(s['card']))
    if not c['must']: sys.exit(f'story {key} points to a good-to-know card')
    lede = s.get('lede') or c['plain']
    if re.search(r'\b(this|the) card\b|grouped here|gathers news', lede, re.I): sys.exit(f'story {key}: lede refers to the notes card; write a lede')
    hook = s.get('hook', c['hook']); trap = s.get('trap', ''); angle = s.get('angle', c['angle'])
    check(key + ' ' + s['h'], ' '.join([s['h'], lede, hook or '', trap, angle or '', s.get('tag', '')] + [' '.join(x) for x in s.get('nums', [])]))
    nums = ''
    if s.get('nums'):
        lng = ' long' if max(len(v) for v, _ in s['nums']) > 10 else ''
        nums = f'<div class="nums{lng}">' + ''.join(f'<div><b>{html.escape(v)}</b><span>{html.escape(l)}</span></div>' for v, l in s['nums']) + '</div>'
    ch = s.get('chart', [])
    for k in ch:
        if k not in CHARTS: sys.exit(f'chart {k} not defined')
        check(key + ' chart ' + k, CHARTS[k])
    charts = ('<div class="split">' + ''.join(f'<div>{CHARTS[k]}</div>' for k in ch) + '</div>') if len(ch) == 2 else (CHARTS[ch[0]] if ch else '')
    boxes = ''
    if hook: boxes += f'<div class="hook"><b>Remember it like this</b>{html.escape(hook)}</div>'
    if trap: boxes += f'<div class="trap"><b>Trap</b>{html.escape(trap)}</div>'
    elif angle: boxes += f'<div class="trap"><b>Likely question</b>{html.escape(angle)}</div>'
    size = s.get('size', 'short')
    return (f'<div class="story {size}" id="st-{key}"><div class="keep">{pre}<div class="tag"><span class="st">★</span>{html.escape(s["tag"])}</div>'
            f'<h2>{html.escape(s["h"])}</h2><div class="official">{html.escape(c["title"])}</div></div>'
            f'<p class="lede">{html.escape(lede)}</p>{nums}{charts}{"<div class=duo>" + boxes + "</div>" if boxes else ""}{fact_file(c)}</div>')

# ---------------------------------------------------------------- In brief
LAB = {'Growth, outlook and data releases': 'Growth and data', 'Trade, FDI and tax': 'Trade and tax', 'Social issue': 'Social',
       'Other regulators and bodies': 'Other regulators', 'Governance, law and institutions': 'Governance and law',
       'Agriculture, food and rural': 'Farms and villages', 'Infrastructure, transport and energy': 'Infrastructure and energy',
       'Environment, wildlife and heritage': 'Environment and heritage', 'Other national items': 'Other national news',
       'State and UT': 'States and UTs', 'International organisations': 'International bodies', 'Indices, rankings and reports': 'Reports and rankings',
       'Science and Technology': 'Science and technology', 'Schemes at a glance': 'Schemes'}
LAB.update(C.get('LAB', {}))
ENT = re.compile(r'^\s*<strong>(.*?)</strong>\s*(\([^)]*\))?\s*(?:→\s*)?(.*)$', re.S)
def bpoints(parts):
    o = []
    for k, v in parts:
        if k == 'p': o.append(f'<p class="ffp">{v}</p>'); continue
        if k == 't': o.append(table(v, 'score')); continue
        ents = [ENT.match(b) for b in v]
        if sum(1 for m in ents if m) >= 2:
            for b, m in zip(v, ents):
                if m:
                    par = f' <span class="par">{m.group(2)}</span>' if m.group(2) else ''
                    body = re.sub(r'^[\s:;,–-]+', '', m.group(3))
                    o.append(f'<div class="ent"><div class="en">{m.group(1)}{par}</div><div class="eb">{body}</div></div>')
                else: o.append(f'<ul><li>{b}</li></ul>')
        else: o.append('<ul>' + ''.join(f'<li>{x}</li>' for x in v) + '</ul>')
    return ''.join(o)
def bitem(d):
    c = read(d); t = c['title']
    m = re.search(r'\s*\(([^)]*\d[^)]*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[^)]*)\)\s*$', t)
    dt = ''
    if m: dt = f'<span class="dt">{html.escape(m.group(1))}</span>'; t = t[:m.start()]
    return f'<div class="bi"><h4><span class="ht">{html.escape(t)}</span>{dt}</h4>{bpoints(c["parts"])}</div>'
def brief_for(secel, sid):
    opts = [d for d in secel.select('details.card') if d.get('class') != ['card']]
    if not opts: return '', 0
    out, cur, buf = [], None, []
    for d in opts:
        h2 = d.find_previous('h2'); raw = h2.get_text(strip=True) if (h2 and secel in h2.parents) else ''
        tp = LAB.get(raw, raw)
        if tp != cur:
            if buf: out.append((cur, buf))
            cur, buf = tp, []
        buf.append(d)
    if buf: out.append((cur, buf))
    inner = ''.join((f'<div class="grp"><div class="gk">{html.escape(tp)}</div>{bitem(g[0])}</div>' if tp else bitem(g[0])) + ''.join(bitem(x) for x in g[1:]) for tp, g in out)
    return f'<div class="brief" id="{sid}-brief"><h3>In brief <span>good to know</span></h3><div class="cols">{inner}</div></div>', len(opts)

# ---------------------------------------------------------------- sections 1–8
SHORT = {1: 'Economy, finance and banking', 2: 'Regulators and circulars', 3: 'The world', 4: 'India and the states',
         5: 'MoUs, summits and appointments', 6: 'Science, defence and sports', 7: 'Awards, books and rankings', 8: 'Schemes', 9: 'Tables and revision'}
def numsvg(n): return (f'<div class="sn"><svg width="40mm" height="30mm" viewBox="0 0 120 90"><text x="0" y="78" font-family="Inter Display" '
                       f'font-weight="900" font-size="96" letter-spacing="-5" fill="#fff" stroke="#000" stroke-width="2.4">{n:02d}</text></svg></div>')
used, body, COUNTS = set(), [], {}
EMPTY = set()
for n in range(1, 9):
    sid = f'sec{n}'; el = SECEL[n]
    if not el.select('details.card'):
        tabs_ = []
        for h in el.find_all('h2'):
            tt = []
            for sib in h.find_next_siblings():
                if sib.name == 'h2': break
                for t in ([sib] if sib.name == 'table' else sib.select('table')): tt.append(table(unbold_numbers(str(t)), 'score'))
            if tt: tabs_.append(f'<div class="sumt"><div class="gk">{html.escape(h.get_text(strip=True))}</div>{"".join(tt)}</div>')
        if not tabs_: EMPTY.add(n); COUNTS[n] = (0, 0); continue
        check(f'sec{n} intro', C['SEC_INTRO'][n])
        body.append(f'''<div class="section" id="{sid}">{numsvg(n)}<div class="sbody"><div class="skick">Section {n} of 9</div><h1 class="stitle" data-n="{n}">{html.escape(SHORT[n])}</h1>
<p>{html.escape(C['SEC_INTRO'][n])}</p></div></div><div class="sumwrap">{"".join(tabs_)}</div>''')
        COUNTS[n] = None; continue
    chs = C['CHAPTERS'].get(n, [])
    check(f'sec{n} intro', C['SEC_INTRO'][n])
    toc = ''.join(f'<li><span class="k">{k}</span>{html.escape(t)}<a class="pg" href="#ch{k.replace(".", "")}"></a></li>' for k, t, _, _ in chs)
    br, nb = brief_for(el, sid)
    if nb: toc += f'<li><span class="k">☆</span>In brief<a class="pg" href="#{sid}-brief"></a></li>'
    o = [f'''<div class="section" id="{sid}">{numsvg(n)}<div class="sbody"><div class="skick">Section {n} of 9</div><h1 class="stitle" data-n="{n}">{html.escape(SHORT[n])}</h1>
<p>{html.escape(C['SEC_INTRO'][n])}</p><ul class="stoc">{toc}</ul></div></div>''']
    for k, t, intro, keys in chs:
        check(k, t + ' ' + intro)
        hd = f'<div class="chapter" id="ch{k.replace(".", "")}"><div class="k">Chapter {k}</div><h1>{html.escape(t)}</h1><p>{html.escape(intro)}</p></div>'
        for i, key in enumerate(keys):
            if key in used: sys.exit(f'story {key} placed twice')
            o.append(story(key, hd if i == 0 else '')); used.add(key)
    if len(o) > 1: o[-1] = o[-1].replace('<div class="story ', '<div class="story last ', 1)
    o.append(br)
    stars = [d for d in el.select('details.card') if d.get('class') == ['card']]
    placed = {find(S[k]['card']) for k in used}
    unplaced = [d.summary.get_text(' ', strip=True) for d in stars if d not in placed]
    if unplaced: sys.exit(f'section {n}: ★ cards without a story: {unplaced}')
    COUNTS[n] = (len(stars), nb)
    body.append('\n'.join(o))
if set(S) - used: sys.exit(f'stories not placed: {set(S) - used}')

# ---------------------------------------------------------------- section 9
s9 = SECEL[9]; tabs = []
for h in s9.find_all('h2'):
    tt = []
    for sib in h.find_next_siblings():
        if sib.name == 'h2': break
        for t in sib.select('table') if sib.name != 'table' else [sib]: tt.append(table(unbold_numbers(str(t)), 'score'))
    if tt: tabs.append(f'<div class="sumt"><div class="gk">{html.escape(h.get_text(strip=True))}</div>{"".join(tt)}</div>')
rev = soup.select_one('.rev')
qn = 0; qs = []; ans = []
for el in rev.find_all(['h3', 'details']):
    if el.name == 'h3':
        lab = re.sub(r'^\d+\.\s*', '', el.get_text(strip=True))
        qs.append(f'<div class="gk">{html.escape(lab)}</div>'); ans.append(f'<div class="ak">{html.escape(lab)}</div>')
    else:
        qn += 1
        qs.append(f'<p class="q"><b>{qn}</b>{unbold_numbers(el.summary.decode_contents())}</p>')
        a = el.select_one('.ans') or el
        ans.append(f'<p class="a"><b>{qn}</b>{unbold_numbers(a.decode_contents() if a is not el else a.get_text(" ", strip=True))}</p>')
body.append(f'''<div class="section" id="sec9">{numsvg(9)}<div class="sbody"><div class="skick">Section 9 of 9</div><h1 class="stitle" data-n="9">{SHORT[9]}</h1>
<p>The {C.get('UNIT', 'month')}'s key numbers and dates, then {qn} questions to test yourself. Answers follow the questions.</p>
<ul class="stoc"><li><span class="k">9.1</span>Key numbers and dates<a class="pg" href="#sumt"></a></li><li><span class="k">9.2</span>Test yourself<a class="pg" href="#rev"></a></li><li><span class="k">9.3</span>Answers<a class="pg" href="#ans"></a></li></ul></div></div>
<div id="sumt" class="sumwrap">{"".join(tabs)}</div>
<div class="revh" id="rev"><h3>Test yourself <span>{qn} questions</span></h3><div class="qcols">{"".join(qs)}</div></div>
<div class="revh" id="ans"><h3>Answers</h3><div class="acols">{"".join(ans)}</div></div>''')

# ---------------------------------------------------------------- cover and contents
CV = C['COVER']
cl = ''.join(f'<div><span>{html.escape(k)}</span><b>{html.escape(h)}</b><a class="pg" href="#st-{i}"></a></div>' for k, h, i in C['COVER_LINES'])
for _, _, i in C['COVER_LINES'] + [('', '', CV['lead'])]:
    if i not in S: sys.exit(f'cover points to unknown story {i}')
strip = ''.join(f'<span><b>{n:02d}</b>{html.escape(SHORT[n])}</span>' for n in range(1, 9) if n not in EMPTY)
stats = ''.join(f'<div><b>{html.escape(v)}</b>{html.escape(l)}</div>' for v, l in CV['stats'])
cvl = ' long' if max(len(v) for v, _ in CV['stats']) > 7 else ''
cover = f'''<div class="cover"><div class="mast"><div class="mt">Current Affairs</div><div class="mi"><b>{html.escape(C['MONTH'])}</b><br>{html.escape(C['PERIOD'])}</div></div>
<div class="lead"><div class="lk">Cover story · {html.escape(CV['kicker'])}</div><div class="cv-title">{html.escape(CV['title'])}</div>
<p class="cv-dek">{html.escape(CV['dek'])} <a class="pg" href="#st-{CV['lead']}"></a></p></div>
<div class="cv-stats{cvl}">{stats}</div><div class="also"><div class="ah">Also in this issue</div><div class="grid">{cl}</div></div><div class="strip">{strip}</div></div>'''
check('cover', cover.replace(C['MONTH'], '').replace(C['PERIOD'], ''))
rows = []
for n in range(1, 10):
    cnt = 'tables and questions' if n == 9 else ('none this month' if n in EMPTY else ('at-a-glance tables' if COUNTS[n] is None else f'{COUNTS[n][0]} {"story" if COUNTS[n][0] == 1 else "stories"} · {COUNTS[n][1]} in brief'))
    pg = '' if n in EMPTY else f'<a class="pg" href="#sec{n}"></a>'
    rows.append(f'<tr class="in"><td class="n">{n:02d}</td><td><b>{html.escape(SHORT[n])}</b><small>{html.escape(C["LEADS"][n])}</small></td>'
                f'<td class="c">{cnt}</td><td class="p">{pg}</td></tr>')
check('leads', ' '.join(C['LEADS'].values()))
tm = sum(v[0] for v in COUNTS.values() if v); tb = sum(v[1] for v in COUNTS.values() if v)
dash = ''
if C.get('DASH'):
    check('dash', C['DASH']); dash = f'<div class="mnum"><div class="ckick">{html.escape(C.get('DASH_TITLE', 'The month in numbers'))}</div>{C["DASH"]}</div>'
contents = f'''<div class="contents"><div class="ckick">Inside this issue</div><h1 class="ct">{9 - len(EMPTY)} sections · {tm} stories · {tb} briefs</h1>
<table class="toc">{''.join(rows)}</table>{dash}</div>'''

print(f'{C["MONTH"]}: {len(S)} stories, {tb} briefs, {qn} questions · number problems: {len(problems)}')
for p in problems: print('  ', p)
if problems: sys.exit(1)
if ARGS.check_only: sys.exit(0)

# ---------------------------------------------------------------- render with layout fixes
CSS = open(os.path.join(HERE, 'print.css'), encoding='utf-8').read().replace('__MONTH__', C['MONTH'])
def build(keep=(), tight=(), flow=()):
    out = '\n'.join(body)
    for t in keep: out = re.sub(rf'<table class="([^"]*)" data-tid="{t}"', rf'<table class="\1 keept" data-tid="{t}"', out, count=1)
    for sid in tight: out = out.replace(f'<div class="brief" id="{sid}-brief">', f'<div class="brief tight" id="{sid}-brief">', 1)
    for sid in flow: out = out.replace(f'<div class="section" id="{sid}">', f'<div class="section flow" id="{sid}">', 1)
    return f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Current Affairs · {html.escape(C["MONTH"])}</title><style>{CSS}</style></head><body>{cover}{contents}{out}</body></html>'

from weasyprint import HTML
from weasyprint.formatting_structure import boxes as B
def analyse(doc):
    splits, pages_of, fill = {}, {}, []
    for i, pg in enumerate(doc.pages):
        for a in pg.anchors: pages_of.setdefault(a, i)
        bottom = 0
        for top in pg._page_box.children:
            if isinstance(top, B.MarginBox): continue
            for bx in top.descendants():
                if isinstance(bx, B.TableBox) and bx.element is not None and bx.element.get('data-tid'):
                    n = sum(sum(1 for r in g.children if isinstance(r, B.TableRowBox)) for g in bx.children if isinstance(g, B.TableRowGroupBox) and not g.is_header)
                    splits.setdefault(bx.element.get('data-tid'), []).append((i, n))
                if isinstance(bx, B.TextBox) and bx.text.strip():
                    bottom = max(bottom, bx.position_y + bx.height)
        fill.append(bottom)
    return splits, pages_of, fill
keep, tight, flow = set(), set(), set()
for it in range(8):
    doc = HTML(string=build(keep, tight, flow), base_url='.').render()
    splits, pages_of, fill = analyse(doc); H = doc.pages[0].height - 14 * 96 / 25.4; new = False
    for tid, segs in splits.items():
        segs = [s for s in segs if s[1] > 0]
        pages = {p for p, _ in segs}
        if len(pages) > 1 and tid not in keep and min(n for _, n in segs) <= 2 and sum(n for _, n in segs) <= 14:
            keep.add(tid); new = True
    live = [n for n in range(1, 10) if n not in EMPTY]
    for a, b in zip(live, live[1:]):
        last = pages_of[f'sec{b}'] - 1; frac = fill[last] / H
        if frac < 0.45:
            if f'sec{a}' not in tight: tight.add(f'sec{a}'); new = True
            elif f'sec{b}' not in flow: flow.add(f'sec{b}'); new = True
    print(f'  layout pass {it}: {len(doc.pages)} pages; tables kept whole {len(keep)}; tightened {sorted(tight)}; sections started mid-page {sorted(flow)}')
    if not new: break
os.makedirs(ARGS.out, exist_ok=True)
stem = os.path.join(ARGS.out, C['OUTFILE'])
doc.write_pdf(stem + '.pdf')
open(stem + '.html', 'w', encoding='utf-8').write(build(keep, tight, flow))
low = [(i + 1, round(f / H, 2)) for i, f in enumerate(fill[:-1]) if f / H < 0.6]
print(f'  wrote {stem}.pdf · {len(doc.pages)} pages · pages under 60% full: {low or "none"}')
