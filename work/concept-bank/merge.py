#!/usr/bin/env python3
"""Auditor tool: merge approved batches into sources/current-affairs/Static_Bank.html.
Usage: merge.py 03 04 05   (run from repo root). NEW cards go to the end of their section;
EXTEND/EXISTS cards keep all old content and gain the new blocks (only missing fact bullets)."""
import re, csv, sys, html as H
CB='work/concept-bank/'; SB='sources/current-affairs/Static_Bank.html'
s=open(SB,encoding='utf-8').read(); before=s
C={r['concept_id']:r for r in csv.DictReader(open(CB+'out/concepts.csv',encoding='utf-8'))}
def block_end(x,start):
    d=0
    for m in re.finditer(r'<details\b|</details>',x[start:]):
        d+=1 if m.group(0).startswith('<details') else -1
        if d==0: return start+m.end()
def T(x): return re.sub(r'\s+',' ',H.unescape(re.sub(r'<[^>]+>',' ',x))).strip()
def N(x): return re.sub(r'[\s;,.:()\-–—|]+',' ',T(x)).lower().strip()
def blocks(card):
    o={}
    for lab in ('Why it exists','How it works','Fixed facts','How it changed','Traps','In the news'):
        k=f'<p><strong>{lab}</strong></p>'
        if k in card: o[lab]=re.sub(r'(\s*</div>)*\s*$','',card.split(k)[1].split('<p><strong>')[0].split('</details>')[0])
    return o
st={'extended':0,'added':0,'skipped_dup':[]}
for nn in sys.argv[1:]:
    b=open(CB+f'out/batch-{nn}.html',encoding='utf-8').read()
    cards=[(m.group(1),b[m.start():block_end(b,m.start())]) for m in re.finditer(r'<details class="card(?: opt)?" open id="(c-[a-z0-9-]+)">',b)]
    fixed=[]
    for cid,card in cards:
        d=card.count('<div')-card.count('</div>')
        if d>0: card=card[:card.rfind('</details>')].rstrip()+'</div>'*d+'</details>'
        fixed.append((cid,card))
    cards=fixed
    revsec={}
    for cid,card in cards:
        if f'id="{cid}"' in s: st['skipped_dup'].append(cid); continue
        r=C[cid]; done=False
        if r['status'] in ('EXTEND','EXISTS') and r['static_match']:
            for m in re.finditer(r'<details class="card[^"]*"[^>]*>(?:\s*<!--[^>]*-->)?\s*<summary>(.*?)</summary>',s,re.S):
                if T(m.group(1)).lstrip('★☆ ').strip()==r['static_match'].strip():
                    e=block_end(s,m.start()); old=s[m.start():e]; on=N(old); bl=blocks(card); add=''
                    for lab in ('Why it exists','How it works'):
                        if lab in bl: add+=f'<p><strong>{lab}</strong></p>{bl[lab]}'
                    for lab,newlab in (('Fixed facts','More fixed facts'),('How it changed','How it changed')):
                        if lab in bl:
                            lis=[li for li in re.findall(r'<li>.*?</li>',bl[lab],re.S) if N(li) not in on]
                            if lis: add+=f'<p><strong>{newlab}</strong></p><ul>'+''.join(lis)+'</ul>'
                    for lab in ('Traps','In the news'):
                        if lab in bl: add+=f'<p><strong>{lab}</strong></p>{bl[lab]}'
                    cut=old.rfind('</div></details>')
                    newold=(old[:cut]+'\n'+add+'\n'+old[cut:]).replace('<details class="card',f'<details id="{cid}" class="card',1)
                    s=s[:m.start()]+newold+s[e:]
                    k=s.rfind('<!-- SECTION-',0,m.start()); revsec[cid]=re.match(r'<!-- SECTION-(\d+)',s[k:]).group(1)
                    st['extended']+=1; done=True; break
        if not done:
            sec=re.match(r'(\d+)\.',r['static_section']); secn=sec.group(1) if sec else '4'
            if not 1<=int(secn)<=8: secn='4'
            a=f'<!-- SECTION-{secn} END -->'; s=s.replace(a,card+'\n'+a,1); revsec[cid]=secn; st['added']+=1
    rv=open(CB+f'out/batch-{nn}-revision.html',encoding='utf-8').read()
    for cid,q,a in re.findall(r'<details data-concept="(c-[a-z0-9-]+)"><summary>([^<]+)</summary><div class="ans">(.*?)</div></details>',rv,re.S):
        if cid not in revsec: continue
        i=s.find(f'<h2>10.{revsec[cid]} ',s.find('id="s10"')); j=s.find('</div>',i)
        s=s[:j]+f'<details><summary>{q}</summary><div class="ans">{a}</div></details>\n'+s[j:]
# safety: no number lost from the notes area
on=set(re.findall(r'\d[\d,]*(?:\.\d+)?%?',T(before.split('id="s10"')[0]))); nw=set(re.findall(r'\d[\d,]*(?:\.\d+)?%?',T(s.split('id="s10"')[0])))
lost=on-nw
assert not lost, f'numbers lost: {sorted(lost)[:20]}'
assert s.count('<details')==s.count('</details>')
m=re.search(r'<h2>[^<]*[Cc]hange log[^<]*</h2>\s*<ul>',s)
from datetime import date
s=s[:m.end()]+f'<li>{date.today():%d %b %Y} (auditor): Concept Bank batches {", ".join(sys.argv[1:])} merged: {st["added"]} new cards, {st["extended"]} existing cards extended (no old fact removed).</li>'+s[m.end():]
open(SB,'w',encoding='utf-8').write(s)
print(st, 'cards', len(re.findall(r'<details (?:id="[^"]+" )?class="card',s)), 'rev', s.split('id="s10"')[1].split('<section class="notes"')[0].count('<details>'))
