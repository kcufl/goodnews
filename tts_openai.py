import io
from pathlib import Path
from typing import List
from pydub import AudioSegment
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
        seg = AudioSegment.from_file(filename)
        results.append({"file": str(filename), "duration": seg.duration_seconds, "text": text})
    return results

def concat_audio(parts: List[dict], outfile: str) -> float:
    audio = AudioSegment.silent(duration=500)  # lead-in
    for p in parts:
        audio += AudioSegment.from_file(p["file"])
        audio += AudioSegment.silent(duration=250)
    audio.export(outfile, format="mp3")
    return len(audio) / 1000.0
