from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import List

def generate_thumbnail(out_path: str, date_str: str, keywords: List[str]):
    W,H = 1280,720
    img = Image.new("RGB", (W,H), (15,18,45))
    d = ImageDraw.Draw(img)

    # Try to use a common font; if unavailable, default
    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 92)
        font_sub = ImageFont.truetype("DejaVuSans-Bold.ttf", 54)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    title = "오늘의 뉴스 요약"
    d.text((60, 80), title, fill=(255,255,255), font=font_title)
    d.rectangle([60, 220, W-60, 230], fill=(80,160,255))

    kw_text = " · ".join(keywords[:3]) if keywords else "핵심 이슈"
    d.text((60, 280), kw_text, fill=(230,230,230), font=font_sub)
    d.text((60, H-120), date_str, fill=(200,200,200), font=font_sub)

    img.save(out_path)
