"""NHKとYahoo!ニュースのRSSを取得して news.json に保存する（GitHub Actionsから実行）"""
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

SOURCES = [
    ("Yahoo!ニュース 主要", "https://news.yahoo.co.jp/rss/topics/top-picks.xml"),
    ("NHKニュース", "https://www3.nhk.or.jp/rss/news/cat0.xml"),
]

out = {"updated": datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M"), "sources": []}
for name, url in SOURCES:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
        items = [{"title": i.findtext("title"), "link": i.findtext("link")} for i in root.iter("item")][:5]
        if items:
            out["sources"].append({"name": name, "items": items})
    except Exception as e:  # 片方が失敗してももう片方は載せる
        print("skip", name, e)

if out["sources"]:
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
