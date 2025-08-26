#!/usr/bin/env python3
"""
Google Cloud Console 설정 도우미
설정 과정을 단계별로 안내하고 확인합니다.
"""

import os
import json
import webbrowser
from pathlib import Path

def print_step(step_num, title, description):
    """단계별 안내 출력"""
    print(f"\n{'='*60}")
    print(f"📋 단계 {step_num}: {title}")
    print(f"{'='*60}")
    print(description)
    print(f"{'='*60}")

def check_file_exists(filename):
    """파일 존재 여부 확인"""
    return Path(filename).exists()

def validate_client_secret_json(filename):
    """client_secret.json 파일 유효성 검사"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        required_keys = ['installed', 'client_id', 'client_secret', 'auth_uri', 'token_uri']
        if 'installed' not in data:
            return False, "OAuth 2.0 클라이언트 ID가 아닙니다. '데스크톱 앱'으로 생성했는지 확인하세요."
        
        installed = data['installed']
        for key in required_keys[1:]:
            if key not in installed:
                return False, f"필수 키 '{key}'가 없습니다."
        
        return True, "파일이 유효합니다."
    except json.JSONDecodeError:
        return False, "JSON 파일 형식이 올바르지 않습니다."
    except Exception as e:
        return False, f"파일 읽기 오류: {str(e)}"

def setup_assistant():
    """설정 도우미 메인 함수"""
    print("🎯 Google Cloud Console 설정 도우미")
    print("YouTube API 설정을 단계별로 안내합니다.")
    
    # 1단계: Google Cloud Console 접속
    print_step(1, "Google Cloud Console 접속", """
1. 브라우저에서 https://console.cloud.google.com/ 접속
2. Google 계정으로 로그인
3. 새 프로젝트 생성 준비
""")
    
    input("준비가 되면 Enter를 눌러주세요...")
    
    # 2단계: 프로젝트 생성
    print_step(2, "프로젝트 생성", """
1. 상단의 "프로젝트 선택" 드롭다운 클릭
2. "새 프로젝트" 클릭
3. 프로젝트 이름: AI-News-Briefing
4. "만들기" 클릭
5. 프로젝트 생성 완료까지 대기 (1-2분)
""")
    
    input("프로젝트 생성이 완료되면 Enter를 눌러주세요...")
    
    # 3단계: YouTube API 활성화
    print_step(3, "YouTube Data API v3 활성화", """
1. 왼쪽 메뉴에서 "API 및 서비스" → "라이브러리" 클릭
2. 검색창에 "YouTube Data API v3" 입력
3. "YouTube Data API v3" 클릭
4. "사용" 버튼 클릭
""")
    
    input("API 활성화가 완료되면 Enter를 눌러주세요...")
    
    # 4단계: OAuth 동의 화면 설정
    print_step(4, "OAuth 동의 화면 설정", """
1. "API 및 서비스" → "사용자 인증 정보" 클릭
2. "OAuth 동의 화면" 탭 클릭
3. "외부" 선택 → "만들기" 클릭
4. 앱 정보 입력:
   - 앱 이름: AI News Briefing
   - 사용자 지원 이메일: 본인 이메일
   - 개발자 연락처 정보: 본인 이메일
5. "저장 후 계속" 클릭
6. 범위 추가: "YouTube Data API v3" 선택
7. 테스트 사용자: 본인 이메일 추가
""")
    
    input("OAuth 동의 화면 설정이 완료되면 Enter를 눌러주세요...")
    
    # 5단계: OAuth 클라이언트 ID 생성
    print_step(5, "OAuth 2.0 클라이언트 ID 생성", """
1. "사용자 인증 정보" 탭 클릭
2. "사용자 인증 정보 만들기" → "OAuth 클라이언트 ID" 클릭
3. 애플리케이션 유형: "데스크톱 앱" 선택
4. 이름: AI News Briefing Desktop Client
5. "만들기" 클릭
6. 생성된 클라이언트 ID 클릭
7. "JSON 다운로드" 클릭
""")
    
    input("JSON 파일 다운로드가 완료되면 Enter를 눌러주세요...")
    
    # 6단계: 파일 저장 및 확인
    print_step(6, "파일 저장 및 확인", """
1. 다운로드된 JSON 파일을 'client_secret.json'으로 이름 변경
2. 프로젝트 루트 폴더에 저장
3. 파일 권한 설정: chmod 600 client_secret.json
""")
    
    # 파일 존재 확인
    while not check_file_exists("client_secret.json"):
        print("❌ client_secret.json 파일을 찾을 수 없습니다.")
        print("파일이 프로젝트 루트 폴더에 저장되었는지 확인해주세요.")
        input("파일을 저장한 후 Enter를 눌러주세요...")
    
    # 파일 유효성 검사
    is_valid, message = validate_client_secret_json("client_secret.json")
    if not is_valid:
        print(f"❌ 파일 유효성 검사 실패: {message}")
        print("Google Cloud Console에서 다시 OAuth 2.0 클라이언트 ID를 생성해주세요.")
        return False
    
    print("✅ client_secret.json 파일이 유효합니다!")
    
    # 7단계: 인증 테스트
    print_step(7, "인증 테스트", """
이제 YouTube API 인증을 테스트합니다.
브라우저가 열리면 Google 계정으로 로그인하고 권한을 허용해주세요.
""")
    
    input("인증 테스트를 시작하려면 Enter를 눌러주세요...")
    
    # 인증 테스트 실행
    try:
        from test_youtube_auth import test_youtube_auth
        if test_youtube_auth():
            print("\n🎉 설정이 완료되었습니다!")
            return True
        else:
            print("\n❌ 인증 테스트에 실패했습니다.")
            return False
    except ImportError:
        print("❌ test_youtube_auth.py 파일을 찾을 수 없습니다.")
        return False
    except Exception as e:
        print(f"❌ 인증 테스트 중 오류 발생: {str(e)}")
        return False

def main():
    """메인 함수"""
    print("🚀 AI 뉴스 브리핑 YouTube API 설정 도우미")
    print("이 도구는 Google Cloud Console 설정을 단계별로 안내합니다.")
    
    choice = input("\n설정을 시작하시겠습니까? (y/n): ").lower()
    if choice != 'y':
        print("설정을 취소했습니다.")
        return
    
    if setup_assistant():
        print("\n" + "="*60)
        print("🎉 모든 설정이 완료되었습니다!")
        print("이제 뉴스 브리핑 시스템을 사용할 수 있습니다.")
        print("\n다음 단계:")
        print("1. python main.py - 전체 시스템 테스트")
        print("2. python test_youtube_upload.py - 업로드 테스트")
        print("3. 자동화 설정 (cron 등)")
    else:
        print("\n" + "="*60)
        print("❌ 설정에 실패했습니다.")
        print("위의 단계를 다시 확인하고 재시도해주세요.")

if __name__ == "__main__":
    main()