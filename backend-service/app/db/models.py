from datetime import datetime
from sqlalchemy import String, Float, DateTime, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class SoundEvent(Base):
    __tablename__ = 'sound_events'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    device_id: Mapped[str] = mapped_column(String(100), index=True)
    sound_type: Mapped[str] = mapped_column(String(100), index=True)
    is_risk: Mapped[bool] = mapped_column(Boolean, default=False)
    direction_deg: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    stt_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_payload: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
