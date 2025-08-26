import re, urllib.parse, os
from datetime import datetime, timezone

def clean_google_news_link(url: str) -> str:
    # Extract real URL from Google News RSS links that are often wrapped with 'url=' parameter.
    try:
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        if "url" in qs:
            real = qs["url"][0]
            return urllib.parse.unquote(real)
        if parsed.netloc.endswith("news.google.com"):
            m = re.search(r'url=([^&]+)', url)
            if m:
                return urllib.parse.unquote(m.group(1))
        return url
    except Exception:
        return url

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def timestamp_ko(dt: datetime) -> str:
    dt = dt.astimezone(timezone.utc).astimezone()  # local tz
    return dt.strftime("%Y-%m-%d %H:%M")
