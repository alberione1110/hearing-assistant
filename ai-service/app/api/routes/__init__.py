from app.api.routes.health import router as health_router
from app.api.routes.event import router as event_router

__all__ = [
    "health_router",
    "event_router",
]