# app/api/routes/ws.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
#WebSocketDisconnect는 클라이언트가 연결 끊었을 때 발생. manager를 가져오는 것임
from app.services.ws_manager import manager

router = APIRouter()

@router.websocket("/ws/{user_id}") # 예) /ws/user123으로 연결 요청 오면 이 함수 실행.
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    # 연결 수락하고 manager에 등록
    await manager.connect(user_id, websocket)
    try:
        while True:
            # 클라이언트가 보내는 메시지 대기 (연결 유지용)
            await websocket.receive_text()
    except WebSocketDisconnect:
        # 연결 끊기면 해당 유저를 manager에서 제거
        manager.disconnect(user_id)