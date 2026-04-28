from datetime import datetime
from sqlalchemy import String, Float, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


# 사용자 계정 정보
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    platform: Mapped[str] = mapped_column(String(10), nullable=False)  # ios | android
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# 방향 감지 이력을 저장하는 테이블
# 프론트가 AI로부터 방향 데이터를 수신한 시점에 JWT와 함께 POST /api/v1/directions 로 저장 요청
class Direction(Base):
    __tablename__ = 'directions'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    direction: Mapped[str] = mapped_column(String(10), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    sound_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


# 사용자별 설정
# - font_size: 자막 폰트 크기 (small / medium / large)
# - vibration_on: 워치 진동 알림 ON/OFF
# - glasses_auto_switch: call 클래스 감지 시 글래스 모드 자동 전환 팝업 ON/OFF
class Setting(Base):
    __tablename__ = 'settings'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    font_size: Mapped[str] = mapped_column(String(10), default='medium')
    vibration_type: Mapped[str] = mapped_column(String(10), default='SINGLE')
    glasses_auto_switch: Mapped[bool] = mapped_column(Boolean, default=True)