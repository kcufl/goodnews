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
    # 단순한 그라데이션 배경 (ColorClip 사용)
    # 어두운 회색에서 검은색으로 그라데이션 효과를 위해 여러 레이어 사용
    
    # 기본 배경 (어두운 회색)
    bg_base = ColorClip(size=(W, H), color=(30, 30, 30)).set_duration(duration)
    
    # 상단 바 (뉴스 채널 스타일)
    top_bar = ColorClip(size=(W, int(H * 0.06)), color=(50, 50, 50)).set_duration(duration)
    top_bar = top_bar.set_position((0, 0))
    
    # 좌측 세로 바
    left_bar = ColorClip(size=(int(W * 0.01), H), color=(70, 70, 70)).set_duration(duration)
    left_bar = left_bar.set_position((0, 0))
    
    # 하단 바 (자막 영역)
    bottom_bar = ColorClip(size=(W, int(H * 0.15)), color=(20, 20, 20)).set_duration(duration)
    bottom_bar = bottom_bar.set_position((0, H - int(H * 0.15)))
    
    # 모든 레이어 합성
    return CompositeVideoClip([bg_base, top_bar, left_bar, bottom_bar])

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
