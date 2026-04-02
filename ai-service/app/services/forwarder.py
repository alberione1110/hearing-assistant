from app.schemas.forward import ForwardAlertRequest
import time


class ForwarderService:
    async def send_alert(self, payload: ForwardAlertRequest) -> dict:
        start = time.perf_counter()

        print("[Forwarder] mock forwarding 시작")
        print(payload.model_dump())

        elapsed = time.perf_counter() - start
        print(f"[Forwarder] mock forwarding 완료 | {elapsed:.4f}s")

        return {
            "mocked": True,
            "message": "Backend forwarding skipped in local/render test",
            "elapsed_sec": round(elapsed, 4),
        }