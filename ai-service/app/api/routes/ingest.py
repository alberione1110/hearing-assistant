from fastapi import APIRouter, Depends
from app.api.deps import require_ai_token
from app.schemas.ingest import IngestRequest, IngestResponse
from app.services.pipeline import PipelineService

router = APIRouter(prefix="/ingest", tags=["ingest"])
pipeline = PipelineService()


@router.post("", response_model=IngestResponse, dependencies=[Depends(require_ai_token)])
async def ingest(payload: IngestRequest):
    normalized, backend_response = await pipeline.process_ingest(payload)

    return IngestResponse(
        message="AI event processed and forwarded successfully",
        normalized_payload=normalized,
        backend_response=backend_response,
    )