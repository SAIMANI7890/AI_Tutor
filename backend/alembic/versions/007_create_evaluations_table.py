"""
Create evaluations table

Revision ID: 007
Revises: 006
Create Date: 2026-06-17 10:00:00

Description:
Creates database foundation for Evaluation Module (Phase 7A)

Table created:
- evaluations: Stores AI-generated evaluations of student answers

Features:
- Links to users, tests, and questions (with cascade handling)
- Stores student answers, model answers, marks, and feedback
- Supports strengths and improvements as JSON arrays
- Chapter-wise tracking for performance analytics
- Comprehensive indexing for fast queries

This table enables:
- Historical tracking of student performance
- Progress analytics over time
- Personalized feedback and recommendations
- Chapter-wise performance analysis
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Upgrade database schema
    Creates evaluations table with proper indexes and constraints
    """
    
    # Create evaluations table
    op.create_table(
        'evaluations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('test_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('question_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('student_answer', sa.Text(), nullable=False),
        sa.Column('model_answer', sa.Text(), nullable=False),
        sa.Column('marks_awarded', sa.Integer(), nullable=False),
        sa.Column('total_marks', sa.Integer(), nullable=False),
        sa.Column('feedback', sa.Text(), nullable=False),
        sa.Column('strengths', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('improvements', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('chapter_name', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        
        # Foreign key constraints
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['test_id'], ['tests.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['question_id'], ['test_questions.id'], ondelete='SET NULL'),
        
        # Check constraints
        sa.CheckConstraint('marks_awarded >= 0', name='check_marks_awarded_non_negative'),
        sa.CheckConstraint('total_marks > 0', name='check_total_marks_positive'),
        sa.CheckConstraint('marks_awarded <= total_marks', name='check_marks_awarded_lte_total')
    )
    
    # Create indexes for evaluations table
    op.create_index('ix_evaluations_id', 'evaluations', ['id'])
    op.create_index('ix_evaluations_user_id', 'evaluations', ['user_id'])
    op.create_index('ix_evaluations_test_id', 'evaluations', ['test_id'])
    op.create_index('ix_evaluations_question_id', 'evaluations', ['question_id'])
    op.create_index('ix_evaluations_chapter_name', 'evaluations', ['chapter_name'])
    op.create_index('ix_evaluations_created_at', 'evaluations', ['created_at'])
    
    # Composite index for chapter-wise queries
    op.create_index(
        'ix_evaluations_user_chapter', 
        'evaluations', 
        ['user_id', 'chapter_name']
    )


def downgrade() -> None:
    """
    Downgrade database schema
    Drops evaluations table and all associated indexes
    """
    
    # Drop indexes
    op.drop_index('ix_evaluations_user_chapter', 'evaluations')
    op.drop_index('ix_evaluations_created_at', 'evaluations')
    op.drop_index('ix_evaluations_chapter_name', 'evaluations')
    op.drop_index('ix_evaluations_question_id', 'evaluations')
    op.drop_index('ix_evaluations_test_id', 'evaluations')
    op.drop_index('ix_evaluations_user_id', 'evaluations')
    op.drop_index('ix_evaluations_id', 'evaluations')
    
    # Drop table
    op.drop_table('evaluations')
