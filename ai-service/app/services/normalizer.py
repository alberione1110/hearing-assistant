from app.schemas.ingest import IngestRequest

VALID_DIRECTIONS = {"front", "back", "left", "right", "unknown"}


def normalize_ingest_payload(payload: IngestRequest) -> dict:
    direction = (payload.direction or "unknown").strip().lower()
    if direction not in VALID_DIRECTIONS:
        direction = "unknown"

    sound_type = payload.sound_type.strip().lower()
    confidence = payload.confidence if payload.confidence is not None else 0.0

    normalized = {
        "device_id": payload.device_id.strip(),
        "sound_type": sound_type,
        "is_risk": payload.is_risk,
        "direction": direction,
        "confidence": confidence,
        "transcript_hint": payload.transcript_hint.strip() if payload.transcript_hint else None,
        "metadata": payload.metadata or {},
    }
    return normalized