"""
Study Plans API Tests
Comprehensive tests for study plan endpoints
"""
import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models.user import User
from app.models.study_plan import StudyPlan, StudyPlanItem, StudyStatus
from app.core.security import hash_password, create_access_token


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


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# ============================================================
# FIXTURES
# ============================================================

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
        email="test@example.com",
        full_name="Test User",
        password_hash=hash_password("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def another_user(db_session):
    """Create another test user"""
    user = User(
        email="another@example.com",
        full_name="Another User",
        password_hash=hash_password("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user):
    """Get authentication headers for test user"""
    access_token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def another_user_headers(another_user):
    """Get authentication headers for another user"""
    access_token = create_access_token(data={"sub": str(another_user.id)})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def sample_study_plan(db_session, test_user):
    """Create a sample study plan with items"""
    from app.models.study_plan import ActivityType
    
    plan = StudyPlan(
        user_id=test_user.id,
        exam_date=date.today() + timedelta(days=30),
        daily_study_hours=3.0
    )
    db_session.add(plan)
    db_session.flush()
    
    # Add some items
    for i in range(5):
        item = StudyPlanItem(
            study_plan_id=plan.id,
            day_number=i + 1,
            study_date=date.today() + timedelta(days=i),
            activity_type=ActivityType.STUDY if i < 3 else ActivityType.REVISION,
            chapter_id=1 if i < 3 else None,
            chapter_name="Test Chapter" if i < 3 else None,
            allocated_hours=3.0,
            status=StudyStatus.COMPLETED if i < 2 else StudyStatus.PENDING
        )
        db_session.add(item)
    
    db_session.commit()
    db_session.refresh(plan)
    return plan


# ============================================================
# TEST: CREATE STUDY PLAN
# ============================================================

class TestCreateStudyPlan:
    """Tests for POST /api/v1/study-plans/"""
    
    def test_create_plan_success(self, auth_headers):
        """Test successful study plan creation"""
        payload = {
            "exam_date": (date.today() + timedelta(days=30)).isoformat(),
            "daily_study_hours": 3.0,
            "selected_chapter_ids": [1, 2, 3]
        }
        
        response = client.post(
            "/api/v1/study-plans/",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert "plan_id" in data["data"]
        assert data["data"]["total_days"] > 0
        assert data["data"]["items_count"] > 0
    
    def test_create_plan_unauthorized(self):
        """Test creation without authentication"""
        payload = {
            "exam_date": (date.today() + timedelta(days=30)).isoformat(),
            "daily_study_hours": 3.0,
            "selected_chapter_ids": [1, 2, 3]
        }
        
        response = client.post("/api/v1/study-plans/", json=payload)
        assert response.status_code == 403  # No auth header
    
    def test_create_plan_past_date(self, auth_headers):
        """Test creation with past exam date"""
        payload = {
            "exam_date": (date.today() - timedelta(days=10)).isoformat(),
            "daily_study_hours": 3.0,
            "selected_chapter_ids": [1, 2, 3]
        }
        
        response = client.post(
            "/api/v1/study-plans/",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 400
    
    def test_create_plan_invalid_hours(self, auth_headers):
        """Test creation with invalid daily hours"""
        payload = {
            "exam_date": (date.today() + timedelta(days=30)).isoformat(),
            "daily_study_hours": 15.0,  # Too many hours
            "selected_chapter_ids": [1, 2, 3]
        }
        
        response = client.post(
            "/api/v1/study-plans/",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_create_plan_no_chapters(self, auth_headers):
        """Test creation with no chapters selected"""
        payload = {
            "exam_date": (date.today() + timedelta(days=30)).isoformat(),
            "daily_study_hours": 3.0,
            "selected_chapter_ids": []
        }
        
        response = client.post(
            "/api/v1/study-plans/",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_create_plan_invalid_chapters(self, auth_headers):
        """Test creation with invalid chapter IDs"""
        payload = {
            "exam_date": (date.today() + timedelta(days=30)).isoformat(),
            "daily_study_hours": 3.0,
            "selected_chapter_ids": [9999, 8888]  # Invalid IDs
        }
        
        response = client.post(
            "/api/v1/study-plans/",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 400


# ============================================================
# TEST: LIST STUDY PLANS
# ============================================================

class TestListStudyPlans:
    """Tests for GET /api/v1/study-plans/"""
    
    def test_list_plans_success(self, auth_headers, sample_study_plan):
        """Test listing study plans"""
        response = client.get("/api/v1/study-plans/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "plans" in data["data"]
        assert data["data"]["total_count"] >= 1
        
        # Check plan structure
        plan = data["data"]["plans"][0]
        assert "id" in plan
        assert "exam_date" in plan
        assert "completion_percentage" in plan
        assert "total_items" in plan
        assert "completed_items" in plan
    
    def test_list_plans_unauthorized(self):
        """Test listing without authentication"""
        response = client.get("/api/v1/study-plans/")
        assert response.status_code == 403
    
    def test_list_plans_empty(self, auth_headers):
        """Test listing when no plans exist"""
        response = client.get("/api/v1/study-plans/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total_count"] == 0
        assert len(data["data"]["plans"]) == 0
    
    def test_list_plans_completion_percentage(self, auth_headers, sample_study_plan):
        """Test that completion percentage is calculated correctly"""
        response = client.get("/api/v1/study-plans/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        plan = data["data"]["plans"][0]
        
        # Sample plan has 2 completed out of 5 items = 40%
        assert plan["completion_percentage"] == 40.0


# ============================================================
# TEST: GET STUDY PLAN DETAILS
# ============================================================

class TestGetStudyPlan:
    """Tests for GET /api/v1/study-plans/{plan_id}"""
    
    def test_get_plan_success(self, auth_headers, sample_study_plan):
        """Test getting study plan details"""
        response = client.get(
            f"/api/v1/study-plans/{sample_study_plan.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        plan = data["data"]
        assert plan["id"] == sample_study_plan.id
        assert "items" in plan
        assert len(plan["items"]) == 5
        assert plan["completion_percentage"] == 40.0
    
    def test_get_plan_unauthorized(self, sample_study_plan):
        """Test getting plan without authentication"""
        response = client.get(f"/api/v1/study-plans/{sample_study_plan.id}")
        assert response.status_code == 403
    
    def test_get_plan_not_found(self, auth_headers):
        """Test getting non-existent plan"""
        response = client.get("/api/v1/study-plans/9999", headers=auth_headers)
        assert response.status_code == 404
    
    def test_get_plan_wrong_owner(self, another_user_headers, sample_study_plan):
        """Test getting another user's plan"""
        response = client.get(
            f"/api/v1/study-plans/{sample_study_plan.id}",
            headers=another_user_headers
        )
        
        assert response.status_code == 403


# ============================================================
# TEST: UPDATE STUDY ITEM STATUS
# ============================================================

class TestUpdateStudyItemStatus:
    """Tests for PATCH /api/v1/study-plans/{plan_id}/items/{item_id}"""
    
    def test_update_status_to_completed(self, auth_headers, sample_study_plan):
        """Test updating item status to completed"""
        item_id = sample_study_plan.items[2].id  # Third item (currently Pending)
        
        response = client.patch(
            f"/api/v1/study-plans/{sample_study_plan.id}/items/{item_id}",
            json={"status": "Completed"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"] == "Completed"
    
    def test_update_status_to_skipped(self, auth_headers, sample_study_plan):
        """Test updating item status to skipped"""
        item_id = sample_study_plan.items[2].id
        
        response = client.patch(
            f"/api/v1/study-plans/{sample_study_plan.id}/items/{item_id}",
            json={"status": "Skipped"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "Skipped"
    
    def test_update_status_unauthorized(self, sample_study_plan):
        """Test updating without authentication"""
        item_id = sample_study_plan.items[0].id
        
        response = client.patch(
            f"/api/v1/study-plans/{sample_study_plan.id}/items/{item_id}",
            json={"status": "Completed"}
        )
        
        assert response.status_code == 403
    
    def test_update_status_wrong_owner(self, another_user_headers, sample_study_plan):
        """Test updating another user's plan item"""
        item_id = sample_study_plan.items[0].id
        
        response = client.patch(
            f"/api/v1/study-plans/{sample_study_plan.id}/items/{item_id}",
            json={"status": "Completed"},
            headers=another_user_headers
        )
        
        assert response.status_code == 404  # Plan not found for this user
    
    def test_update_status_invalid_item(self, auth_headers, sample_study_plan):
        """Test updating non-existent item"""
        response = client.patch(
            f"/api/v1/study-plans/{sample_study_plan.id}/items/9999",
            json={"status": "Completed"},
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    def test_update_status_invalid_value(self, auth_headers, sample_study_plan):
        """Test updating with invalid status value"""
        item_id = sample_study_plan.items[0].id
        
        response = client.patch(
            f"/api/v1/study-plans/{sample_study_plan.id}/items/{item_id}",
            json={"status": "InvalidStatus"},
            headers=auth_headers
        )
        
        assert response.status_code == 422  # Validation error


# ============================================================
# TEST: DELETE STUDY PLAN
# ============================================================

class TestDeleteStudyPlan:
    """Tests for DELETE /api/v1/study-plans/{plan_id}"""
    
    def test_delete_plan_success(self, auth_headers, sample_study_plan, db_session):
        """Test successful plan deletion"""
        plan_id = sample_study_plan.id
        
        response = client.delete(
            f"/api/v1/study-plans/{plan_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # Verify plan is deleted
        deleted_plan = db_session.query(StudyPlan).filter(StudyPlan.id == plan_id).first()
        assert deleted_plan is None
    
    def test_delete_plan_cascade(self, auth_headers, sample_study_plan, db_session):
        """Test that items are cascade deleted"""
        plan_id = sample_study_plan.id
        
        # Count items before deletion
        items_before = db_session.query(StudyPlanItem).filter(
            StudyPlanItem.study_plan_id == plan_id
        ).count()
        assert items_before == 5
        
        # Delete plan
        response = client.delete(
            f"/api/v1/study-plans/{plan_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        
        # Verify items are deleted
        items_after = db_session.query(StudyPlanItem).filter(
            StudyPlanItem.study_plan_id == plan_id
        ).count()
        assert items_after == 0
    
    def test_delete_plan_unauthorized(self, sample_study_plan):
        """Test deletion without authentication"""
        response = client.delete(f"/api/v1/study-plans/{sample_study_plan.id}")
        assert response.status_code == 403
    
    def test_delete_plan_not_found(self, auth_headers):
        """Test deleting non-existent plan"""
        response = client.delete("/api/v1/study-plans/9999", headers=auth_headers)
        assert response.status_code == 404
    
    def test_delete_plan_wrong_owner(self, another_user_headers, sample_study_plan):
        """Test deleting another user's plan"""
        response = client.delete(
            f"/api/v1/study-plans/{sample_study_plan.id}",
            headers=another_user_headers
        )
        
        assert response.status_code == 404


# ============================================================
# TEST: COMPLETION CALCULATION
# ============================================================

class TestCompletionCalculation:
    """Tests for completion percentage calculation"""
    
    def test_completion_zero_percent(self, auth_headers, db_session, test_user):
        """Test 0% completion"""
        from app.models.study_plan import ActivityType
        
        # Create plan with no completed items
        plan = StudyPlan(
            user_id=test_user.id,
            exam_date=date.today() + timedelta(days=30),
            daily_study_hours=3.0
        )
        db_session.add(plan)
        db_session.flush()
        
        for i in range(5):
            item = StudyPlanItem(
                study_plan_id=plan.id,
                day_number=i + 1,
                study_date=date.today() + timedelta(days=i),
                activity_type=ActivityType.STUDY,
                chapter_id=1,
                chapter_name="Test Chapter",
                allocated_hours=3.0,
                status=StudyStatus.PENDING
            )
            db_session.add(item)
        
        db_session.commit()
        
        response = client.get(f"/api/v1/study-plans/{plan.id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["data"]["completion_percentage"] == 0.0
    
    def test_completion_hundred_percent(self, auth_headers, db_session, test_user):
        """Test 100% completion"""
        from app.models.study_plan import ActivityType
        
        # Create plan with all completed items
        plan = StudyPlan(
            user_id=test_user.id,
            exam_date=date.today() + timedelta(days=30),
            daily_study_hours=3.0
        )
        db_session.add(plan)
        db_session.flush()
        
        for i in range(5):
            item = StudyPlanItem(
                study_plan_id=plan.id,
                day_number=i + 1,
                study_date=date.today() + timedelta(days=i),
                activity_type=ActivityType.STUDY,
                chapter_id=1,
                chapter_name="Test Chapter",
                allocated_hours=3.0,
                status=StudyStatus.COMPLETED
            )
            db_session.add(item)
        
        db_session.commit()
        
        response = client.get(f"/api/v1/study-plans/{plan.id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["data"]["completion_percentage"] == 100.0
    
    def test_completion_partial(self, auth_headers, sample_study_plan):
        """Test partial completion (40%)"""
        response = client.get(
            f"/api/v1/study-plans/{sample_study_plan.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        # Sample plan: 2 completed out of 5 = 40%
        assert response.json()["data"]["completion_percentage"] == 40.0


# ============================================================
# TEST: OWNERSHIP VALIDATION
# ============================================================

class TestOwnershipValidation:
    """Tests for plan ownership security"""
    
    def test_cannot_view_others_plans(self, auth_headers, another_user_headers, db_session, test_user, another_user):
        """Test that users cannot see each other's plans"""
        # Create plan for test_user
        plan1 = StudyPlan(
            user_id=test_user.id,
            exam_date=date.today() + timedelta(days=30),
            daily_study_hours=3.0
        )
        db_session.add(plan1)
        
        # Create plan for another_user
        plan2 = StudyPlan(
            user_id=another_user.id,
            exam_date=date.today() + timedelta(days=30),
            daily_study_hours=3.0
        )
        db_session.add(plan2)
        db_session.commit()
        
        # test_user should only see their own plan
        response = client.get("/api/v1/study-plans/", headers=auth_headers)
        data = response.json()
        assert data["data"]["total_count"] == 1
        assert data["data"]["plans"][0]["id"] == plan1.id
        
        # another_user should only see their own plan
        response = client.get("/api/v1/study-plans/", headers=another_user_headers)
        data = response.json()
        assert data["data"]["total_count"] == 1
        assert data["data"]["plans"][0]["id"] == plan2.id


# ============================================================
# TEST: API RESPONSE FORMAT
# ============================================================

class TestAPIResponseFormat:
    """Tests for consistent API response format"""
    
    def test_success_response_format(self, auth_headers):
        """Test success response structure"""
        response = client.get("/api/v1/study-plans/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check standard fields
        assert "success" in data
        assert "message" in data
        assert "data" in data
        assert data["success"] is True
    
    def test_error_response_format(self, auth_headers):
        """Test error response structure"""
        response = client.get("/api/v1/study-plans/9999", headers=auth_headers)
        
        assert response.status_code == 404
        data = response.json()
        
        # FastAPI automatically provides detail
        assert "detail" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
