"""
Alembic 마이그레이션 환경 설정 파일

이 파일의 역할:
1. DATABASE_URL 환경변수를 읽어서 DB 접속
2. 우리 프로젝트의 Base.metadata를 Alembic에 알려줘서
   models.py의 테이블 변경사항을 자동 감지하도록 함
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# 우리 프로젝트의 설정과 모델을 import
from app.core.config import settings
from app.db.base import Base
# models.py를 import 해야 Base.metadata에 테이블들이 등록됨
from app.db import models  # noqa: F401

# Alembic 설정 객체 (alembic.ini의 값을 읽어옴)
config = context.config

# .env의 DATABASE_URL을 Alembic에 주입
# (alembic.ini에 하드코딩하지 않고 런타임에 주입하는 방식)
config.set_main_option('sqlalchemy.url', settings.database_url)

# 로깅 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 자동 마이그레이션 생성 시 기준이 되는 메타데이터
# (이것이 있어야 Alembic이 models.py의 변경사항을 감지함)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """오프라인 모드: SQL 스크립트만 생성 (실제 DB 연결 없음)"""
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """온라인 모드: 실제 DB에 연결해서 마이그레이션 적용"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()