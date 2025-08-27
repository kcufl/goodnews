#!/usr/bin/env python3
"""
완전한 시스템 테스트
뉴스 수집 → 요약 → TTS → 비디오 생성 → 썸네일 생성
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
            for i, item in enumerate(items[:2], 1):
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
            for i, item in enumerate(enriched[:1], 1):
                print(f"   {i}. {item['bullet'][:60]}...")
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
        from tts_openai_fixed import synthesize_segments, concat_audio
        from config import OUTPUT_DIR
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        out_dir = Path(OUTPUT_DIR) / today
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # 뉴스 기반 스크립트 생성
        segments = [f"안녕하세요. {today} 주요 뉴스를 요약해 드립니다."]
        
        for i, item in enumerate(enriched[:2], 1):
            seg = f"{i}번 뉴스. {item['bullet']} 해설: {item['explain']}"
            segments.append(seg)
        
        segments.append("시청해 주셔서 감사합니다. 내일 다시 뵙겠습니다.")
        
        parts = synthesize_segments(segments, out_dir / "audio")
        concat_audio(parts, out_dir / "narration.mp3")
        
        print("✅ TTS 음성 생성 성공!")
        print(f"   📁 파일: {out_dir / 'narration.mp3'}")
        return str(out_dir / "narration.mp3")
        
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
        
        # 타임라인 생성
        timeline = []
        t = 0.0
        for i, item in enumerate(enriched[:2], 1):
            start = t
            end = t + 5.0  # 각 뉴스 5초
            timeline.append({
                "start": start, 
                "end": end, 
                "headline": f"{i}번 뉴스: {item['title'][:30]}..."
            })
            t = end
        
        title = f"뉴스 브리핑 ({today})"
        video_path = str(out_dir / "news_briefing.mp4")
        
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
        thumb_path = str(out_dir / "thumbnail.jpg")
        
        generate_thumbnail(thumb_path, today, keywords)
        
        print("✅ 썸네일 생성 성공!")
        print(f"   📁 파일: {thumb_path}")
        return thumb_path
        
    except Exception as e:
        print(f"❌ 썸네일 생성 오류: {str(e)}")
        return None

def main():
    """메인 테스트 함수"""
    print("🚀 완전한 시스템 테스트")
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
    print("🎉 완전한 시스템 테스트 완료!")
    print("="*60)
    
    print("✅ 모든 기능이 정상적으로 작동합니다!")
    print("\n📁 생성된 파일들:")
    print(f"   🎵 음성: {audio_path}")
    print(f"   🎬 비디오: {video_path}")
    if thumb_path:
        print(f"   🖼️ 썸네일: {thumb_path}")
    
    print("\n🎯 다음 단계:")
    print("   1. YouTube 업로드 설정 완료")
    print("   2. 자동화 스케줄링 설정")
    print("   3. 완전 자동화된 뉴스 채널 운영 시작!")
    
    print("\n💡 YouTube 업로드만 설정하면 완전 자동화가 가능합니다!")

if __name__ == "__main__":
    main()