from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, Field
from app.core.config import settings
from app.services.forwarder import forward_to_backend
from app.services.stt_service import run_stt

router = APIRouter(prefix='/api/v1/ingest', tags=['ingest'])


class IngestPayload(BaseModel):
    device_id: str = Field(..., examples=['cap-001'])
    sound_type: str = Field(..., examples=['car_horn'])
    is_risk: bool = Field(..., examples=[True])
    direction_deg: float | None = Field(default=None, examples=[45.0])
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    transcript_hint: str | None = Field(default=None, examples=['경적'])
    metadata: dict | None = None


def verify_shared_token(x_ai_token: str | None):
    if x_ai_token != settings.ai_shared_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid AI token')


@router.post('')
async def ingest_event(payload: IngestPayload, x_ai_token: str | None = Header(default=None)):
    verify_shared_token(x_ai_token)

    stt_text = run_stt(payload.sound_type, payload.transcript_hint)

    normalized = {
        'device_id': payload.device_id,
        'sound_type': payload.sound_type,
        'is_risk': payload.is_risk,
        'direction_deg': payload.direction_deg,
        'confidence': payload.confidence,
        'stt_text': stt_text,
        'raw_payload': {
            'metadata': payload.metadata,
            'source': 'raspberry-pi',
        },
    }

    backend_response = await forward_to_backend(normalized)

    return {
        'message': 'AI event processed and forwarded successfully',
        'normalized_payload': normalized,
        'backend_response': backend_response,
    }
