from fastapi import FastAPI
from app.api.routes import health_router, ingest_router, event_router, stt_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(ingest_router)
app.include_router(event_router)
app.include_router(stt_router)