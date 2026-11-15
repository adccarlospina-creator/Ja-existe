"""Recolhe notícias e vídeos públicos para revisão humana. Nunca publica produtos."""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

FEEDS = [
    ("Nuno Agonia (YouTube)", "https://www.youtube.com/feeds/videos.xml?channel_id=UCUDCUqwwlV7NwLBWo3oFMwA"),
    ("Engadget", "https://www.engadget.com/rss.xml"),
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("TechCrunch", "https://techcrunch.com/feed/"),
]
KEYWORDS = re.compile(
    r"gadget|robot|robô|drone|wearable|óculos|glasses|smart|relógio|watch|"
    r"impressora|printer|inven|tecnolog|technology|unboxing|teste|testei|"
    r"lanç|lanc|launch|release|review|device|produto|product|"
    r"futur|novo|nova|new|incrível|insano|surpreend|"
    r"ai\b|inteligência artificial", re.I
)
NS = {"a": "http://www.w3.org/2005/Atom"}

def clean(value):
    return unescape(re.sub(r"<[^>]+>", "", value or "")).strip()

def field(node, tag):
    child = node.find(tag, NS)
    return "".join(child.itertext()).strip() if child is not None else ""

def entries(data):
    root = ET.fromstring(data)
    for node in root.findall(".//item"):
        yield field(node, "title"), field(node, "link"), field(node, "pubDate")
    for node in root.findall(".//a:entry", NS):
        link = node.find("a:link", NS)
        yield field(node, "a:title"), (link.get("href", "") if link is not None else ""), field(node, "a:published") or field(node, "a:updated")

path = Path(__file__).with_name("sugestoes.json")
old = []
try:
    previous = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(previous.get("sugestoes"), list):
        old = previous["sugestoes"]
except (OSError, ValueError, TypeError):
    pass

collected = []
seen = set()
errors = []
for name, url in FEEDS:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 JaExisteReviewBot/1.1"})
        with urllib.request.urlopen(request, timeout=20) as response:
            data = response.read(1_500_000)
        for title, link, date in entries(data):
            title = clean(title)
            if not title or not link.startswith("https://") or not KEYWORDS.search(title) or link in seen:
                continue
            seen.add(link)
            collected.append({
                "titulo_original": title,
                "fonte": name,
                "url": link,
                "data_original": date,
                "estado": "POR VERIFICAR",
            })
    except Exception as exc:
        errors.append(f"{name}: {type(exc).__name__}: {exc}")

# Preserva sugestões anteriores; evita perder notícias quando uma fonte falha.
for item in old:
    if isinstance(item, dict) and item.get("url") not in seen:
        collected.append(item)
        seen.add(item.get("url"))
result = {
    "recolhido_em_utc": datetime.now(timezone.utc).isoformat(),
    "nota": "Títulos e vídeos são pistas para revisão humana, não provas de lançamento. Nunca publicar sem confirmar a fonte oficial.",
    "sugestoes": collected[:100],
    "erros": errors,
}
path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"{len(result['sugestoes'])} sugestões guardadas; {len(errors)} fontes com erro")
