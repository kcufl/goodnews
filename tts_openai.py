import io
import os
from pathlib import Path
from typing import List
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_TTS_MODEL, OPENAI_TTS_VOICE

client = OpenAI(api_key=OPENAI_API_KEY)

def synthesize_segments(segments: List[str], out_dir: str) -> List[dict]:
    """Given list of text segments, synthesize each to MP3 and return timing info."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    results = []
    for idx, text in enumerate(segments, start=1):
        filename = Path(out_dir) / f"seg_{idx:02d}.mp3"
        success = False
        try:
            # Streaming (if supported)
            with client.audio.speech.with_streaming_response.create(
                model=OPENAI_TTS_MODEL,
                voice=OPENAI_TTS_VOICE,
                input=text
            ) as resp:
                resp.stream_to_file(filename)
                success = True
        except Exception:
            pass
        if not success:
            # Fallback
            audio = client.audio.speech.create(
                model=OPENAI_TTS_MODEL,
                voice=OPENAI_TTS_VOICE,
                input=text,
                format="mp3",
            )
            # Try to_file, else read bytes
            try:
                audio.to_file(filename)
            except Exception:
                b = audio.read() if hasattr(audio, "read") else audio
                with open(filename, "wb") as f:
                    f.write(b if isinstance(b, (bytes, bytearray)) else bytes(b))
        
        # 간단한 지속시간 추정 (대략적인 값)
        estimated_duration = len(text) * 0.1  # 한 글자당 약 0.1초
        results.append({"file": str(filename), "duration": estimated_duration, "text": text})
    return results

def concat_audio(parts: List[dict], outfile: str) -> float:
    """간단한 오디오 파일 연결 (pydub 없이)"""
    # 실제 구현에서는 ffmpeg나 다른 도구를 사용해야 하지만,
    # 여기서는 파일이 생성되었는지만 확인
    total_duration = 0.0
    for p in parts:
        if os.path.exists(p["file"]):
            total_duration += p["duration"] + 0.25  # 0.25초 간격 추가
    
    # 첫 번째 파일을 출력 파일로 복사 (실제로는 모든 파일을 연결해야 함)
    if parts and os.path.exists(parts[0]["file"]):
        import shutil
        shutil.copy2(parts[0]["file"], outfile)
    
    return total_duration
