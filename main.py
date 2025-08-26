import os, datetime
from pathlib import Path
from config import (NEWS_TOPICS, CHANNEL_LOCALE, CHANNEL_TITLE_PREFIX,
                    OUTPUT_DIR, BACKGROUND_IMAGE, VIDEO_RESOLUTION,
                    YOUTUBE_CLIENT_SECRETS_FILE)
from news_fetcher import fetch_news
from summarizer_openai import summarize_items
from tts_openai import synthesize_segments, concat_audio
from video_maker import make_video, build_srt
from thumbnail_gen import generate_thumbnail
from uploader_youtube import get_service, upload_video, get_or_create_playlist, add_video_to_playlist
from utils import ensure_dir

def run_once():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(OUTPUT_DIR) / today
    ensure_dir(out_dir)
    # 1) Fetch
    items = fetch_news(NEWS_TOPICS, per_topic=2, ceid=CHANNEL_LOCALE)
    # 2) Summarize
    enriched = summarize_items(items)
    # 3) Narration segments
    title = f"{CHANNEL_TITLE_PREFIX} ({today})"
    segments = [f"안녕하세요. {today} 주요 뉴스를 3분 안에 요약해 드립니다."]
    headlines = []
    for i, it in enumerate(enriched, start=1):
        seg = f"{i}번 뉴스. {it['bullet']} 해설: {it['explain']}"
        segments.append(seg)
        headlines.append(it["title"])
    segments.append("시청해 주셔서 감사합니다. 내일 다시 뵙겠습니다.")

    # 4) TTS
    parts = synthesize_segments(segments, out_dir / "audio")
    concat_audio(parts, out_dir / "narration.mp3")

    # Build timeline
    timeline = []
    t = 0.0
    for idx, p in enumerate(parts, start=1):
        start = t
        end = t + p["duration"] + 0.25
        headline = headlines[idx-2] if 1 < idx < len(parts) else "뉴스 브리핑"
        timeline.append({"start": start, "end": end, "headline": headline})
        t = end

    # 5) Captions
    srt_segs = []
    t = 0.0
    for p in parts:
        srt_segs.append({"start": t, "end": t + p["duration"], "text": p["text"]})
        t += p["duration"] + 0.25
    build_srt(srt_segs, out_dir / "captions.srt")

    # 6) Thumbnails (auto)
    keywords = [it['topic'] for it in enriched]
    thumb_path = str(out_dir / "thumbnail.jpg")
    generate_thumbnail(thumb_path, today, keywords)

    # 7) Videos: landscape and shorts
    landscape_path = str(out_dir / "news_briefing.mp4")
    make_video(str(out_dir / "narration.mp3"), timeline, BACKGROUND_IMAGE, VIDEO_RESOLUTION, title, landscape_path, mode="landscape")

    # shorts 1080x1920
    shorts_res = "1080x1920"
    shorts_path = str(out_dir / "news_briefing_shorts.mp4")
    make_video(str(out_dir / "narration.mp3"), timeline, BACKGROUND_IMAGE, shorts_res, title, shorts_path, mode="shorts")

    # 8) YouTube: upload + playlists
    try:
        youtube = get_service(str(YOUTUBE_CLIENT_SECRETS_FILE))
        desc_lines = [f"{it['title']} - {it['link']}" for it in enriched]
        description = "오늘의 주요 뉴스 출처:\n" + "\n".join(desc_lines)
        # Upload landscape as main
        video_id = upload_video(youtube, landscape_path, title, description, tags=["뉴스","요약","브리핑","한국"], privacy_status="public", thumbnail_path=thumb_path)

        # Create/Add to playlists by topic
        for topic in set([it["topic"] for it in enriched]):
            pl_id = get_or_create_playlist(youtube, f"뉴스 - {topic}", "자동 생성된 주제별 재생목록")
            add_video_to_playlist(youtube, pl_id, video_id)

        # Optionally upload Shorts as unlisted or public
        shorts_id = upload_video(youtube, shorts_path, f"{title} #shorts", description, tags=["뉴스","요약","브리핑","shorts"], privacy_status="unlisted", thumbnail_path=thumb_path)

        (out_dir / "video_ids.txt").write_text(f"landscape={video_id}\nshorts={shorts_id}\n", encoding="utf-8")
    except Exception as e:
        print("YouTube 업로드/재생목록 처리 건너뜀/오류:", e)

if __name__ == "__main__":
    run_once()
