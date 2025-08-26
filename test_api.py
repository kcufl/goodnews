#!/usr/bin/env python3
"""
API 키 테스트 스크립트
OpenAI API가 제대로 작동하는지 확인합니다.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

def test_openai_api():
    """OpenAI API 연결 및 간단한 테스트"""
    try:
        # 환경 변수 로드
        load_dotenv()
        
        # API 키 확인
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY가 설정되지 않았습니다.")
            return False
        
        print(f"✅ API 키 확인됨: {api_key[:20]}...")
        
        # OpenAI 클라이언트 생성
        client = OpenAI(api_key=api_key)
        
        # 간단한 테스트 요청
        print("🔄 OpenAI API 테스트 중...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "안녕하세요! 간단한 테스트입니다. 'Hello World'라고 한국어로 응답해주세요."}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ API 테스트 성공!")
        print(f"📝 응답: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ API 테스트 실패: {str(e)}")
        return False

def test_tts_api():
    """TTS API 테스트"""
    try:
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        print("🔄 TTS API 테스트 중...")
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input="안녕하세요. TTS 테스트입니다."
        )
        
        # 오디오 파일로 저장
        with open("test_tts.mp3", "wb") as f:
            f.write(response.content)
        
        print("✅ TTS 테스트 성공! test_tts.mp3 파일이 생성되었습니다.")
        return True
        
    except Exception as e:
        print(f"❌ TTS 테스트 실패: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 OpenAI API 테스트 시작")
    print("=" * 50)
    
    # 기본 API 테스트
    if test_openai_api():
        print("\n" + "=" * 50)
        # TTS 테스트
        test_tts_api()
    
    print("\n" + "=" * 50)
    print("🏁 테스트 완료")