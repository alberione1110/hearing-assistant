import requests
from fastapi import HTTPException, status

from app.core.config import settings
from app.schemas.forward import ForwardPayload


def forward_to_backend(payload: ForwardPayload) -> dict:
    url = f"{settings.backend_internal_url.rstrip('/')}/api/v1/alerts"
    headers = {
        "x-api-key": settings.backend_api_key,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload.model_dump(),
            timeout=settings.forward_timeout_sec,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to forward event to backend: {exc}",
        ) from exc