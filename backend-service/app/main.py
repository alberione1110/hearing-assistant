from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.api.routes.directions import router as directions_router
from app.api.routes.settings import router as settings_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins(),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(directions_router)
app.include_router(settings_router)


@app.get('/')
def root():
    return {
        'message': 'hearing-backend-service is running',
        'docs': '/docs',
        'health': '/health',
    }
