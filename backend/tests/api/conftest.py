"""
Conftest for Phase 4C API tests.

Uses FastAPI TestClient with an in-memory SQLite database and
a mocked QuestionGeneratorService so that no Gemini calls are made.
"""
import uuid
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, types
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import create_access_token
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.enums import QuestionType, TestStatus
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.user import User


# ---------------------------------------------------------------------------
# SQLite UUID compatibility (same trick as in existing conftest.py)
# ---------------------------------------------------------------------------

class GUID(types.TypeDecorator):
    """Platform-independent GUID — stores as CHAR(36) in SQLite."""
    impl = types.CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(types.UUID())
        return dialect.type_descriptor(types.CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return str(value) if isinstance(value, uuid.UUID) else str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(value)


@event.listens_for(Base.metadata, "before_create")
def replace_uuid_columns(target, connection, **kw):
    for table in target.tables.values():
        for column in table.columns:
            if isinstance(column.type, types.UUID):
                column.type = GUID()


# ---------------------------------------------------------------------------
# In-memory test database
# ---------------------------------------------------------------------------

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create fresh tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session() -> Generator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Override FastAPI dependency with test database
# ---------------------------------------------------------------------------

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# ---------------------------------------------------------------------------
# Test client
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# Fixtures: users, tokens, tests, questions
# ---------------------------------------------------------------------------

@pytest.fixture
def test_user(db_session) -> User:
    user = User(
        email="student@test.com",
        full_name="Test Student",
        password_hash="$2b$12$fakehash",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def other_user(db_session) -> User:
    """A second user to test authorization."""
    user = User(
        email="other@test.com",
        full_name="Other Student",
        password_hash="$2b$12$fakehash",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user: User) -> dict:
    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_auth_headers(other_user: User) -> dict:
    token = create_access_token(data={"sub": str(other_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_test(db_session, test_user: User) -> Test:
    test = Test(
        user_id=test_user.id,
        subject="Social Studies",
        question_type=QuestionType.MCQ,
        selected_categories=["History", "Geography"],
        question_count=2,
        status=TestStatus.GENERATED,
    )
    db_session.add(test)
    db_session.commit()
    db_session.refresh(test)
    return test


@pytest.fixture
def sample_questions(db_session, sample_test: Test):
    """Two MCQ questions attached to sample_test."""
    questions = []
    for i in range(1, 3):
        q = TestQuestion(
            test_id=sample_test.id,
            question_number=i,
            question_type=QuestionType.MCQ,
            question_text=f"Sample question {i}?",
            options_json=["Option A", "Option B", "Option C", "Option D"],
            correct_answer="Option A",
            model_answer="Detailed explanation here.",
            category="History",
        )
        db_session.add(q)
        questions.append(q)
    db_session.commit()
    for q in questions:
        db_session.refresh(q)
    return questions


@pytest.fixture
def submitted_test(db_session, test_user: User) -> Test:
    from datetime import datetime, timezone
    test = Test(
        user_id=test_user.id,
        subject="Social Studies",
        question_type=QuestionType.MCQ,
        selected_categories=["History"],
        question_count=2,
        status=TestStatus.SUBMITTED,
        completed_at=datetime.now(timezone.utc),
    )
    db_session.add(test)
    db_session.commit()
    db_session.refresh(test)
    return test
