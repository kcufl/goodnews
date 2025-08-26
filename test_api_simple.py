#!/usr/bin/env python3
"""
간단한 API 키 테스트 스크립트
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

def test_simple_api():
    """간단한 API 테스트"""
    try:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            print("❌ API 키가 설정되지 않았습니다.")
            return False
        
        print(f"✅ API 키 확인: {api_key[:20]}...")
        
        client = OpenAI(api_key=api_key)
        
        # 더 간단한 요청으로 테스트
        print("🔄 간단한 API 테스트 중...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 더 저렴한 모델 사용
            messages=[
                {"role": "user", "content": "Hi"}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ API 테스트 성공!")
        print(f"📝 응답: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ API 테스트 실패: {str(e)}")
        return False

def test_models_list():
    """사용 가능한 모델 목록 확인"""
    try:
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        print("🔄 사용 가능한 모델 확인 중...")
        models = client.models.list()
        
        print("✅ 사용 가능한 모델:")
        for model in models.data[:5]:  # 처음 5개만 표시
            print(f"  - {model.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ 모델 목록 조회 실패: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 간단한 OpenAI API 테스트")
    print("=" * 40)
    
    test_simple_api()
    
    print("\n" + "=" * 40)
    test_models_list()
    
    print("\n" + "=" * 40)
    print("🏁 테스트 완료")