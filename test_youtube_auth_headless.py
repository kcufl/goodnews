#!/usr/bin/env python3
"""
브라우저 없는 YouTube API 인증 테스트
서버 환경에서 사용할 수 있는 인증 방법
"""

import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]

def test_youtube_auth_headless():
    """브라우저 없는 YouTube API 인증 테스트"""
    try:
        load_dotenv()
        
        # 클라이언트 시크릿 파일 확인
        client_secrets_file = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "./client_secret.json")
        
        if not os.path.exists(client_secrets_file):
            print("❌ client_secret.json 파일이 없습니다!")
            return False
        
        print(f"✅ 클라이언트 시크릿 파일 확인: {client_secrets_file}")
        
        # 인증 토큰 확인
        creds = None
        token_path = "token.json"
        
        if os.path.exists(token_path):
            print("🔄 기존 토큰 파일 확인 중...")
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        # 토큰이 없거나 만료된 경우
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 토큰 갱신 중...")
                creds.refresh(Request())
            else:
                print("🔄 새로운 인증 토큰 생성 중...")
                print("💡 브라우저가 열리지 않는 환경입니다.")
                print("다음 URL을 브라우저에서 열어 인증을 완료해주세요:")
                
                # OAuth 플로우 시작
                flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
                auth_url, _ = flow.authorization_url(prompt='consent')
                
                print(f"\n🔗 인증 URL: {auth_url}")
                print("\n📋 인증 방법:")
                print("1. 위 URL을 브라우저에서 열기")
                print("2. Google 계정으로 로그인")
                print("3. 권한 허용")
                print("4. 인증 코드를 복사")
                
                # 사용자로부터 인증 코드 입력 받기
                auth_code = input("\n인증 코드를 입력하세요: ").strip()
                
                if auth_code:
                    # 인증 코드로 토큰 교환
                    flow.fetch_token(code=auth_code)
                    creds = flow.credentials
                    
                    # 토큰 저장
                    with open(token_path, "w") as token:
                        token.write(creds.to_json())
                    print("✅ 토큰이 저장되었습니다.")
                else:
                    print("❌ 인증 코드가 입력되지 않았습니다.")
                    return False
        
        # YouTube 서비스 생성
        print("🔄 YouTube 서비스 연결 중...")
        youtube = build("youtube", "v3", credentials=creds)
        
        # 채널 정보 가져오기
        print("🔄 채널 정보 확인 중...")
        channels_response = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        ).execute()
        
        if channels_response.get("items"):
            channel = channels_response["items"][0]
            channel_title = channel["snippet"]["title"]
            channel_id = channel["id"]
            subscriber_count = channel["statistics"].get("subscriberCount", "비공개")
            
            print("✅ YouTube API 인증 성공!")
            print(f"   📺 채널명: {channel_title}")
            print(f"   🆔 채널 ID: {channel_id}")
            print(f"   👥 구독자 수: {subscriber_count}")
            
            return True
        else:
            print("❌ 채널 정보를 가져올 수 없습니다.")
            return False
            
    except Exception as e:
        print(f"❌ YouTube API 인증 실패: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 브라우저 없는 YouTube API 인증 테스트")
    print("=" * 50)
    
    if test_youtube_auth_headless():
        print("\n" + "=" * 50)
        print("🎉 인증 테스트 완료!")
        print("✅ YouTube API가 정상적으로 설정되었습니다.")
        print("💡 이제 뉴스 비디오를 자동으로 업로드할 수 있습니다.")
    else:
        print("\n" + "=" * 50)
        print("❌ 인증 테스트 실패")
        print("💡 인증 과정을 다시 확인해주세요.")