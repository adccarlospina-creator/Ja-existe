"""Recolhe manchetes de feeds RSS para revisão editorial, sem as publicar."""
import json, re, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from html import unescape

FEEDS = [
    ('Engadget', 'https://www.engadget.com/rss.xml'),
    ('The Verge', 'https://www.theverge.com/rss/index.xml'),
    ('TechCrunch', 'https://techcrunch.com/feed/'),
]
KEYWORDS = re.compile(r'launch|release|unveil|announce|available|new |robot|gadget|device|smart|glasses|phone|wearable|drone|ai |lanc|novo|inven', re.I)
NS={'a':'http://www.w3.org/2005/Atom'}

def txt(node, tag):
    e=node.find(tag,NS)
    return (''.join(e.itertext()).strip() if e is not None else '')

def get_items(data):
    root=ET.fromstring(data)
    for node in root.findall('.//item'):
        yield txt(node,'title'), txt(node,'link'), txt(node,'pubDate')
    for node in root.findall('.//a:entry',NS):
        link=node.find('a:link',NS)
        yield txt(node,'a:title'), (link.get('href','') if link is not None else ''), txt(node,'a:updated')

out=[]; seen=set(); errors=[]
for name,url in FEEDS:
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'JaExisteEditorialBot/1.0 (RSS reader)'})
        with urllib.request.urlopen(req,timeout=18) as resp:
            data=resp.read(1_500_000)
        for title,link,date in get_items(data):
            title=unescape(re.sub(r'<[^>]+>','',title)).strip()
            if not title or not link.startswith('https://') or link in seen or not KEYWORDS.search(title):continue
            seen.add(link)
            out.append({'titulo_original':title,'fonte':name,'url':link,'data_original':date,'estado':'POR VERIFICAR'})
    except Exception as exc:
        errors.append(f'{name}: {type(exc).__name__}: {exc}')

result={'recolhido_em_utc':datetime.now(timezone.utc).isoformat(),'nota':'Sugestões automáticas, não verificadas. Não publicar sem confirmar que o produto foi lançado.','sugestoes':out[:45],'erros':errors}
Path(__file__).with_name('sugestoes.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'{len(result["sugestoes"])} sugestões, {len(errors)} fontes com erro')
