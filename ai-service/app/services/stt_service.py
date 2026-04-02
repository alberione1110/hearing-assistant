from pathlib import Path
import time

from openai import OpenAI
from app.core.config import settings


class STTService:
    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=settings.openai_api_key)
        print("[STTService] OpenAI STT client initialized")

    def transcribe_file(self, file_path: str, language: str | None = None) -> tuple[str, float]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        start = time.perf_counter()

        with open(path, "rb") as audio_file:
            response = self.client.audio.transcriptions.create(
                model=settings.openai_stt_model,
                file=audio_file,
                language=language or settings.stt_language,
            )

        elapsed = time.perf_counter() - start

        text = response.text.strip() if hasattr(response, "text") else ""

        print(f"[STTService] 결과 텍스트: {text}")
        print(f"[STTService] 처리 시간: {elapsed:.4f}s")

        return text, elapsed