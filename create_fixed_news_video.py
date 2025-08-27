#!/usr/bin/env python3
"""
텍스트 렌더링 문제를 해결한 뉴스 브리핑 비디오 생성
"""

from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
from pathlib import Path
import datetime

def create_fixed_news_video():
    """텍스트 렌더링 문제를 해결한 뉴스 브리핑 비디오 생성"""
    
    # 설정
    W, H = 1920, 1080
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    print("🎬 수정된 뉴스 브리핑 비디오 생성 중...")
    
    # 뉴스 데이터
    news_data = [
        {
            "title": "중국 경제와 증시 괴리 현상",
            "summary": "중국의 경제가 부진한 가운데 증시는 상승세를 보이며 10년 만에 괴리가 발생하고 있습니다."
        },
        {
            "title": "한미일 북한 IT 인력 공동성명",
            "summary": "북한 IT 인력에 대한 한미일 공동성명이 발표되었습니다."
        },
        {
            "title": "AI 기술 발전으로 일자리 변화",
            "summary": "인공지능 기술의 급속한 발전으로 다양한 산업 분야에서 일자리 변화가 가속화되고 있습니다."
        }
    ]
    
    # 비디오 길이 계산
    duration = 3.0 + (len(news_data) * 6.0)  # 제목 3초 + 뉴스들 6초씩
    
    # 1. 기본 배경 (밝은 회색으로 변경)
    bg = ColorClip(size=(W, H), color=(60, 60, 60)).set_duration(duration)
    
    # 2. 상단 바 (더 밝게)
    top_bar = ColorClip(size=(W, int(H * 0.08)), color=(80, 80, 80)).set_duration(duration)
    top_bar = top_bar.set_position((0, 0))
    
    # 3. 제목 (더 간단하게)
    try:
        title = TextClip(
            txt=f"뉴스 브리핑 ({today})", 
            fontsize=60, 
            color="white",
            font="Arial-Bold"
        ).set_position(("center", 120)).set_start(0).set_duration(3.0)
    except:
        # 폰트 문제시 기본 설정
        title = TextClip(
            txt=f"뉴스 브리핑 ({today})", 
            fontsize=60, 
            color="white"
        ).set_position(("center", 120)).set_start(0).set_duration(3.0)
    
    # 4. 뉴스 내용들
    clips = [bg, top_bar, title]
    current_time = 3.0
    
    for i, news in enumerate(news_data):
        try:
            # 뉴스 번호와 제목 (더 간단하게)
            news_title = TextClip(
                txt=f"{i+1}. {news['title']}", 
                fontsize=40, 
                color="white",
                font="Arial"
            ).set_position((100, 300 + i*200)).set_start(current_time).set_duration(6.0)
            
            # 뉴스 요약 (더 간단하게)
            news_summary = TextClip(
                txt=news['summary'], 
                fontsize=24, 
                color="yellow",
                font="Arial"
            ).set_position((100, 350 + i*200)).set_start(current_time).set_duration(6.0)
            
            clips.extend([news_title, news_summary])
            
        except Exception as e:
            print(f"⚠️ 텍스트 생성 오류 (뉴스 {i+1}): {e}")
            # 오류시 간단한 색상 블록으로 대체
            color_block = ColorClip(size=(400, 100), color=(100, 150, 200)).set_duration(6.0)
            color_block = color_block.set_position((100, 300 + i*200)).set_start(current_time)
            clips.append(color_block)
        
        current_time += 6.0
    
    # 모든 클립 합성
    video = CompositeVideoClip(clips)
    
    # 출력
    output_path = "fixed_news_briefing.mp4"
    print(f"📹 비디오 저장 중: {output_path}")
    video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", preset="medium")
    
    print("✅ 수정된 뉴스 브리핑 비디오 생성 완료!")
    print(f"📊 비디오 정보:")
    print(f"   - 길이: {duration:.1f}초")
    print(f"   - 해상도: {W}x{H}")
    print(f"   - 뉴스 개수: {len(news_data)}개")
    
    return output_path

if __name__ == "__main__":
    create_fixed_news_video()