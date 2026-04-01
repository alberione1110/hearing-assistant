from typing import Any

from pydantic import BaseModel, Field


class ForwardPayload(BaseModel):
    device_id: str
    sound_type: str
    is_risk: bool
    direction: str | None = Field(default="unknown")
    confidence: float | None = Field(default=0.0, ge=0.0, le=1.0)
    stt_text: str | None = None
    raw_payload: dict[str, Any] | None = None