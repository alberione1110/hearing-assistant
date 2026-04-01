from app.core.config import settings


def run_stt(transcript_hint: str | None, sound_type: str) -> str | None:
    if settings.stt_provider == "dummy":
        if transcript_hint:
            return transcript_hint

        dummy_map = {
            "car_horn": "경적 소리 감지",
            "siren": "사이렌 소리 감지",
            "dog_bark": "개 짖는 소리 감지",
            "baby_cry": "아기 울음소리 감지",
        }
        return dummy_map.get(sound_type)

    # 나중에 Whisper/OpenAI 연동
    if transcript_hint:
        return transcript_hint

    return None