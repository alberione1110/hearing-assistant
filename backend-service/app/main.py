import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.alerts import router as alerts_router
from app.api.routes.health import router as health_router
from app.api.routes.ws import router as ws_router
from app.api.routes.auth import router as auth_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.dummy import send_dummy_data


Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작할 때 더미 데이터 전송 시작
    asyncio.create_task(send_dummy_data())
    yield
    # 서버 종료 시 정리 (필요시)


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins(),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health_router)
app.include_router(alerts_router)
app.include_router(ws_router)
app.include_router(auth_router)


@app.get('/')
def root():
    return {
        'message': 'hearing-backend-service is running',
        'docs': '/docs',
        'health': '/health',
    }
