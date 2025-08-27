#!/usr/bin/env python3
"""
최종 뉴스 브리핑 비디오 생성 - 배경과 텍스트 모두 확실히 표시
"""

from moviepy.editor import ImageClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path
import datetime
import os

def create_final_news_frame(title, summary, frame_number, total_frames):
    """최종 뉴스 프레임 생성 - 배경과 텍스트 모두 확실히 표시"""
    W, H = 1920, 1080
    
    # 1. 기본 배경 (밝은 파란색 그라데이션)
    img = Image.new('RGB', (W, H), (30, 60, 120))
    draw = ImageDraw.Draw(img)
    
    # 그라데이션 효과 (상단에서 하단으로)
    for y in range(H):
        # 파란색에서 어두운 파란색으로 그라데이션
        blue_intensity = int(120 - (y / H) * 60)  # 120에서 60으로
        color = (30, 60, blue_intensity)
        draw.line([(0, y), (W, y)], fill=color)
    
    # 2. 상단 바 (뉴스 채널 스타일)
    top_bar_color = (50, 100, 180)
    draw.rectangle([0, 0, W, int(H*0.10)], fill=top_bar_color)
    
    # 3. 좌측 세로 바
    left_bar_color = (80, 120, 200)
    draw.rectangle([0, 0, int(W*0.02), H], fill=left_bar_color)
    
    # 4. 하단 바 (자막 영역)
    bottom_bar_color = (20, 40, 80)
    draw.rectangle([0, H-int(H*0.20), W, H], fill=bottom_bar_color)
    
    # 5. 제목 (상단 중앙)
    try:
        # 폰트 설정
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        ]
        
        title_font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                title_font = ImageFont.truetype(font_path, 72)
                break
        
        if title_font is None:
            title_font = ImageFont.load_default()
    except:
        title_font = ImageFont.load_default()
    
    # 제목 텍스트
    title_text = f"뉴스 브리핑 ({datetime.datetime.now().strftime('%Y-%m-%d')})"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    title_x = (W - title_width) // 2
    draw.text((title_x, 30), title_text, fill=(255, 255, 255), font=title_font)
    
    # 6. 뉴스 번호와 제목
    try:
        news_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        news_font = ImageFont.load_default()
    
    news_title_text = f"{frame_number}. {title}"
    draw.text((100, 200), news_title_text, fill=(255, 255, 255), font=news_font)
    
    # 7. 뉴스 요약 (여러 줄로 나누기)
    try:
        summary_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        summary_font = ImageFont.load_default()
    
    # 요약 텍스트를 여러 줄로 나누기
    words = summary.split()
    lines = []
    current_line = ""
    max_width = W - 200
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=summary_font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    # 요약 텍스트 그리기
    y_position = 300
    for line in lines:
        draw.text((100, y_position), line, fill=(255, 255, 0), font=summary_font)
        y_position += 40
    
    # 8. 시각적 요소 추가 (뉴스 스타일)
    # 우측 상단에 뉴스 아이콘 (간단한 사각형)
    icon_color = (255, 255, 255)
    draw.rectangle([W-150, 30, W-50, 80], fill=icon_color, outline=(200, 200, 200), width=3)
    draw.text((W-140, 40), "NEWS", fill=(30, 60, 120), font=title_font)
    
    return img

def create_final_news_video():
    """최종 뉴스 브리핑 비디오 생성"""
    
    print("🎬 최종 뉴스 브리핑 비디오 생성 중...")
    
    # 뉴스 데이터
    news_data = [
        {
            "title": "중국 경제와 증시 괴리 현상",
            "summary": "중국의 경제가 부진한 가운데 증시는 상승세를 보이며 10년 만에 괴리가 발생하고 있습니다. 전문가들은 이러한 현상이 지속될 경우 경제적 불균형을 초래할 수 있다고 경고하고 있습니다."
        },
        {
            "title": "한미일 북한 IT 인력 공동성명",
            "summary": "북한 IT 인력에 대한 한미일 공동성명이 발표되었습니다. 이번 성명에서는 북한의 사이버 공격 능력과 IT 인력 활용에 대한 우려를 표명하고, 국제적 협력을 강화하겠다는 의지를 밝혔습니다."
        },
        {
            "title": "AI 기술 발전으로 일자리 변화 가속화",
            "summary": "인공지능 기술의 급속한 발전으로 다양한 산업 분야에서 일자리 변화가 가속화되고 있습니다. 전문가들은 새로운 기술에 적응하는 것이 중요하다고 강조하고 있습니다."
        }
    ]
    
    # 각 뉴스별로 프레임 생성
    frames = []
    fps = 30
    duration_per_news = 8.0  # 각 뉴스당 8초
    
    for i, news in enumerate(news_data):
        print(f"📝 뉴스 {i+1} 프레임 생성 중...")
        frame = create_final_news_frame(news['title'], news['summary'], i+1, len(news_data))
        frames.append(frame)
    
    # 프레임을 비디오로 변환
    clips = []
    
    for i, frame in enumerate(frames):
        print(f"🎬 뉴스 {i+1} 비디오 클립 생성 중...")
        # numpy 배열로 변환
        frame_array = np.array(frame)
        clip = ImageClip(frame_array).set_duration(duration_per_news)
        clips.append(clip)
    
    # 모든 클립 합성
    video = CompositeVideoClip(clips)
    
    # 출력
    output_path = "final_news_briefing.mp4"
    print(f"📹 비디오 저장 중: {output_path}")
    video.write_videofile(output_path, fps=fps, codec="libx264", audio_codec="aac", preset="medium")
    
    print("✅ 최종 뉴스 브리핑 비디오 생성 완료!")
    print(f"📊 비디오 정보:")
    print(f"   - 길이: {len(news_data) * duration_per_news:.1f}초")
    print(f"   - 해상도: 1920x1080")
    print(f"   - 뉴스 개수: {len(news_data)}개")
    print(f"   - 배경: 파란색 그라데이션 + 뉴스 스타일 요소")
    print(f"   - 텍스트: 흰색 헤드라인 + 노란색 요약")
    
    return output_path

if __name__ == "__main__":
    create_final_news_video()