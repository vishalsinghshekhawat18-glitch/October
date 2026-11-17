"""Build the Jan–Mar 2026 magazine-style print book from the archived notes file.
Usage (from repo root): python3 work/magazine/build.py
"""
import re, copy, html
from bs4 import BeautifulSoup, NavigableString, Comment

SRC = 'archive/current-affairs/CA_Jan-Mar_2026.html'
SAMPLE = 'work/magazine/sample.html'
OUT = 'work/magazine/CA_Jan-Mar_2026_magazine.html'

src = BeautifulSoup(open(SRC).read(), 'html.parser')
sample = BeautifulSoup(open(SAMPLE).read(), 'html.parser')
CSS = sample.style.string

# ---------- section metadata ----------
SECS = {
 1: ('ESI, Finance & Business', "The economy's first quarter in numbers: how fast India grew, what prices did, who forecast what, and what changed in banking and insurance."),
 2: ('Regulators, PIB & Circulars', 'What RBI, SEBI, PFRDA, TRAI and other bodies changed between January and March, and who each change affects.'),
 3: ('The World & India', 'Treaties, trade deals, new members and walk-outs: the international stories that shaped the quarter.'),
 4: ('Nation & States', 'Laws, courts, budgets, infrastructure, environment and the States, with Rajasthan where it made news.'),
 5: ('MoUs, Meets & Appointments', 'Who signed with whom, who met where, and who took which chair.'),
 6: ('Science, Defence & Sports', 'Launches, exercises, missiles, policies and results, in compact tables.'),
 7: ('Awards, Books & Rankings', "Honours, new books and the indices where India's rank is the question."),
 8: ('Schemes & Static Links', 'Government schemes at a glance: who runs them, who benefits and how they work.'),
 9: ('Numbers at a Glance', 'The quarter in one place: key figures, dates ahead and days to remember. Read this the night before.'),
}
# hero card per section: (card id, big number, small suffix)
HERO = {1: None, 2: ('JAN-', None), }
HERO = {
 1: ('JAN-001', '7.4', '%', 'Number of the quarter'),
 2: (None, '75', '%', 'Number of the quarter'),
 3: (None, '21', 'st', 'Number of the quarter'),
 4: (None, '98', '', 'Number of the quarter'),
 6: (None, '7', '', 'Number of the quarter'),
 7: (None, '27', '', 'Number of the quarter'),
 8: (None, '125', ' days', 'Number of the quarter'),
}
HERO_TITLE = {  # title prefix of the card whose plain-words line becomes the caption
 2: 'RBI draft: bank dividend payout cap 75% of PAT',
 3: 'Bulgaria joins the euro',
 4: 'Ramsar sites: India now has 98',
 6: 'PRAHAAR',
 7: 'QS World University Rankings by Subject 2026',
 8: 'Viksit Bharat–G RAM G Act',
}
REV_AFTER = {'ESI, finance and business': 1, 'Regulators': 2, 'Schemes': 8,
             'International and national': 4, 'Defence, science, indices': 7}
REV_TITLE = {8: 'Schemes', 1: 'ESI, finance & business', 2: 'Regulators', 4: 'International & national', 7: 'Defence, science & indices'}

def card_id(d):
    for c in d.contents:
        if isinstance(c, Comment):
            return c.strip()
    return None

def clean_summary(t):
    t = t.strip().lstrip('★☆').strip()
    t = t.replace(' (from Jan 2026 PDF)', '')
    return t

def strip_num_bold(tag):
    """Remove <strong> around anything containing a digit (no bold numbers)."""
    for st in tag.find_all('strong'):
        if re.search(r'\d', st.get_text()):
            st.unwrap()
    return tag

def inner(tag):
    return ''.join(str(c) for c in tag.contents)

def timeline_html(text):
    steps = [x.strip() for x in text.split('→')]
    out = ['<p class="chartlab" style="margin-top:2mm">Timeline</p><div class="tl small">']
    for i, st in enumerate(steps):
        out.append(f'<div class="step{" on" if i == len(steps)-1 else ""}"><div class="t">{html.escape(st)}</div></div>')
    out.append('</div>')
    return ''.join(out)

def render_body(body, must):
    parts, side = [], []
    for ch in body.children:
        if not getattr(ch, 'name', None):
            continue
        cls = ch.get('class') or []
        if 'plain' in cls:
            t = ch.get_text(' ', strip=True)
            t = re.sub(r'^In plain words:\s*', '', t)
            parts.append(f'<p class="plain">{html.escape(t)}</p>')
        elif ch.name == 'ul':
            lis, tls = [], []
            for li in ch.find_all('li', recursive=False):
                if li.get_text().startswith('Timeline:'):
                    tls.append(timeline_html(li.get_text()[len('Timeline:'):]))
                else:
                    lis.append(f'<li>{inner(strip_num_bold(li))}</li>')
            parts.append('<ul class="f">' + ''.join(lis) + '</ul>' + ''.join(tls))
        elif 'angle' in cls:
            side.append(f'<div class="sidebox"><b>Exam angle</b>{inner(ch).replace("<strong>Exam angle:</strong>", "").strip()}</div>')
        elif 'hook' in cls:
            side.append(f'<div class="sidebox hook"><b>Remember</b>{inner(ch).replace("<strong>Remember:</strong>", "").strip()}</div>')
        else:
            parts.append(str(ch))
    if side:
        parts.append('<div class="split sides">' + ''.join(side) + '</div>' if len(side) > 1 else side[0])
    return ''.join(parts)

def must_card(d, kicker):
    title = clean_summary(d.summary.get_text())
    return (f'<div class="card"><div class="head"><div class="star">★</div>'
            f'<div class="title"><small>{html.escape(kicker)}</small>{html.escape(title)}</div></div>'
            f'<div class="inner">{render_body(d.select_one("div.body"), True)}</div></div>')

def mini_card(d):
    title = clean_summary(d.summary.get_text())
    return (f'<div class="mini"><h4><span class="hs">☆</span>{html.escape(title)}</h4>'
            f'{render_body(d.select_one("div.body"), False)}</div>')

def table_html(tw):
    t = copy.copy(tw.find('table'))
    for tr in t.find_all('tr'):
        if 'Left out: source-only rule' in tr.get_text():
            tr.decompose()
    for a in ('id',):
        t.attrs.pop(a, None)
    t['class'] = 'score data'
    return f'<div class="tblwrap">{t}</div>'

# ---------- sample blocks (hand-designed cards for section 1) ----------
scards = sample.select('div.card')
SPECIAL = {'JAN-001': str(scards[0]), 'JAN-047': str(scards[1]),
           'JAN-002': str(scards[2]).replace(' pagebreak', ''), 'JAN-003': str(scards[3])}
SKIP = {'JAN-004'}  # folded into the forecasts card (table row + tabled-by line)

# ---------- revision ----------
h10 = src.find('h1', id='s10')
groups, cur = {}, None
for el in h10.find_all_next(['h1', 'h3', 'details']):
    if el.name == 'h1': break
    if el.name == 'h3':
        cur = el.get_text().strip().replace('More: ', ''); groups.setdefault(cur, [])
    else:
        groups[cur].append((el.summary.get_text().strip(), inner(el.select_one('div.ans'))))
qnum = 0
selftests, answers = {}, []
for g, qs in sorted(groups.items(), key=lambda kv: REV_AFTER[kv[0]]):
    sec = REV_AFTER[g]
    items = []
    for q, a in qs:
        qnum += 1
        items.append(f'<li value="{qnum}">{html.escape(q)}</li>')
        answers.append((qnum, q, a, REV_TITLE[sec]))
    selftests[sec] = (REV_TITLE[sec], qnum - len(qs) + 1, qnum, items)

# ---------- body ----------
out = []
sections = src.find_all('section')[:9]
all_cards = {}
for n, sec in enumerate(sections, 1):
    for d in sec.select('details.card'):
        all_cards[clean_summary(d.summary.get_text())] = d

def hero_html(n):
    if n not in HERO: return ''
    cid, num, suf, lab = HERO[n]
    if n == 1:
        cap = ('Real GDP growth for FY2025-26, the first advance estimate released by NSO in January 2026.'
               '<span class="was">FY25 &nbsp;6.5% &nbsp;→&nbsp; FY26 &nbsp;7.4%</span>')
    else:
        key = next(k for k in all_cards if k.startswith(HERO_TITLE[n]))
        cap = html.escape(re.sub(r'^In plain words:\s*', '', all_cards[key].select_one('.plain').get_text(' ', strip=True)))
    return (f'<div class="hero"><div class="lab"><span>{lab}</span></div>'
            f'<div class="num">{num}<small>{suf}</small></div><div class="cap">{cap}</div></div>')

for n, sec in enumerate(sections, 1):
    title, dek = SECS[n]
    h2s = [h.get_text().strip() for h in sec.find_all('h2')]
    chips = ''.join(f'<span>{html.escape(h)}</span>' for h in h2s)
    numtxt = f'{n:02d}'
    out.append(f'''<div class="opener" id="s{n}">
  <svg class="bignum" width="78mm" height="62mm" viewBox="0 0 300 240"><defs><pattern id="d{n}" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".9" fill="#000"/></pattern></defs><text x="300" y="200" text-anchor="end" font-family="Inter Display" font-weight="900" font-size="250" letter-spacing="-10" fill="url(#d{n})" stroke="#000" stroke-width="2.5">{numtxt}</text></svg>
  <div class="kicker"><span>Section {["One","Two","Three","Four","Five","Six","Seven","Eight","Nine"][n-1]}</span></div>
  <h1 class="sectitle" data-run="{numtxt} · {html.escape(title)}">{html.escape(title)}</h1>
  <div class="dek">{html.escape(dek)}</div>
  {f'<div class="inthis"><b>In this section</b>{chips}</div>' if chips else ''}
</div>''')
    out.append(hero_html(n))
    kicker = title
    buf = []  # pending good-to-know minis
    def flush():
        if buf:
            out.append('<div class="gtk-band">☆ Good to know</div><div class="cols">' + ''.join(buf) + '</div>')
            buf.clear()
    skip_next_table = False
    for el in sec.children:
        name = getattr(el, 'name', None)
        if not name: continue
        if name == 'h1': continue
        if name == 'h2':
            flush()
            kicker = el.get_text().strip()
            out.append(f'<h2 class="sub"><span>{html.escape(kicker)}</span></h2>')
        elif name == 'details' and 'card' in (el.get('class') or []):
            cid = card_id(el)
            if cid in SKIP: continue
            if 'opt' in el['class']:
                buf.append(mini_card(el))
            else:
                flush()
                if cid in SPECIAL:
                    out.append(SPECIAL[cid])
                    if cid == 'JAN-003': skip_next_table = True
                else:
                    out.append(must_card(el, kicker))
        elif name == 'div' and 'tw' in (el.get('class') or []):
            if skip_next_table:
                skip_next_table = False; continue
            flush()
            out.append(table_html(el))
        elif name == 'p' or name == 'ul':
            flush(); out.append(str(strip_num_bold(el)))
    flush()
    if n in selftests:
        t, a, b, items = selftests[n]
        out.append(f'<div class="selftest big"><div class="bar"><span>Self-test · {html.escape(t)} · Q{a}–{b}</span>'
                   f'<span>Answers at the back</span></div><ol>{"".join(items)}</ol></div>')

body = '\n'.join(out)
body = body.replace('<h1 class="sectitle">ESI, Finance &amp; Business</h1>', '')

# ---------- answer key ----------
ak = ['<div class="opener short" id="answers"><div class="kicker"><span>Back matter</span></div>'
      '<h1 class="sectitle" data-run="Answer key">Answer key</h1>'
      '<div class="dek">Check yourself only after you have tried the question. Tick the box beside the question in the section when you get it right.</div></div>',
      '<div class="akey">']
last = None
for q, qt, a, g in answers:
    if g != last:
        ak.append(f'<h3>{html.escape(g)}</h3>'); last = g
    ak.append(f'<p><b>{q:02d}</b> <i>{html.escape(qt)}</i><br>{a}</p>')
ak.append('</div>')

# ---------- front matter ----------
n_cards = len(src.select('details.card')); n_must = len(src.select('details.card:not(.opt)'))
toc = ''.join(f'<li><a href="#s{n}"><span class="tn">{n:02d}</span><span class="tt">{html.escape(SECS[n][0])}</span></a></li>' for n in SECS)
toc += '<li><a href="#answers"><span class="tn">✓</span><span class="tt">Answer key</span></a></li>'
rows = ''.join(f'<tr><td>{n:02d} · {html.escape(SECS[n][0])}</td>' + '<td></td>'*6 + '</tr>' for n in SECS)
front = f'''
<div class="cover">
  <div class="cv-top"><span>Current Affairs</span><span>Bank PO · RBI · NABARD · SEBI · Govt exams</span></div>
  <svg class="cv-q" viewBox="0 0 400 260"><defs><pattern id="cvd" width="5" height="5" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r="1.1" fill="#000"/></pattern></defs>
   <text x="0" y="230" font-family="Inter Display" font-weight="900" font-size="270" letter-spacing="-14" fill="url(#cvd)" stroke="#000" stroke-width="3">Q1</text></svg>
  <div class="cv-year">2026</div>
  <h1 class="cv-title">January<br>February<br>March</h1>
  <div class="cv-dek">The quarter's current affairs, edited for the exam hall: every must-learn story in plain words first, then the facts, then a question to test yourself.</div>
  <div class="cv-stats"><div><b>{n_cards}</b>stories</div><div><b>{n_must}</b>must-learn</div><div><b>{qnum}</b>self-test questions</div><div><b>9</b>sections</div></div>
  <div class="cv-legend"><span class="k">★</span> must-learn &nbsp;&nbsp; <span class="k2">☆</span> good to know</div>
</div>
<div class="inside">
  <div class="kicker"><span>Revision tracker</span></div>
  <h2 class="ih">Read once, then come back</h2>
  <p class="dek">Memory fades fast unless you revisit. Tick a box each time you finish a section's self-test. Aim for the full row before the exam.</p>
  <table class="tracker"><thead><tr><th>Section</th><th>Day 1</th><th>Day 3</th><th>Day 7</th><th>Day 21</th><th>Day 35</th><th>Exam week</th></tr></thead><tbody>{rows}</tbody></table>
  <div class="howto">
    <h3>How to read a page</h3>
    <div class="ht"><div class="star sm">★</div><p><b>Must-learn card.</b> Read the quote line first: it is the story in plain words. Then the facts. The grey box is how it is likely to be asked; the dashed box is a hook for a tricky number.</p></div>
    <div class="ht"><div class="star sm hollow">☆</div><p><b>Good to know.</b> Two-column notes. Skim them on the second pass.</p></div>
    <div class="ht"><div class="star sm hollow">✓</div><p><b>Self-test.</b> At the end of sections 1, 2, 4, 7 and 8. Answer from memory, then check the key at the back.</p></div>
  </div>
</div>
<div class="contents">
  <div class="kicker"><span>Contents</span></div>
  <h2 class="ih">Inside this issue</h2>
  <ol class="toc">{toc}</ol>
</div>
'''

EXTRA_CSS = r'''
h1.sectitle { string-set: sec attr(data-run); }
.opener { break-before: right; }
.opener.short { height: auto; padding-bottom: 4mm }
.inthis { position: static; margin-top: 4mm; width: 120mm }
.opener { height: auto; min-height: 62mm; padding-bottom: 3mm }
.gtk-band { break-after: avoid }
h2.sub { font: 800 8pt Inter; letter-spacing: .26em; text-transform: uppercase; margin: 5mm 0 3mm; display:flex; align-items:center; gap: 3mm; break-after: avoid }
h2.sub span { background:#000; color:#fff; padding: 1.2mm 3mm }
h2.sub:after { content:""; flex:1; border-top: 2pt solid #000 }
.card { break-inside: auto }
.card .head { break-after: avoid }
.plain { break-after: avoid }
.mini { break-inside: avoid }
.mini ul.f li { margin-bottom: .6mm }
.mini .sidebox { font-size: 7.8pt; padding: 1.4mm 2mm; margin-top: 1.5mm }
.mini { margin-bottom: 3mm !important }
.cols { margin-bottom: 3mm }
.split.sides { margin-top: 2.5mm } .split.sides .sidebox { margin-top: 0 }
.tl.small .t { font: 8pt/1.3 Lora; padding-right: 3mm }
.tblwrap { margin: 0 0 4mm; break-inside: auto }
table.data { font-size: 7.8pt; }
table.data td { vertical-align: top }
table.data thead { display: table-header-group }
table.data tr { break-inside: avoid }
.card .inner table.data { margin-top: 2mm }
.selftest.big ol li { padding-left: 17mm }
.selftest.big li:before { content: counter(list-item, decimal-leading-zero) }
.selftest.big li:after { left: 11mm }
.selftest.big { break-inside: auto; margin-top: 5mm }
.selftest .bar { break-after: avoid }
/* answer key */
.akey { columns: 2; column-gap: 7mm; column-rule: .5pt solid #bbb; font: 8pt/1.38 Inter }
.akey h3 { font: 800 7.4pt Inter; letter-spacing: .22em; text-transform: uppercase; background:#000; color:#fff; padding: 1mm 2mm; margin: 0 0 2mm; break-after: avoid }
.akey p { margin: 0 0 2.2mm; break-inside: avoid }
.akey p b { font: 900 8.5pt 'Inter Display'; margin-right: 1mm }
.akey p i { font: italic 8pt Lora; color:#444 }
/* cover */
@page cover { margin: 0; @top-left{content:none} @top-right{content:none} @bottom-right{content:none} @bottom-left{content:none} }
@page plainpg { @top-left{content:none} @top-right{content:none} }
.cover { page: cover; height: 297mm; padding: 16mm 15mm 16mm 22mm; position: relative; border-left: 9mm solid #000; }
.cv-top { display:flex; justify-content:space-between; font: 800 8pt Inter; letter-spacing: .26em; text-transform: uppercase; border-bottom: 2pt solid #000; padding-bottom: 2mm }
.cv-q { width: 150mm; height: 98mm; margin-top: 10mm; display:block }
.cv-year { font: 900 30pt 'Inter Display'; letter-spacing: .3em; margin: -2mm 0 6mm 2mm }
.cv-title { font: 900 40pt/0.98 'Inter Display'; margin: 0 0 6mm; letter-spacing: -.02em }
.cv-dek { font: italic 13pt/1.4 Lora; width: 125mm; }
.cv-stats { position:absolute; bottom: 30mm; left: 22mm; right: 15mm; display:flex; border-top: 2pt solid #000; border-bottom: .6pt solid #000 }
.cv-stats div { flex:1; padding: 3mm 0; font: 600 7.4pt Inter; letter-spacing:.14em; text-transform: uppercase }
.cv-stats b { display:block; font: 900 26pt 'Inter Display'; letter-spacing: -.02em; text-transform:none }
.cv-legend { position:absolute; bottom: 18mm; left: 22mm; font: 600 8.5pt Inter }
.cv-legend .k { background:#000; color:#fff; padding: 0 1.2mm; font-family:'DejaVu Sans' } .cv-legend .k2 { font-family:'DejaVu Sans' }
.inside, .contents { page: plainpg; break-before: page }
.ih { font: 900 26pt/1 'Inter Display'; margin: 4mm 0 3mm; letter-spacing: -.02em }
.tracker { width: 100%; border-collapse: collapse; font: 8.4pt Inter; margin: 5mm 0 8mm }
.tracker th { font: 700 6.8pt Inter; letter-spacing: .14em; text-transform: uppercase; border-bottom: 1.2pt solid #000; padding: 1.5mm; text-align:left }
.tracker td { border-bottom: .5pt solid #999; padding: 3.2mm 1.5mm; }
.tracker td + td { border-left: .5pt dotted #999; width: 14mm }
.tracker td + td:before { content:""; display:inline-block; width: 4mm; height: 4mm; border: .9pt solid #000; }
.howto h3 { font: 800 8pt Inter; letter-spacing: .24em; text-transform: uppercase; border-bottom: 1.2pt solid #000; padding-bottom: 1.5mm }
.ht { display:flex; gap: 4mm; align-items:flex-start; margin: 3mm 0; font: 9.4pt/1.45 Lora }
.ht p { margin: 0 }
.star.sm { background:#000; color:#fff; width: 9mm; height: 9mm; font: 13pt/9mm 'DejaVu Sans'; text-align:center; flex: none }
.star.sm.hollow { background:#fff; color:#000; border: 1.2pt solid #000 }
.toc { list-style: none; padding: 0; margin: 8mm 0 0 }
.toc li { border-bottom: .6pt solid #000; }
.toc a { display:flex; align-items: baseline; gap: 5mm; padding: 3.2mm 0; color: #000; text-decoration: none }
.toc .tn { font: 900 22pt/1 'Inter Display'; width: 16mm }
.toc .tt { flex:1; font: 700 13pt 'Inter Display' }
.toc a:after { content: target-counter(attr(href), page); font: 800 12pt 'Inter Display'; width: 14mm; text-align: right }
.toc li:nth-child(odd) a .tn { color: #000 }
a { color: inherit; text-decoration: none }
'''

doc = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Current Affairs Q1 2026 (Jan–Mar): print edition</title>
<style>{CSS}{EXTRA_CSS}</style></head><body>{front}{body}{"".join(ak)}</body></html>'''
# toc href fix: target-counter needs the attr on the span; use a:after instead
doc += ''
open(OUT, 'w').write(doc)
print('written', OUT, 'questions', qnum, 'cards', n_cards, 'must', n_must)
