# app/core/security.py

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# 비밀번호 암호화 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 설정
SECRET_KEY = "change-me-in-production" # 나중에 .env로 옮겨야함
ALGORITHM = "HS256" # jwt 서명 방식
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 30분
REFRESH_TOKEN_EXPIRE_DAYS = 7 # 7일


def hash_password(password: str) -> str:
    # 비밀번호 암호화
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 입력한 비밀번호와 암호화된 비밀번호 비교
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    # Access Token 생성 (30분)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # 현재 시간 + 30분
    payload = {"sub": str(user_id), "exp": expire, "type": "access"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) # payload를 SECRET_KEY로 서명하여 토큰 생성


def create_refresh_token(user_id: int) -> str:
    # Refresh Token 생성 (7일)
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "exp": expire, "type": "refresh"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> int | None:
    # 토큰 해석해서 user_id 반환
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except JWTError:
        return None
    
    
# ── JWT 인증 의존성 (API에서 현재 로그인한 유저 확인용) ──
# FastAPI의 Depends()에 넣어서 사용하는 함수
# API 호출 시 자동으로 토큰을 확인하고, 유효하면 user_id를 반환함
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# HTTPBearer: 요청 헤더에서 "Authorization: Bearer {토큰}" 형식을 자동으로 읽어줌
bearer_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> int:
    """
    사용 방법: API 함수 파라미터에 user_id: int = Depends(get_current_user) 추가
    그러면 해당 API는 자동으로 JWT 인증이 필요해지고,
    토큰이 유효하면 user_id를 받아서 사용할 수 있음
    """
    token = credentials.credentials          # 헤더에서 토큰 문자열 꺼냄
    user_id = decode_token(token)            # 토큰 해석해서 user_id 추출
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='유효하지 않거나 만료된 토큰입니다',
        )
    return user_id    