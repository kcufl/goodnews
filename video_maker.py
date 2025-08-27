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
    """일반적인 뉴스 스타일의 배경 생성"""
    # 그라데이션 배경 생성
    gradient = np.zeros((H, W, 3), dtype=np.uint8)
    
    # 어두운 회색에서 검은색으로 그라데이션 (일반적인 뉴스 스타일)
    for y in range(H):
        intensity = int(20 + (y / H) * 15)  # 20-35 범위
        gradient[y, :] = [intensity, intensity, intensity]
    
    # 뉴스 스타일 요소 추가 (오버레이)
    overlay = np.zeros((H, W, 3), dtype=np.uint8)
    
    # 상단 바 (뉴스 채널 스타일)
    bar_height = int(H * 0.06)
    overlay[:bar_height, :] = [40, 40, 40]
    
    # 좌측 세로 바 (더 얇게)
    bar_width = int(W * 0.01)
    overlay[:, :bar_width] = [60, 60, 60]
    
    # 하단 바 (자막 영역)
    bottom_bar_height = int(H * 0.15)
    overlay[H-bottom_bar_height:, :] = [15, 15, 15]
    
    # 배경 합성
    background = np.clip(gradient + overlay * 0.4, 0, 255).astype(np.uint8)
    
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
        dur = max(2.0, min(8.0, seg["end"]-seg["start"]))
        width_margin = 80 if mode=="shorts" else 140
        
        # 헤드라인 (큰 글씨, 상단)
        headline_fontsize = 48 if mode=="shorts" else 36
        headline_y_pos = int(H*0.25) if mode=="landscape" else int(H*0.30)
        headline_text = f"{i+1}. {seg['headline']}"
        headline_clip = TextClip(txt=headline_text, fontsize=headline_fontsize, color="white", 
                               method="caption", size=(W-width_margin, None), align="West")
        text_clips.append(headline_clip.set_position((40, headline_y_pos)).set_start(seg["start"]).set_duration(dur))
        
        # 요약 내용 (작은 글씨, 하단)
        if "summary" in seg and seg["summary"]:
            summary_fontsize = 32 if mode=="shorts" else 24
            summary_y_pos = int(H*0.45) if mode=="landscape" else int(H*0.50)
            summary_text = seg["summary"]
            summary_clip = TextClip(txt=summary_text, fontsize=summary_fontsize, color="lightblue", 
                                  method="caption", size=(W-width_margin, None), align="West")
            text_clips.append(summary_clip.set_position((40, summary_y_pos)).set_start(seg["start"]).set_duration(dur))

    audio = AudioFileClip(audio_path)
    comp = CompositeVideoClip([bg, *text_clips]).set_audio(audio)
    comp.write_videofile(out_path, fps=30, codec="libx264", audio_codec="aac", preset="medium")
