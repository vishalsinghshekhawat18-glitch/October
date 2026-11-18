"""Build Section 1 in story style. Run from work/magazine: python3 build_story.py"""
import json, re, html, sys
from s1_story import CHAPTERS

cards = json.load(open('s1_cards.json'))
SRC_TEXT = ' '.join(c['text'] + ' ' + c['title'] for c in cards.values())

def nums_in(t):
    t = re.sub(r'<[^>]+>', ' ', t)
    return {x.replace(',', '').rstrip('.') for x in re.findall(r'\d[\d,]*(?:\.\d+)?', t)}
SRC_NUMS = nums_in(SRC_TEXT)
WHITELIST = {'57', '43', '1', '2', '3', '4', '5', '6', '10', '12', '0'}

# ---------------- charts ----------------
PAT = ('<defs><pattern id="{id}" width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
       '<rect width="3" height="3" fill="#fff"/><line x1="0" y1="0" x2="0" y2="3" stroke="#000" stroke-width="1.1"/></pattern></defs>')
FILLS = ['#000', '#555', '#999', 'url(#{p})', '#fff']
_pid = [0]
def pid():
    _pid[0] += 1; return f'p{_pid[0]}'

def hbar(title, rows, maxv, h=None):
    """rows: (label, value, shown)"""
    p = pid(); n = len(rows); H = n * 18 + 4
    out = [f'<p class="chartlab">{title}</p><svg style="width:100%;height:{h or round(H*0.40,1)}mm;display:block" viewBox="0 0 200 {H}" font-family="Inter" font-size="6.2">', PAT.format(id=p)]
    for i, (lab, v, shown) in enumerate(rows):
        y = i * 18; w = 150 * v / maxv; f = FILLS[min(i, 4)].format(p=p)
        out.append(f'<text x="0" y="{y+7}">{html.escape(lab)}</text>'
                   f'<rect x="0" y="{y+9}" width="{w:.1f}" height="6" fill="{f}" stroke="#000" stroke-width=".5"/>'
                   f'<text x="{w+3:.1f}" y="{y+14.5}" font-weight="800">{html.escape(shown)}</text>')
    out.append('</svg>')
    return ''.join(out)

def steps(title, items, on_last=True):
    """timeline: items (value, label)"""
    o = [f'<p class="chartlab">{title}</p><div class="tl">']
    for i, (v, d) in enumerate(items):
        o.append(f'<div class="step{" on" if (i == len(items)-1 and on_last) else ""}"><div class="v">{v}</div><div class="d">{d}</div></div>')
    return ''.join(o) + '</div>'

CPI = open('sample_v2.html').read()
cpi_svgs = re.findall(r'<p class="chartlab">.*?</svg>', CPI, re.S)
CHARTS = {
 'cpi': '<div class="split">' + f'<div>{cpi_svgs[0]}</div><div>{cpi_svgs[1]}</div>' + '</div>',
 'sectors': hbar('Who pulled growth (real, FY26, %)', [('Finance, real estate, prof. + pub. admin', 9.9, '9.9'), ('Trade, hotels, transport', 7.5, '7.5'),
            ('Manufacturing and construction', 7.0, '7.0'), ('Agriculture', 3.1, '3.1'), ('Utilities', 2.1, '2.1')], 9.9),
 'podium': '''<p class="chartlab">World's largest economies</p><svg style="width:100%;height:30mm;display:block" viewBox="0 0 200 80" font-family="Inter">
   <rect x="2" y="20" width="44" height="50" fill="#000"/><text x="24" y="15" text-anchor="middle" font-size="8" font-weight="800">US</text><text x="24" y="50" text-anchor="middle" font-size="16" font-weight="900" fill="#fff" font-family="Inter Display">1</text>
   <rect x="51" y="30" width="44" height="40" fill="#555"/><text x="73" y="25" text-anchor="middle" font-size="8" font-weight="800">China</text><text x="73" y="56" text-anchor="middle" font-size="16" font-weight="900" fill="#fff" font-family="Inter Display">2</text>
   <rect x="100" y="40" width="44" height="30" fill="#999"/><text x="122" y="35" text-anchor="middle" font-size="8" font-weight="800">Germany</text><text x="122" y="61" text-anchor="middle" font-size="16" font-weight="900" fill="#fff" font-family="Inter Display">3</text>
   <rect x="149" y="48" width="44" height="22" fill="#fff" stroke="#000" stroke-width="1.6"/><text x="171" y="43" text-anchor="middle" font-size="8" font-weight="900">INDIA</text><text x="171" y="65" text-anchor="middle" font-size="14" font-weight="900" font-family="Inter Display">4</text>
   <line x1="0" y1="70" x2="200" y2="70" stroke="#000"/><text x="171" y="78" text-anchor="middle" font-size="5.5">USD 4.18 tn · 3rd by 2030?</text><text x="2" y="78" font-size="5.5">Japan pushed to 5th</text></svg>''',
 'core': hbar('Weight in the core index (%)', [('Refinery products', 28.04, '28.04'), ('Electricity', 19.85, '19.85'), ('Steel', 17.92, '17.92'), ('Coal', 10.33, '10.33'),
          ('Crude oil', 8.98, '8.98'), ('Natural gas', 6.88, '6.88'), ('Cement', 5.37, '5.37'), ('Fertilizers', 2.63, '2.63')], 28.04),
 'gas': '''<p class="chartlab">Who gets gas first (Essential Commodities Act rationing)</p><table class="score"><thead><tr><th>Priority</th><th>Users</th><th>Supply</th></tr></thead><tbody>
   <tr><td class="big">Tier 1</td><td>Domestic PNG, CNG, LPG production</td><td class="big">100%</td></tr>
   <tr><td class="big">Tier 2</td><td>Fertiliser</td><td class="big">70%</td></tr>
   <tr><td class="big">Tier 3 + 4</td><td>Industry / CGD</td><td class="big">80%</td></tr></tbody></table>''',
 'nmp': hbar('NMP 2.0 targets by sector (₹ lakh crore)', [('Highways, logistics parks, ropeways', 4.42, '4.42 (26%)'), ('Power', 2.76, '2.76'), ('Railways', 2.62, '≈2.62'), ('Ports', 2.62, '≈2.62')], 4.42),
 'eu': steps('India–EU: the long road', [('2004', 'Strategic partners'), ('2007', 'Talks launched'), ('2022', 'Talks relaunched'), ('26 Jan 2026', 'Deal concluded'), ('27 Jan 2026', '16th India–EU Summit')]),
 'itact': hbar('Income-tax Act 2025 vs the 1961 Act', [('Sections: 819 → 536', 819, '819'), ('', 536, '536 new'), ('Chapters: 47 → 23 (scaled ×10)', 470, '47'), ('', 230, '23 new')], 819),
 'savings': hbar('Small savings rates, Jan–Mar 2026 (%)', [('Sukanya Samriddhi', 8.2, '8.2'), ('National Savings Certificate', 7.7, '7.7'), ('Kisan Vikas Patra', 7.5, '7.5'),
            ('PPF', 7.1, '7.1'), ('3-year term deposit', 7.1, '7.1'), ('Post office savings deposit', 4, '4')], 8.2),
 'fdi': steps('Foreign ownership limits in insurance', [('74%', 'Insurers, earlier'), ('100%', 'Intermediaries, since 2020'), ('20%', 'LIC, since 2022'), ('100%', 'Insurers, Feb 2026')]),
 'lives': hbar('Who is covered (share of lives, %)', [('Group policies', 47.4, '47.4'), ('Government schemes', 42.3, '42.3'), ('Individual policies', 10.3, '10.3')], 47.4),
 'ladder': hbar("India's growth forecast: the ladder (%)", [('IMF · FY25-26', 7.3, '7.3'), ('World Bank · FY25-26', 7.2, '7.2'), ('Economic Survey · FY27', 7.2, '6.8–7.2'),
            ('UN DESA · 2026-27', 6.6, '6.6'), ('World Bank · FY26-27', 6.5, '6.5'), ('IMF · FY26-27', 6.4, '6.4')], 7.3),
}

DASH = '''<p class="chartlab">The quarter's dashboard</p><table class="score dash"><thead><tr><th>Indicator</th><th>Dec 2025</th><th>Jan 2026</th><th>Feb 2026</th><th>Trend</th></tr></thead><tbody>
<tr><td>CPI inflation</td><td>1.33%<small> old base</small></td><td>2.75%<small> new base</small></td><td>3.21%</td><td>▲ rising</td></tr>
<tr><td>WPI inflation</td><td>0.83%</td><td>1.81%</td><td>2.13%</td><td>▲ rising</td></tr>
<tr><td>IIP (factory output)</td><td>7.8%<small> 26-month high</small></td><td>4.8%</td><td>5.2%</td><td>▼ then ▲</td></tr>
<tr><td>Eight core industries</td><td>+3.7%</td><td>+4%</td><td>+2.3%</td><td>▼ slowing</td></tr>
<tr><td>Manufacturing PMI (HSBC)</td><td>55.0<small> 38-month low</small></td><td>55.4</td><td>56.9</td><td>▲ recovering</td></tr>
<tr><td>Gross GST (₹ lakh crore)</td><td>1.74</td><td>1.93</td><td>~1.83</td><td>steady</td></tr>
<tr><td>UPI transactions</td><td>21.63 bn</td><td>21.70 bn</td><td>–</td><td></td></tr>
</tbody></table>'''

# ---------------- render ----------------
used, problems = [], []
def check(where, text):
    bad = nums_in(text) - SRC_NUMS - WHITELIST
    if bad: problems.append(f'{where}: {sorted(bad)}')

def fact_file(ids):
    lis = []
    for i in ids:
        c = cards[i]; lis += [f'<li>{b}</li>' for b in c['bul']]
    tabs = ''.join(t.replace('<table', '<table class="score ff"') for i in ids for t in cards[i]['tables'])
    return f'<div class="ff"><b>Fact file</b><ul>{"".join(lis)}</ul>{tabs}</div>'

out = []
for n, ch in enumerate(CHAPTERS, 1):
    check(f'ch{n} intro', ch['title'] + ch['intro'])
    o = [f'<div class="chapter{" first" if n == 1 else ""}"><div class="k">Chapter 1.{n}</div><h1>{html.escape(ch["title"])}</h1><p>{html.escape(ch["intro"])}</p></div>']
    if 'bigidea' in ch:
        lab, rows = ch['bigidea']
        cells = ''.join(f'<div><span>{a}</span><b>{b}</b><span>{c}</span></div>' for a, b, c in rows)
        check(f'ch{n} bigidea', ' '.join(' '.join(r) for r in rows))
        o.append(f'<div class="bigidea"><div class="lab"><span>{lab}</span></div><div class="rows">{cells}</div></div>')
    if ch.get('dashboard'):
        check('dash', DASH); o.append(DASH)
    for st in ch['stories']:
        used += st['ids']
        txt = ' '.join([st['h'], st['lede'], st.get('hook', ''), st.get('trap', '')] + [' '.join(x) for x in st.get('nums', [])])
        check(st['ids'][0], txt)
        must = any(cards[i]['must'] for i in st['ids'])
        nums = ''
        if st.get('nums'):
            nums = '<div class="nums">' + ''.join(f'<div><b>{html.escape(v)}</b><span>{html.escape(l)}</span></div>' for v, l in st['nums']) + '</div>'
        chart = CHARTS.get(st.get('chart'), '')
        if st.get('chart'): check(st['ids'][0] + ' chart', chart)
        boxes = ''
        if st.get('hook'): boxes += f'<div class="hook"><b>Remember it like this</b>{html.escape(st["hook"])}</div>'
        if st.get('trap'): boxes += f'<div class="trap"><b>Trap</b>{html.escape(st["trap"])}</div>'
        o.append(f'''<div class="story"><div class="tag"><span class="st">{"★" if must else "☆"}</span>{html.escape(st["tag"])}</div>
<h2>{html.escape(st["h"])}</h2><div class="official">{html.escape(" · ".join(cards[i]["title"] for i in st["ids"]))}</div>
<p class="lede">{html.escape(st["lede"])}</p>{nums}{chart}<div class="duo">{boxes}</div>{fact_file(st["ids"])}</div>''')
    if ch.get('hits'):
        items = []
        for i in ch['hits']:
            used.append(i); c = cards[i]
            items.append(f'<div class="hit"><h4>☆ {html.escape(c["title"])}</h4><ul>{"".join("<li>"+b+"</li>" for b in c["bul"])}</ul></div>')
        o.append(f'<div class="qh"><h3>Quick hits · good to know</h3><div class="hits">{"".join(items)}</div></div>')
    out.append('\n'.join(o))

missing = set(cards) - set(used); dup = {u for u in used if used.count(u) > 1}
print('cards used', len(set(used)), 'missing', sorted(missing), 'dup', sorted(dup))
print('number problems:'); print('\n'.join(problems) or '  none')

CSS = re.search(r'<style>(.*?)</style>', CPI, re.S).group(1)
CSS += r'''
@page { @top-left { content: "01 · ESI, Finance & Business" } }
.chapter { break-before: page; }
.chapter.first { break-before: auto }
.story { break-inside: auto; margin-bottom: 7mm; padding-bottom: 4mm; border-bottom: .6pt solid #999 }
.story h2, .story .official, .story .tag { break-after: avoid }
.nums { break-inside: avoid } .lede { orphans: 3; widows: 3 }
.duo { margin: 2mm 0 0 } .duo:empty { display: none }
.chartlab { margin-top: 2mm }
.tl { display:flex; margin: 3mm 0 2mm; font-family: Inter }
.tl .step { flex:1; border-top: 2pt solid #000; position:relative; padding: 2.5mm 2mm 0 0 }
.tl .step:before { content:""; position:absolute; top:-2.3mm; left:0; width: 3.4mm; height:3.4mm; border-radius:50%; background:#fff; border:1.5pt solid #000 }
.tl .step.on:before { background:#000 }
.tl .v { font: 900 12pt/1.1 'Inter Display' } .tl .d { font: 600 6.8pt/1.3 Inter; letter-spacing:.06em; text-transform:uppercase; color:#444; margin-top:.8mm }
table.score { width:100%; border-collapse: collapse; font: 8.2pt Inter; margin: 1mm 0 2mm }
table.score th { font: 700 6.6pt Inter; letter-spacing:.14em; text-transform:uppercase; text-align:left; border-bottom:1.2pt solid #000; padding: 1.2mm 1.5mm }
table.score td { padding: 1.1mm 1.5mm; border-bottom: .5pt solid #999; vertical-align: top }
table.score tr:nth-child(even) td { background:#eee }
table.score td.big { font: 900 11pt 'Inter Display' }
table.dash td { font: 800 9pt Inter } table.dash td:first-child { font-weight: 600 } table.dash small { font: 500 6.4pt Inter; color:#555; display:block }
table.dash { margin-bottom: 6mm }
.ff { margin-top: 3mm; padding: 2mm 3mm 1mm; background: #f2f2f2; font: 7.9pt/1.42 Inter; color:#222 }
.ff > b { font: 800 6.6pt Inter; letter-spacing: .22em; text-transform: uppercase; display:block; margin-bottom: 1mm }
.ff ul { margin: 0; padding-left: 3.5mm; columns: 2; column-gap: 6mm } .ff li { margin-bottom: .9mm; break-inside: avoid }
.ff table.ff { font-size: 7.4pt; margin-top: 1.5mm }
.qh { margin-top: 2mm; break-before: auto }
.hits { columns: 2; column-gap: 7mm; column-rule: .5pt solid #bbb }
.hit { break-inside: auto; margin-bottom: 3mm }
.hit h4 { font: 800 9pt/1.25 'Inter Display'; margin: 0 0 1mm; break-after: avoid }
.hit ul { columns: 1 !important; list-style: disc; margin: 0; padding-left: 3.5mm; font: 8.3pt/1.4 Lora } .hit li { margin-bottom: .8mm; break-inside: avoid }
.opener { position: relative; height: 66mm; border-bottom: 3pt solid #000; margin-bottom: 6mm }
.opener svg { position:absolute; right:-3mm; top:2mm }
.opener .kk { font: 700 8pt Inter; letter-spacing:.3em; text-transform:uppercase; margin-top: 4mm } .opener .kk span { background:#000; color:#fff; padding: 1mm 2.5mm }
.opener h1 { font: 900 34pt/0.98 'Inter Display'; margin: 5mm 0 3mm; width: 105mm; letter-spacing:-.02em }
.opener p { font: italic 11pt/1.4 Lora; width: 100mm; color:#333 }
.howto { border: 1.2pt solid #000; padding: 3mm 4mm; margin-bottom: 4mm; font: 9pt/1.45 Inter }
.howto b { font-weight: 800 }
'''
opener = '''<div class="opener"><svg width="78mm" height="62mm" viewBox="0 0 300 240"><defs><pattern id="d1" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".9" fill="#000"/></pattern></defs><text x="300" y="200" text-anchor="end" font-family="Inter Display" font-weight="900" font-size="250" letter-spacing="-10" fill="url(#d1)" stroke="#000" stroke-width="2.5">01</text></svg>
<div class="kk"><span>Section One</span></div><h1>ESI, Finance &amp; Business</h1><p>Nine chapters: how India measures its economy, how fast it grew, the monthly numbers, the war shock, the Budget, trade and tax, credit schemes, banking and insurance.</p></div>
<div class="howto"><b>How to read each story.</b> Read the headline and the paragraph first: that is the story. The big numbers strip is what to memorise. "Remember it like this" gives a hook; "Trap" is the confusion examiners test. The grey fact file underneath keeps every exact figure from the notes, for your second and third reading.</div>'''
doc = f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Section 1 · story edition</title><style>{CSS}</style></head><body>{opener}{"".join(out)}</body></html>'
open('CA_Q1_S1_story.html', 'w').write(doc)
if problems or missing: sys.exit(1)
