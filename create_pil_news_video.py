#!/usr/bin/env python3
"""
PIL을 직접 사용한 뉴스 브리핑 비디오 생성
"""

from moviepy.editor import ImageClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path
import datetime
import os

def create_text_image(text, size=(800, 200), bg_color=(60, 60, 60), text_color=(255, 255, 255), font_size=40):
    """PIL을 사용해서 텍스트 이미지 생성"""
    # 이미지 생성
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # 폰트 설정 (시스템 폰트 사용)
    try:
        # Linux에서 사용 가능한 폰트들
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/System/Library/Fonts/Arial.ttf",  # macOS
            "arial.ttf"  # Windows
        ]
        
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
                break
        
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # 텍스트 그리기
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    draw.text((x, y), text, fill=text_color, font=font)
    
    return img

def create_news_frame(title, summary, frame_number, total_frames):
    """뉴스 프레임 생성"""
    W, H = 1920, 1080
    
    # 기본 배경
    img = Image.new('RGB', (W, H), (60, 60, 60))
    draw = ImageDraw.Draw(img)
    
    # 상단 바
    draw.rectangle([0, 0, W, int(H*0.08)], fill=(80, 80, 80))
    
    # 제목 (상단)
    title_img = create_text_image(f"뉴스 브리핑 ({datetime.datetime.now().strftime('%Y-%m-%d')})", 
                                 (W-100, 150), (60, 60, 60), (255, 255, 255), 60)
    img.paste(title_img, (50, 50))
    
    # 뉴스 제목
    news_title_img = create_text_image(f"{frame_number}. {title}", 
                                      (W-100, 100), (60, 60, 60), (255, 255, 255), 40)
    img.paste(news_title_img, (50, 250))
    
    # 뉴스 요약
    summary_img = create_text_image(summary, 
                                   (W-100, 200), (60, 60, 60), (255, 255, 0), 28)
    img.paste(summary_img, (50, 400))
    
    return img

def create_pil_news_video():
    """PIL을 사용한 뉴스 브리핑 비디오 생성"""
    
    print("🎬 PIL을 사용한 뉴스 브리핑 비디오 생성 중...")
    
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
    
    # 각 뉴스별로 프레임 생성
    frames = []
    fps = 30
    duration_per_news = 6.0  # 각 뉴스당 6초
    
    for i, news in enumerate(news_data):
        frame = create_news_frame(news['title'], news['summary'], i+1, len(news_data))
        frames.append(frame)
    
    # 프레임을 비디오로 변환
    clips = []
    
    for i, frame in enumerate(frames):
        # numpy 배열로 변환
        frame_array = np.array(frame)
        clip = ImageClip(frame_array).set_duration(duration_per_news)
        clips.append(clip)
    
    # 모든 클립 합성
    video = CompositeVideoClip(clips)
    
    # 출력
    output_path = "pil_news_briefing.mp4"
    print(f"📹 비디오 저장 중: {output_path}")
    video.write_videofile(output_path, fps=fps, codec="libx264", audio_codec="aac", preset="medium")
    
    print("✅ PIL을 사용한 뉴스 브리핑 비디오 생성 완료!")
    print(f"📊 비디오 정보:")
    print(f"   - 길이: {len(news_data) * duration_per_news:.1f}초")
    print(f"   - 해상도: 1920x1080")
    print(f"   - 뉴스 개수: {len(news_data)}개")
    
    return output_path

if __name__ == "__main__":
    create_pil_news_video()