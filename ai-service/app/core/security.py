from fastapi import Header, HTTPException, status

from app.core.config import settings


def verify_ai_token(x_ai_token: str = Header(...)) -> str:
    if x_ai_token != settings.ai_shared_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid x-ai-token",
        )
    return x_ai_token