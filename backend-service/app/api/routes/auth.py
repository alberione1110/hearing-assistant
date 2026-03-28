# app/api/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import UserCreate, UserResponse, LoginRequest, TokenResponse, RefreshRequest
from app.db.models import User #DB의 users 테이블
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])
#/register 써도 /api/v1/auth/register로 동작


# 회원가입
@router.post('/register', response_model=UserResponse, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    # 이메일 중복 확인
    existing = db.query(User).filter(User.email == payload.email).first() #DB에서 같은 이메일 있는지 찾기
    if existing:
        raise HTTPException(status_code=409, detail='이미 등록된 이메일입니다')

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password), #암호화 저장
        platform=payload.platform,
    )
    db.add(user) #DB에 추가
    db.commit() #실제로 저장
    db.refresh(user)
    return user


# 로그인
@router.post('/login', response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first() # 이메일로 유저 찾기
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='이메일 또는 비밀번호가 올바르지 않습니다')

    access_token = create_access_token(user.id) #30분
    refresh_token = create_refresh_token(user.id) #7일/ access_token 만료시 새로 발급
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


# 토큰 갱신
@router.post('/refresh', response_model=TokenResponse)
def refresh(payload: RefreshRequest):
    user_id = decode_token(payload.refresh_token) #refresh_token 해석
    if not user_id:
        raise HTTPException(status_code=401, detail='유효하지 않은 토큰입니다')

    access_token = create_access_token(user_id) 
    return TokenResponse(access_token=access_token) 