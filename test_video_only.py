#!/usr/bin/env python3
"""
비디오 생성 전용 테스트 (TTS 제외)
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

def test_video_creation_without_audio(enriched):
    """오디오 없이 비디오 생성 테스트"""
    try:
        print("\n🎬 비디오 생성 테스트 중...")
        from video_maker import make_video
        from config import OUTPUT_DIR, BACKGROUND_IMAGE, VIDEO_RESOLUTION
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        out_dir = Path(OUTPUT_DIR) / today
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # 더미 오디오 파일 생성 (1초 무음)
        dummy_audio_path = str(out_dir / "dummy_audio.mp3")
        try:
            from pydub import AudioSegment
            from pydub.generators import Silence
            
            # 1초 무음 생성
            silence = Silence().to_audio_segment(duration=1000)  # 1초
            silence.export(dummy_audio_path, format="mp3")
            print("   ✅ 더미 오디오 파일 생성됨")
        except Exception as e:
            print(f"   ⚠️ 더미 오디오 생성 실패: {str(e)}")
            # 더미 오디오 없이 진행
            dummy_audio_path = None
        
        # 타임라인 생성
        timeline = []
        t = 0.0
        for i, item in enumerate(enriched[:3], 1):
            start = t
            end = t + 3.0  # 각 뉴스 3초
            timeline.append({
                "start": start, 
                "end": end, 
                "headline": f"{i}번 뉴스: {item['title'][:30]}..."
            })
            t = end
        
        title = f"뉴스 브리핑 테스트 ({today})"
        video_path = str(out_dir / "test_video.mp4")
        
        # 비디오 생성 (오디오 없이)
        if dummy_audio_path and os.path.exists(dummy_audio_path):
            make_video(
                audio_path=dummy_audio_path,
                timeline=timeline,
                background_image=BACKGROUND_IMAGE,
                resolution=VIDEO_RESOLUTION,
                title=title,
                out_path=video_path,
                mode="landscape"
            )
        else:
            # 오디오 없이 비디오만 생성
            print("   ⚠️ 오디오 없이 비디오 생성 시도...")
            # 더미 오디오 경로로 빈 파일 지정
            make_video(
                audio_path="/dev/null",  # 빈 파일
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
    print("🚀 비디오 생성 전용 테스트")
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
    
    # 3. 비디오 생성 (오디오 제외)
    video_path = test_video_creation_without_audio(enriched)
    if not video_path:
        print("❌ 비디오 생성 실패로 테스트 중단")
        return
    
    # 4. 썸네일 생성
    thumb_path = test_thumbnail_generation(enriched)
    
    print("\n" + "="*60)
    print("🎉 비디오 생성 테스트 완료!")
    print("✅ 핵심 기능이 정상적으로 작동합니다.")
    print("\n📁 생성된 파일들:")
    print(f"   🎬 비디오: {video_path}")
    if thumb_path:
        print(f"   🖼️ 썸네일: {thumb_path}")
    
    print("\n💡 TTS와 YouTube 업로드만 설정하면 완전 자동화가 가능합니다!")

if __name__ == "__main__":
    main()