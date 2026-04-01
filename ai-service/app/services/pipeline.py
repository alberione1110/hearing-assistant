from app.core.config import settings
from app.schemas.forward import ForwardPayload
from app.schemas.ingest import IngestRequest
from app.services.forwarder import forward_to_backend
from app.services.normalizer import normalize_ingest_payload
from app.services.stt_service import run_stt


def process_ingest_event(payload: IngestRequest) -> dict:
    normalized = normalize_ingest_payload(payload)

    if normalized["confidence"] < settings.min_confidence:
        return {
            "message": "Event ignored due to low confidence",
            "normalized_payload": normalized,
            "backend_response": None,
        }

    stt_text = run_stt(
        transcript_hint=normalized["transcript_hint"],
        sound_type=normalized["sound_type"],
    )

    forward_payload = ForwardPayload(
        device_id=normalized["device_id"],
        sound_type=normalized["sound_type"],
        is_risk=normalized["is_risk"],
        direction=normalized["direction"],
        confidence=normalized["confidence"],
        stt_text=stt_text,
        raw_payload={
            "transcript_hint": normalized["transcript_hint"],
            "metadata": normalized["metadata"],
        },
    )

    backend_response = forward_to_backend(forward_payload)

    return {
        "message": "AI event processed and forwarded successfully",
        "normalized_payload": forward_payload.model_dump(),
        "backend_response": backend_response,
    }