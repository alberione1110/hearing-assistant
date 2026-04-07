from typing import Any, Literal
from pydantic import BaseModel, Field


class EventIn(BaseModel):
    device_id: str = Field(..., min_length=1)
    event_type: Literal["risk_sound", "human_call"]
    sound_type: str = Field(..., min_length=1)
    is_risk: bool
    direction: str | None = "unknown"
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    metadata: dict[str, Any] | None = None


class EventOut(BaseModel):
    message: str
    normalized_payload: dict[str, Any]
    backend_response: dict[str, Any] | None = None