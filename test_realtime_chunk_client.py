import time
import queue
import tempfile
from pathlib import Path

import numpy as np
import requests
import sounddevice as sd
import soundfile as sf

SERVER_URL = "http://127.0.0.1:8001/ingest/stt"
AI_TOKEN = "change-me"
DEVICE_ID = "cap-001"
SOUND_TYPE = "conversation"

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SECONDS = 2
TOTAL_CHUNKS = 5   # 2초 * 5번 = 총 10초 테스트


audio_queue = queue.Queue()


def audio_callback(indata, frames, time_info, status):
    if status:
        print("[Mic status]", status)
    audio_queue.put(indata.copy())


def record_chunk(seconds: int) -> np.ndarray:
    target_frames = SAMPLE_RATE * seconds
    collected = []
    collected_frames = 0

    while collected_frames < target_frames:
        data = audio_queue.get()
        collected.append(data)
        collected_frames += len(data)

    chunk = np.concatenate(collected, axis=0)
    chunk = chunk[:target_frames]
    return chunk


def send_chunk(wav_path: str, chunk_index: int):
    start = time.perf_counter()

    with open(wav_path, "rb") as f:
        response = requests.post(
            SERVER_URL,
            headers={"x-ai-token": AI_TOKEN},
            files={"audio": (Path(wav_path).name, f, "audio/wav")},
            data={
                "device_id": DEVICE_ID,
                "sound_type": SOUND_TYPE,
                "direction": "unknown",
                "confidence": "1.0",
            },
            timeout=120,
        )

    elapsed = time.perf_counter() - start
    return response, elapsed


def main():
    print("=== 실시간 청크 테스트 시작 ===")
    print(f"- 서버: {SERVER_URL}")
    print(f"- 샘플레이트: {SAMPLE_RATE}")
    print(f"- 청크 길이: {CHUNK_SECONDS}초")
    print(f"- 청크 개수: {TOTAL_CHUNKS}")
    print("지금부터 마이크로 말하세요.\n")

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        callback=audio_callback,
    ):
        for chunk_index in range(1, TOTAL_CHUNKS + 1):
            print(f"\n[Chunk {chunk_index}] 녹음 중...")
            chunk_audio = record_chunk(CHUNK_SECONDS)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                temp_wav_path = tmp.name

            sf.write(temp_wav_path, chunk_audio, SAMPLE_RATE)
            print(f"[Chunk {chunk_index}] wav 저장 완료: {temp_wav_path}")

            response, roundtrip_sec = send_chunk(temp_wav_path, chunk_index)

            print(f"[Chunk {chunk_index}] HTTP status: {response.status_code}")
            print(f"[Chunk {chunk_index}] 왕복 시간: {roundtrip_sec:.4f}s")

            try:
                data = response.json()
                print(f"[Chunk {chunk_index}] STT 결과: {data.get('stt_text')}")
                print(f"[Chunk {chunk_index}] timing: {data.get('timing')}")
            except Exception:
                print(f"[Chunk {chunk_index}] 응답 본문:", response.text)

            Path(temp_wav_path).unlink(missing_ok=True)

    print("\n=== 테스트 종료 ===")


if __name__ == "__main__":
    main()