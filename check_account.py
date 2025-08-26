#!/usr/bin/env python3
"""
OpenAI 계정 상태 확인 스크립트
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

def check_account_status():
    """계정 상태 확인"""
    try:
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        print("🔄 계정 정보 확인 중...")
        
        # 사용량 정보 확인 (가능한 경우)
        try:
            usage = client.usage.list()
            print("✅ 사용량 정보:")
            print(f"  - 사용량 데이터: {len(usage.data)} 개의 기록")
        except Exception as e:
            print(f"⚠️ 사용량 정보 조회 실패: {str(e)}")
        
        # 모델 목록으로 연결 상태 확인
        models = client.models.list()
        print(f"✅ 연결 상태: 정상 (사용 가능한 모델: {len(models.data)}개)")
        
        # API 키 정보 확인
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key.startswith("sk-proj-"):
            print("✅ API 키 유형: 프로젝트 API 키")
        else:
            print("✅ API 키 유형: 일반 API 키")
        
        return True
        
    except Exception as e:
        print(f"❌ 계정 상태 확인 실패: {str(e)}")
        return False

def test_minimal_request():
    """최소한의 요청으로 테스트"""
    try:
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        print("🔄 최소 요청 테스트 중...")
        
        # 가장 간단한 요청
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "1"}],
            max_tokens=1
        )
        
        print("✅ 최소 요청 성공!")
        return True
        
    except Exception as e:
        print(f"❌ 최소 요청 실패: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 OpenAI 계정 상태 확인")
    print("=" * 50)
    
    check_account_status()
    
    print("\n" + "=" * 50)
    test_minimal_request()
    
    print("\n" + "=" * 50)
    print("💡 해결 방법:")
    print("1. OpenAI 계정에 로그인하여 결제 정보 확인")
    print("2. 신용카드 정보가 유효한지 확인")
    print("3. 무료 계정의 경우 월별 한도 확인")
    print("4. 새로운 API 키 생성 시도")