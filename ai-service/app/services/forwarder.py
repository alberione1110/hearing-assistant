import httpx
from fastapi import HTTPException
from app.core.config import settings


async def forward_to_backend(payload: dict) -> dict:
    target = f"{settings.backend_internal_url.rstrip('/')}/api/v1/alerts"
    headers = {'x-api-key': settings.backend_api_key}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(target, json=payload, headers=headers)

    if response.status_code >= 400:
        raise HTTPException(status_code=502, detail=f'Failed to forward to backend: {response.text}')

    return response.json()
