from datetime import datetime
from sqlalchemy import String, Float, DateTime, Boolean, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class SoundEvent(Base):
    __tablename__ = 'sound_events'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    device_id: Mapped[str] = mapped_column(String(100), index=True)
    sound_type: Mapped[str] = mapped_column(String(100), index=True)
    is_risk: Mapped[bool] = mapped_column(Boolean, default=False)
    direction: Mapped[str | None] = mapped_column(String(20), nullable=True)  # front | back | left | right | unknown
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    stt_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_payload: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    platform: Mapped[str] = mapped_column(String(10), nullable=False)  # ios | android
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)    
    
#STT로 변환된 자막 기록을 저장하는 테이블    
class Subtitle(Base):
    __tablename__ = 'subtitles'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    direction: Mapped[str | None] = mapped_column(String(10), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)    
    
#방향 감지 이력을 저장하는 테이블(자막 없이 방향만 감지된 경우)
class Direction(Base):
    __tablename__ = 'directions'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    direction: Mapped[str] = mapped_column(String(10), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    sound_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
#사용자별 설정(폰트 크기, 언어, 진동 ON/OFF 등)    
class Setting(Base):
    __tablename__ = 'settings'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    font_size: Mapped[int] = mapped_column(Integer, default=14)
    language: Mapped[str] = mapped_column(String(5), default='ko')
    vibration_on: Mapped[bool] = mapped_column(Boolean, default=True)
    output_device: Mapped[str] = mapped_column(String(10), default='both')
    
            