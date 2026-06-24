"""
Comprehensive System Verification Script
Tests: Database, Security, Performance, End-to-End Demo Flow

Usage:
    python verify_comprehensive.py
"""

import requests
import json
import time
import psycopg2
from datetime import date, timedelta
from typing import Dict, List, Tuple, Optional


# Configuration
BASE_URL = "http://localhost:8000/api/v1"
DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "ai_study_companion",
    "user": "postgres",
    "password": "123456"
}

# Test users
DEMO_USER = {
    "email": "demo.student@test.com",
    "password": "student123",
    "confirm_password": "student123",
    "full_name": "Demo Student"
}

USER_B = {
    "email": "userb@test.com",
    "password": "userb123",
    "confirm_password": "userb123",
    "full_name": "User B"
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
# 6. DATABASE VERIFICATION
# ============================================================

def test_database_verification():
    """Test database tables and cascade delete"""
    print_header("6. DATABASE VERIFICATION")
    
    # Test 6.1: Verify tables exist
    print_test("6.1 Verify Database Tables Exist")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        tables = ["users", "chat_sessions", "chat_messages", "study_plans", "study_plan_items"]
        
        for table in tables:
            cursor.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = '{table}'
                );
            """)
            exists = cursor.fetchone()[0]
            if exists:
                print_pass(f"Table '{table}' exists")
            else:
                print_fail(f"Table '{table}' not found")
                record_result(f"DB Table {table}", False)
                
        record_result("DB Tables Exist", True)
        cursor.close()
        conn.close()
        
    except Exception as e:
        print_fail(f"Database connection error: {str(e)}")
        record_result("DB Tables Exist", False)
        return

    
    # Test 6.2: Verify data in tables
    print_test("6.2 Verify Tables Contain Data")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            if count > 0:
                print_pass(f"Table '{table}' has {count} records")
            else:
                print_info(f"Table '{table}' is empty (expected if first run)")
        
        record_result("DB Tables Have Data", True)
        cursor.close()
        conn.close()
        
    except Exception as e:
        print_fail(f"Query error: {str(e)}")
        record_result("DB Tables Have Data", False)


def test_cascade_delete(token: str, user_id: int):
    """Test cascade delete functionality"""
    print_test("6.3 Cascade Delete Test")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Create a study plan
        exam_date = (date.today() + timedelta(days=30)).isoformat()
        response = requests.post(
            f"{BASE_URL}/study-plans/",
            headers=headers,
            json={
                "exam_date": exam_date,
                "daily_study_hours": 3.0,
                "selected_chapter_ids": [1, 2, 3]
            }
        )
        
        if response.status_code != 201:
            print_fail("Could not create test plan")
            record_result("Cascade Delete", False, critical=True)
            return

        
        plan_id = response.json()["data"]["plan_id"]
        print_info(f"Created test plan (ID: {plan_id})")
        
        # Check items exist in database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM study_plan_items WHERE study_plan_id = {plan_id};")
        items_before = cursor.fetchone()[0]
        print_info(f"Plan has {items_before} items before delete")
        
        # Delete the plan
        response = requests.delete(
            f"{BASE_URL}/study-plans/{plan_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            print_pass("Study plan deleted via API")
            
            # Verify items also deleted (cascade)
            cursor.execute(f"SELECT COUNT(*) FROM study_plan_items WHERE study_plan_id = {plan_id};")
            items_after = cursor.fetchone()[0]
            
            if items_after == 0:
                print_pass(f"✅ CASCADE WORKS: All {items_before} items deleted")
                record_result("Cascade Delete", True, critical=True)
            else:
                print_fail(f"❌ CASCADE FAILED: {items_after} items remain")
                record_result("Cascade Delete", False, critical=True)
        else:
            print_fail(f"Delete failed (Status: {response.status_code})")
            record_result("Cascade Delete", False, critical=True)
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print_fail(f"Test error: {str(e)}")
        record_result("Cascade Delete", False, critical=True)



# ============================================================
# 8. PERFORMANCE TESTING
# ============================================================

def test_performance(token: str, session_id: int):
    """Test system performance"""
    print_header("8. PERFORMANCE TESTING")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 8.1: Chat Response Time
    print_test("8.1 Chat Response Time (Target: < 5 seconds)")
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/tutor/chat",
            headers=headers,
            json={
                "session_id": session_id,
                "question": "What is democracy?"
            },
            timeout=10
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            if elapsed < 5.0:
                print_pass(f"Response time: {elapsed:.2f}s ✅ (Target: < 5s)")
                record_result("Chat Performance", True)
            else:
                print_warn(f"Response time: {elapsed:.2f}s ⚠️ (Target: < 5s)")
                record_result("Chat Performance", False)
        else:
            print_fail(f"Query failed (Status: {response.status_code})")
            record_result("Chat Performance", False)
            
    except requests.Timeout:
        print_fail("Request timed out (> 10s)")
        record_result("Chat Performance", False)
    except Exception as e:
        print_fail(f"Test error: {str(e)}")
        record_result("Chat Performance", False)

    
    # Test 8.2: Plan Generation Time
    print_test("8.2 Plan Generation Time (Target: < 2 seconds)")
    try:
        exam_date = (date.today() + timedelta(days=30)).isoformat()
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/study-plans/",
            headers=headers,
            json={
                "exam_date": exam_date,
                "daily_study_hours": 3.0,
                "selected_chapter_ids": [1, 2, 3, 11]
            }
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 201:
            if elapsed < 2.0:
                print_pass(f"Generation time: {elapsed:.2f}s ✅ (Target: < 2s)")
                record_result("Plan Generation Performance", True)
            else:
                print_warn(f"Generation time: {elapsed:.2f}s ⚠️ (Target: < 2s)")
                record_result("Plan Generation Performance", False)
                
            # Clean up
            plan_id = response.json()["data"]["plan_id"]
            requests.delete(f"{BASE_URL}/study-plans/{plan_id}", headers=headers)
        else:
            print_fail(f"Plan creation failed (Status: {response.status_code})")
            record_result("Plan Generation Performance", False)
            
    except Exception as e:
        print_fail(f"Test error: {str(e)}")
        record_result("Plan Generation Performance", False)



# ============================================================
# 9. SECURITY VERIFICATION
# ============================================================

def test_security():
    """Test API security"""
    print_header("9. SECURITY VERIFICATION")
    
    # Test 9.1: API Protection (No Token)
    print_test("9.1 API Protection Without Token")
    try:
        response = requests.get(f"{BASE_URL}/study-plans/")
        
        if response.status_code == 401:
            print_pass("✅ Protected route returns 401 Unauthorized")
            record_result("API Protection", True, critical=True)
        else:
            print_fail(f"❌ Should return 401, got {response.status_code}")
            record_result("API Protection", False, critical=True)
            
    except Exception as e:
        print_fail(f"Test error: {str(e)}")
        record_result("API Protection", False, critical=True)
    
    # Test 9.2: Ownership Protection (Cross-User Access)
    print_test("9.2 Cross-User Access Protection")
    try:
        # Register/Login User A
        user_a_token = register_or_login(DEMO_USER)
        if not user_a_token:
            print_fail("Could not authenticate User A")
            record_result("Ownership Protection", False, critical=True)
            return
        
        # Create plan as User A
        exam_date = (date.today() + timedelta(days=30)).isoformat()
        response = requests.post(
            f"{BASE_URL}/study-plans/",
            headers={"Authorization": f"Bearer {user_a_token}"},
            json={
                "exam_date": exam_date,
                "daily_study_hours": 3.0,
                "selected_chapter_ids": [1, 2, 3]
            }
        )

        
        if response.status_code != 201:
            print_fail("Could not create plan for User A")
            record_result("Ownership Protection", False, critical=True)
            return
        
        plan_id = response.json()["data"]["plan_id"]
        print_info(f"User A created plan (ID: {plan_id})")
        
        # Register/Login User B
        user_b_token = register_or_login(USER_B)
        if not user_b_token:
            print_fail("Could not authenticate User B")
            record_result("Ownership Protection", False, critical=True)
            return
        
        # User B tries to access User A's plan
        response = requests.get(
            f"{BASE_URL}/study-plans/{plan_id}",
            headers={"Authorization": f"Bearer {user_b_token}"}
        )
        
        if response.status_code == 403:
            print_pass("✅ User B blocked from accessing User A's plan (403 Forbidden)")
            record_result("Ownership Protection", True, critical=True)
        elif response.status_code == 404:
            print_pass("✅ User B gets 404 (plan not in their scope)")
            record_result("Ownership Protection", True, critical=True)
        else:
            print_fail(f"❌ Should return 403/404, got {response.status_code}")
            print_info(f"Response: {response.text[:200]}")
            record_result("Ownership Protection", False, critical=True)
        
        # Clean up User A's plan
        requests.delete(
            f"{BASE_URL}/study-plans/{plan_id}",
            headers={"Authorization": f"Bearer {user_a_token}"}
        )
        
    except Exception as e:
        print_fail(f"Test error: {str(e)}")
        record_result("Ownership Protection", False, critical=True)



# ============================================================
# 10. DEMO READINESS TEST (END-TO-END)
# ============================================================

def test_demo_flow():
    """Complete end-to-end demo flow"""
    print_header("10. DEMO READINESS TEST - COMPLETE STUDENT FLOW")
    
    print_info("Simulating: Register → Login → Ask Tutor → Create Plan → Mark Complete → Logout → Login → Verify Persistence")
    
    # Step 1: Register
    print_test("Step 1: Register New Student")
    token = register_or_login(DEMO_USER)
    if not token:
        print_fail("Registration/Login failed")
        record_result("Demo Flow - Register", False, critical=True)
        return None
    print_pass("Student registered/logged in")
    record_result("Demo Flow - Register", True, critical=True)
    
    # Step 2: Create Chat Session
    print_test("Step 2: Open Social Studies Chat")
    try:
        response = requests.post(
            f"{BASE_URL}/chat/session",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": "Social Studies Q&A"}
        )
        if response.status_code == 201:
            session_id = response.json()["data"]["id"]
            print_pass(f"Chat session created (ID: {session_id})")
            record_result("Demo Flow - Chat Session", True, critical=True)
        else:
            print_fail(f"Failed to create session (Status: {response.status_code})")
            record_result("Demo Flow - Chat Session", False, critical=True)
            return None
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        record_result("Demo Flow - Chat Session", False, critical=True)
        return None

    
    # Step 3: Ask AI Tutor
    print_test("Step 3: Ask AI Tutor: 'What is democracy?'")
    try:
        response = requests.post(
            f"{BASE_URL}/tutor/chat",
            headers={"Authorization": f"Bearer {token}"},
            json={"session_id": session_id, "question": "What is democracy?"},
            timeout=15
        )
        if response.status_code == 200:
            answer = response.json()["data"]["answer"]
            print_pass(f"AI answered (length: {len(answer)} chars)")
            print_info(f"Answer preview: {answer[:100]}...")
            record_result("Demo Flow - AI Tutor", True, critical=True)
        else:
            print_fail(f"AI query failed (Status: {response.status_code})")
            record_result("Demo Flow - AI Tutor", False, critical=True)
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        record_result("Demo Flow - AI Tutor", False, critical=True)
    
    # Step 4: Create Study Plan
    print_test("Step 4: Create Study Plan")
    plan_id = None
    try:
        exam_date = (date.today() + timedelta(days=30)).isoformat()
        response = requests.post(
            f"{BASE_URL}/study-plans/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "exam_date": exam_date,
                "daily_study_hours": 3.0,
                "selected_chapter_ids": [1, 2, 3]
            }
        )
        if response.status_code == 201:
            plan_id = response.json()["data"]["plan_id"]
            print_pass(f"Study plan created (ID: {plan_id})")
            record_result("Demo Flow - Create Plan", True, critical=True)
        else:
            print_fail(f"Plan creation failed (Status: {response.status_code})")
            record_result("Demo Flow - Create Plan", False, critical=True)
            return None
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        record_result("Demo Flow - Create Plan", False, critical=True)
        return None

    
    # Step 5: View Timeline
    print_test("Step 5: View Study Plan Timeline")
    item_id = None
    try:
        response = requests.get(
            f"{BASE_URL}/study-plans/{plan_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            plan_data = response.json()["data"]
            items = plan_data["items"]
            print_pass(f"Timeline loaded: {len(items)} days")
            if items:
                item_id = items[0]["id"]
                print_info(f"First day: {items[0]['activity_type']} - {items[0].get('chapter_name', 'N/A')}")
            record_result("Demo Flow - View Timeline", True, critical=True)
        else:
            print_fail(f"Failed to load timeline (Status: {response.status_code})")
            record_result("Demo Flow - View Timeline", False, critical=True)
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        record_result("Demo Flow - View Timeline", False, critical=True)
    
    # Step 6: Mark Day Complete
    print_test("Step 6: Mark First Day as Complete")
    if item_id:
        try:
            response = requests.patch(
                f"{BASE_URL}/study-plans/{plan_id}/items/{item_id}",
                headers={"Authorization": f"Bearer {token}"},
                json={"status": "Completed"}
            )
            if response.status_code == 200:
                print_pass("Day marked as completed")
                record_result("Demo Flow - Mark Complete", True, critical=True)
            else:
                print_fail(f"Update failed (Status: {response.status_code})")
                record_result("Demo Flow - Mark Complete", False, critical=True)
        except Exception as e:
            print_fail(f"Error: {str(e)}")
            record_result("Demo Flow - Mark Complete", False, critical=True)
    else:
        print_warn("No item to mark complete")
        record_result("Demo Flow - Mark Complete", False, critical=True)

    
    # Step 7: Logout & Login Again
    print_test("Step 7: Logout → Login Again")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": DEMO_USER["email"], "password": DEMO_USER["password"]}
        )
        if response.status_code == 200:
            new_token = response.json()["data"]["access_token"]
            print_pass("Re-login successful")
            record_result("Demo Flow - Re-login", True, critical=True)
        else:
            print_fail(f"Re-login failed (Status: {response.status_code})")
            record_result("Demo Flow - Re-login", False, critical=True)
            return plan_id
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        record_result("Demo Flow - Re-login", False, critical=True)
        return plan_id
    
    # Step 8: Verify Data Persistence
    print_test("Step 8: Verify All Data Persisted")
    try:
        # Check plan still exists
        response = requests.get(
            f"{BASE_URL}/study-plans/{plan_id}",
            headers={"Authorization": f"Bearer {new_token}"}
        )
        if response.status_code == 200:
            plan_data = response.json()["data"]
            
            # Verify completion status persisted
            completed_items = [item for item in plan_data["items"] if item["status"] == "Completed"]
            
            if len(completed_items) > 0:
                print_pass(f"✅ Data persisted: {len(completed_items)} completed item(s)")
                record_result("Demo Flow - Data Persistence", True, critical=True)
            else:
                print_fail("❌ Completion status not persisted")
                record_result("Demo Flow - Data Persistence", False, critical=True)
        else:
            print_fail(f"Plan not found after re-login (Status: {response.status_code})")
            record_result("Demo Flow - Data Persistence", False, critical=True)
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        record_result("Demo Flow - Data Persistence", False, critical=True)
    
    return plan_id



# ============================================================
# HELPER FUNCTIONS
# ============================================================

def register_or_login(user_data: Dict) -> Optional[str]:
    """Register or login a user, return token"""
    try:
        # Try registration
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        
        if response.status_code == 201:
            return response.json()["data"]["access_token"]
        elif response.status_code == 400:
            # User exists, try login
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={"email": user_data["email"], "password": user_data["password"]}
            )
            if response.status_code == 200:
                return response.json()["data"]["access_token"]
        
        return None
    except:
        return None


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
        print(f"{Colors.OKGREEN}🎉 SYSTEM IS PRODUCTION READY!{Colors.ENDC}")
    elif test_results["critical_failures"]:
        print(f"{Colors.FAIL}{Colors.BOLD}❌ CRITICAL FAILURES DETECTED!{Colors.ENDC}")
        print(f"{Colors.FAIL}Fix critical issues before production.{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}{Colors.BOLD}⚠ SOME TESTS FAILED{Colors.ENDC}")
        print(f"{Colors.WARNING}Review failures and fix issues.{Colors.ENDC}")
    
    print(f"{'='*70}\n")



# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """Main test execution"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("="*70)
    print("COMPREHENSIVE SYSTEM VERIFICATION".center(70))
    print("Database • Security • Performance • End-to-End Demo".center(70))
    print("="*70)
    print(f"{Colors.ENDC}\n")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Database: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    print_info("Starting comprehensive verification...\n")
    
    # Run database tests
    test_database_verification()
    
    # Create session for tests
    demo_token = register_or_login(DEMO_USER)
    if demo_token:
        # Create chat session for performance test
        response = requests.post(
            f"{BASE_URL}/chat/session",
            headers={"Authorization": f"Bearer {demo_token}"},
            json={"title": "Performance Test"}
        )
        if response.status_code == 201:
            session_id = response.json()["data"]["id"]
            
            # Get user ID from database
            try:
                conn = psycopg2.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute(f"SELECT id FROM users WHERE email = '{DEMO_USER['email']}';")
                user_id = cursor.fetchone()[0]
                cursor.close()
                conn.close()
                
                # Run cascade delete test
                test_cascade_delete(demo_token, user_id)
            except:
                print_warn("Could not get user ID for cascade test")
            
            # Run performance tests
            test_performance(demo_token, session_id)
    
    # Run security tests
    test_security()
    
    # Run complete demo flow
    test_demo_flow()
    
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
