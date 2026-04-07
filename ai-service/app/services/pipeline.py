import time
from app.schemas.event import EventIn
from app.schemas.forward import ForwardAlertRequest
from app.services.forwarder import ForwarderService
from app.services.normalizer import NormalizerService


class PipelineService:
    def __init__(self) -> None:
        self.normalizer = NormalizerService()
        self.forwarder = ForwarderService()

    async def process_event(self, payload: EventIn) -> tuple[dict, dict]:
        pipeline_start = time.perf_counter()

        normalized = self.normalizer.normalize_event(payload)
        forward_payload = ForwardAlertRequest(**normalized)
        backend_response = await self.forwarder.send_alert(forward_payload)

        total_elapsed = time.perf_counter() - pipeline_start
        print(f"[Pipeline] event processed | {total_elapsed:.4f}s")

        return normalized, backend_response