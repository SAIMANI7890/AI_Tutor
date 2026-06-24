"""
Add missing columns to evaluations table

Revision ID: 008
Revises: 007
Create Date: 2026-06-17 21:00:00

Description:
    The evaluations table was created via SQLAlchemy's create_all() before
    migration 007 ran, meaning it was built from an older version of the model
    that did not include several columns.

    This migration safely adds all missing columns using ALTER TABLE ... IF NOT EXISTS,
    so it is idempotent — safe to run even if some columns already exist.

Columns added (if missing):
    - question       TEXT NOT NULL  (the question text asked to the student)
    - student_answer TEXT NOT NULL  (what the student wrote)
    - model_answer   TEXT NOT NULL  (AI-generated ideal answer)
    - marks_awarded  INTEGER NOT NULL
    - total_marks    INTEGER NOT NULL
    - feedback       TEXT NOT NULL
    - strengths      JSON
    - improvements   JSON
    - chapter_name   VARCHAR(255)
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '008'
down_revision = '007'
branch_labels = None
depends_on = None


def _column_exists(table_name: str, column_name: str) -> bool:
    """Check if a column already exists in a table."""
    bind = op.get_bind()
    result = bind.execute(sa.text(
        """
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = :table
          AND column_name = :col
        """
    ), {"table": table_name, "col": column_name})
    return result.fetchone() is not None


def upgrade() -> None:
    """
    Safely add missing columns to the evaluations table.
    Each column is only added if it does not already exist.
    """

    missing_text_cols = [
        ("question",       "TEXT NOT NULL DEFAULT 'Question not recorded'"),
        ("student_answer", "TEXT NOT NULL DEFAULT 'No answer provided'"),
        ("model_answer",   "TEXT NOT NULL DEFAULT 'Model answer not recorded'"),
        ("feedback",       "TEXT NOT NULL DEFAULT 'Feedback not available'"),
    ]

    missing_int_cols = [
        ("marks_awarded", "INTEGER NOT NULL DEFAULT 0"),
        ("total_marks",   "INTEGER NOT NULL DEFAULT 10"),
    ]

    missing_json_cols = [
        ("strengths",    "JSON"),
        ("improvements", "JSON"),
    ]

    missing_str_cols = [
        ("chapter_name", "VARCHAR(255)"),
    ]

    bind = op.get_bind()

    for col_name, col_def in (
        missing_text_cols + missing_int_cols + missing_json_cols + missing_str_cols
    ):
        if not _column_exists("evaluations", col_name):
            bind.execute(sa.text(
                f"ALTER TABLE evaluations ADD COLUMN {col_name} {col_def}"
            ))
            print(f"  [ADDED] evaluations.{col_name}")
        else:
            print(f"  [SKIP]  evaluations.{col_name} (already exists)")

    # Remove the temporary defaults that were only needed to satisfy NOT NULL
    # on existing rows (they are now set, so the defaults are no longer needed).
    for col_name in ("question", "student_answer", "model_answer", "feedback",
                     "marks_awarded", "total_marks"):
        if _column_exists("evaluations", col_name):
            bind.execute(sa.text(
                f"ALTER TABLE evaluations ALTER COLUMN {col_name} DROP DEFAULT"
            ))


def downgrade() -> None:
    """
    Remove the columns added by this migration.
    Only drops columns that exist.
    """
    cols_to_drop = [
        "question", "student_answer", "model_answer", "feedback",
        "marks_awarded", "total_marks", "strengths", "improvements", "chapter_name",
    ]

    bind = op.get_bind()
    for col_name in cols_to_drop:
        if _column_exists("evaluations", col_name):
            bind.execute(sa.text(
                f"ALTER TABLE evaluations DROP COLUMN {col_name}"
            ))
