# app/dummy.py
import asyncio
import random
from app.services.ws_manager import manager

DIRECTIONS = ["front", "back", "left", "right",
              "fornt-left", "front-right", "back-left", "back-right"
              ]

SOUND_TYPES = [
    "call", "shout", "car_horn", "dog_bark", "alarm", "knock", "crying"
]

# SUBTITLES = {
#     "call":     ["저기요!", "잠시만요!", "야!", "잠깐만요!"],
#     "shout":    ["으아아!", "살려주세요!", "비켜요!"],
#     "car_horn": ["빵빵", "경적 소리가 납니다"],
#     "dog_bark": ["왈왈", "으와르쾅쾅왈왈멍왈왈!", "개 짖는 소리가 납니다"],
#     "alarm":    ["화재 경보가 울립니다", "사이렌 소리가 납니다"],
#     "knock":    ["노크 소리가 납니다", "똑똑"],
#     "crying":   ["아기 울음소리가 납니다", "으앙으앙", "응애응애", "빵애"],
#     }

async def send_dummy_data():
    while True:
        await asyncio.sleep(5)  # 5초마다 전송

        if not manager.active_connections:
            continue  # 연결된 유저 없으면 스킵

        direction = random.choice(DIRECTIONS)
        sound_type = random.choice(SOUND_TYPES)
        # is_subtitle = random.choice([True, False])

        message = {
            "type": "direction",
            "text": None,
            "direction": direction,
            "sound_type": sound_type,
            "confidence": round(random.uniform(0.6, 1.0), 2),
            "timestamp": int(asyncio.get_event_loop().time() * 1000)
        }

        for user_id in list(manager.active_connections.keys()):
            await manager.send_to_user(user_id, message)