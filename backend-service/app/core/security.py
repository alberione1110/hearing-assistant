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