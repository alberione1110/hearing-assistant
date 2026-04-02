from app.schemas.forward import ForwardAlertRequest
from app.services.forwarder import ForwarderService
from app.services.normalizer import NormalizerService
from app.services.stt_service import STTService
import time


class PipelineService:
    def __init__(self) -> None:
        self.normalizer = NormalizerService()
        self.forwarder = ForwarderService()
        self.stt_service = STTService()

    async def process_stt_file(
        self,
        *,
        file_path: str,
        device_id: str,
        sound_type: str,
        direction: str = "unknown",
        confidence: float = 1.0,
        metadata: dict | None = None,
    ) -> tuple[str, dict, dict, dict]:
        pipeline_start = time.perf_counter()

        stt_text, stt_elapsed = self.stt_service.transcribe_file(file_path)

        normalize_start = time.perf_counter()
        normalized = self.normalizer.normalize_stt(
            device_id=device_id,
            sound_type=sound_type,
            stt_text=stt_text,
            direction=direction,
            confidence=confidence,
            metadata=metadata,
        )
        normalize_elapsed = time.perf_counter() - normalize_start

        forward_start = time.perf_counter()
        forward_payload = ForwardAlertRequest(**normalized)
        backend_response = await self.forwarder.send_alert(forward_payload)
        forward_elapsed = time.perf_counter() - forward_start

        total_elapsed = time.perf_counter() - pipeline_start

        timing = {
            "stt_sec": round(stt_elapsed, 4),
            "normalize_sec": round(normalize_elapsed, 4),
            "forward_sec": round(forward_elapsed, 4),
            "pipeline_total_sec": round(total_elapsed, 4),
        }

        return stt_text, normalized, backend_response, timing