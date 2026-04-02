from fastapi import Depends
from app.core.security import verify_ai_token


def require_ai_token(_: str = Depends(verify_ai_token)) -> None:
    return None