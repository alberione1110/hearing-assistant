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
    
    
# ── 자막 히스토리 응답 ──
# GET /api/v1/subtitles 에서 자막 하나하나의 형태를 정의
class SubtitleResponse(BaseModel):
    id: int                      # 자막 고유 번호
    text: str                    # STT 변환된 자막 텍스트
    direction: str | None        # 소리 방향 (front/back/left/right/unknown)
    confidence: float | None     # 방향 신뢰도 (0.0~1.0)
    created_at: datetime         # 감지 시각

    model_config = {'from_attributes': True}  # DB 모델 → 응답 자동 변환 허용


# 자막 목록을 페이지 단위로 묶어서 응답하는 형태
# 예: {"items": [...], "total": 150, "page": 1, "size": 20}
class PaginatedSubtitles(BaseModel):
    items: list[SubtitleResponse]  # 자막 목록
    total: int                     # 전체 건수
    page: int                      # 현재 페이지 번호
    size: int                      # 페이지당 건수    
    
    
# ── 방향 감지 이력 응답 ──
# GET /api/v1/directions 에서 방향 감지 하나하나의 형태를 정의
class DirectionResponse(BaseModel):
    id: int                      # 방향 감지 고유 번호
    direction: str               # 소리 방향 (front/back/left/right)
    confidence: float            # 방향 신뢰도 (0.0~1.0)
    sound_type: str | None       # 소리 유형 (car_horn, siren 등)
    created_at: datetime         # 감지 시각

    model_config = {'from_attributes': True}


# 방향 감지 목록을 페이지 단위로 묶어서 응답하는 형태
class PaginatedDirections(BaseModel):
    items: list[DirectionResponse]  # 방향 감지 목록
    total: int                      # 전체 건수
    page: int                       # 현재 페이지 번호
    size: int                       # 페이지당 건수
    
    
# ── 설정 조회 응답 ──
# GET /api/v1/settings 에서 반환되는 사용자 설정 형태
class SettingResponse(BaseModel):
    font_size: int          # 자막 폰트 크기 (14~28)
    language: str           # 언어 (ko, en, ja)
    vibration_on: bool      # 진동 알림 ON/OFF
    output_device: str      # 출력 장치 (watch, glasses, both)

    model_config = {'from_attributes': True}


# ── 설정 수정 요청 ──
# PUT /api/v1/settings 에서 클라이언트가 보내는 형태
# 모든 필드가 선택(None 가능)이라서, 바꾸고 싶은 값만 보내면 됨
# 예: {"font_size": 20} 만 보내면 폰트만 변경됨
class SettingUpdate(BaseModel):
    font_size: int | None = Field(default=None, ge=14, le=28)          # ge=최소값, le=최대값
    language: str | None = Field(default=None, pattern='^(ko|en|ja)$')  # 정규식으로 ko/en/ja만 허용
    vibration_on: bool | None = None
    output_device: str | None = Field(default=None, pattern='^(watch|glasses|both)$')
    
    
            