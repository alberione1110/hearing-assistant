# app/api/routes/settings.py
# 사용자 설정 조회/저장 API
# GET  /api/v1/settings → 설정 조회
# PUT  /api/v1/settings → 설정 수정

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Setting
from app.schemas import SettingResponse, SettingUpdate
from app.core.security import get_current_user

router = APIRouter(prefix='/api/v1/settings', tags=['settings'])


@router.get('', response_model=SettingResponse)
def get_settings(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """사용자 설정 조회 (JWT 인증 필요)"""
    setting = db.query(Setting).filter(Setting.user_id == user_id).first()

    # 설정이 아직 없으면 기본값으로 새로 생성
    # (회원가입 직후 처음 설정을 조회하면 이 경우에 해당)
    if not setting:
        setting = Setting(user_id=user_id)
        db.add(setting)
        db.commit()
        db.refresh(setting)

    return setting


@router.put('', response_model=SettingResponse)
def update_settings(
    # payload: 클라이언트가 보낸 수정할 설정값
    payload: SettingUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """사용자 설정 저장 (JWT 인증 필요)"""
    setting = db.query(Setting).filter(Setting.user_id == user_id).first()

    # 설정이 아직 없으면 기본값으로 새로 생성
    if not setting:
        setting = Setting(user_id=user_id)
        db.add(setting)
        db.commit()
        db.refresh(setting)

    # exclude_unset=True: 클라이언트가 보내지 않은 필드는 무시
    # 예: {"font_size": 20}만 보내면 font_size만 바뀌고 나머지는 기존값 유지
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(setting, field, value)  # setting.font_size = 20 과 같은 효과

    db.commit()
    db.refresh(setting)  # DB에서 최신 상태로 다시 읽어옴
    return setting