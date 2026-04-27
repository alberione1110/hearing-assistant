# app/api/routes/directions.py

from datetime import datetime, date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Direction
from app.schemas import DirectionCreate, DirectionResponse, PaginatedDirections
from app.core.security import get_current_user

router = APIRouter(prefix='/api/v1/directions', tags=['directions'])


@router.post('', response_model=DirectionResponse, status_code=201)
def create_direction(
    payload: DirectionCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    event = Direction(
        user_id=user_id,
        direction=payload.direction,
        confidence=payload.confidence,
        sound_type=payload.sound_type,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get('', response_model=PaginatedDirections)
def get_directions(
    page: int = Query(default=1, ge=1, description='페이지 번호'),
    size: int = Query(default=20, ge=1, le=100, description='페이지당 건수'),
    # 방향 필터: 특정 방향에서 온 소리만 조회 가능
    direction: str | None = Query(default=None, description='방향 필터 (front|back|left|right)'),
    date_from: date | None = Query(default = None, description='시작 날짜 (YYYY-MM-DD)'),
    date_to: date | None = Query(default=None, description='종료 날짜 (YYYY-MM-DD)'),
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 기본 쿼리: 현재 로그인한 사용자의 방향 감지만 조회
    query = db.query(Direction).filter(Direction.user_id == user_id)

    # 방향 필터가 있으면 해당 방향만 조회
    #    예: ?direction=left 이면 왼쪽에서 온 소리만 조회
    if direction:
        query = query.filter(Direction.direction == direction)
    
    # date_from 있으면 해당 날짜 00:00:00 이후, 
    # date_to 있으면 23:59:59 이전으로 필터링     
    if date_from:
        query = query.filter(Direction.created_at >= datetime(date_from.year, date_from.month, date_from.day, 0, 0, 0))

    if date_to:
        query = query.filter(Direction.created_at <= datetime(date_to.year, date_to.month, date_to.day, 23, 59, 59))

    # 전체 건수
    total = query.count()

    # 최신순 정렬 + 페이지네이션
    items = (
        query
        .order_by(Direction.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return PaginatedDirections(items=items, total=total, page=page, size=size)