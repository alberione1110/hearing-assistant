import json
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.models import SoundEvent
from app.db.session import get_db
from app.schemas import SoundEventCreate, SoundEventResponse
from app.services.ws_manager import manager
import asyncio

router = APIRouter(prefix='/api/v1/alerts', tags=['alerts'])


def verify_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid API key')


@router.post('', response_model=SoundEventResponse, dependencies=[Depends(verify_api_key)])
async def create_alert(payload: SoundEventCreate, db: Session = Depends(get_db)): #async 비동기 선언
    event = SoundEvent(
        device_id=payload.device_id,
        sound_type=payload.sound_type,
        is_risk=payload.is_risk,
        direction=payload.direction,
        confidence=payload.confidence,
        stt_text=payload.stt_text,
        raw_payload=json.dumps(payload.raw_payload, ensure_ascii=False) if payload.raw_payload else None,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    
    # WebSocket으로 연결된 모든 유저에게 푸시
    message = {
        "type": "subtitle" if payload.stt_text else "direction",
        "text": payload.stt_text,
        "direction": payload.direction,
        "confidence": payload.confidence,
        "timestamp": int(event.created_at.timestamp() * 1000)
    }
    for user_id in list(manager.active_connections.keys()):
        await manager.send_to_user(user_id, message) # .이거 끝날 때까지 기달, 근데 다른 요청 처리해도 됨

    return event


@router.get('', response_model=list[SoundEventResponse])
def list_alerts(db: Session = Depends(get_db)):
    rows = db.query(SoundEvent).order_by(SoundEvent.created_at.desc()).limit(100).all()
    return rows
