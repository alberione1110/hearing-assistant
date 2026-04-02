from typing import Any
from pydantic import BaseModel


class STTResultOut(BaseModel):
    message: str
    stt_text: str
    normalized_payload: dict[str, Any]
    backend_response: dict[str, Any] | None = None
    timing: dict[str, Any] | None = None