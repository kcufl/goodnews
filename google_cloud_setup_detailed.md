# Google Cloud Console 설정 상세 가이드

## 📋 준비사항
- Google 계정 (YouTube 채널이 있는 계정 권장)
- 웹 브라우저 (Chrome, Firefox, Safari 등)

---

## 1단계: Google Cloud Console 접속

### 1.1 브라우저에서 접속
- **URL**: https://console.cloud.google.com/
- Google 계정으로 로그인

### 1.2 프로젝트 선택 화면
- 상단에 "프로젝트 선택" 드롭다운 메뉴 클릭
- "새 프로젝트" 버튼 클릭

### 1.3 새 프로젝트 생성
- **프로젝트 이름**: `AI-News-Briefing` (또는 원하는 이름)
- **조직**: (선택사항) 조직이 있다면 선택
- **위치**: (선택사항) 프로젝트 위치 선택
- **만들기** 버튼 클릭

### 1.4 프로젝트 생성 완료
- 생성 완료까지 1-2분 소요
- 상단에 새 프로젝트 이름이 표시되면 완료

---

## 2단계: YouTube Data API v3 활성화

### 2.1 API 라이브러리 접속
- 왼쪽 메뉴에서 **"API 및 서비스"** 클릭
- **"라이브러리"** 클릭

### 2.2 YouTube Data API v3 검색
- 검색창에 **"YouTube Data API v3"** 입력
- 검색 결과에서 **"YouTube Data API v3"** 클릭

### 2.3 API 활성화
- **"사용"** 버튼 클릭
- 활성화 완료 메시지 확인

---

## 3단계: 사용자 인증 정보 생성

### 3.1 사용자 인증 정보 페이지 접속
- 왼쪽 메뉴에서 **"API 및 서비스"** 클릭
- **"사용자 인증 정보"** 클릭

### 3.2 OAuth 동의 화면 설정
- **"OAuth 동의 화면"** 탭 클릭
- **"외부"** 선택 (개인 사용자)
- **"만들기"** 클릭

#### OAuth 동의 화면 정보 입력:
- **앱 이름**: `AI News Briefing`
- **사용자 지원 이메일**: 본인 이메일
- **개발자 연락처 정보**: 본인 이메일
- **저장 후 계속** 클릭

#### 범위 추가:
- **"범위 추가 또는 삭제"** 클릭
- **"YouTube Data API v3"** 선택
- **"업데이트"** 클릭
- **"저장 후 계속"** 클릭

#### 테스트 사용자:
- **"테스트 사용자 추가"** 클릭
- 본인 Google 계정 이메일 추가
- **"저장 후 계속"** 클릭

### 3.3 OAuth 2.0 클라이언트 ID 생성
- **"사용자 인증 정보"** 탭 클릭
- **"사용자 인증 정보 만들기"** 클릭
- **"OAuth 클라이언트 ID"** 선택

#### 애플리케이션 유형 선택:
- **"데스크톱 앱"** 선택
- **"이름"**: `AI News Briefing Desktop Client`
- **"만들기"** 클릭

### 3.4 클라이언트 시크릿 다운로드
- 생성된 OAuth 2.0 클라이언트 ID 클릭
- **"JSON 다운로드"** 버튼 클릭
- 다운로드된 파일을 `client_secret.json`으로 이름 변경

---

## 4단계: 프로젝트에 파일 저장

### 4.1 파일 이동
- 다운로드된 `client_secret.json` 파일을 프로젝트 루트 폴더로 이동
- 파일 구조:
```
프로젝트폴더/
├── client_secret.json  ← 여기에 저장
├── main.py
├── config.py
├── .env
└── ...
```

### 4.2 파일 권한 확인
```bash
chmod 600 client_secret.json
```

---

## 5단계: 인증 테스트

### 5.1 가상환경 활성화
```bash
source venv/bin/activate
```

### 5.2 인증 테스트 실행
```bash
python test_youtube_auth.py
```

### 5.3 브라우저 인증
- 브라우저가 자동으로 열림
- Google 계정으로 로그인
- **"계속"** 클릭하여 권한 허용
- **"허용"** 클릭

### 5.4 인증 완료 확인
- `token.json` 파일이 생성됨
- 콘솔에 채널 정보가 표시됨

---

## 6단계: 업로드 테스트 (선택사항)

### 6.1 테스트 비디오 업로드
```bash
python test_youtube_upload.py
```

### 6.2 결과 확인
- YouTube 채널에 테스트 비디오가 업로드됨
- 비디오 ID와 링크가 표시됨

---

## 🔧 문제 해결

### 인증 오류
```bash
# token.json 파일 삭제 후 재인증
rm token.json
python test_youtube_auth.py
```

### API 할당량 확인
- Google Cloud Console → API 및 서비스 → 대시보드
- YouTube Data API v3 사용량 확인

### 권한 문제
- YouTube 채널 소유자 계정으로 인증
- 브라우저에서 권한 취소 후 재인증

---

## 📊 예상 비용

### 무료 할당량
- **일일 할당량**: 10,000 units
- **비디오 업로드**: 1,600 units/업로드
- **하루 최대**: 약 6개 비디오 업로드

### 유료 사용
- 할당량 초과 시 자동 과금
- $5/1,000,000 units (약 $0.008/업로드)

---

## ✅ 완료 체크리스트

- [ ] Google Cloud Console 프로젝트 생성
- [ ] YouTube Data API v3 활성화
- [ ] OAuth 동의 화면 설정
- [ ] OAuth 2.0 클라이언트 ID 생성
- [ ] client_secret.json 다운로드
- [ ] 프로젝트에 파일 저장
- [ ] 인증 테스트 성공
- [ ] 업로드 테스트 성공 (선택사항)

---

## 🎉 완료 후 사용법

### 전체 시스템 실행
```bash
python main.py
```

### 자동화 설정 (cron)
```bash
# 매일 07:30 실행
30 7 * * * /path/to/venv/bin/python /path/to/main.py
```

이제 완전 자동화된 뉴스 브리핑 YouTube 채널을 운영할 수 있습니다! 🚀