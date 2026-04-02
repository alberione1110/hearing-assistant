from app.schemas.event import EventIn
from app.schemas.ingest import IngestRequest


class NormalizerService:
    @staticmethod
    def normalize_ingest(payload: IngestRequest) -> dict:
        return {
            "device_id": payload.device_id,
            "sound_type": payload.sound_type,
            "is_risk": payload.is_risk,
            "direction": payload.direction or "unknown",
            "confidence": payload.confidence if payload.confidence is not None else 0.0,
            "stt_text": payload.transcript_hint or "",
            "raw_payload": {
                "transcript_hint": payload.transcript_hint,
                "metadata": payload.metadata or {},
            },
        }

    @staticmethod
    def normalize_event(payload: EventIn) -> dict:
        return {
            "device_id": payload.device_id,
            "sound_type": payload.sound_type,
            "is_risk": payload.is_risk,
            "direction": payload.direction or "unknown",
            "confidence": payload.confidence,
            "stt_text": payload.detected_text or "",
            "raw_payload": {
                "event_type": payload.event_type,
                "metadata": payload.metadata or {},
            },
        }

    @staticmethod
    def normalize_stt(
        *,
        device_id: str,
        sound_type: str,
        stt_text: str,
        direction: str = "unknown",
        confidence: float = 1.0,
        metadata: dict | None = None,
    ) -> dict:
        return {
            "device_id": device_id,
            "sound_type": sound_type,
            "is_risk": False,
            "direction": direction,
            "confidence": confidence,
            "stt_text": stt_text,
            "raw_payload": {
                "mode": "communication",
                "metadata": metadata or {},
            },
        }