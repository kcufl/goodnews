import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_TEXT_MODEL = os.getenv("OPENAI_TEXT_MODEL", "gpt-5")
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
OPENAI_TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")

YOUTUBE_CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "./client_secret.json")

CHANNEL_TITLE_PREFIX = os.getenv("CHANNEL_TITLE_PREFIX", "오늘의 뉴스 요약")
CHANNEL_LOCALE = os.getenv("CHANNEL_LOCALE", "KR:ko")
NEWS_TOPICS = [s.strip() for s in os.getenv("NEWS_TOPICS", "경제,IT,국내").split(",")]
VIDEO_RESOLUTION = os.getenv("VIDEO_RESOLUTION", "1920x1080")
BACKGROUND_IMAGE = os.getenv("BACKGROUND_IMAGE", "./assets/background.jpg")

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./data")
