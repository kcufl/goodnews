# AI 뉴스 요약 브리핑 자동화 (YouTube)

뉴스 수집 → 요약(LLM) → 음성 합성(TTS) → 영상 합성 → 유튜브 업로드 자동화 예시입니다.

## 1) 설치
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# .env: OPENAI_API_KEY, YOUTUBE_CLIENT_SECRETS_FILE 등 설정
```

## 2) 실행
```bash
python main.py
```
결과는 `data/YYYY-MM-DD/`에 저장됩니다.

## 3) 자동화(cron)
```bash
# 매일 07:30 (Asia/Seoul)
30 7 * * * /path/to/.venv/bin/python /path/to/ai_news_briefing_full_v2/main.py >> /path/to/run.log 2>&1
```

## 주의
- 요약 정확도는 원문/모델에 따라 달라질 수 있어 민감 이슈는 검수 권장
- 기사 본문 무단 복제 금지, 설명란에 제목/링크 출처 표기
- MoviePy TextClip은 ImageMagick 설치가 필요할 수 있습니다.
