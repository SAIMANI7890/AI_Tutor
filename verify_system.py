"""
Automated System Verification Script
Tests all critical features of the AI Study Companion

Usage:
    python verify_system.py
"""

import requests
import json
from datetime import date, timedelta
from typing import Dict, List, Tuple


# Configuration
BASE_URL = "http://localhost:8000/api/v1"
TEST_USER = {
    "email": "verify@test.com",
    "password": "verify123",
    "confirm_password": "verify123",
    "full_name": "Verify Test User"
}

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print test section header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def print_test(name: str):
    """Print test name"""
    print(f"\n{Colors.OKBLUE}TEST: {name}{Colors.ENDC}")


def print_pass(msg: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}  ✓ PASS: {msg}{Colors.ENDC}")


def print_fail(msg: str):
    """Print failure message"""
    print(f"{Colors.FAIL}  ✗ FAIL: {msg}{Colors.ENDC}")


def print_warn(msg: str):
    """Print warning message"""
    print(f"{Colors.WARNING}  ⚠ WARN: {msg}{Colors.ENDC}")


def print_info(msg: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}  ℹ INFO: {msg}{Colors.ENDC}")


# Test results tracking
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "critical_failures": []
}


def record_result(test_name: str, passed: bool, critical: bool = False):
    """Record test result"""
    test_results["total"] += 1
    if passed:
        test_results["passed"] += 1
    else:
        test_results["failed"] += 1
        if critical:
            test_results["critical_failures"].append(test_name)


# ============================================================
# 1. AUTHENTICATION TESTS
# ============================================================

def test_authentication() -> Tuple[bool, str]:
    """Test authentication flow"""
    print_header("1. AUTHENTICATION TESTING")
    
    # Test 1.1: Registration or Login
    print_test("1.1 User Registration/Login")
    token = None
    try:
        # Try to register
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=TEST_USER
        )
        
        if response.status_code == 201:
            data = response.json()
            if data.get("success") and "access_token" in data.get("data", {}):
                token = data["data"]["access_token"]
                print_pass(f"Registration successful (Status: {response.status_code})")
                print_pass("Access token received")
                record_result("Registration", True)
            else:
                print_fail("No token in response")
                record_result("Registration", False)
                return False, None
        elif response.status_code == 400:
            # User already exists, try to login
            print_info("User already exists, attempting login...")
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={"email": TEST_USER["email"], "password": TEST_USER["password"]}
            )
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data.get("data", {}):
                    token = data["data"]["access_token"]
                    print_pass("Login successful (using existing user)")
                    print_pass("Access token received")
                    record_result("Registration", True)
                else:
                    print_fail("No token in login response")
                    record_result("Registration", False)
                    return False, None
            else:
                print_fail(f"Login failed (Status: {response.status_code})")
                record_result("Registration", False)
                return False, None
        else:
            print_fail(f"Registration failed (Status: {response.status_code})")
            print_info(f"Response: {response.text[:200]}")
            record_result("Registration", False)
            return False, None
            
    except Exception as e:
        print_fail(f"Registration error: {str(e)}")
        record_result("Registration", False)
        return False, None
    
    # Test 1.2: Login Valid
    print_test("1.2 Login with Valid Credentials")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": TEST_USER["email"], "password": TEST_USER["password"]}
        )
        
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data.get("data", {}):
                token = data["data"]["access_token"]
                print_pass("Login successful")
                print_pass("Token generated")
                record_result("Login Valid", True)
            else:
                print_fail("No token in response")
                record_result("Login Valid", False)
                return False, None
        else:
            print_fail(f"Login failed (Status: {response.status_code})")
            record_result("Login Valid", False)
            return False, None
            
    except Exception as e:
        print_fail(f"Login error: {str(e)}")
        record_result("Login Valid", False)
        return False, None
    
    # Test 1.3: Login Invalid
    print_test("1.3 Login with Invalid Credentials")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": TEST_USER["email"], "password": "wrongpassword"}
        )
        
        if response.status_code == 401:
            print_pass("Invalid login rejected (401 Unauthorized)")
            record_result("Login Invalid", True)
        else:
            print_fail(f"Should return 401, got {response.status_code}")
            record_result("Login Invalid", False)
            
    except Exception as e:
        print_fail(f"Test error: {str(e)}")
        record_result("Login Invalid", False)
    
    return True, token


# ============================================================
# 2. RAG VERIFICATION (CRITICAL)
# ============================================================

def test_rag(token: str):
    """Test RAG system"""
    print_header("2. RAG VERIFICATION (CRITICAL)")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # First create a chat session for testing
    print_test("2.0 Create Test Chat Session")
    session_id = None
    try:
        response = requests.post(
            f"{BASE_URL}/chat/session",
            headers=headers,
            json={"title": "RAG Test Session"}
        )
        
        if response.status_code == 201:
            data = response.json()
            session_id = data.get("data", {}).get("id")
            if session_id:
                print_pass(f"Test session created (ID: {session_id})")
            else:
                print_fail("No session ID returned")
                return
        else:
            print_fail(f"Failed to create session (Status: {response.status_code})")
            return
    except Exception as e:
        print_fail(f"Test error: {str(e)}")
        return
    
    # Test 2.1: Democracy Question
    print_test("2.1 Democracy Question")
    try:
        response = requests.post(
            f"{BASE_URL}/tutor/chat",
            headers=headers,
            json={
                "session_id": session_id,
                "question": "What is democracy?"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("data", {}).get("answer", "")
            sources = data.get("data", {}).get("sources", [])
            
            if answer and len(answer) > 50:
                print_pass("Answer received")
                
                if sources and any("politics" in str(s).lower() for s in sources):
                    print_pass("Sources cited (politics PDF)")
                    record_result("RAG Democracy", True)
                else:
                    print_warn("No sources or wrong PDF cited")
                    record_result("RAG Democracy", False)
            else:
                print_fail("No answer or too short")
                record_result("RAG Democracy", False)
        else:
            print_fail(f"Query failed (Status: {response.status_code})")
            print_info(f"Response: {response.text[:200]}")
            record_result("RAG Democracy", False)
            
    except Exception as e:
        print_fail(f"Test error: {str(e)}")
        record_result("RAG Democracy", False)
    
    # Test 2.2: Out-of-Syllabus (CRITICAL)
    print_test("2.2 Out-of-Syllabus Question (CRITICAL)")
    try:
        response = requests.post(
            f"{BASE_URL}/tutor/chat",
            headers=headers,
            json={
                "session_id": session_id,
                "question": "What is quantum computing?"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("data", {}).get("answer", "").lower()
            
            # Check for refusal phrases
            refusal_phrases = [
                "could not find",
                "not find this information",
                "social studies",
                "cannot help",
                "outside"
            ]
            
            if any(phrase in answer for phrase in refusal_phrases):
                print_pass("✅ CRITICAL: RAG guardrail working!")
                print_pass("System correctly refuses out-of-syllabus question")
                record_result("RAG Out-of-Syllabus", True, critical=True)
            else:
                print_fail("🔴 CRITICAL: RAG guardrail NOT working!")
                print_fail("System answered quantum computing question")
                print_info(f"Answer preview: {answer[:150]}...")
                record_result("RAG Out-of-Syllabus", False, critical=True)
        else:
            print_fail(f"Query failed (Status: {response.status_code})")
            print_info(f"Response: {response.text[:200]}")
            record_result("RAG Out-of-Syllabus", False, critical=True)
            
    except Exception as e:
        print_fail(f"Test error: {str(e)}")
        record_result("RAG Out-of-Syllabus", False, critical=True)


# ============================================================
# 3. STUDY PLANNER VERIFICATION (CRITICAL)
# ============================================================

def test_study_planner(token: str):
    """Test study planner"""
    print_header("4. STUDY PLANNER VERIFICATION (CRITICAL)")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 4.1: Normal Plan
    print_test("4.1 Normal Plan Generation")
    try:
        exam_date = (date.today() + timedelta(days=30)).isoformat()
        response = requests.post(
            f"{BASE_URL}/study-plans/",
            headers=headers,
            json={
                "exam_date": exam_date,
                "daily_study_hours": 3.0,
                "selected_chapter_ids": [1, 2, 3, 11, 21]
            }
        )
        
        if response.status_code == 201:
            data = response.json()
            plan_data = data.get("data", {})
            plan_id = plan_data.get("plan_id")
            
            if plan_id:
                print_pass(f"Plan created (ID: {plan_id})")
                print_pass(f"Total days: {plan_data.get('total_days')}")
                print_pass(f"Items: {plan_data.get('items_count')}")
                record_result("Study Plan Normal", True, critical=True)
                
                # Get plan details for further tests
                return test_plan_details(token, plan_id)
            else:
                print_fail("No plan ID returned")
                record_result("Study Plan Normal", False, critical=True)
                return False
        else:
            print_fail(f"Plan creation failed (Status: {response.status_code})")
            print_info(f"Response: {response.text[:200]}")
            record_result("Study Plan Normal", False, critical=True)
            return False
            
    except Exception as e:
        print_fail(f"Test error: {str(e)}")
        record_result("Study Plan Normal", False, critical=True)
        return False


def test_plan_details(token: str, plan_id: int) -> bool:
    """Test plan details and structure"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get plan details
    print_test("4.2 Hard Chapter Priority")
    try:
        response = requests.get(
            f"{BASE_URL}/study-plans/{plan_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            plan = data.get("data", {})
            items = plan.get("items", [])
            
            if items:
                # Check hard chapter prioritization
                study_items = [item for item in items if item.get("activity_type") == "Study"]
                
                if study_items:
                    first_chapters = [item.get("chapter_name") for item in study_items[:3]]
                    print_pass(f"First chapters: {', '.join(first_chapters)}")
                    record_result("Hard Priority", True, critical=True)
                
                # Test 4.3: Check for revision days
                print_test("4.3 Revision Days")
                revision_items = [item for item in items if item.get("activity_type") == "Revision"]
                
                if revision_items:
                    print_pass(f"Found {len(revision_items)} revision days")
                    record_result("Revision Days", True, critical=True)
                else:
                    print_warn("No revision days found")
                    record_result("Revision Days", False, critical=True)
                
                # Test 4.4: Check for mock tests
                print_test("4.4 Mock Tests")
                mock_test_items = [item for item in items if item.get("activity_type") == "MockTest"]
                
                if mock_test_items:
                    print_pass(f"Found {len(mock_test_items)} mock test days")
                    record_result("Mock Tests", True, critical=True)
                else:
                    print_warn("No mock test days found")
                    record_result("Mock Tests", False, critical=True)
                
                # Test 4.5: Plan ends before exam
                print_test("4.5 Plan Ends Before Exam")
                exam_date = plan.get("exam_date")
                last_item_date = items[-1].get("study_date") if items else None
                
                if last_item_date and last_item_date < exam_date:
                    print_pass(f"Last item: {last_item_date}, Exam: {exam_date}")
                    print_pass("Plan ends before exam ✓")
                    record_result("Plan Ends Before Exam", True, critical=True)
                else:
                    print_fail("Plan extends to or past exam date")
                    record_result("Plan Ends Before Exam", False, critical=True)
                
                return True
            else:
                print_fail("No items in plan")
                return False
        else:
            print_fail(f"Failed to get plan details (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print_fail(f"Test error: {str(e)}")
        return False


# ============================================================
# 5. EDGE CASES
# ============================================================

def test_edge_cases(token: str):
    """Test edge cases"""
    print_header("5. EDGE CASES TESTING")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 5.1: Past Date
    print_test("5.1 Past Exam Date Rejection")
    try:
        past_date = (date.today() - timedelta(days=10)).isoformat()
        response = requests.post(
            f"{BASE_URL}/study-plans/",
            headers=headers,
            json={
                "exam_date": past_date,
                "daily_study_hours": 3.0,
                "selected_chapter_ids": [1, 2, 3]
            }
        )
        
        if response.status_code == 400:
            print_pass("Past date rejected (400 Bad Request)")
            record_result("Past Date Rejection", True)
        else:
            print_fail(f"Should return 400, got {response.status_code}")
            record_result("Past Date Rejection", False)
            
    except Exception as e:
        print_fail(f"Test error: {str(e)}")
        record_result("Past Date Rejection", False)
    
    # Test 5.2: No Chapters
    print_test("5.2 No Chapters Selected")
    try:
        exam_date = (date.today() + timedelta(days=30)).isoformat()
        response = requests.post(
            f"{BASE_URL}/study-plans/",
            headers=headers,
            json={
                "exam_date": exam_date,
                "daily_study_hours": 3.0,
                "selected_chapter_ids": []
            }
        )
        
        if response.status_code == 422:
            print_pass("Empty chapters rejected (422 Unprocessable Entity)")
            record_result("No Chapters Rejection", True)
        else:
            print_fail(f"Should return 422, got {response.status_code}")
            record_result("No Chapters Rejection", False)
            
    except Exception as e:
        print_fail(f"Test error: {str(e)}")
        record_result("No Chapters Rejection", False)


# ============================================================
# MAIN EXECUTION
# ============================================================

def print_summary():
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    total = test_results["total"]
    passed = test_results["passed"]
    failed = test_results["failed"]
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"\nTotal Tests: {total}")
    print(f"{Colors.OKGREEN}Passed: {passed}{Colors.ENDC}")
    print(f"{Colors.FAIL}Failed: {failed}{Colors.ENDC}")
    print(f"\nSuccess Rate: {percentage:.1f}%")
    
    if test_results["critical_failures"]:
        print(f"\n{Colors.FAIL}{Colors.BOLD}🔴 CRITICAL FAILURES:{Colors.ENDC}")
        for failure in test_results["critical_failures"]:
            print(f"{Colors.FAIL}  - {failure}{Colors.ENDC}")
    
    print(f"\n{'='*70}")
    
    if failed == 0:
        print(f"{Colors.OKGREEN}{Colors.BOLD}✅ ALL TESTS PASSED!{Colors.ENDC}")
        print(f"{Colors.OKGREEN}System is ready for production.{Colors.ENDC}")
    elif test_results["critical_failures"]:
        print(f"{Colors.FAIL}{Colors.BOLD}❌ CRITICAL FAILURES DETECTED!{Colors.ENDC}")
        print(f"{Colors.FAIL}Fix critical issues before proceeding.{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}{Colors.BOLD}⚠ SOME TESTS FAILED{Colors.ENDC}")
        print(f"{Colors.WARNING}Review failures and fix issues.{Colors.ENDC}")
    
    print(f"{'='*70}\n")


def main():
    """Main test execution"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("="*70)
    print("AI STUDY COMPANION - SYSTEM VERIFICATION".center(70))
    print("="*70)
    print(f"{Colors.ENDC}\n")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info("Starting verification tests...\n")
    
    # Run tests
    success, token = test_authentication()
    
    if success and token:
        test_rag(token)
        test_study_planner(token)
        test_edge_cases(token)
    else:
        print_fail("\n❌ Authentication failed. Cannot proceed with other tests.")
        print_info("Make sure the server is running and the database is set up.")
    
    # Print summary
    print_summary()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Test interrupted by user{Colors.ENDC}\n")
    except Exception as e:
        print(f"\n\n{Colors.FAIL}Unexpected error: {str(e)}{Colors.ENDC}\n")
        import traceback
        traceback.print_exc()
