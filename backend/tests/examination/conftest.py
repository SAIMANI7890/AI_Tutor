"""
Pytest fixtures for examination tests
"""
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.dialects import sqlite
from sqlalchemy import types
import uuid

from app.db.base import Base
from app.models.user import User
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.enums import QuestionType, TestStatus


# ============================================================
# UUID SUPPORT FOR SQLITE
# ============================================================

class GUID(types.TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses CHAR(36), storing as stringified hex values.
    """
    impl = types.CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(types.UUID())
        else:
            return dialect.type_descriptor(types.CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if isinstance(value, uuid.UUID):
                return str(value)
            return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(value)


# Replace UUID type with GUID for SQLite compatibility
@event.listens_for(Base.metadata, "before_create")
def replace_uuid_columns(target, connection, **kw):
    """Replace UUID columns with GUID for SQLite compatibility"""
    for table in target.tables.values():
        for column in table.columns:
            if isinstance(column.type, types.UUID):
                column.type = GUID()


# ============================================================
# TEST DATABASE SETUP
# ============================================================

# Create in-memory SQLite database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Get database session for tests"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        email="exam_test@example.com",
        full_name="Exam Test User",
        password_hash="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_test(db_session, test_user):
    """Create a sample test"""
    test = Test(
        user_id=test_user.id,
        subject="Social Studies",
        question_type=QuestionType.MCQ,
        selected_categories=["History", "Geography"],
        question_count=5,
        status=TestStatus.GENERATED
    )
    db_session.add(test)
    db_session.commit()
    db_session.refresh(test)
    return test


@pytest.fixture
def sample_question(db_session, sample_test):
    """Create a sample question"""
    question = TestQuestion(
        test_id=sample_test.id,
        question_number=1,
        question_type=QuestionType.MCQ,
        question_text="Sample question?",
        options_json=["Option A", "Option B", "Option C", "Option D"],
        correct_answer="A",
        model_answer="Sample answer explanation",
        source_document="sample.pdf",
        source_page=1,
        category="History"
    )
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)
    return question
