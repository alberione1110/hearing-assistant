from typing import Any
from pydantic import BaseModel, Field


class ForwardAlertRequest(BaseModel):
    device_id: str = Field(..., min_length=1)
    sound_type: str = Field(..., min_length=1)
    is_risk: bool
    direction: str | None = None
    confidence: float | None = None
    stt_text: str | None = None
    raw_payload: dict[str, Any] | None = None