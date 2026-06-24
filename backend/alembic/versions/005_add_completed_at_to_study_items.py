"""add completed_at to study_plan_items

Revision ID: 005
Revises: 004
Create Date: 2026-06-15 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add completed_at column to study_plan_items
    op.add_column(
        'study_plan_items',
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    # Remove completed_at column from study_plan_items
    op.drop_column('study_plan_items', 'completed_at')
