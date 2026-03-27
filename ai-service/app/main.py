from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.ingest import router as ingest_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(health_router)
app.include_router(ingest_router)


@app.get('/')
def root():
    return {
        'message': 'hearing-ai-service is running',
        'docs': '/docs',
        'health': '/health',
    }
