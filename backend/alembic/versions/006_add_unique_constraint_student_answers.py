"""add unique constraint to student answers

Revision ID: 006
Revises: 005
Create Date: 2026-06-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade():
    """
    Add unique constraint on (test_id, question_id) to student_test_answers table.
    This prevents duplicate answers and enables atomic upsert operations.
    """
    # First, remove any duplicate answers that might exist
    # Keep the most recent answer for each test_id, question_id combination
    op.execute("""
        DELETE FROM student_test_answers
        WHERE id NOT IN (
            SELECT DISTINCT ON (test_id, question_id) id
            FROM student_test_answers
            ORDER BY test_id, question_id, updated_at DESC
        )
    """)
    
    # Add the unique constraint
    op.create_unique_constraint(
        'uq_test_question_answer',
        'student_test_answers',
        ['test_id', 'question_id']
    )
    
    # Add composite index for performance optimization
    op.create_index(
        'idx_student_answers_test_question',
        'student_test_answers',
        ['test_id', 'question_id']
    )


def downgrade():
    """
    Remove unique constraint and index
    """
    op.drop_index('idx_student_answers_test_question', table_name='student_test_answers')
    op.drop_constraint('uq_test_question_answer', 'student_test_answers', type_='unique')
