from pathlib import Path
from faster_whisper import WhisperModel
from app.core.config import settings
import time


class STTService:
    def __init__(self) -> None:
        model_load_start = time.perf_counter()

        print("[STTService] Whisper 모델 로드 시작")
        self.model = WhisperModel(
            settings.whisper_model_size,
            device=settings.whisper_device,
            compute_type=settings.whisper_compute_type,
        )
        model_load_elapsed = time.perf_counter() - model_load_start
        print(f"[STTService] Whisper 모델 로드 완료 | {model_load_elapsed:.4f}s")

    def transcribe_file(self, file_path: str, language: str | None = None) -> tuple[str, float]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        start = time.perf_counter()

        segments, info = self.model.transcribe(
            str(path),
            language=language or settings.stt_language,
            vad_filter=True,
        )

        texts: list[str] = []

        for i, segment in enumerate(segments, start=1):
            text = segment.text.strip()
            print(
                f"[STTService] segment {i} | "
                f"{segment.start:.2f}s ~ {segment.end:.2f}s | {text}"
            )
            if text:
                texts.append(text)

        final_text = " ".join(texts).strip()
        elapsed = time.perf_counter() - start

        print(f"[STTService] 감지 언어: {info.language}")
        print(f"[STTService] 언어 확률: {info.language_probability}")
        print(f"[STTService] 최종 텍스트: {final_text}")
        print(f"[STTService] STT 처리 시간: {elapsed:.4f}s")

        return final_text, elapsed