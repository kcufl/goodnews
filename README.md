# AI 뉴스 요약 브리핑 자동화 (YouTube)

뉴스 수집 → 요약(LLM) → 음성 합성(TTS) → 영상 합성 → 유튜브 업로드 자동화 예시입니다.

## 1) 설치

### 시스템 요구사항
- Python 3.8 이상
- Linux/macOS/Windows

### 의존성 설치
```bash
# Python 패키지 설치
python3 -m pip install --break-system-packages -r requirements.txt

# 또는 가상환경 사용 (권장)
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 환경 설정
```bash
# .env 파일 생성 및 설정
cp .env.example .env  # .env.example이 있는 경우
# 또는 직접 .env 파일 생성

# .env 파일 편집
# OPENAI_API_KEY, YOUTUBE_CLIENT_SECRETS_FILE 등 설정
```

## 2) 실행

### 기본 실행
```bash
python3 main.py
```

### 프로젝트 검증
```bash
# API 키 없이도 기본 기능 검증 가능
python3 test_basic.py
```

결과는 `data/YYYY-MM-DD/`에 저장됩니다.

## 3) 자동화(cron)
```bash
# 매일 07:30 (Asia/Seoul)
30 7 * * * /path/to/.venv/bin/python /path/to/ai_news_briefing_full_v2/main.py >> /path/to/run.log 2>&1
```

## 4) 프로젝트 구조
```
├── main.py                 # 메인 실행 파일
├── config.py              # 설정 파일
├── news_fetcher.py        # 뉴스 수집
├── summarizer_openai.py   # OpenAI 요약
├── tts_openai.py          # OpenAI TTS
├── video_maker.py         # 비디오 제작
├── thumbnail_gen.py       # 썸네일 생성
├── uploader_youtube.py    # YouTube 업로드
├── utils.py               # 유틸리티
├── requirements.txt       # Python 의존성
├── .env                   # 환경 변수
└── README.md             # 프로젝트 문서
```

## 5) 환경 변수 설정

### 필수 설정
- `OPENAI_API_KEY`: OpenAI API 키
- `YOUTUBE_CLIENT_SECRETS_FILE`: YouTube API 클라이언트 시크릿 파일 경로

### 선택 설정
- `CHANNEL_TITLE_PREFIX`: 채널 제목 접두사 (기본값: "오늘의 뉴스 요약")
- `CHANNEL_LOCALE`: 채널 로케일 (기본값: "KR:ko")
- `NEWS_TOPICS`: 뉴스 주제 (기본값: "경제,IT,국내")
- `VIDEO_RESOLUTION`: 비디오 해상도 (기본값: "1920x1080")
- `OUTPUT_DIR`: 출력 디렉토리 (기본값: "./data")

## 주의사항
- 요약 정확도는 원문/모델에 따라 달라질 수 있어 민감 이슈는 검수 권장
- 기사 본문 무단 복제 금지, 설명란에 제목/링크 출처 표기
- MoviePy TextClip은 ImageMagick 설치가 필요할 수 있습니다.
- Python 3.13에서는 일부 오디오 처리 라이브러리 호환성 문제가 있을 수 있습니다.

## 문제 해결

### 일반적인 문제
1. **API 키 오류**: .env 파일에서 OPENAI_API_KEY가 올바르게 설정되었는지 확인
2. **의존성 오류**: `pip install -r requirements.txt` 재실행
3. **권한 오류**: 가상환경 사용 또는 `--break-system-packages` 플래그 사용

### 검증
프로젝트가 정상적으로 설정되었는지 확인하려면:
```bash
python3 test_basic.py
```

모든 테스트가 통과하면 프로젝트가 정상적으로 작동할 준비가 된 것입니다.
