"""create study plan tables

Revision ID: 003
Revises: 002
Create Date: 2026-06-10 19:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create study_plans and study_plan_items tables"""
    
    # Create study_plans table
    op.create_table(
        'study_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('exam_date', sa.Date(), nullable=False),
        sa.Column('daily_study_hours', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_study_plans_id'), 'study_plans', ['id'], unique=False)
    op.create_index(op.f('ix_study_plans_user_id'), 'study_plans', ['user_id'], unique=False)
    
    # Create study_plan_items table
    op.create_table(
        'study_plan_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('study_plan_id', sa.Integer(), nullable=False),
        sa.Column('day_number', sa.Integer(), nullable=False),
        sa.Column('study_date', sa.Date(), nullable=False),
        sa.Column('activity_type', sa.Enum('Study', 'Revision', 'MockTest', name='activitytype'), nullable=False),
        sa.Column('chapter_id', sa.Integer(), nullable=True),
        sa.Column('chapter_name', sa.String(length=255), nullable=True),
        sa.Column('allocated_hours', sa.Float(), nullable=False),
        sa.Column('status', sa.Enum('Pending', 'Completed', 'Skipped', name='studystatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['study_plan_id'], ['study_plans.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_study_plan_items_id'), 'study_plan_items', ['id'], unique=False)
    op.create_index(op.f('ix_study_plan_items_study_plan_id'), 'study_plan_items', ['study_plan_id'], unique=False)


def downgrade() -> None:
    """Drop study plan tables"""
    op.drop_index(op.f('ix_study_plan_items_study_plan_id'), table_name='study_plan_items')
    op.drop_index(op.f('ix_study_plan_items_id'), table_name='study_plan_items')
    op.drop_table('study_plan_items')
    
    op.drop_index(op.f('ix_study_plans_user_id'), table_name='study_plans')
    op.drop_index(op.f('ix_study_plans_id'), table_name='study_plans')
    op.drop_table('study_plans')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS activitytype')
    op.execute('DROP TYPE IF EXISTS studystatus')
