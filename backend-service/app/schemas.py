from datetime import datetime
from pydantic import BaseModel, Field


# 서버 상태 확인
class HealthResponse(BaseModel):
    status: str
    service: str
    env: str


class SoundEventCreate(BaseModel):
    device_id: str = Field(..., examples=['cap-001'])
    sound_type: str = Field(..., examples=['car_horn'])
    is_risk: bool = True
    direction: str | None = Field(default=None, examples=['front'])  # front | back | left | right | unknown
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    stt_text: str | None = Field(default=None, examples=['뒤에서 자동차 경적'])
    raw_payload: dict | None = None


class SoundEventResponse(BaseModel):
    id: int
    device_id: str
    sound_type: str
    is_risk: bool
    direction: str | None
    confidence: float | None
    stt_text: str | None
    created_at: datetime
    
    model_config = {'from_attributes': True}
    
# 회원가입 요청
class UserCreate(BaseModel):
    email: str = Field(..., examples=['user@example.com'])
    password: str = Field(..., min_length=8, examples=['password123']) # 비번 8자 이상만 허용
    platform: str = Field(..., examples=['ios'])  # ios | android


# 회원가입 응답
class UserResponse(BaseModel):
    id: int
    email: str
    platform: str
    created_at: datetime

    model_config = {'from_attributes': True}


# 로그인 요청
class LoginRequest(BaseModel):
    email: str = Field(..., examples=['user@example.com'])
    password: str = Field(..., examples=['password123'])


# 토큰 응답
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'bearer'


# 토큰 갱신 요청
class RefreshRequest(BaseModel):
    refresh_token: str