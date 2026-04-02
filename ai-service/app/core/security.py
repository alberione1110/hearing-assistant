from fastapi import Header, HTTPException, status
from app.core.config import settings


def verify_ai_token(x_ai_token: str | None = Header(default=None)) -> str:
    if not x_ai_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing x-ai-token",
        )

    if x_ai_token != settings.ai_shared_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid x-ai-token",
        )

    return x_ai_token