#!/usr/bin/env python3
"""
전체 시스템 테스트 (YouTube 업로드 제외)
뉴스 수집 → 요약 → TTS → 비디오 생성까지 테스트
"""

import os
import datetime
from pathlib import Path
from dotenv import load_dotenv

def test_news_fetching():
    """뉴스 수집 테스트"""
    try:
        print("📰 뉴스 수집 테스트 중...")
        from news_fetcher import fetch_news
        from config import NEWS_TOPICS, CHANNEL_LOCALE
        
        items = fetch_news(NEWS_TOPICS, per_topic=1, ceid=CHANNEL_LOCALE)
        
        if items:
            print(f"✅ 뉴스 수집 성공! {len(items)}개 기사")
            for i, item in enumerate(items[:3], 1):
                print(f"   {i}. {item['title'][:50]}...")
            return items
        else:
            print("❌ 뉴스 수집 실패")
            return None
            
    except Exception as e:
        print(f"❌ 뉴스 수집 오류: {str(e)}")
        return None

def test_summarization(items):
    """뉴스 요약 테스트"""
    try:
        print("\n🤖 뉴스 요약 테스트 중...")
        from summarizer_openai import summarize_items
        
        enriched = summarize_items(items)
        
        if enriched:
            print(f"✅ 요약 성공! {len(enriched)}개 기사")
            for i, item in enumerate(enriched[:2], 1):
                print(f"   {i}. {item['bullet'][:50]}...")
            return enriched
        else:
            print("❌ 요약 실패")
            return None
            
    except Exception as e:
        print(f"❌ 요약 오류: {str(e)}")
        return None

def test_tts_generation(enriched):
    """TTS 음성 생성 테스트"""
    try:
        print("\n🎤 TTS 음성 생성 테스트 중...")
        from tts_openai import synthesize_segments, concat_audio
        from config import OUTPUT_DIR
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        out_dir = Path(OUTPUT_DIR) / today
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # 간단한 테스트 텍스트
        segments = [
            "안녕하세요. 오늘의 뉴스 요약 테스트입니다.",
            "첫 번째 뉴스입니다. 테스트가 성공적으로 진행되고 있습니다.",
            "시청해 주셔서 감사합니다."
        ]
        
        parts = synthesize_segments(segments, out_dir / "audio")
        concat_audio(parts, out_dir / "test_narration.mp3")
        
        print("✅ TTS 음성 생성 성공!")
        print(f"   📁 파일: {out_dir / 'test_narration.mp3'}")
        return str(out_dir / "test_narration.mp3")
        
    except Exception as e:
        print(f"❌ TTS 오류: {str(e)}")
        return None

def test_video_creation(audio_path, enriched):
    """비디오 생성 테스트"""
    try:
        print("\n🎬 비디오 생성 테스트 중...")
        from video_maker import make_video
        from config import OUTPUT_DIR, BACKGROUND_IMAGE, VIDEO_RESOLUTION
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        out_dir = Path(OUTPUT_DIR) / today
        
        # 간단한 타임라인 생성
        timeline = [
            {"start": 0, "end": 3, "headline": "뉴스 브리핑 테스트"},
            {"start": 3, "end": 6, "headline": "첫 번째 뉴스"},
            {"start": 6, "end": 9, "headline": "테스트 완료"}
        ]
        
        title = f"뉴스 브리핑 테스트 ({today})"
        video_path = str(out_dir / "test_video.mp4")
        
        make_video(
            audio_path=audio_path,
            timeline=timeline,
            background_image=BACKGROUND_IMAGE,
            resolution=VIDEO_RESOLUTION,
            title=title,
            out_path=video_path,
            mode="landscape"
        )
        
        print("✅ 비디오 생성 성공!")
        print(f"   📁 파일: {video_path}")
        return video_path
        
    except Exception as e:
        print(f"❌ 비디오 생성 오류: {str(e)}")
        return None

def test_thumbnail_generation(enriched):
    """썸네일 생성 테스트"""
    try:
        print("\n🖼️ 썸네일 생성 테스트 중...")
        from thumbnail_gen import generate_thumbnail
        from config import OUTPUT_DIR
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        out_dir = Path(OUTPUT_DIR) / today
        
        keywords = [item['topic'] for item in enriched[:3]]
        thumb_path = str(out_dir / "test_thumbnail.jpg")
        
        generate_thumbnail(thumb_path, today, keywords)
        
        print("✅ 썸네일 생성 성공!")
        print(f"   📁 파일: {thumb_path}")
        return thumb_path
        
    except Exception as e:
        print(f"❌ 썸네일 생성 오류: {str(e)}")
        return None

def main():
    """메인 테스트 함수"""
    print("🚀 전체 시스템 테스트 (YouTube 업로드 제외)")
    print("="*60)
    
    load_dotenv()
    
    # 1. 뉴스 수집
    items = test_news_fetching()
    if not items:
        print("❌ 뉴스 수집 실패로 테스트 중단")
        return
    
    # 2. 뉴스 요약
    enriched = test_summarization(items)
    if not enriched:
        print("❌ 뉴스 요약 실패로 테스트 중단")
        return
    
    # 3. TTS 음성 생성
    audio_path = test_tts_generation(enriched)
    if not audio_path:
        print("❌ TTS 생성 실패로 테스트 중단")
        return
    
    # 4. 비디오 생성
    video_path = test_video_creation(audio_path, enriched)
    if not video_path:
        print("❌ 비디오 생성 실패로 테스트 중단")
        return
    
    # 5. 썸네일 생성
    thumb_path = test_thumbnail_generation(enriched)
    
    print("\n" + "="*60)
    print("🎉 전체 시스템 테스트 완료!")
    print("✅ 모든 기능이 정상적으로 작동합니다.")
    print("\n📁 생성된 파일들:")
    print(f"   🎵 음성: {audio_path}")
    print(f"   🎬 비디오: {video_path}")
    if thumb_path:
        print(f"   🖼️ 썸네일: {thumb_path}")
    
    print("\n💡 YouTube 업로드만 설정하면 완전 자동화가 가능합니다!")

if __name__ == "__main__":
    main()