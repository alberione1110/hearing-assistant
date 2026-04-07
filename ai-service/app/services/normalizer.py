from app.schemas.event import EventIn


class NormalizerService:
    @staticmethod
    def normalize_event(payload: EventIn) -> dict:
        return {
            "device_id": payload.device_id,
            "event_type": payload.event_type,
            "sound_type": payload.sound_type,
            "is_risk": payload.is_risk,
            "direction": payload.direction or "unknown",
            "confidence": payload.confidence,
            "raw_payload": {
                "metadata": payload.metadata or {},
            },
        }