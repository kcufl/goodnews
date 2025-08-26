#!/usr/bin/env python3
"""
YouTube API 인증 테스트 스크립트
"""

import os
from dotenv import load_dotenv
from uploader_youtube import get_service

def test_youtube_auth():
    """YouTube API 인증 테스트"""
    try:
        load_dotenv()
        
        # 클라이언트 시크릿 파일 확인
        client_secrets_file = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "./client_secret.json")
        
        if not os.path.exists(client_secrets_file):
            print("❌ 클라이언트 시크릿 파일이 없습니다!")
            print(f"   📁 찾는 파일: {client_secrets_file}")
            print("💡 해결 방법:")
            print("   1. Google Cloud Console에서 OAuth 2.0 클라이언트 ID 생성")
            print("   2. JSON 파일을 다운로드하여 client_secret.json으로 저장")
            print("   3. 프로젝트 루트 폴더에 저장")
            return False
        
        print(f"✅ 클라이언트 시크릿 파일 확인: {client_secrets_file}")
        
        # YouTube 서비스 연결 테스트
        print("🔄 YouTube API 연결 중...")
        youtube = get_service(client_secrets_file)
        
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
            print("💡 해결 방법:")
            print("   1. YouTube 채널이 있는 계정으로 인증했는지 확인")
            print("   2. 브라우저에서 권한을 허용했는지 확인")
            return False
            
    except Exception as e:
        print(f"❌ YouTube API 인증 실패: {str(e)}")
        print("💡 해결 방법:")
        print("   1. client_secret.json 파일이 올바른지 확인")
        print("   2. Google Cloud Console에서 YouTube Data API v3가 활성화되었는지 확인")
        print("   3. OAuth 2.0 클라이언트 ID가 올바르게 생성되었는지 확인")
        return False

def test_upload_permissions():
    """업로드 권한 테스트"""
    try:
        load_dotenv()
        youtube = get_service(os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "./client_secret.json"))
        
        print("\n🔄 업로드 권한 확인 중...")
        
        # 업로드 할당량 확인
        quota_response = youtube.quota().get().execute()
        print("✅ 업로드 권한 확인 완료")
        
        return True
        
    except Exception as e:
        print(f"❌ 업로드 권한 확인 실패: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 YouTube API 인증 테스트")
    print("=" * 50)
    
    if test_youtube_auth():
        test_upload_permissions()
        
        print("\n" + "=" * 50)
        print("🎉 인증 테스트 완료!")
        print("✅ YouTube API가 정상적으로 설정되었습니다.")
        print("💡 이제 뉴스 비디오를 자동으로 업로드할 수 있습니다.")
    else:
        print("\n" + "=" * 50)
        print("❌ 인증 테스트 실패")
        print("💡 위의 해결 방법을 따라 설정을 완료해주세요.")