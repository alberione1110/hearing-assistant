from typing import Any, Literal
from pydantic import BaseModel, Field


class ForwardAlertRequest(BaseModel):
    device_id: str = Field(..., min_length=1)
    event_type: Literal["risk_sound", "human_call"]
    sound_type: str = Field(..., min_length=1)
    is_risk: bool
    direction: str | None = "unknown"
    confidence: float | None = 0.0
    raw_payload: dict[str, Any] | None = None