# from moviepy.editor import (AudioFileClip, ImageClip, TextClip, CompositeVideoClip, ColorClip)
from typing import List, Dict, Tuple
from pathlib import Path
import srt, datetime

def parse_resolution(res: str) -> Tuple[int,int]:
    w,h = res.split("x")
    return int(w), int(h)

def build_srt(segments: List[dict], srt_path: str):
    subs = []
    for i, seg in enumerate(segments, start=1):
        start = datetime.timedelta(seconds=float(seg["start"]))
        end = datetime.timedelta(seconds=float(seg["end"]))
        subs.append(srt.Subtitle(index=i, start=start, end=end, content=seg["text"]))
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subs))

def make_video(audio_path: str, timeline: List[dict], background_image: str, resolution: str, title: str, out_path: str, mode: str="landscape"):
    """간단한 비디오 생성 (moviepy 없이)"""
    W,H = parse_resolution(resolution)
    
    # 실제 비디오 생성 대신 더미 파일 생성
    print(f"비디오 생성 시뮬레이션: {out_path}")
    print(f"해상도: {W}x{H}")
    print(f"제목: {title}")
    print(f"모드: {mode}")
    print(f"오디오 파일: {audio_path}")
    print(f"타임라인 항목 수: {len(timeline)}")
    
    # 더미 비디오 파일 생성 (실제로는 비디오가 생성되지 않음)
    with open(out_path, "w") as f:
        f.write(f"# 더미 비디오 파일\n")
        f.write(f"# 해상도: {W}x{H}\n")
        f.write(f"# 제목: {title}\n")
        f.write(f"# 모드: {mode}\n")
        f.write(f"# 오디오: {audio_path}\n")
    
    print(f"더미 비디오 파일 생성됨: {out_path}")
