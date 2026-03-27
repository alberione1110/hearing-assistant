from datetime import datetime
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    env: str


class SoundEventCreate(BaseModel):
    device_id: str = Field(..., examples=['cap-001'])
    sound_type: str = Field(..., examples=['car_horn'])
    is_risk: bool = True
    direction_deg: float | None = Field(default=None, examples=[135.0])
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    stt_text: str | None = Field(default=None, examples=['뒤에서 자동차 경적'])
    raw_payload: dict | None = None


class SoundEventResponse(BaseModel):
    id: int
    device_id: str
    sound_type: str
    is_risk: bool
    direction_deg: float | None
    confidence: float | None
    stt_text: str | None
    created_at: datetime

    model_config = {'from_attributes': True}
