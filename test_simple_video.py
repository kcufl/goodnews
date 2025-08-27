#!/usr/bin/env python3
"""
간단한 뉴스 스타일 비디오 테스트
"""

from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip
from pathlib import Path
import datetime

def create_simple_news_video():
    """간단한 뉴스 스타일 비디오 생성"""
    
    # 설정
    W, H = 1920, 1080
    duration = 15.0
    
    print("🎬 간단한 뉴스 비디오 생성 중...")
    
    # 1. 기본 배경 (어두운 회색)
    bg = ColorClip(size=(W, H), color=(40, 40, 40)).set_duration(duration)
    
    # 2. 제목
    title = TextClip(
        txt="뉴스 브리핑 (2025-08-27)", 
        fontsize=60, 
        color="white",
        method="caption",
        size=(W-100, None)
    ).set_position(("center", 100)).set_start(0).set_duration(3.0)
    
    # 3. 뉴스 1
    news1_title = TextClip(
        txt="1. 중국 경제와 증시 괴리 현상", 
        fontsize=40, 
        color="white",
        method="caption",
        size=(W-100, None)
    ).set_position((50, 300)).set_start(3.0).set_duration(4.0)
    
    news1_content = TextClip(
        txt="중국의 경제가 부진한 가운데 증시는 상승세를 보이며 10년 만에 괴리가 발생하고 있습니다.", 
        fontsize=28, 
        color="lightblue",
        method="caption",
        size=(W-100, None)
    ).set_position((50, 400)).set_start(3.0).set_duration(4.0)
    
    # 4. 뉴스 2
    news2_title = TextClip(
        txt="2. 한미일 북한 IT 인력 공동성명", 
        fontsize=40, 
        color="white",
        method="caption",
        size=(W-100, None)
    ).set_position((50, 500)).set_start(7.0).set_duration(4.0)
    
    news2_content = TextClip(
        txt="북한 IT 인력에 대한 한미일 공동성명이 발표되었습니다.", 
        fontsize=28, 
        color="lightblue",
        method="caption",
        size=(W-100, None)
    ).set_position((50, 600)).set_start(7.0).set_duration(4.0)
    
    # 5. 뉴스 3
    news3_title = TextClip(
        txt="3. 추가 뉴스 내용", 
        fontsize=40, 
        color="white",
        method="caption",
        size=(W-100, None)
    ).set_position((50, 700)).set_start(11.0).set_duration(4.0)
    
    news3_content = TextClip(
        txt="추가 뉴스 요약 내용이 여기에 표시됩니다.", 
        fontsize=28, 
        color="lightblue",
        method="caption",
        size=(W-100, None)
    ).set_position((50, 800)).set_start(11.0).set_duration(4.0)
    
    # 모든 클립 합성
    video = CompositeVideoClip([
        bg, 
        title, 
        news1_title, news1_content,
        news2_title, news2_content,
        news3_title, news3_content
    ])
    
    # 출력
    output_path = "test_simple_news.mp4"
    print(f"📹 비디오 저장 중: {output_path}")
    video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", preset="medium")
    
    print("✅ 간단한 뉴스 비디오 생성 완료!")
    return output_path

if __name__ == "__main__":
    create_simple_news_video()