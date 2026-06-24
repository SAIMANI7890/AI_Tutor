"""
Create examination tables

Revision ID: 004
Revises: 003
Create Date: 2026-06-10 14:15:00

Description:
Creates database foundation for Examination Module (Phase 4A)

Tables created:
- tests: Stores generated examinations
- test_questions: Stores questions within each test
- student_test_answers: Stores student responses

Future compatibility:
These tables are designed to support Phase 5 (Evaluation) without redesign:
- Marks allocation can be added to test_questions
- Student scores and feedback can be added to student_test_answers
- Evaluation status tracking can be extended
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Upgrade database schema
    Creates examination module tables with proper indexes and constraints
    """
    
    # Create enum types (will skip if already exists due to checkfirst=True)
    test_status_enum = postgresql.ENUM(
        'GENERATED', 
        'IN_PROGRESS', 
        'SUBMITTED', 
        'EVALUATED',
        name='teststatus',
        create_type=False
    )
    test_status_enum.create(op.get_bind(), checkfirst=True)
    
    question_type_enum = postgresql.ENUM(
        'MCQ',
        'FILL_BLANKS',
        'SHORT_ANSWER',
        'LONG_ANSWER',
        name='questiontype',
        create_type=False
    )
    question_type_enum.create(op.get_bind(), checkfirst=True)
    
    # Create tests table
    op.create_table(
        'tests',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('subject', sa.String(255), nullable=False),
        sa.Column('question_type', question_type_enum, nullable=False),
        sa.Column('selected_categories', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('question_count', sa.Integer(), nullable=False),
        sa.Column('status', test_status_enum, nullable=False, server_default='GENERATED'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.CheckConstraint('question_count > 0', name='check_question_count_positive'),
        sa.CheckConstraint('question_count <= 10', name='check_question_count_max')
    )
    
    # Create indexes for tests table
    op.create_index('ix_tests_id', 'tests', ['id'])
    op.create_index('ix_tests_user_id', 'tests', ['user_id'])
    op.create_index('ix_tests_status', 'tests', ['status'])
    op.create_index('ix_tests_question_type', 'tests', ['question_type'])
    op.create_index('ix_tests_created_at', 'tests', ['created_at'])
    
    # Create test_questions table
    op.create_table(
        'test_questions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('test_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('question_number', sa.Integer(), nullable=False),
        sa.Column('question_type', question_type_enum, nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('options_json', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('correct_answer', sa.Text(), nullable=False),
        sa.Column('model_answer', sa.Text(), nullable=True),
        sa.Column('source_document', sa.String(255), nullable=True),
        sa.Column('source_page', sa.Integer(), nullable=True),
        sa.Column('category', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['test_id'], ['tests.id'], ondelete='CASCADE'),
        sa.CheckConstraint('question_number > 0', name='check_question_number_positive'),
        sa.UniqueConstraint('test_id', 'question_number', name='uq_test_question_number')
    )
    
    # Create indexes for test_questions table
    op.create_index('ix_test_questions_id', 'test_questions', ['id'])
    op.create_index('ix_test_questions_test_id', 'test_questions', ['test_id'])
    op.create_index('ix_test_questions_category', 'test_questions', ['category'])
    
    # Create student_test_answers table
    op.create_table(
        'student_test_answers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('test_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('question_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('student_answer', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['test_id'], ['tests.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['question_id'], ['test_questions.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('test_id', 'question_id', name='uq_test_question_answer')
    )
    
    # Create indexes for student_test_answers table
    op.create_index('ix_student_test_answers_id', 'student_test_answers', ['id'])
    op.create_index('ix_student_test_answers_test_id', 'student_test_answers', ['test_id'])
    op.create_index('ix_student_test_answers_question_id', 'student_test_answers', ['question_id'])


def downgrade() -> None:
    """
    Downgrade database schema
    Drops all examination tables and enum types
    """
    
    # Drop tables (cascades will handle relationships)
    op.drop_index('ix_student_test_answers_question_id', 'student_test_answers')
    op.drop_index('ix_student_test_answers_test_id', 'student_test_answers')
    op.drop_index('ix_student_test_answers_id', 'student_test_answers')
    op.drop_table('student_test_answers')
    
    op.drop_index('ix_test_questions_category', 'test_questions')
    op.drop_index('ix_test_questions_test_id', 'test_questions')
    op.drop_index('ix_test_questions_id', 'test_questions')
    op.drop_table('test_questions')
    
    op.drop_index('ix_tests_created_at', 'tests')
    op.drop_index('ix_tests_question_type', 'tests')
    op.drop_index('ix_tests_status', 'tests')
    op.drop_index('ix_tests_user_id', 'tests')
    op.drop_index('ix_tests_id', 'tests')
    op.drop_table('tests')
    
    # Drop enum types
    sa.Enum(name='questiontype').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='teststatus').drop(op.get_bind(), checkfirst=True)
