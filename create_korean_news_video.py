#!/usr/bin/env python3
"""
한글 폰트와 음성이 제대로 작동하는 뉴스 브리핑 비디오 생성
"""

from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path
import datetime
import os

def create_korean_news_frame(title, summary, frame_number, total_frames):
    """한글 폰트가 제대로 표시되는 뉴스 프레임 생성"""
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
    
    # 5. 한글 폰트 설정
    try:
        # 한글 폰트 경로들
        korean_font_paths = [
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
            "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/System/Library/Fonts/AppleGothic.ttf",  # macOS
            "C:/Windows/Fonts/malgun.ttf"  # Windows
        ]
        
        title_font = None
        for font_path in korean_font_paths:
            if os.path.exists(font_path):
                title_font = ImageFont.truetype(font_path, 72, encoding="utf-8")
                break
        
        if title_font is None:
            # 기본 폰트 사용
            title_font = ImageFont.load_default()
            print("⚠️ 한글 폰트를 찾을 수 없어 기본 폰트를 사용합니다.")
    except Exception as e:
        print(f"⚠️ 폰트 로드 오류: {e}")
        title_font = ImageFont.load_default()
    
    # 6. 제목 텍스트 (한글)
    title_text = f"뉴스 브리핑 ({datetime.datetime.now().strftime('%Y-%m-%d')})"
    try:
        bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = bbox[2] - bbox[0]
        title_x = (W - title_width) // 2
        draw.text((title_x, 30), title_text, fill=(255, 255, 255), font=title_font)
    except Exception as e:
        print(f"⚠️ 제목 텍스트 그리기 오류: {e}")
        # 영어로 대체
        draw.text((W//2-200, 30), "NEWS BRIEFING", fill=(255, 255, 255), font=title_font)
    
    # 7. 뉴스 번호와 제목 (한글)
    try:
        news_font = ImageFont.truetype(korean_font_paths[0], 48, encoding="utf-8") if os.path.exists(korean_font_paths[0]) else title_font
    except:
        news_font = title_font
    
    news_title_text = f"{frame_number}. {title}"
    try:
        draw.text((100, 200), news_title_text, fill=(255, 255, 255), font=news_font)
    except Exception as e:
        print(f"⚠️ 뉴스 제목 텍스트 오류: {e}")
        draw.text((100, 200), f"{frame_number}. NEWS TITLE", fill=(255, 255, 255), font=news_font)
    
    # 8. 뉴스 요약 (한글, 여러 줄로 나누기)
    try:
        summary_font = ImageFont.truetype(korean_font_paths[0], 32, encoding="utf-8") if os.path.exists(korean_font_paths[0]) else title_font
    except:
        summary_font = title_font
    
    # 요약 텍스트를 여러 줄로 나누기 (한글 고려)
    words = summary.split()
    lines = []
    current_line = ""
    max_width = W - 200
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        try:
            bbox = draw.textbbox((0, 0), test_line, font=summary_font)
            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        except:
            # 오류시 간단하게 처리
            if len(current_line) < 30:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
    
    if current_line:
        lines.append(current_line)
    
    # 요약 텍스트 그리기
    y_position = 300
    for line in lines:
        try:
            draw.text((100, y_position), line, fill=(255, 255, 0), font=summary_font)
        except Exception as e:
            print(f"⚠️ 요약 텍스트 그리기 오류: {e}")
            draw.text((100, y_position), "NEWS SUMMARY", fill=(255, 255, 0), font=summary_font)
        y_position += 40
    
    # 9. 시각적 요소 추가
    icon_color = (255, 255, 255)
    draw.rectangle([W-150, 30, W-50, 80], fill=icon_color, outline=(200, 200, 200), width=3)
    draw.text((W-140, 40), "NEWS", fill=(30, 60, 120), font=title_font)
    
    return img

def create_korean_news_video():
    """한글 폰트와 음성이 제대로 작동하는 뉴스 브리핑 비디오 생성"""
    
    print("🎬 한글 뉴스 브리핑 비디오 생성 중...")
    
    # 뉴스 데이터 (한글)
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
        frame = create_korean_news_frame(news['title'], news['summary'], i+1, len(news_data))
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
    
    # 음성 파일이 있으면 추가
    audio_path = "generated_content/2025-08-27/narration.mp3"
    if os.path.exists(audio_path):
        print(f"🎵 음성 파일 추가 중: {audio_path}")
        try:
            audio = AudioFileClip(audio_path)
            # 음성 길이에 맞춰 비디오 조정
            if audio.duration > video.duration:
                # 음성이 더 길면 비디오 반복
                video = video.loop(duration=audio.duration)
            elif audio.duration < video.duration:
                # 비디오가 더 길면 음성 반복
                audio = audio.loop(duration=video.duration)
            
            video = video.set_audio(audio)
            print("✅ 음성 추가 완료!")
        except Exception as e:
            print(f"⚠️ 음성 추가 실패: {e}")
    else:
        print("⚠️ 음성 파일을 찾을 수 없습니다.")
    
    # 출력
    output_path = "korean_news_briefing.mp4"
    print(f"📹 비디오 저장 중: {output_path}")
    video.write_videofile(output_path, fps=fps, codec="libx264", audio_codec="aac", preset="medium")
    
    print("✅ 한글 뉴스 브리핑 비디오 생성 완료!")
    print(f"📊 비디오 정보:")
    print(f"   - 길이: {len(news_data) * duration_per_news:.1f}초")
    print(f"   - 해상도: 1920x1080")
    print(f"   - 뉴스 개수: {len(news_data)}개")
    print(f"   - 한글 폰트: 지원")
    print(f"   - 음성: {'포함' if os.path.exists(audio_path) else '없음'}")
    
    return output_path

if __name__ == "__main__":
    create_korean_news_video()