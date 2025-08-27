from moviepy.editor import (AudioFileClip, ImageClip, TextClip, CompositeVideoClip, ColorClip)
from typing import List, Dict, Tuple
from pathlib import Path
import srt, datetime
import PIL
import numpy as np

def parse_resolution(res: str) -> Tuple[int,int]:
    w,h = res.split("x")
    return int(w), int(h)

def create_news_background(W: int, H: int, duration: float):
    """뉴스 스타일의 동적 배경 생성"""
    # 그라데이션 배경 생성
    gradient = np.zeros((H, W, 3), dtype=np.uint8)
    
    # 파란색에서 어두운 파란색으로 그라데이션
    for y in range(H):
        intensity = int(40 + (y / H) * 20)  # 40-60 범위
        gradient[y, :] = [intensity//2, intensity//3, intensity]
    
    # 뉴스 스타일 요소 추가 (오버레이)
    overlay = np.zeros((H, W, 3), dtype=np.uint8)
    
    # 상단 바
    bar_height = int(H * 0.08)
    overlay[:bar_height, :] = [30, 50, 100]
    
    # 좌측 세로 바
    bar_width = int(W * 0.02)
    overlay[:, :bar_width] = [50, 80, 150]
    
    # 하단 바
    bottom_bar_height = int(H * 0.12)
    overlay[H-bottom_bar_height:, :] = [20, 30, 60]
    
    # 배경 합성
    background = np.clip(gradient + overlay * 0.3, 0, 255).astype(np.uint8)
    
    # ColorClip으로 변환
    return ColorClip(size=(W, H), color=background[0, 0].tolist()).set_duration(duration)

def build_srt(segments: List[dict], srt_path: str):
    subs = []
    for i, seg in enumerate(segments, start=1):
        start = datetime.timedelta(seconds=float(seg["start"]))
        end = datetime.timedelta(seconds=float(seg["end"]))
        subs.append(srt.Subtitle(index=i, start=start, end=end, content=seg["text"]))
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subs))

def make_video(audio_path: str, timeline: List[dict], background_image: str, resolution: str, title: str, out_path: str, mode: str="landscape"):
    W,H = parse_resolution(resolution)
    
    # 배경 이미지 사용 시도
    if background_image and Path(background_image).exists():
        try:
            # PIL 호환성을 위한 resize 설정
            bg = ImageClip(background_image).resize(newsize=(W,H)).set_duration(timeline[-1]["end"] + 1.0)
            print(f"✅ 배경 이미지 사용: {background_image}")
        except Exception as e:
            print(f"⚠️ 배경 이미지 로드 실패, 뉴스 스타일 배경 사용: {e}")
            # 뉴스 스타일 배경 사용
            bg = create_news_background(W, H, timeline[-1]["end"] + 1.0)
    else:
        # 뉴스 스타일 배경 사용
        print("🎨 뉴스 스타일 배경 생성 중...")
        bg = create_news_background(W, H, timeline[-1]["end"] + 1.0)

    # Title with shadow effect
    title_clip = TextClip(txt=title, fontsize=64 if mode=="shorts" else 54, color="white", 
                         method="caption", size=(W-120, None), align="West")
    title_pos = ("center", 80) if mode=="landscape" else ("center", 80)
    title_clip = title_clip.set_position(title_pos).set_start(0).set_duration(3.0)

    text_clips = [title_clip]
    for i, seg in enumerate(timeline):
        dur = max(2.0, min(5.0, seg["end"]-seg["start"]))
        fontsize = 58 if mode=="shorts" else 42
        width_margin = 80 if mode=="shorts" else 140
        y_pos = int(H*0.70) if mode=="landscape" else int(H*0.80)
        
        # 뉴스 번호와 함께 표시
        news_text = f"{i+1}. {seg['headline']}"
        txt = TextClip(txt=news_text, fontsize=fontsize, color="white", 
                      method="caption", size=(W-width_margin, None), align="West")
        text_clips.append(txt.set_position((40, y_pos)).set_start(seg["start"]).set_duration(dur))

    audio = AudioFileClip(audio_path)
    comp = CompositeVideoClip([bg, *text_clips]).set_audio(audio)
    comp.write_videofile(out_path, fps=30, codec="libx264", audio_codec="aac", preset="medium")
