from fastapi import APIRouter, Depends
from app.api.deps import require_ai_token
from app.schemas.event import EventIn, EventOut
from app.services.pipeline import PipelineService

router = APIRouter(prefix="/ingest/event", tags=["event"])
pipeline = PipelineService()


@router.post("", response_model=EventOut, dependencies=[Depends(require_ai_token)])
async def ingest_event(payload: EventIn):
    normalized, backend_response = await pipeline.process_event(payload)

    return EventOut(
        message="Event processed and forwarded successfully",
        normalized_payload=normalized,
        backend_response=backend_response,
    )