#!/usr/bin/env python3
"""
실제 뉴스 데이터를 사용한 뉴스 브리핑 비디오 생성
"""

from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip
from pathlib import Path
import datetime
import json

def create_better_news_video():
    """실제 뉴스 데이터로 뉴스 브리핑 비디오 생성"""
    
    # 설정
    W, H = 1920, 1080
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    print("🎬 뉴스 브리핑 비디오 생성 중...")
    
    # 실제 뉴스 데이터 (테스트용)
    news_data = [
        {
            "title": "뜨거운 증시와 그렇지 못한 中 경제… 10년 만에 나타난 '괴리'",
            "summary": "중국의 경제가 부진한 가운데 증시는 상승세를 보이며 10년 만에 괴리가 발생하고 있습니다. 전문가들은 이러한 현상이 지속될 경우 경제적 불균형을 초래할 수 있다고 경고하고 있습니다."
        },
        {
            "title": "韓·美·日, 북한 IT 인력 우려에 공동성명 발표",
            "summary": "북한 IT 인력에 대한 한미일 공동성명이 발표되었습니다. 이번 성명에서는 북한의 사이버 공격 능력과 IT 인력 활용에 대한 우려를 표명하고, 국제적 협력을 강화하겠다는 의지를 밝혔습니다."
        },
        {
            "title": "AI 기술 발전으로 일자리 변화 가속화",
            "summary": "인공지능 기술의 급속한 발전으로 다양한 산업 분야에서 일자리 변화가 가속화되고 있습니다. 전문가들은 새로운 기술에 적응하는 것이 중요하다고 강조하고 있습니다."
        }
    ]
    
    # 비디오 길이 계산 (각 뉴스당 8초)
    duration = 3.0 + (len(news_data) * 8.0)  # 제목 3초 + 뉴스들
    
    # 1. 기본 배경 (어두운 회색)
    bg = ColorClip(size=(W, H), color=(35, 35, 35)).set_duration(duration)
    
    # 2. 상단 바
    top_bar = ColorClip(size=(W, int(H * 0.08)), color=(50, 50, 50)).set_duration(duration)
    top_bar = top_bar.set_position((0, 0))
    
    # 3. 제목
    title = TextClip(
        txt=f"뉴스 브리핑 ({today})", 
        fontsize=64, 
        color="white",
        method="caption",
        size=(W-120, None)
    ).set_position(("center", 120)).set_start(0).set_duration(3.0)
    
    # 4. 뉴스 내용들
    clips = [bg, top_bar, title]
    current_time = 3.0
    
    for i, news in enumerate(news_data):
        # 뉴스 번호와 제목
        news_title = TextClip(
            txt=f"{i+1}. {news['title']}", 
            fontsize=42, 
            color="white",
            method="caption",
            size=(W-140, None)
        ).set_position((70, 250)).set_start(current_time).set_duration(8.0)
        
        # 뉴스 요약
        news_summary = TextClip(
            txt=news['summary'], 
            fontsize=28, 
            color="lightblue",
            method="caption",
            size=(W-140, None)
        ).set_position((70, 350)).set_start(current_time).set_duration(8.0)
        
        clips.extend([news_title, news_summary])
        current_time += 8.0
    
    # 모든 클립 합성
    video = CompositeVideoClip(clips)
    
    # 출력
    output_path = "better_news_briefing.mp4"
    print(f"📹 비디오 저장 중: {output_path}")
    video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", preset="medium")
    
    print("✅ 뉴스 브리핑 비디오 생성 완료!")
    print(f"📊 비디오 정보:")
    print(f"   - 길이: {duration:.1f}초")
    print(f"   - 해상도: {W}x{H}")
    print(f"   - 뉴스 개수: {len(news_data)}개")
    
    return output_path

if __name__ == "__main__":
    create_better_news_video()