from moviepy.editor import (AudioFileClip, ImageClip, TextClip, CompositeVideoClip, ColorClip)
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
    W,H = parse_resolution(resolution)
    if background_image and Path(background_image).exists():
        bg = ImageClip(background_image).resize(newsize=(W,H)).set_duration(timeline[-1]["end"] + 1.0)
    else:
        bg = ColorClip(size=(W,H), color=(10,10,20)).set_duration(timeline[-1]["end"] + 1.0)

    # Title
    title_clip = TextClip(txt=title, fontsize=64 if mode=="shorts" else 54, color="white", method="caption", size=(W-120, None), align="West")
    title_pos = ("center","top") if mode=="landscape" else ("center","top")
    title_clip = title_clip.set_position(title_pos).set_start(0).set_duration(3.0)

    text_clips = [title_clip]
    for seg in timeline:
        dur = max(2.0, min(5.0, seg["end"]-seg["start"]))
        fontsize = 58 if mode=="shorts" else 42
        width_margin = 80 if mode=="shorts" else 140
        y_pos = int(H*0.70) if mode=="landscape" else int(H*0.80)
        txt = TextClip(txt=seg["headline"], fontsize=fontsize, color="white", method="caption", size=(W-width_margin, None), align="West")
        text_clips.append(txt.set_position((40, y_pos)).set_start(seg["start"]).set_duration(dur))

    audio = AudioFileClip(audio_path)
    comp = CompositeVideoClip([bg, *text_clips]).set_audio(audio)
    comp.write_videofile(out_path, fps=30, codec="libx264", audio_codec="aac", preset="medium")
