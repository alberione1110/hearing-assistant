from typing import Any

from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    device_id: str = Field(..., examples=["cap-001"])
    sound_type: str = Field(..., examples=["car_horn"])
    is_risk: bool
    direction: str | None = Field(default="unknown", examples=["front", "left", "unknown"])
    confidence: float | None = Field(default=0.0, ge=0.0, le=1.0)
    transcript_hint: str | None = None
    metadata: dict[str, Any] | None = None


class IngestResponse(BaseModel):
    message: str
    normalized_payload: dict[str, Any]
    backend_response: dict[str, Any] | None = None