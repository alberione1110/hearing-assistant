# app/services/ws_manager.py

from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        # 연결된 유저들 저장하는 딕셔너리
        # { "user123": WebSocket객체, "user456": WebSocket객체 } 형태로 저장됨.
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()  # 연결 수락
        self.active_connections[user_id] = websocket  # 목록(딕셔너리)에 추가

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)  # 목록에서 제거
        # None은 해당 유저 없어도 에러 안 나게 하려는 것

    async def send_to_user(self, user_id: str, message: dict):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json(message)  # 해당 유저한테 전송

# 앱 전체에서 하나만 쓰도록 인스턴스 생성
manager = WebSocketManager()