# YouTube API 설정 가이드

## 1단계: Google Cloud Console 설정

### 1.1 Google Cloud Console 접속
- https://console.cloud.google.com/ 접속
- Google 계정으로 로그인

### 1.2 새 프로젝트 생성
- 상단의 프로젝트 선택 드롭다운 클릭
- "새 프로젝트" 클릭
- 프로젝트 이름: `AI-News-Briefing` (또는 원하는 이름)
- "만들기" 클릭

### 1.3 YouTube Data API v3 활성화
- 왼쪽 메뉴에서 "API 및 서비스" → "라이브러리" 클릭
- 검색창에 "YouTube Data API v3" 입력
- "YouTube Data API v3" 클릭
- "사용" 버튼 클릭

## 2단계: 사용자 인증 정보 생성

### 2.1 OAuth 2.0 클라이언트 ID 생성
- "API 및 서비스" → "사용자 인증 정보" 클릭
- "사용자 인증 정보 만들기" → "OAuth 클라이언트 ID" 클릭
- 애플리케이션 유형: "데스크톱 앱" 선택
- 이름: `AI News Briefing Desktop Client`
- "만들기" 클릭

### 2.2 클라이언트 시크릿 파일 다운로드
- 생성된 OAuth 2.0 클라이언트 ID 클릭
- "JSON 다운로드" 클릭
- 다운로드된 파일을 `client_secret.json`으로 이름 변경
- 프로젝트 루트 폴더에 저장

## 3단계: 프로젝트 설정

### 3.1 필요한 패키지 설치
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 3.2 환경 변수 설정
`.env` 파일에 다음 추가:
```
YOUTUBE_CLIENT_SECRETS_FILE=./client_secret.json
```

## 4단계: 인증 테스트

### 4.1 인증 테스트 스크립트 실행
```bash
python test_youtube_auth.py
```

### 4.2 브라우저에서 인증
- 브라우저가 열리면 Google 계정으로 로그인
- "계속" 클릭하여 권한 허용
- 인증 완료 후 `token.json` 파일이 생성됨

## 5단계: 테스트 업로드

### 5.1 테스트 비디오 업로드
```bash
python test_youtube_upload.py
```

## 주의사항

### 권한 설정
- YouTube 채널 소유자 계정으로 인증해야 함
- 업로드 권한이 있는 계정 사용

### 할당량 제한
- YouTube API 일일 할당량: 10,000 units
- 비디오 업로드: 1,600 units/업로드
- 하루 최대 약 6개 비디오 업로드 가능

### 보안
- `client_secret.json`과 `token.json` 파일을 Git에 커밋하지 않음
- `.gitignore`에 이미 추가되어 있음

## 문제 해결

### 인증 오류
- `token.json` 파일 삭제 후 재인증
- 브라우저에서 권한 취소 후 재인증

### 업로드 실패
- 파일 크기 확인 (최대 128GB)
- 네트워크 연결 상태 확인
- API 할당량 확인