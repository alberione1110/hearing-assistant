# app/dummy.py
import asyncio
import random
from app.services.ws_manager import manager

DIRECTIONS = ["front", "back", "left", "right"]
SUBTITLES = [
    "안녕하세요",
    "뒤에서 자동차 경적 소리가 납니다",
    "왼쪽에서 사람이 부르고 있어요",
    "앞에서 신호음이 들립니다",
]

async def send_dummy_data():
    while True:
        await asyncio.sleep(5)  # 5초마다 전송

        if not manager.active_connections:
            continue  # 연결된 유저 없으면 스킵

        direction = random.choice(DIRECTIONS)
        is_subtitle = random.choice([True, False])

        if is_subtitle:
            message = {
                "type": "subtitle",
                "text": random.choice(SUBTITLES),
                "direction": direction,
                "confidence": round(random.uniform(0.6, 1.0), 2),
                "timestamp": int(asyncio.get_event_loop().time() * 1000)
            }
        else:
            message = {
                "type": "direction",
                "text": None,
                "direction": direction,
                "confidence": round(random.uniform(0.6, 1.0), 2),
                "timestamp": int(asyncio.get_event_loop().time() * 1000)
            }

        for user_id in list(manager.active_connections.keys()):
            await manager.send_to_user(user_id, message)