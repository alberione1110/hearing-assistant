def run_stt(sound_type: str, transcript_hint: str | None = None) -> str | None:
    """
    임시 STT 함수입니다.
    실제 운영에서는 Whisper / faster-whisper / 외부 STT API 등으로 교체하세요.
    """
    if transcript_hint:
        return transcript_hint

    demo_map = {
        'car_horn': '자동차 경적 소리가 감지되었습니다.',
        'siren': '사이렌 소리가 감지되었습니다.',
        'dog_bark': '개 짖는 소리가 감지되었습니다.',
    }
    return demo_map.get(sound_type)
