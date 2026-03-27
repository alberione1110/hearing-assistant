import json
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.models import SoundEvent
from app.db.session import get_db
from app.schemas import SoundEventCreate, SoundEventResponse

router = APIRouter(prefix='/api/v1/alerts', tags=['alerts'])


def verify_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid API key')


@router.post('', response_model=SoundEventResponse, dependencies=[Depends(verify_api_key)])
def create_alert(payload: SoundEventCreate, db: Session = Depends(get_db)):
    event = SoundEvent(
        device_id=payload.device_id,
        sound_type=payload.sound_type,
        is_risk=payload.is_risk,
        direction_deg=payload.direction_deg,
        confidence=payload.confidence,
        stt_text=payload.stt_text,
        raw_payload=json.dumps(payload.raw_payload, ensure_ascii=False) if payload.raw_payload else None,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get('', response_model=list[SoundEventResponse])
def list_alerts(db: Session = Depends(get_db)):
    rows = db.query(SoundEvent).order_by(SoundEvent.created_at.desc()).limit(100).all()
    return rows
