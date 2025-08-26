import feedparser, time
from typing import List, Dict
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from dateutil import parser as dateparser
from utils import clean_google_news_link

def google_news_rss(topic: str, ceid: str="KR:ko") -> str:
    q = quote_plus(topic)
    return f"https://news.google.com/rss/search?q={q}&hl=ko&gl=KR&ceid={ceid}"

def fetch_news(topics: List[str], per_topic: int=3, ceid: str="KR:ko") -> List[Dict]:
    items = []
    for t in topics:
        url = google_news_rss(t, ceid=ceid)
        feed = feedparser.parse(url)
        for entry in feed.entries[:per_topic]:
            link = clean_google_news_link(entry.link)
            published = None
            if hasattr(entry, 'published'):
                try:
                    published = dateparser.parse(entry.published)
                except Exception:
                    published = None
            summary = BeautifulSoup(getattr(entry, "summary", ""), "html.parser").get_text(" ", strip=True)
            items.append({
                "topic": t,
                "title": entry.get("title", ""),
                "summary": summary,
                "link": link,
                "published": published.isoformat() if published else None,
                "source": entry.get("source", {}).get("title") if hasattr(entry, "source") else None
            })
        time.sleep(0.2)
    seen, deduped = set(), []
    for it in items:
        if it["link"] in seen:
            continue
        seen.add(it["link"])
        deduped.append(it)
    return deduped[: max(1, per_topic*len(topics))]
