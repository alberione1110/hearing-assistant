from fastapi import APIRouter, Depends

from app.core.security import verify_ai_token
from app.schemas.ingest import IngestRequest, IngestResponse
from app.services.pipeline import process_ingest_event

router = APIRouter(prefix="/api/v1", tags=["ingest"])


@router.post("/ingest", response_model=IngestResponse)
def ingest_event(
    payload: IngestRequest,
    _: str = Depends(verify_ai_token),
):
    result = process_ingest_event(payload)
    return IngestResponse(**result)