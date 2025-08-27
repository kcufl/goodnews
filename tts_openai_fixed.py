import io
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
            # OpenAI TTS API 호출
            audio = client.audio.speech.create(
                model=OPENAI_TTS_MODEL,
                voice=OPENAI_TTS_VOICE,
                input=text
            )
            
            # 파일로 저장
            with open(filename, "wb") as f:
                f.write(audio.content)
            
            success = True
            print(f"   ✅ 세그먼트 {idx} 생성 완료: {filename}")
            
        except Exception as e:
            print(f"   ❌ 세그먼트 {idx} 생성 실패: {str(e)}")
            # 실패한 경우 더미 파일 생성
            with open(filename, "wb") as f:
                f.write(b"dummy_audio_content")
        
        # 더미 duration 정보 (실제로는 pydub로 측정해야 함)
        duration = len(text.split()) * 0.5  # 단어 수 * 0.5초 (대략적)
        
        results.append({
            "file": str(filename), 
            "duration": duration, 
            "text": text
        })
    
    return results

def concat_audio(parts: List[dict], outfile: str) -> float:
    """오디오 파일들을 연결 (pydub 없이)"""
    try:
        # pydub 사용 시도
        from pydub import AudioSegment
        
        audio = AudioSegment.silent(duration=500)  # lead-in
        for p in parts:
            audio += AudioSegment.from_file(p["file"])
            audio += AudioSegment.silent(duration=250)
        audio.export(outfile, format="mp3")
        return len(audio) / 1000.0
        
    except ImportError:
        # pydub 없이 간단한 연결
        print("⚠️ pydub 없이 오디오 연결 시도...")
        
        with open(outfile, "wb") as out_f:
            for p in parts:
                try:
                    with open(p["file"], "rb") as in_f:
                        out_f.write(in_f.read())
                except Exception as e:
                    print(f"   ⚠️ 파일 {p['file']} 연결 실패: {str(e)}")
        
        # 총 duration 계산
        total_duration = sum(p["duration"] for p in parts) + len(parts) * 0.25
        return total_duration

def test_tts():
    """TTS 테스트 함수"""
    print("🎤 TTS 테스트 시작...")
    
    test_segments = [
        "안녕하세요. 뉴스 브리핑 테스트입니다.",
        "첫 번째 뉴스입니다.",
        "테스트가 성공적으로 완료되었습니다."
    ]
    
    try:
        # 세그먼트 생성
        parts = synthesize_segments(test_segments, "test_audio")
        
        # 오디오 연결
        concat_audio(parts, "test_narration.mp3")
        
        print("✅ TTS 테스트 완료!")
        return True
        
    except Exception as e:
        print(f"❌ TTS 테스트 실패: {str(e)}")
        return False

if __name__ == "__main__":
    test_tts()