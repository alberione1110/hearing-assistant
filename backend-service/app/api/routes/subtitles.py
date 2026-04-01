# app/api/routes/subtitles.py
# 자막 히스토리 조회 API
# GET /api/v1/subtitles → 로그인한 사용자의 자막 기록을 조회

from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Subtitle
from app.schemas import PaginatedSubtitles
from app.core.security import get_current_user

# prefix: 이 파일의 모든 API 경로 앞에 /api/v1/subtitles 가 자동으로 붙음
router = APIRouter(prefix='/api/v1/subtitles', tags=['subtitles'])


@router.get('', response_model=PaginatedSubtitles)
def get_subtitles(
    # Query 파라미터: URL 뒤에 ?page=1&size=20&date=2025-01-01 형태로 전달됨
    page: int = Query(default=1, ge=1, description='페이지 번호'),
    size: int = Query(default=20, ge=1, le=100, description='페이지당 건수'),
    date: str | None = Query(default=None, description='날짜 필터 (YYYY-MM-DD)'),
    # Depends(get_current_user): JWT 토큰에서 user_id를 자동으로 꺼내줌
    # 토큰이 없거나 만료되면 여기서 자동으로 401 에러 발생
    user_id: int = Depends(get_current_user),
    # Depends(get_db): DB 연결을 자동으로 열고 닫아줌
    db: Session = Depends(get_db),
):
    # 1. 기본 쿼리: 현재 로그인한 사용자의 자막만 조회
    query = db.query(Subtitle).filter(Subtitle.user_id == user_id)

    # 2. 날짜 필터가 있으면 해당 날짜만 조회
    if date:
        target_date = datetime.strptime(date, '%Y-%m-%d').date()
        query = query.filter(
            Subtitle.created_at >= datetime.combine(target_date, datetime.min.time()),
            Subtitle.created_at < datetime.combine(target_date, datetime.max.time()),
        )

    # 3. 전체 건수 (페이지네이션 정보에 필요)
    total = query.count()

    # 4. 최신순 정렬 + 페이지네이션
    #    offset: 건너뛸 개수 (page 2, size 20이면 20개 건너뜀)
    #    limit: 가져올 개수
    items = (
        query
        .order_by(Subtitle.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return PaginatedSubtitles(items=items, total=total, page=page, size=size)