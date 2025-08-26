import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]

def get_service(client_secrets_file: str):
    creds = None
    token_path = "token.json"
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

def upload_video(youtube, file_path: str, title: str, description: str, tags=None, privacy_status="unlisted", thumbnail_path: str=None):
    body = dict(
        snippet=dict(
            title=title,
            description=description,
            tags=tags or [],
            categoryId="25"
        ),
        status=dict(
            privacyStatus=privacy_status,
            selfDeclaredMadeForKids=False
        )
    )
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress()*100)}%")
    video_id = response.get("id")
    print("Upload complete:", video_id)

    if thumbnail_path and os.path.exists(thumbnail_path):
        youtube.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(thumbnail_path)).execute()
    return video_id

def get_or_create_playlist(youtube, title: str, description: str="자동 생성된 재생목록"):
    # try to find existing
    pl = youtube.playlists().list(part="snippet,contentDetails", mine=True, maxResults=50).execute()
    for item in pl.get("items", []):
        if item["snippet"]["title"] == title:
            return item["id"]
    # create
    body = {
        "snippet": {"title": title, "description": description},
        "status": {"privacyStatus": "public"}
    }
    res = youtube.playlists().insert(part="snippet,status", body=body).execute()
    return res["id"]

def add_video_to_playlist(youtube, playlist_id: str, video_id: str):
    body = {
        "snippet": {"playlistId": playlist_id, "resourceId": {"kind": "youtube#video", "videoId": video_id}}
    }
    youtube.playlistItems().insert(part="snippet", body=body).execute()
