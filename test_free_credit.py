#!/usr/bin/env python3
"""
무료 크레딧 계정 테스트 스크립트
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

def test_with_different_models():
    """다양한 모델로 테스트"""
    models_to_test = [
        "gpt-3.5-turbo",
        "gpt-4o-mini", 
        "gpt-4o-mini-2024-07-18"
    ]
    
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    for model in models_to_test:
        try:
            print(f"🔄 {model} 모델로 테스트 중...")
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            
            result = response.choices[0].message.content
            print(f"✅ {model} 성공: {result}")
            return True
            
        except Exception as e:
            print(f"❌ {model} 실패: {str(e)}")
            continue
    
    return False

def test_billing_status():
    """결제 상태 확인"""
    try:
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        print("🔄 결제 상태 확인 중...")
        
        # 간단한 요청으로 결제 상태 확인
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=1
        )
        
        print("✅ 결제 상태: 정상 (무료 크레딧 사용 가능)")
        return True
        
    except Exception as e:
        error_msg = str(e)
        if "insufficient_quota" in error_msg:
            print("❌ 무료 크레딧이 소진되었거나 결제 정보가 필요합니다.")
            print("💡 해결 방법:")
            print("   1. OpenAI 계정에서 무료 크레딧 잔액 확인")
            print("   2. 결제 정보 추가 (무료 크레딧 사용 후)")
            print("   3. 새로운 계정으로 무료 크레딧 받기")
        else:
            print(f"❌ 기타 오류: {error_msg}")
        return False

def check_api_key_format():
    """API 키 형식 확인"""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    print(f"🔍 API 키 형식 확인:")
    print(f"   - 길이: {len(api_key)} 문자")
    print(f"   - 접두사: {api_key[:10]}...")
    
    if api_key.startswith("sk-proj-"):
        print("   - 유형: 프로젝트 API 키 (정상)")
    elif api_key.startswith("sk-"):
        print("   - 유형: 일반 API 키 (정상)")
    else:
        print("   - 유형: 알 수 없는 형식")

if __name__ == "__main__":
    print("🎯 무료 크레딧 계정 테스트")
    print("=" * 50)
    
    check_api_key_format()
    
    print("\n" + "=" * 50)
    test_billing_status()
    
    print("\n" + "=" * 50)
    test_with_different_models()
    
    print("\n" + "=" * 50)
    print("💡 추가 확인사항:")
    print("1. OpenAI 계정에서 무료 크레딧 잔액 확인")
    print("2. 계정 생성 후 90일이 지났는지 확인")
    print("3. 다른 브라우저나 기기에서 로그인 시도")