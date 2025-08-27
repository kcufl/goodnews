#!/usr/bin/env python3
"""
빠른 YouTube API 테스트 (30초 타임아웃)
"""

import os
import signal
import time
from dotenv import load_dotenv

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("30초 타임아웃")

def test_youtube_quick():
    """30초 타임아웃으로 빠른 테스트"""
    try:
        # 30초 타임아웃 설정
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)
        
        load_dotenv()
        
        # 클라이언트 시크릿 파일 확인
        client_secrets_file = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "./client_secret.json")
        
        if not os.path.exists(client_secrets_file):
            print("❌ client_secret.json 파일이 없습니다!")
            return False
        
        print(f"✅ 클라이언트 시크릿 파일 확인: {client_secrets_file}")
        
        # 간단한 연결 테스트
        print("🔄 YouTube API 연결 테스트 중... (30초 제한)")
        
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        
        SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
        
        # OAuth 플로우 시작
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
        auth_url, _ = flow.authorization_url(prompt='consent')
        
        print(f"🔗 인증 URL: {auth_url}")
        print("⏰ 30초 후 자동 취소됩니다...")
        
        # 사용자 입력 대기 (30초 제한)
        auth_code = input("인증 코드를 입력하세요 (30초 제한): ").strip()
        
        if not auth_code:
            print("❌ 인증 코드가 입력되지 않았습니다.")
            return False
        
        # 토큰 교환
        flow.fetch_token(code=auth_code)
        creds = flow.credentials
        
        # YouTube 서비스 생성
        youtube = build("youtube", "v3", credentials=creds)
        
        # 간단한 API 호출 테스트
        channels_response = youtube.channels().list(
            part="snippet",
            mine=True
        ).execute()
        
        if channels_response.get("items"):
            channel = channels_response["items"][0]
            channel_title = channel["snippet"]["title"]
            
            print("✅ YouTube API 연결 성공!")
            print(f"   📺 채널명: {channel_title}")
            
            # 토큰 저장
            with open("token.json", "w") as token:
                token.write(creds.to_json())
            print("   💾 토큰이 저장되었습니다.")
            
            signal.alarm(0)  # 타임아웃 해제
            return True
        else:
            print("❌ 채널 정보를 가져올 수 없습니다.")
            return False
            
    except TimeoutError:
        print("⏰ 30초 타임아웃! 다른 방법을 시도합니다.")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False
    finally:
        signal.alarm(0)  # 타임아웃 해제

def provide_alternatives():
    """대안 방법 제시"""
    print("\n" + "="*60)
    print("🔄 대안 방법들")
    print("="*60)
    
    print("1️⃣ 로컬 환경에서 테스트:")
    print("   - 로컬 컴퓨터에서 같은 코드 실행")
    print("   - 브라우저가 자동으로 열림")
    
    print("\n2️⃣ 수동 인증:")
    print("   - Google Cloud Console에서 직접 테스트")
    print("   - API 탐색기 사용")
    
    print("\n3️⃣ 설정 확인:")
    print("   - OAuth 동의 화면 설정 확인")
    print("   - API 활성화 상태 확인")
    
    print("\n4️⃣ 전체 시스템 테스트 (YouTube 제외):")
    print("   - 뉴스 수집 및 요약 테스트")
    print("   - TTS 및 비디오 생성 테스트")

if __name__ == "__main__":
    print("🎯 빠른 YouTube API 테스트 (30초 타임아웃)")
    print("="*50)
    
    if test_youtube_quick():
        print("\n" + "="*50)
        print("🎉 테스트 성공!")
        print("✅ YouTube API가 정상적으로 설정되었습니다.")
    else:
        print("\n" + "="*50)
        print("❌ 테스트 실패 또는 타임아웃")
        provide_alternatives()