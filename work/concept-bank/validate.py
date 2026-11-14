#!/usr/bin/env python3
"""Checks Antigravity's Concept Bank output. Usage: validate.py A  |  validate.py B NN"""
import csv, os, re, sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
errors, warns = [], []

def rd(name):
    with open(os.path.join(HERE, name), encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

def rdo(name):
    p = os.path.join(OUT, name)
    if not os.path.exists(p):
        errors.append(f'missing file out/{name}'); return []
    with open(p, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

months = rd('month_cards.csv')
statics = rd('static_cards.csv')
month_keys = {(r['part'], r['title']) for r in months}
must_keys = {(r['part'], r['title']) for r in months if r['priority'] == 'must'}
static_titles = {r['title'] for r in statics}
PARTS = {'nov-2026','oct-2026','sep-2026','may-2026','apr-2026','jan-mar-2026'}

def phase_a():
    cols = ['concept_id','concept_name','static_section','status','static_match','priority','month_refs','learner_must_understand']
    rows = rdo('concepts.csv')
    if rows and list(rows[0].keys()) != cols:
        errors.append(f'concepts.csv columns must be exactly: {",".join(cols)}')
    seen, covered = set(), set()
    for i, r in enumerate(rows, 2):
        cid = r.get('concept_id','')
        if not re.fullmatch(r'c-[a-z0-9]+(-[a-z0-9]+)*', cid): errors.append(f'concepts.csv line {i}: bad concept_id {cid!r}')
        if cid in seen: errors.append(f'concepts.csv line {i}: duplicate concept_id {cid}')
        seen.add(cid)
        st = r.get('status','')
        if st not in ('EXISTS','EXTEND','NEW'): errors.append(f'line {i} {cid}: status must be EXISTS/EXTEND/NEW')
        if st in ('EXISTS','EXTEND') and r.get('static_match','') not in static_titles:
            errors.append(f'line {i} {cid}: static_match not an exact Static Bank title: {r.get("static_match")!r}')
        if st == 'NEW' and r.get('static_match'): errors.append(f'line {i} {cid}: NEW must have empty static_match')
        if r.get('priority') not in ('A','B','C'): errors.append(f'line {i} {cid}: priority must be A/B/C')
        refs = [x.strip() for x in r.get('month_refs','').split(';;') if x.strip()]
        if not refs: errors.append(f'line {i} {cid}: no month_refs')
        for ref in refs:
            if '|' not in ref: errors.append(f'line {i} {cid}: bad ref {ref!r}'); continue
            part, title = ref.split('|', 1)
            key = (part.strip(), title.strip())
            if key not in month_keys: errors.append(f'line {i} {cid}: ref not found in month_cards.csv: {ref!r}')
            covered.add(key)
        if not r.get('learner_must_understand','').strip():
            errors.append(f'line {i} {cid}: empty learner_must_understand')
    unm = rdo('unmapped.csv')
    unm_keys = set()
    for i, r in enumerate(unm, 2):
        key = (r.get('part',''), r.get('title',''))
        if key not in must_keys: errors.append(f'unmapped.csv line {i}: not a must card: {key}')
        if not r.get('reason','').strip(): errors.append(f'unmapped.csv line {i}: reason missing')
        unm_keys.add(key)
    missing = must_keys - covered - unm_keys
    for k in sorted(missing)[:40]: errors.append(f'must card neither mapped nor in unmapped.csv: {k[0]} | {k[1]}')
    if len(missing) > 40: errors.append(f'... and {len(missing)-40} more uncovered must cards')
    sd = rdo('static_dated.csv')
    for i, r in enumerate(sd, 2):
        if r.get('static_card_title','') not in static_titles: errors.append(f'static_dated.csv line {i}: unknown static card title')
        h = r.get('suggested_home','')
        if h not in PARTS and h not in ('drop','keep','hold'): errors.append(f'static_dated.csv line {i}: suggested_home must be a part id, drop, keep or hold')
    print(f'concepts {len(rows)}; must cards covered {len(covered & must_keys)}/{len(must_keys)}; unmapped {len(unm_keys)}; static dated items {len(sd)}')

ALLOWED = ('rbi.org.in','sebi.gov.in','irdai.gov.in','pfrda.org.in','pib.gov.in','indiacode.nic.in','egazette.gov.in',
           'finmin.nic.in','dea.gov.in','financialservices.gov.in','mospi.gov.in','cga.nic.in','gstcouncil.gov.in',
           'ibbi.gov.in','npci.org.in','legislative.gov.in','imf.org','worldbank.org','bis.org','wto.org','un.org',
           'gov.in','nic.in','int','org')
BANNED = ('wikipedia','adda247','gktoday','testbook','jagranjosh','drishti','byjus','affairscloud','oliveboard','smartkeeda','cgb','economictimes','livemint','thehindu','indianexpress','ndtv','moneycontrol','businessstandard','business-standard')

def phase_b(nn):
    concepts = {r['concept_id']: r for r in rdo('concepts.csv')}
    p = os.path.join(OUT, f'batch-{nn}.html')
    if not os.path.exists(p): errors.append(f'missing out/batch-{nn}.html'); return
    html = open(p, encoding='utf-8').read()
    if html.count('<details') != html.count('</details>'): errors.append('details tags unbalanced')
    cards = re.findall(r'<details class="(card(?: opt)?)" open id="(c-[a-z0-9-]+)"><summary>([★☆]) ([^<]+)</summary>(.*?)</details>', html, re.S)
    if len(cards) != html.count('<details'): errors.append('some cards do not match the required opening markup')
    ids = set()
    for cls, cid, star, title, body in cards:
        if cid not in concepts: errors.append(f'{cid}: not in concepts.csv')
        if cid in ids: errors.append(f'{cid}: duplicate card')
        if not body.rstrip().endswith('</div>') or '</div>' in body.rstrip()[:-6].split('<p><strong>Why it exists</strong></p>')[-1].replace('<div class="ans">','').split('<p><strong>In the news</strong></p>')[0][-0:] and False: pass
        _tail = body.split('<p><strong>Why it exists</strong></p>')[-1]
        if _tail.count('</div>') != 1 or not _tail.rstrip().endswith('</div>'): errors.append(f'{cid}: card body must stay open until the end (close </div> only once, right before </details>)')
        ids.add(cid)
        pri = concepts.get(cid, {}).get('priority')
        want_star = pri in ('A','B')
        if (cls == 'card') != want_star or (star == '★') != want_star: errors.append(f'{cid}: star/class does not match priority {pri}')
        has_plain = 'class="plain"' in body
        if want_star and not has_plain: errors.append(f'{cid}: ★ card needs In plain words')
        if not want_star and has_plain: errors.append(f'{cid}: ☆ card must not have In plain words')
        for lab in ('Why it exists','How it works','Fixed facts','In the news'):
            if f'<p><strong>{lab}</strong></p>' not in body: errors.append(f'{cid}: missing block {lab}')
        if re.search(r'<strong>[^<]*\d[^<]*</strong>', body.replace('<strong>In plain words:</strong>','')):
            errors.append(f'{cid}: bold number found')
        for word in ('per source','Agent Notes','verified','updated:','TODO','TBD','lorem'):
            if word.lower() in body.lower(): errors.append(f'{cid}: forbidden text {word!r}')
        refs = [x.strip() for x in concepts.get(cid, {}).get('month_refs','').split(';;') if x.strip()]
        news = body.split('<p><strong>In the news</strong></p>')[-1]
        for ref in refs:
            part, t = ref.split('|', 1)
            if f'href="#{part.strip()}"' not in news or t.strip() not in news:
                warns.append(f'{cid}: In the news may be missing {ref}')
    import html as _h
    def _norm(t):
        t = _h.unescape(re.sub(r'<[^>]+>', ' ', t))
        return re.sub(r'[\s;,.:()\-–—|]+', ' ', t).strip().lower()
    book = open(os.path.join(HERE, '..', '..', 'books', 'current-affairs', 'content.html'), encoding='utf-8').read()
    BOOK = _norm(book)
    LIS = set()
    for li in re.findall(r'<li>(.*?)(?=</li>|<ul>)', book, re.S):
        LIS.add(_norm(li))
        LIS.update(_norm(x) for x in re.split(r'\s;\s', _h.unescape(re.sub(r'<[^>]+>', '', li))) if len(x) > 25)
    for td in re.findall(r'<tr>(.*?)</tr>', book, re.S):
        LIS.add(_norm(td))
    if '<!--' in html: errors.append('HTML comments are not allowed in batch files')
    for cls, cid, star, title, body in cards:
        facts_txt = ''
        for lab in ('Fixed facts','How it changed'):
            if f'<p><strong>{lab}</strong></p>' in body:
                blk = body.split(f'<p><strong>{lab}</strong></p>')[1].split('<p><strong>')[0]
                for li in re.findall(r'<li>(.*?)</li>', blk, re.S):
                    facts_txt += ' ' + li
                    t = re.sub(r'^\s*(\d{1,2} )?([A-Z][a-z]+ )?\d{4}:\s*', '', _h.unescape(re.sub(r'<[^>]+>', '', li)))
                    if _norm(t) not in BOOK:
                        errors.append(f'{cid}: {lab} bullet is not copied word for word from the book: {t[:90]!r}')
                    elif _norm(t) not in LIS:
                        errors.append(f'{cid}: {lab} bullet is a fragment; copy one whole bullet from the book: {t[:90]!r}')
        expl = body.split('<p><strong>Fixed facts</strong></p>')[0] + (body.split('<p><strong>Traps</strong></p>')[1].split('<p><strong>In the news</strong></p>')[0] if '<p><strong>Traps</strong></p>' in body else '')
        allowed = set(re.findall(r'\d+(?:\.\d+)?', _h.unescape(re.sub(r'<[^>]+>', ' ', facts_txt))))
        for n in re.findall(r'\d+(?:\.\d+)?', _h.unescape(re.sub(r'<[^>]+>', ' ', expl))):
            if n not in allowed: errors.append(f'{cid}: number {n} in the explanation blocks is not in the card\'s fact bullets'); break
    src = rdo(f'batch-{nn}-sources.csv') if os.path.exists(os.path.join(OUT, f'batch-{nn}-sources.csv')) else []
    if src and list(src[0].keys()) != ['concept_id','fact','url','quote']:
        errors.append('sources csv columns must be exactly: concept_id,fact,url,quote')
    with_src = set()
    per = {}
    for i, r in enumerate(src, 2):
        u = r.get('url','').strip()
        cid0 = r.get('concept_id'); with_src.add(cid0); per[cid0] = per.get(cid0, 0) + 1
        q = (r.get('quote') or '').strip()
        if u != 'NOT FOUND':
            if not q: errors.append(f'sources line {i}: quote missing (copy the exact words from the page)')
            elif len(q.split()) > 40: errors.append(f'sources line {i}: quote longer than 40 words')
        if u.startswith('month:'):
            ref = u[6:]
            if '|' not in ref or (ref.split('|',1)[0].strip(), ref.split('|',1)[1].strip()) not in month_keys:
                errors.append(f'sources line {i}: month ref not found in month_cards.csv: {ref!r}')
            continue
        if u == 'NOT FOUND': warns.append(f'sources line {i}: NOT FOUND for {r.get("concept_id")}: {r.get("fact","")[:60]}'); continue
        host = urlparse(u).netloc.lower()
        if not host: errors.append(f'sources line {i}: bad url {u!r}'); continue
        if any(b in host for b in BANNED): errors.append(f'sources line {i}: banned source {host}')
        elif not host.endswith(ALLOWED): warns.append(f'sources line {i}: check source {host}')
    for cls, cid, star, title, body in cards:
        need = 0
        for lab in ('Fixed facts','How it changed'):
            if f'<p><strong>{lab}</strong></p>' in body:
                need += body.split(f'<p><strong>{lab}</strong></p>')[1].split('<p><strong>')[0].count('<li>')
        txt = re.sub(r'<[^>]+>', ' ', body)
        for m in re.finditer(r'\b[A-Z][a-z]+(?:[ -][A-Za-z]+){1,6} \(([A-Z]{2,}[a-z]?)\)', txt):
            errors.append(f'{cid}: acronym expanded in the body: {m.group(0)[:60]!r} (write only the acronym)')
    rp = os.path.join(OUT, f'batch-{nn}-revision.html')
    if not os.path.exists(rp): errors.append(f'missing out/batch-{nn}-revision.html')
    else:
        rv = open(rp, encoding='utf-8').read()
        qs = re.findall(r'<details data-concept="(c-[a-z0-9-]+)"><summary>([^<]+)</summary><div class="ans">(.*?)</div></details>', rv, re.S)
        if len(qs) != rv.count('<details'): errors.append('revision: every question must use the exact markup in BRIEF.md')
        have = {q[0] for q in qs}
        for cls, cid, star, title, body in cards:
            if star == '★' and cid not in have: errors.append(f'{cid}: no revision question')
        for cid, q, a in qs:
            body = next((b for c_, i_, s_, t_, b in cards if i_ == cid), '')
            facts = _norm(body)
            for n in re.findall(r'\d+(?:\.\d+)?', _h.unescape(re.sub(r'<[^>]+>', ' ', a))):
                if n not in facts: errors.append(f'{cid}: revision answer number {n} is not in the card'); break
    print(f'batch {nn}: {len(cards)} cards, {len(src)} source rows')

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ('A','B'): sys.exit('usage: validate.py A | validate.py B NN')
    if sys.argv[1] == 'A': phase_a()
    else:
        if len(sys.argv) < 3: sys.exit('usage: validate.py B NN')
        phase_b(sys.argv[2])
    for w in warns: print('WARN ', w)
    for e in errors: print('ERROR', e)
    print('RESULT:', 'PASS' if not errors else f'FAIL ({len(errors)} errors)')
    sys.exit(1 if errors else 0)
