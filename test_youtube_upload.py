#!/usr/bin/env python3
"""
YouTube 업로드 테스트 스크립트
간단한 테스트 비디오를 업로드하여 기능을 확인합니다.
"""

import os
from dotenv import load_dotenv
from uploader_youtube import get_service, upload_video

def create_test_video():
    """간단한 테스트 비디오 생성"""
    try:
        from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
        
        print("🎬 테스트 비디오 생성 중...")
        
        # 5초짜리 간단한 비디오 생성
        duration = 5
        size = (1280, 720)
        
        # 배경 (파란색)
        background = ColorClip(size=size, color=(0, 100, 200), duration=duration)
        
        # 텍스트
        text = TextClip(
            "YouTube API 테스트\n성공!", 
            fontsize=60, 
            color='white',
            method='caption',
            size=(size[0]-100, None)
        ).set_position('center').set_duration(duration)
        
        # 합성
        video = CompositeVideoClip([background, text])
        
        # 저장
        output_path = "test_video.mp4"
        video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")
        
        print(f"✅ 테스트 비디오 생성 완료: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ 테스트 비디오 생성 실패: {str(e)}")
        return None

def test_youtube_upload():
    """YouTube 업로드 테스트"""
    try:
        load_dotenv()
        
        # 클라이언트 시크릿 파일 확인
        client_secrets_file = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "./client_secret.json")
        
        if not os.path.exists(client_secrets_file):
            print("❌ client_secret.json 파일이 없습니다!")
            print("💡 YouTube API 설정 가이드를 따라 설정해주세요.")
            return False
        
        # YouTube 서비스 연결
        print("🔄 YouTube 서비스 연결 중...")
        youtube = get_service(client_secrets_file)
        
        # 테스트 비디오 생성
        video_path = create_test_video()
        if not video_path:
            return False
        
        # 업로드
        print("🔄 YouTube에 업로드 중...")
        title = "YouTube API 테스트 - AI 뉴스 브리핑"
        description = """
이것은 AI 뉴스 브리핑 시스템의 YouTube API 테스트입니다.

테스트 목적으로 업로드된 비디오입니다.
        """.strip()
        
        video_id = upload_video(
            youtube=youtube,
            file_path=video_path,
            title=title,
            description=description,
            tags=["테스트", "AI", "뉴스", "브리핑"],
            privacy_status="unlisted",  # 테스트용으로 비공개
            thumbnail_path=None
        )
        
        print("✅ YouTube 업로드 성공!")
        print(f"   🎥 비디오 ID: {video_id}")
        print(f"   🔗 링크: https://youtu.be/{video_id}")
        print(f"   📺 상태: 비공개 (테스트용)")
        
        # 테스트 파일 정리
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"   🗑️ 테스트 파일 정리: {video_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ YouTube 업로드 테스트 실패: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 YouTube 업로드 테스트")
    print("=" * 50)
    
    if test_youtube_upload():
        print("\n" + "=" * 50)
        print("🎉 업로드 테스트 완료!")
        print("✅ YouTube API 업로드 기능이 정상적으로 작동합니다.")
        print("💡 이제 뉴스 비디오를 자동으로 업로드할 수 있습니다.")
    else:
        print("\n" + "=" * 50)
        print("❌ 업로드 테스트 실패")
        print("💡 설정을 다시 확인해주세요.")