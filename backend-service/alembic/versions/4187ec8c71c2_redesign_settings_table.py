"""redesign settings table

Revision ID: 4187ec8c71c2
Revises: 0b4148d74e0a
Create Date: 2026-04-22 15:25:54.018448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4187ec8c71c2'
down_revision: Union[str, None] = '0b4148d74e0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. glasses_auto_switch 컬럼 추가
    #    server_default=sa.true(): 기존 행에 대해 기본값 TRUE로 채움 (A안 결정사항)
    op.add_column(
        'settings',
        sa.Column(
            'glasses_auto_switch',
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    # 2. font_size 타입 변경 (INTEGER → VARCHAR(10))
    #    postgresql_using: 기존 숫자 값을 'medium' 문자열로 일괄 변환
    #    (any integer → 'medium'. small/medium/large 중 기본값 medium으로 통일)
    op.alter_column(
        'settings',
        'font_size',
        existing_type=sa.INTEGER(),
        type_=sa.String(length=10),
        existing_nullable=False,
        postgresql_using="'medium'",
        server_default='medium',
    )

    # 3. 불필요해진 컬럼 제거
    op.drop_column('settings', 'output_device')
    op.drop_column('settings', 'language')


def downgrade() -> None:
    # 1. 제거했던 language / output_device 복원 (기존 기본값으로 채움)
    op.add_column(
        'settings',
        sa.Column(
            'language',
            sa.VARCHAR(length=5),
            autoincrement=False,
            nullable=False,
            server_default='ko',
        ),
    )
    op.add_column(
        'settings',
        sa.Column(
            'output_device',
            sa.VARCHAR(length=10),
            autoincrement=False,
            nullable=False,
            server_default='both',
        ),
    )

    # 2. font_size 타입 원복 (VARCHAR → INTEGER)
    #    medium/small/large 같은 문자열을 숫자 14로 일괄 변환
    op.alter_column(
        'settings',
        'font_size',
        existing_type=sa.String(length=10),
        type_=sa.INTEGER(),
        existing_nullable=False,
        postgresql_using='14',
        server_default='14',
    )

    # 3. 새로 추가했던 컬럼 제거
    op.drop_column('settings', 'glasses_auto_switch')