#!/usr/bin/env python3
"""Repository-owned profile visuals. Standard library only; no paid services."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json, math, os, urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
C = '#39C8FF'; V = '#A78BFA'; G = '#3DE0B2'; W = '#EDF5FF'; M = '#94A6BC'
FONT = 'DejaVu Sans,Arial,sans-serif'
MONO = 'DejaVu Sans Mono,monospace'

def text(x,y,t,size=16,color=W,weight='400',mono=False,anchor='start',spacing=0):
    return f'<text x="{x}" y="{y}" font-family="{MONO if mono else FONT}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}" letter-spacing="{spacing}">{escape(str(t))}</text>'

def rect(x,y,w,h,fill='#0F1826',stroke='#233246',r=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'

def line(x1,y1,x2,y2,c='#263F55',width=1,dash=''):
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{c}" stroke-width="{width}" stroke-dasharray="{dash}"/>'

def circle(x,y,r,c,opacity=1,stroke='none'):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{opacity}" stroke="{stroke}"/>'

def start(w,h,label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label,quote=True)}">
    <title>{escape(label)}</title>
    <defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#08121D"/><stop offset=".58" stop-color="#0A101B"/><stop offset="1" stop-color="#151029"/></linearGradient>
    <linearGradient id="accent"><stop stop-color="{C}"/><stop offset=".5" stop-color="{V}"/><stop offset="1" stop-color="{G}"/></linearGradient>
    <radialGradient id="core"><stop stop-color="#A8E7FF"/><stop offset=".25" stop-color="#39C8FF"/><stop offset=".62" stop-color="#634ED0"/><stop offset="1" stop-color="#12192A" stop-opacity="0"/></radialGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#1A293C" stroke-width=".55"/></pattern></defs>
    {rect(1,1,w-2,h-2,'url(#bg)','#253247',22)}
    <rect x="2" y="2" width="{w-4}" height="{h-4}" rx="22" fill="url(#grid)" opacity=".42"/>'''

def save(name,w,h,s,label):
    (ASSETS/name).write_text(start(w,h,label)+s+'</svg>',encoding='utf-8')

def hero(phase=0):
    s=text(48,48,'VAIBHAV / ENGINEERING CONTROL ROOM',13,C,'700',True,spacing=2)
    s+=rect(920,25,308,36,'#0D2625','#215247',18)+circle(940,43,4,G)+text(956,48,'OPEN TO MY FIRST FULL-TIME ROLE',11,G,'700',True)
    s+=text(48,134,'VAIBHAV',65,W,'700')+text(48,208,'SHARMA',65,W,'700')
    s+=text(52,254,'APPLIED AI  /  FULL-STACK ENGINEER',17,C,'700',True)
    s+=text(52,296,'Intelligent systems. Visible execution.',21,W)+text(52,328,'Human control.',21,W)
    s+=text(52,373,'2026 CS GRADUATE  ·  MMMUT  ·  MUMBAI, INDIA',12,M,'400',True)
    s+=rect(50,402,515,38,'#0D1927','#294459',8)+text(67,427,'> ship()  →  evaluate()  →  harden()  ↻',14,G,'400',True)
    cx,cy=929,261
    s+=circle(cx,cy,158,'url(#core)',.45)
    for rad in [66,104,143,178]:
        s+=f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="{C if rad%2 else V}" stroke-opacity=".23" stroke-dasharray="{10 if rad==143 else 3} {8 if rad==143 else 12}"/>'
    for angle in range(0,360,30):
        a=math.radians(angle)
        s+=line(cx+182*math.cos(a),cy+182*math.sin(a),cx+189*math.cos(a),cy+189*math.sin(a),'#33516B')
    for j in range(-3,4):
        s+=f'<ellipse cx="{cx}" cy="{cy}" rx="{110*math.sqrt(1-(j/4)**2):.2f}" ry="22" transform="translate(0 {j*26})" fill="none" stroke="{C}" opacity=".16"/>'
    for ang in [0,45,90,135]:
        s+=f'<ellipse cx="{cx}" cy="{cy}" rx="55" ry="110" transform="rotate({ang} {cx} {cy})" fill="none" stroke="{V}" opacity=".16"/>'
    s+=circle(cx,cy,61,'url(#core)')
    nodes=[('AI LOOPS',-120,C),('INCIDENT OPS',-25,G),('DEV TOOLS',53,V),('SECURITY',143,C),('EDGE APPS',212,G)]
    for i,(label,deg,col) in enumerate(nodes):
        a=math.radians(deg);x=cx+151*math.cos(a);y=cy+151*math.sin(a)
        s+=line(cx,cy,x,y,col,.8)
        pulse=.4+.35*math.sin(phase*2*math.pi+i)
        s+=circle(x,y,17,col,pulse*.2)+circle(x,y,8,'#0B1B2B',1,col)+circle(x,y,3,col)
        lx=x+18 if x>cx else x-18;anchor='start' if x>cx else 'end'
        s+=text(lx,y+4,label,11,col,'700',True,anchor)
    for i,col in enumerate([C,V,G]):
        a=phase*2*math.pi+i*2.1;r=104+i*18
        x=cx+r*math.cos(a);y=cy+r*math.sin(a)
        s+=circle(x,y,11,col,.1)+circle(x,y,3.5,col)
    s+=circle(cx,cy,34,'#0B1728',.95,'#5179B5')+text(cx,cy+6,'VS',22,W,'700',True,'middle')
    s+=line(48,466,1232,466,'#253348')+text(49,491,'OBSERVE THE LOOP.  REVIEW THE ACTION.  OWN THE OUTCOME.',11,M,'400',True,spacing=1)
    return start(1280,514,'Vaibhav Sharma — Applied AI and Full-Stack Engineer; engineering control room')+s+'</svg>'

PROJECTS=[
    dict(id='runbookos',name='RunbookOS',category='INCIDENT RESPONSE / JAVA SYSTEMS',color=G,headline='AI recommends. Humans approve.',desc=['Evidence-grounded triage, deterministic policy,','reviewed runbooks, and complete incident replay.'],tech='Java 21 · Spring Boot · Next.js · n8n',proof='Policy engine  /  RBAC  /  signed workflows',motif='ops'),
    dict(id='loopos',name='LoopOS',category='APPLIED AI / OBSERVABILITY',color=C,headline='Watch the loop. Measure the outcome.',desc=['Generator–evaluator execution with live scores,','cost telemetry, anomaly signals, and budgets.'],tech='React · Hono · Durable Objects · D1',proof='Stateful execution  /  WebSocket telemetry',motif='loop'),
    dict(id='llmguard',name='LLMGuard Lab',category='AI SECURITY / DEFENSIVE TESTING',color=V,headline='Evidence over security theater.',desc=['Bounded endpoint checks, SSRF protections,','OWASP-mapped findings, and redacted reports.'],tech='Next.js · TypeScript · Zod · Supabase',proof='Static tests  /  deterministic heuristics',motif='security'),
    dict(id='codeshift',name='CodeShift AI',category='DEVELOPER TOOLS / CODE MIGRATION',color='#FFBF69',headline='Analyze. Scope. Validate. Review.',desc=['JavaScript → TypeScript migration workflows','with conservative refactors and approved PRs.'],tech='TypeScript · Node.js · CLI · GitHub API',proof='Scoped transformations  /  review-first changes',motif='code'),
    dict(id='gitblamed',name='GitBlamed',category='SOCIAL PRODUCT / EDGE ENGINEERING',color='#F792C9',headline='Serious resilience. Unserious output.',desc=['GitHub activity roasts and shareable cards,','with edge caching and AI-provider fallback.'],tech='React 19 · Hono · Workers · KV',proof='3-provider cascade  /  24-hour edge cache',motif='social'),
    dict(id='matchengine',name='MatchEngine',category='C++ SYSTEMS / EXCHANGE ENGINEERING',color='#9CE56B',headline='Every order. A deterministic outcome.',desc=['Price-time matching, self-trade prevention,','indexed cancellation, and market-data parsing.'],tech='C++17 · CMake · Catch2 · Python bindings',proof='Limit order book  /  ITCH 5.0 parser',motif='exchange'),
]

def project(p,i):
    c=p['color'];s=text(28,39,f'0{i+1}  /  '+p['category'],11,c,'700',True,spacing=.7)
    s+=rect(28,60,564,148,'#0A1320','#1D3046',12)
    if p['motif']=='ops':
        stages=[('SIGNAL',70),('EVIDENCE',205),('POLICY',350),('APPROVAL',492)]
        for j,(label,x) in enumerate(stages):
            if j:s+=line(stages[j-1][1]+20,113,x-20,113,c,2)
            s+=circle(x,113,19,'#13262C',1,c)+text(x,119,['!','≡','✓','◎'][j],20,c,'700',False,'middle')+text(x,158,label,10,M,'400',True,'middle')
        s+=text(310,191,'AI recommends · Java authorizes · n8n orchestrates',10,c,'400',True,'middle')
    elif p['motif']=='loop':
        s+=rect(52,91,134,49,'#122235','#325674',9)+text(119,120,'GENERATOR',12,C,'700',True,'middle')
        s+=rect(256,91,130,49,'#1D1934','#534B81',9)+text(321,120,'EVALUATOR',12,V,'700',True,'middle')
        s+=line(186,116,256,116,C,2)+f'<path d="M320 140V168H119V140" stroke="{G}" fill="none" stroke-width="2"/>'
        s+=text(217,190,'feedback',10,G,'400',True,'middle')
        s+=text(493,90,'SCORE / ITERATION',9,M,'400',True,'middle')
        s+='<polyline points="427,161 452,147 477,153 502,121 527,115 561,93" fill="none" stroke="'+C+'" stroke-width="3"/>'
        for k,v in enumerate([40,53,49,77,85]):s+=rect(433+k*24,181-v/2,13,v/2,'#234965','none',2)
    elif p['motif']=='security':
        s+=f'<path d="M127 83L175 103V140Q175 167 127 188Q79 167 79 140V103Z" fill="#24203B" stroke="{c}" stroke-width="2"/>'
        s+=text(127,144,'✓',37,c,'700',False,'middle')
        for j,label in enumerate(['PROMPT INJECTION','LEAKAGE SIGNALS','UNSAFE OUTPUT']):
            s+=circle(244,96+j*36,4,c)+text(260,101+j*36,label,10,M,'400',True)
            s+=rect(435,88+j*36,119,19,'#201D36','#3D345D',4)+text(449,102+j*36,'[REDACTED]',10,c,'400',True)
    elif p['motif']=='code':
        s+=rect(48,80,221,106,'#111A26','#263A50',8)+text(65,102,'legacy.js',11,M,'400',True)
        s+=text(65,129,'function migrate(repo) {',11,'#FFBF69','400',True)+text(65,150,'  return plan(repo);',11,W,'400',True)+text(65,172,'}',11,'#FFBF69','400',True)
        s+=text(308,143,'→',25,c,'700',False,'middle')
        s+=rect(347,80,224,106,'#111A26','#3C484C',8)+text(364,102,'reviewed.ts',11,G,'400',True)
        s+=text(364,129,'plan: MigrationPlan',11,C,'400',True)+text(364,151,'scope: explicit',11,W,'400',True)+text(364,174,'approval: required',11,G,'400',True)
    elif p['motif']=='social':
        colors=['#142238','#25374C','#33556C','#60508A','#B16C9B']
        for col in range(15):
            for row in range(4):
                s+=rect(49+col*17,81+row*24,12,16,colors[(col*row+col+row)%5],'none',2)
        s+=rect(334,80,230,107,'#1C182A','#4A2F47',8)+text(352,103,'> analyze(github)',11,c,'400',True)
        s+=text(352,132,'3 providers. 1 roast.',13,W,'700')+text(352,157,'Fallback included.',12,M)
        s+=text(49,196,'CONTRIBUTIONS → AI ROAST → SHARE CARD',9,c,'400',True)
    elif p['motif']=='exchange':
        s+=text(62,89,'BID QUEUE',10,G,'700',True)+text(405,89,'ASK QUEUE',10,'#F792C9','700',True)
        for j,v in enumerate([154,112,179]):
            s+=rect(50,102+j*26,v,17,'#173F38','none',3)
            s+=rect(405,102+j*26,150-j*24,17,'#442239','none',3)
        s+=rect(253,107,111,62,'#1B2A24','#4D785B',9)+text(309,132,'PRICE / TIME',10,c,'700',True,'middle')+text(309,153,'MATCH',15,W,'700',True,'middle')
        s+=line(215,137,253,137,G,2)+line(364,137,401,137,'#F792C9',2)
        s+=text(310,194,'FIFO priority · indexed cancel · retained status',10,M,'400',True,'middle')
    s+=text(28,250,p['name'],31,W,'700')+text(28,280,p['headline'],16,c,'700')
    for j,t in enumerate(p['desc']):s+=text(28,312+j*23,t,14,M)
    s+=line(28,354,592,354,'#263447')+text(28,383,p['tech'],11,W,'400',True)
    s+=text(28,409,p['proof'],10,M,'400',True)+text(592,408,'EXPLORE ↗',10,c,'700',True,'end')
    save(p['id']+'.svg',620,438,s,p['name']+' — '+p['headline']+' '+ ' '.join(p['desc']))

def get(url):
    headers={'Accept':'application/vnd.github+json','User-Agent':'vaibhav-profile-observatory'}
    if os.environ.get('GH_TOKEN'):headers['Authorization']='Bearer '+os.environ['GH_TOKEN']
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30) as r:return json.load(r)

def observatory(user=None,repos=None):
    if user is None:
        user=get('https://api.github.com/users/vaibhav7506');repos=[];page=1
        while True:
            batch=get(f'https://api.github.com/users/vaibhav7506/repos?per_page=100&page={page}')
            repos.extend(batch)
            if len(batch)<100:break
            page+=1
    owned=[r for r in repos if not r['fork']]
    languages=Counter(r['language'] for r in owned if r.get('language'))
    s=text(42,47,'PUBLIC REPOSITORY SIGNAL / GITHUB API',12,C,'700',True,spacing=1.5)
    s+=text(42,91,'Engineering observatory',31,W,'700')
    s+=text(42,119,'A dated snapshot of public work. Language bars count repositories, not code volume.',13,M)
    s+=rect(975,37,261,33,'#0F2428','#284A4C',16)+circle(994,54,4,G)+text(1009,59,'API SNAPSHOT · PUBLIC DATA',11,G,'400',True)
    metrics=[('PUBLIC REPOS',user['public_repos']),('REPO STARS',sum(r['stargazers_count'] for r in repos)),('FOLLOWERS',user['followers']),('ORIGINAL REPOS',len(owned))]
    for i,(label,value) in enumerate(metrics):
        x=42+(i%2)*222;y=154+(i//2)*120
        s+=rect(x,y,204,102,'#0D1929','#273B53',13)+text(x+19,y+29,label,10,M,'400',True,spacing=1)+text(x+19,y+77,value,37,W,'700')
    s+=rect(508,154,293,222,'#0D1522','#26334B',14)
    cx,cy=654,256
    for r in [42,66,89]:s+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#36466C" stroke-dasharray="5 8"/>'
    s+=circle(cx,cy,53,'url(#core)')+text(cx,cy+5,'BUILD',14,W,'700',True,'middle')
    for i,col in enumerate([C,V,G]):
        a=i*2.1-1.2;x=cx+89*math.cos(a);y=cy+89*math.sin(a);s+=circle(x,y,5,col)
    s+=text(cx,361,'AI / SYSTEMS / PRODUCTS',10,M,'400',True,'middle')
    s+=rect(829,154,407,222,'#0D1522','#26334B',14)+text(854,183,'PRIMARY LANGUAGE / ORIGINAL REPOS',10,C,'700',True)
    total=sum(languages.values()) or 1
    for i,(name,n) in enumerate(languages.most_common(4)):
        y=211+i*43;percent=n/total*100
        s+=text(854,y,name,13,W)+text(1210,y,f'{n} repos · {percent:.0f}%',11,M,'400',True,'end')
        s+=rect(854,y+8,354,6,'#1A283B','none',3)+rect(854,y+8,354*n/total,6,'url(#accent)','none',3)
    s+=line(42,411,1236,411,'#27384F')
    s+=text(42,443,'VERIFIABLE WORK  /  RUNBOOKOS · LOOPOS · LL MGUARD · CODESHIFT'.replace('LL M','LLM'),11,M,'400',True)
    stamp=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    s+=text(1236,474,'UPDATED '+stamp,10,M,'400',True,'end')
    save('observatory.svg',1280,496,s,'GitHub observatory — dated public repository metrics and primary-language distribution')

def blueprint():
    s=text(40,43,'ONE ENGINEERING PHILOSOPHY. DIFFERENT SYSTEMS.',12,C,'700',True,spacing=1.5)
    rows=[('LOOPOS','MEASURE THE LOOP',['Goal + rubric','Generator','Evaluator','Telemetry'],C),('RUNBOOKOS','GOVERN THE ACTION',['Incident','Evidence','Policy','Human approval'],G),('CODESHIFT','REVIEW THE CHANGE',['Repository','Scoped plan','Validation','Reviewed PR'],V)]
    for j,(name,desc,labels,c) in enumerate(rows):
        y=89+j*106;s+=text(40,y+24,name,17,c,'700')+text(40,y+48,desc,9,M,'400',True)
        for i,label in enumerate(labels):
            x=320+i*232
            if i:s+=line(x-30,y+24,x-7,y+24,c,2)+text(x-12,y+28,'›',18,c)
            s+=rect(x,y,200,51,'#0E1B2A','#2B4257',8)+circle(x+18,y+26,3,c)+text(x+34,y+31,label,12,W)
    s+=text(40,429,'Explicit boundaries · Observable state · Recoverable failure · Human ownership',13,M)
    save('blueprint.svg',1280,460,s,'Architecture patterns: measured AI loops, governed incident actions, and reviewed code migrations')

def main():
    (ASSETS/'hero.svg').write_text(hero())
    for i,p in enumerate(PROJECTS):project(p,i)
    blueprint()
    # Local snapshots let the supplied package be rebuilt without another API call.
    local=os.environ.get('PROFILE_SNAPSHOT_DIR')
    if local:
        observatory(json.loads(Path(local,'profile-user.json').read_text()),json.loads(Path(local,'profile-repos.json').read_text()))
    else:observatory()
    print('Generated hero, six project cards, blueprint, and GitHub observatory.')

if __name__=='__main__':main()
