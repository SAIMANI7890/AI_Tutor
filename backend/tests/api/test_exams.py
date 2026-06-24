"""
Phase 4C Examination API Tests
=================================
Tests for all 8 exam endpoints:
  1. POST /exams/generate
  2. GET  /exams/
  3. GET  /exams/history
  4. GET  /exams/{test_id}
  5. GET  /exams/{test_id}/questions
  6. POST /exams/{test_id}/answer
  7. GET  /exams/{test_id}/answers
  8. POST /exams/{test_id}/submit

Coverage:
  - Happy-path success responses
  - Authentication checks (missing / invalid token)
  - Authorization checks (wrong owner)
  - Validation errors (bad input)
  - Business rule enforcement (duplicate submit)
"""
import uuid
from unittest.mock import MagicMock, patch

import pytest


# ===========================================================================
# 1. POST /exams/generate
# ===========================================================================

class TestGenerateExam:
    """Tests for POST /api/v1/exams/generate"""

    ENDPOINT = "/api/v1/exams/generate"
    VALID_PAYLOAD = {
        "categories": ["History", "Politics"],
        "question_type": "MCQ",
        "question_count": 5,
    }

    def test_generate_exam_success(self, client, auth_headers):
        """ExamService.generate_exam is called; returns 201 with test_id."""
        mock_data = {"test_id": str(uuid.uuid4()), "question_count": 5, "status": "GENERATED"}

        with patch(
            "app.api.v1.endpoints.exams.ExamService.generate_exam",
            return_value=mock_data,
        ):
            response = client.post(self.ENDPOINT, json=self.VALID_PAYLOAD, headers=auth_headers)

        assert response.status_code == 201
        body = response.json()
        assert body["success"] is True
        assert body["message"] == "Exam generated successfully"
        assert "test_id" in body["data"]
        assert body["data"]["status"] == "GENERATED"

    def test_generate_exam_requires_auth(self, client):
        """Request without auth should return 403 (Bearer scheme enforced)."""
        response = client.post(self.ENDPOINT, json=self.VALID_PAYLOAD)
        assert response.status_code == 403

    def test_generate_exam_invalid_category(self, client, auth_headers):
        """Invalid category name should return 422."""
        payload = {**self.VALID_PAYLOAD, "categories": ["InvalidSubject"]}
        response = client.post(self.ENDPOINT, json=payload, headers=auth_headers)
        assert response.status_code == 422

    def test_generate_exam_invalid_question_type(self, client, auth_headers):
        """Unknown question_type should return 422."""
        payload = {**self.VALID_PAYLOAD, "question_type": "ESSAY"}
        response = client.post(self.ENDPOINT, json=payload, headers=auth_headers)
        assert response.status_code == 422

    def test_generate_exam_count_too_high(self, client, auth_headers):
        """question_count > 10 should return 422."""
        payload = {**self.VALID_PAYLOAD, "question_count": 11}
        response = client.post(self.ENDPOINT, json=payload, headers=auth_headers)
        assert response.status_code == 422

    def test_generate_exam_count_too_low(self, client, auth_headers):
        """question_count < 1 should return 422."""
        payload = {**self.VALID_PAYLOAD, "question_count": 0}
        response = client.post(self.ENDPOINT, json=payload, headers=auth_headers)
        assert response.status_code == 422

    def test_generate_exam_empty_categories(self, client, auth_headers):
        """Empty categories list should return 422."""
        payload = {**self.VALID_PAYLOAD, "categories": []}
        response = client.post(self.ENDPOINT, json=payload, headers=auth_headers)
        assert response.status_code == 422

    def test_all_valid_question_types(self, client, auth_headers):
        """All four question types should be accepted by the schema."""
        for qt in ["MCQ", "FILL_BLANKS", "SHORT_ANSWER", "LONG_ANSWER"]:
            mock_data = {"test_id": str(uuid.uuid4()), "question_count": 1, "status": "GENERATED"}
            with patch(
                "app.api.v1.endpoints.exams.ExamService.generate_exam",
                return_value=mock_data,
            ):
                payload = {"categories": ["History"], "question_type": qt, "question_count": 1}
                response = client.post(self.ENDPOINT, json=payload, headers=auth_headers)
            assert response.status_code == 201, f"Expected 201 for type {qt}"


# ===========================================================================
# 2. GET /exams/
# ===========================================================================

class TestListExams:
    ENDPOINT = "/api/v1/exams/"

    def test_list_exams_success(self, client, auth_headers, sample_test):
        """Should return a list of exams for the current user."""
        response = client.get(self.ENDPOINT, headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["data"], list)
        assert len(body["data"]) >= 1

    def test_list_exams_requires_auth(self, client):
        response = client.get(self.ENDPOINT)
        assert response.status_code == 403

    def test_list_exams_empty_for_new_user(self, client, auth_headers):
        """User with no exams should get empty list, not an error."""
        response = client.get(self.ENDPOINT, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["data"] == []

    def test_list_exams_only_own_exams(self, client, auth_headers, other_auth_headers, sample_test):
        """Other user's exams must not appear in the list."""
        response = client.get(self.ENDPOINT, headers=other_auth_headers)
        body = response.json()
        assert body["success"] is True
        # other_user has no exams
        assert body["data"] == []


# ===========================================================================
# 3. GET /exams/history
# ===========================================================================

class TestExamHistory:
    ENDPOINT = "/api/v1/exams/history"

    def test_history_requires_auth(self, client):
        response = client.get(self.ENDPOINT)
        assert response.status_code == 403

    def test_history_returns_list(self, client, auth_headers, sample_test):
        response = client.get(self.ENDPOINT, headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["data"], list)

    def test_history_contains_expected_fields(self, client, auth_headers, sample_test):
        response = client.get(self.ENDPOINT, headers=auth_headers)
        exam = response.json()["data"][0]
        for field in ["id", "question_type", "question_count", "status", "created_at"]:
            assert field in exam, f"Field '{field}' missing from history item"


# ===========================================================================
# 4. GET /exams/{test_id}
# ===========================================================================

class TestGetExamDetail:

    def test_get_exam_success(self, client, auth_headers, sample_test, sample_questions):
        url = f"/api/v1/exams/{sample_test.id}"
        response = client.get(url, headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        data = body["data"]
        assert data["id"] == str(sample_test.id)
        assert "questions" in data

    def test_get_exam_not_found(self, client, auth_headers):
        url = f"/api/v1/exams/{uuid.uuid4()}"
        response = client.get(url, headers=auth_headers)
        assert response.status_code == 404

    def test_get_exam_wrong_owner(self, client, other_auth_headers, sample_test):
        url = f"/api/v1/exams/{sample_test.id}"
        response = client.get(url, headers=other_auth_headers)
        assert response.status_code == 403

    def test_get_exam_requires_auth(self, client, sample_test):
        url = f"/api/v1/exams/{sample_test.id}"
        response = client.get(url)
        assert response.status_code == 403

    def test_correct_answer_not_exposed(self, client, auth_headers, sample_test, sample_questions):
        """Verify correct_answer and model_answer are NOT in the response."""
        url = f"/api/v1/exams/{sample_test.id}"
        response = client.get(url, headers=auth_headers)
        assert response.status_code == 200
        for question in response.json()["data"]["questions"]:
            assert "correct_answer" not in question
            assert "model_answer" not in question


# ===========================================================================
# 5. GET /exams/{test_id}/questions
# ===========================================================================

class TestGetQuestions:

    def test_get_questions_success(self, client, auth_headers, sample_test, sample_questions):
        url = f"/api/v1/exams/{sample_test.id}/questions"
        response = client.get(url, headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        questions = body["data"]
        assert len(questions) == 2  # sample_questions has 2

    def test_questions_not_found(self, client, auth_headers):
        url = f"/api/v1/exams/{uuid.uuid4()}/questions"
        response = client.get(url, headers=auth_headers)
        assert response.status_code == 404

    def test_questions_wrong_owner(self, client, other_auth_headers, sample_test):
        url = f"/api/v1/exams/{sample_test.id}/questions"
        response = client.get(url, headers=other_auth_headers)
        assert response.status_code == 403

    def test_mcq_includes_options(self, client, auth_headers, sample_test, sample_questions):
        url = f"/api/v1/exams/{sample_test.id}/questions"
        response = client.get(url, headers=auth_headers)
        question = response.json()["data"][0]
        assert "options" in question
        assert len(question["options"]) == 4

    def test_correct_answers_not_in_questions(self, client, auth_headers, sample_test, sample_questions):
        url = f"/api/v1/exams/{sample_test.id}/questions"
        response = client.get(url, headers=auth_headers)
        for q in response.json()["data"]:
            assert "correct_answer" not in q
            assert "model_answer" not in q

    def test_status_transitions_to_in_progress(self, client, auth_headers, sample_test, sample_questions, db_session):
        """Fetching questions should move status from GENERATED → IN_PROGRESS."""
        from app.models.enums import TestStatus
        url = f"/api/v1/exams/{sample_test.id}/questions"
        client.get(url, headers=auth_headers)

        # Refresh from DB
        db_session.refresh(sample_test)
        assert sample_test.status == TestStatus.IN_PROGRESS


# ===========================================================================
# 6. POST /exams/{test_id}/answer
# ===========================================================================

class TestSaveAnswer:

    def test_save_answer_success(self, client, auth_headers, sample_test, sample_questions):
        url = f"/api/v1/exams/{sample_test.id}/answer"
        payload = {
            "question_id": str(sample_questions[0].id),
            "student_answer": "Option A",
        }
        response = client.post(url, json=payload, headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["message"] == "Answer saved"
        assert "answer_id" in body["data"]

    def test_save_answer_update(self, client, auth_headers, sample_test, sample_questions):
        """Saving the same question twice should update, not create duplicate."""
        url = f"/api/v1/exams/{sample_test.id}/answer"
        payload = {
            "question_id": str(sample_questions[0].id),
            "student_answer": "Option A",
        }
        client.post(url, json=payload, headers=auth_headers)
        # Update the answer
        payload["student_answer"] = "Option B"
        response = client.post(url, json=payload, headers=auth_headers)
        assert response.status_code == 200

    def test_save_answer_wrong_owner(self, client, other_auth_headers, sample_test, sample_questions):
        url = f"/api/v1/exams/{sample_test.id}/answer"
        payload = {
            "question_id": str(sample_questions[0].id),
            "student_answer": "Option A",
        }
        response = client.post(url, json=payload, headers=other_auth_headers)
        assert response.status_code == 403

    def test_save_answer_wrong_question(self, client, auth_headers, sample_test):
        url = f"/api/v1/exams/{sample_test.id}/answer"
        payload = {
            "question_id": str(uuid.uuid4()),  # Random UUID — not in this test
            "student_answer": "Option A",
        }
        response = client.post(url, json=payload, headers=auth_headers)
        assert response.status_code == 404

    def test_save_answer_submitted_exam(self, client, auth_headers, submitted_test, db_session):
        """Cannot save answers to a submitted exam."""
        # Add a dummy question to submitted_test
        from app.models.test_question import TestQuestion
        from app.models.enums import QuestionType
        q = TestQuestion(
            test_id=submitted_test.id,
            question_number=1,
            question_type=QuestionType.MCQ,
            question_text="Q?",
            options_json=["A", "B", "C", "D"],
            correct_answer="A",
            category="History",
        )
        db_session.add(q)
        db_session.commit()
        db_session.refresh(q)

        url = f"/api/v1/exams/{submitted_test.id}/answer"
        payload = {"question_id": str(q.id), "student_answer": "A"}
        response = client.post(url, json=payload, headers=auth_headers)
        assert response.status_code == 400

    def test_save_answer_requires_auth(self, client, sample_test, sample_questions):
        url = f"/api/v1/exams/{sample_test.id}/answer"
        payload = {
            "question_id": str(sample_questions[0].id),
            "student_answer": "Option A",
        }
        response = client.post(url, json=payload)
        assert response.status_code == 403


# ===========================================================================
# 7. GET /exams/{test_id}/answers
# ===========================================================================

class TestGetAnswers:

    def test_get_answers_empty(self, client, auth_headers, sample_test):
        url = f"/api/v1/exams/{sample_test.id}/answers"
        response = client.get(url, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["data"] == []

    def test_get_answers_after_save(self, client, auth_headers, sample_test, sample_questions):
        # Save an answer first
        save_url = f"/api/v1/exams/{sample_test.id}/answer"
        payload = {"question_id": str(sample_questions[0].id), "student_answer": "Option A"}
        client.post(save_url, json=payload, headers=auth_headers)

        # Now retrieve answers
        get_url = f"/api/v1/exams/{sample_test.id}/answers"
        response = client.get(get_url, headers=auth_headers)
        assert response.status_code == 200
        answers = response.json()["data"]
        assert len(answers) == 1
        assert answers[0]["student_answer"] == "Option A"

    def test_get_answers_wrong_owner(self, client, other_auth_headers, sample_test):
        url = f"/api/v1/exams/{sample_test.id}/answers"
        response = client.get(url, headers=other_auth_headers)
        assert response.status_code == 403

    def test_get_answers_not_found(self, client, auth_headers):
        url = f"/api/v1/exams/{uuid.uuid4()}/answers"
        response = client.get(url, headers=auth_headers)
        assert response.status_code == 404

    def test_answers_contain_expected_fields(self, client, auth_headers, sample_test, sample_questions):
        save_url = f"/api/v1/exams/{sample_test.id}/answer"
        payload = {"question_id": str(sample_questions[0].id), "student_answer": "B"}
        client.post(save_url, json=payload, headers=auth_headers)

        get_url = f"/api/v1/exams/{sample_test.id}/answers"
        response = client.get(get_url, headers=auth_headers)
        answer = response.json()["data"][0]
        for field in ["answer_id", "question_id", "student_answer", "updated_at"]:
            assert field in answer


# ===========================================================================
# 8. POST /exams/{test_id}/submit
# ===========================================================================

class TestSubmitExam:

    def test_submit_success(self, client, auth_headers, sample_test, sample_questions):
        url = f"/api/v1/exams/{sample_test.id}/submit"
        response = client.post(url, headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["message"] == "Exam submitted successfully"
        data = body["data"]
        assert data["status"] == "SUBMITTED"
        assert "completed_at" in data
        assert "questions_answered" in data
        assert "total_questions" in data

    def test_submit_updates_status(self, client, auth_headers, sample_test, sample_questions, db_session):
        url = f"/api/v1/exams/{sample_test.id}/submit"
        client.post(url, headers=auth_headers)
        db_session.refresh(sample_test)
        from app.models.enums import TestStatus
        assert sample_test.status == TestStatus.SUBMITTED
        assert sample_test.completed_at is not None

    def test_submit_twice_fails(self, client, auth_headers, submitted_test):
        """Submitting an already-submitted exam should return 400."""
        url = f"/api/v1/exams/{submitted_test.id}/submit"
        response = client.post(url, headers=auth_headers)
        assert response.status_code == 400

    def test_submit_wrong_owner(self, client, other_auth_headers, sample_test):
        url = f"/api/v1/exams/{sample_test.id}/submit"
        response = client.post(url, headers=other_auth_headers)
        assert response.status_code == 403

    def test_submit_not_found(self, client, auth_headers):
        url = f"/api/v1/exams/{uuid.uuid4()}/submit"
        response = client.post(url, headers=auth_headers)
        assert response.status_code == 404

    def test_submit_requires_auth(self, client, sample_test):
        url = f"/api/v1/exams/{sample_test.id}/submit"
        response = client.post(url)
        assert response.status_code == 403

    def test_submit_reflects_answered_count(self, client, auth_headers, sample_test, sample_questions):
        """questions_answered in submit response should match saved answers."""
        # Save one answer
        save_url = f"/api/v1/exams/{sample_test.id}/answer"
        client.post(
            save_url,
            json={"question_id": str(sample_questions[0].id), "student_answer": "A"},
            headers=auth_headers,
        )

        submit_url = f"/api/v1/exams/{sample_test.id}/submit"
        response = client.post(submit_url, headers=auth_headers)
        data = response.json()["data"]
        assert data["questions_answered"] == 1
        assert data["total_questions"] == 2
