"""initial baseline

Revision ID: 0b4148d74e0a
Revises: 
Create Date: 2026-04-21 17:49:10.856682

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '0b4148d74e0a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('platform', sa.String(10), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        'settings',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('font_size', sa.String(10), nullable=False, server_default='medium'),
        sa.Column('vibration_type', sa.String(10), nullable=False, server_default='SINGLE'),
        sa.Column('glasses_auto_switch', sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_table(
        'directions',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('direction', sa.String(10), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('sound_type', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), index=True),
    )


def downgrade() -> None:
    op.drop_table('directions')
    op.drop_table('settings')
    op.drop_table('users')