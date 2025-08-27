#!/usr/bin/env python3
"""
핵심 기능 테스트 (비디오 생성 제외)
뉴스 수집 → 요약 → 썸네일 생성까지 테스트
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
        
        items = fetch_news(NEWS_TOPICS, per_topic=2, ceid=CHANNEL_LOCALE)
        
        if items:
            print(f"✅ 뉴스 수집 성공! {len(items)}개 기사")
            for i, item in enumerate(items[:3], 1):
                print(f"   {i}. {item['title'][:50]}...")
                print(f"      주제: {item['topic']}")
                print(f"      링크: {item['link']}")
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
                print(f"   {i}. 요약: {item['bullet'][:80]}...")
                print(f"      해설: {item['explain'][:80]}...")
            return enriched
        else:
            print("❌ 요약 실패")
            return None
            
    except Exception as e:
        print(f"❌ 요약 오류: {str(e)}")
        return None

def test_thumbnail_generation(enriched):
    """썸네일 생성 테스트"""
    try:
        print("\n🖼️ 썸네일 생성 테스트 중...")
        from thumbnail_gen import generate_thumbnail
        from config import OUTPUT_DIR
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        out_dir = Path(OUTPUT_DIR) / today
        out_dir.mkdir(parents=True, exist_ok=True)
        
        keywords = [item['topic'] for item in enriched[:3]]
        thumb_path = str(out_dir / "test_thumbnail.jpg")
        
        generate_thumbnail(thumb_path, today, keywords)
        
        print("✅ 썸네일 생성 성공!")
        print(f"   📁 파일: {thumb_path}")
        return thumb_path
        
    except Exception as e:
        print(f"❌ 썸네일 생성 오류: {str(e)}")
        return None

def test_tts_simple():
    """간단한 TTS 테스트"""
    try:
        print("\n🎤 TTS 간단 테스트 중...")
        from tts_openai import synthesize_segments
        from config import OUTPUT_DIR
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        out_dir = Path(OUTPUT_DIR) / today
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # 매우 간단한 테스트
        segments = ["안녕하세요. 테스트입니다."]
        
        parts = synthesize_segments(segments, out_dir / "audio")
        
        print("✅ TTS 테스트 성공!")
        print(f"   📁 생성된 오디오 파일: {len(parts)}개")
        return True
        
    except Exception as e:
        print(f"❌ TTS 테스트 오류: {str(e)}")
        return False

def test_youtube_auth_simple():
    """YouTube 인증 간단 테스트"""
    try:
        print("\n📺 YouTube API 간단 테스트 중...")
        from uploader_youtube import get_service
        
        client_secrets_file = "./client_secret.json"
        
        if not os.path.exists(client_secrets_file):
            print("❌ client_secret.json 파일이 없습니다.")
            return False
        
        # 서비스 객체 생성만 테스트
        youtube = get_service(client_secrets_file)
        
        print("✅ YouTube API 연결 성공!")
        return True
        
    except Exception as e:
        print(f"❌ YouTube API 테스트 오류: {str(e)}")
        return False

def generate_sample_script(enriched):
    """샘플 스크립트 생성"""
    try:
        print("\n📝 샘플 스크립트 생성 중...")
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        script = [f"안녕하세요. {today} 주요 뉴스를 요약해 드립니다."]
        
        for i, item in enumerate(enriched, 1):
            script.append(f"{i}번 뉴스. {item['bullet']} 해설: {item['explain']}")
        
        script.append("시청해 주셔서 감사합니다. 내일 다시 뵙겠습니다.")
        
        # 스크립트 저장
        out_dir = Path("data") / today
        out_dir.mkdir(parents=True, exist_ok=True)
        
        script_path = out_dir / "sample_script.txt"
        with open(script_path, "w", encoding="utf-8") as f:
            for line in script:
                f.write(line + "\n")
        
        print("✅ 샘플 스크립트 생성 성공!")
        print(f"   📁 파일: {script_path}")
        
        print("\n📋 생성된 스크립트:")
        for i, line in enumerate(script, 1):
            print(f"   {i}. {line}")
        
        return script_path
        
    except Exception as e:
        print(f"❌ 스크립트 생성 오류: {str(e)}")
        return None

def main():
    """메인 테스트 함수"""
    print("🚀 핵심 기능 테스트")
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
    
    # 3. 썸네일 생성
    thumb_path = test_thumbnail_generation(enriched)
    
    # 4. TTS 간단 테스트
    tts_success = test_tts_simple()
    
    # 5. YouTube API 간단 테스트
    youtube_success = test_youtube_auth_simple()
    
    # 6. 샘플 스크립트 생성
    script_path = generate_sample_script(enriched)
    
    print("\n" + "="*60)
    print("🎉 핵심 기능 테스트 완료!")
    print("="*60)
    
    print("✅ 성공한 기능들:")
    print("   📰 뉴스 수집")
    print("   🤖 뉴스 요약")
    if thumb_path:
        print("   🖼️ 썸네일 생성")
    if tts_success:
        print("   🎤 TTS 음성 생성")
    if youtube_success:
        print("   📺 YouTube API 연결")
    if script_path:
        print("   📝 스크립트 생성")
    
    print("\n💡 다음 단계:")
    print("   1. MoviePy 설치 문제 해결")
    print("   2. 비디오 생성 기능 완성")
    print("   3. YouTube 업로드 완성")
    print("   4. 전체 자동화 시스템 완성")

if __name__ == "__main__":
    main()