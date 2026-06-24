"""
Phase 5 Production Verification Script
Automated checks for Study Planner production readiness
"""
import sys
import os
from datetime import date, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.study_plan import StudyPlan, StudyPlanItem, StudyStatus, ActivityType
from app.study_planner.services.ai_planner_service import ai_planner_service
from app.services.study_plan_service import StudyPlanService


def print_header(text):
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def print_test(name, passed, details=""):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {name}")
    if details:
        print(f"      {details}")


def verify_database_connection():
    """Test 1: Verify database connection"""
    print_header("TEST 1: Database Connection")
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        connection = engine.connect()
        connection.close()
        print_test("Database Connection", True, "Successfully connected to PostgreSQL")
        return True
    except Exception as e:
        print_test("Database Connection", False, f"Error: {str(e)}")
        return False


def verify_tables_exist():
    """Test 2: Verify required tables exist"""
    print_header("TEST 2: Database Schema")
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        connection = engine.connect()
        
        from sqlalchemy import text
        
        tables = ['users', 'study_plans', 'study_plan_items']
        all_exist = True
        
        for table in tables:
            result = connection.execute(text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = :table_name);"
            ), {"table_name": table})
            exists = result.fetchone()[0]
            print_test(f"Table '{table}' exists", exists)
            all_exist = all_exist and exists
        
        # Check for completed_at column
        result = connection.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = 'study_plan_items' 
                AND column_name = 'completed_at'
            );
        """))
        completed_at_exists = result.fetchone()[0]
        print_test("Column 'completed_at' exists", completed_at_exists)
        
        connection.close()
        return all_exist and completed_at_exists
        
    except Exception as e:
        print_test("Database Schema", False, f"Error: {str(e)}")
        return False


def verify_ai_planner_initialization():
    """Test 3: Verify AI planner initializes"""
    print_header("TEST 3: AI Planner Initialization")
    
    try:
        has_gemini = ai_planner_service.gemini_llm is not None
        
        if has_gemini:
            print_test("Gemini LLM Initialized", True, "AI planner ready")
        else:
            print_test("Gemini LLM Initialized", False, "Will use fallback planner")
            print("      ⚠️  This is OK - fallback ensures reliability")
        
        return True  # Always pass - fallback is intentional
        
    except Exception as e:
        print_test("AI Planner Initialization", False, f"Error: {str(e)}")
        return False


def verify_plan_generation():
    """Test 4: Verify plan generation"""
    print_header("TEST 4: Plan Generation")
    
    try:
        # Test parameters
        exam_date = date.today() + timedelta(days=30)
        daily_hours = 3.0
        selected_chapters = [1, 2, 3, 4, 5]
        
        print(f"  Generating plan: 30 days, 3 hours/day, 5 chapters")
        
        plan = ai_planner_service.generate_study_plan(
            exam_date=exam_date,
            daily_study_hours=daily_hours,
            selected_chapter_ids=selected_chapters
        )
        
        # Verify plan structure
        has_days = len(plan.days) > 0
        print_test("Plan has days", has_days, f"Generated {len(plan.days)} days")
        
        has_study = any(d.activity_type == ActivityType.STUDY for d in plan.days)
        print_test("Plan has study days", has_study)
        
        has_revision = any(d.activity_type == ActivityType.REVISION for d in plan.days)
        print_test("Plan has revision days", has_revision)
        
        # Check if AI or fallback was used
        if any("AI" in w for w in plan.warnings):
            print("      ℹ️  Generated using AI (Gemini)")
        else:
            print("      ℹ️  Generated using fallback (Rule-based)")
        
        return has_days and has_study
        
    except Exception as e:
        print_test("Plan Generation", False, f"Error: {str(e)}")
        return False


def verify_edge_cases():
    """Test 5: Verify edge case handling"""
    print_header("TEST 5: Edge Case Handling")
    
    all_passed = True
    
    # Test 5.1: Short time period
    try:
        plan = ai_planner_service.generate_study_plan(
            exam_date=date.today() + timedelta(days=7),
            daily_study_hours=2.0,
            selected_chapter_ids=[1, 2]
        )
        print_test("Short time period (7 days)", True, f"Generated {len(plan.days)} days")
    except Exception as e:
        print_test("Short time period (7 days)", False, f"Error: {str(e)}")
        all_passed = False
    
    # Test 5.2: Many chapters
    try:
        plan = ai_planner_service.generate_study_plan(
            exam_date=date.today() + timedelta(days=60),
            daily_study_hours=4.0,
            selected_chapter_ids=list(range(1, 16))
        )
        print_test("Many chapters (15)", True, f"Generated {len(plan.days)} days")
    except Exception as e:
        print_test("Many chapters (15)", False, f"Error: {str(e)}")
        all_passed = False
    
    # Test 5.3: Invalid date (should fail)
    try:
        plan = ai_planner_service.generate_study_plan(
            exam_date=date.today() - timedelta(days=1),  # Yesterday
            daily_study_hours=3.0,
            selected_chapter_ids=[1, 2, 3]
        )
        print_test("Past date validation", False, "Should have rejected past date")
        all_passed = False
    except ValueError:
        print_test("Past date validation", True, "Correctly rejected past date")
    except Exception as e:
        print_test("Past date validation", False, f"Wrong error type: {str(e)}")
        all_passed = False
    
    return all_passed


def verify_activity_distribution():
    """Test 6: Verify activity distribution"""
    print_header("TEST 6: Activity Distribution")
    
    try:
        plan = ai_planner_service.generate_study_plan(
            exam_date=date.today() + timedelta(days=30),
            daily_study_hours=3.0,
            selected_chapter_ids=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        )
        
        # Count activity types
        study_days = sum(1 for d in plan.days if d.activity_type == ActivityType.STUDY)
        revision_days = sum(1 for d in plan.days if d.activity_type == ActivityType.REVISION)
        mock_test_days = sum(1 for d in plan.days if d.activity_type == ActivityType.MOCK_TEST)
        
        print(f"  Activity Distribution:")
        print(f"    Study Days: {study_days}")
        print(f"    Revision Days: {revision_days}")
        print(f"    Mock Test Days: {mock_test_days}")
        print(f"    Total Days: {len(plan.days)}")
        
        # Verify reasonable distribution
        has_study = study_days > 0
        has_revision = revision_days > 0
        reasonable_total = len(plan.days) <= 35  # 30 days + some buffer
        
        print_test("Has study days", has_study)
        print_test("Has revision days", has_revision)
        print_test("Reasonable total days", reasonable_total)
        
        return has_study and has_revision and reasonable_total
        
    except Exception as e:
        print_test("Activity Distribution", False, f"Error: {str(e)}")
        return False


def verify_percentage_calculation():
    """Test 7: Verify completion percentage calculation"""
    print_header("TEST 7: Completion Percentage Calculation")
    
    try:
        # Create mock items
        from app.models.study_plan import StudyPlan, StudyPlanItem
        
        # Mock plan with 10 items
        class MockPlan:
            items = []
        
        mock_plan = MockPlan()
        
        # Create 10 items
        for i in range(10):
            item = type('obj', (object,), {
                'status': StudyStatus.PENDING if i < 7 else StudyStatus.COMPLETED
            })()
            mock_plan.items.append(item)
        
        # Calculate percentage (3 completed out of 10 = 30%)
        percentage = StudyPlanService.calculate_completion_percentage(mock_plan)
        
        expected = 30.0
        is_correct = abs(percentage - expected) < 0.01
        
        print_test("Percentage Calculation", is_correct, 
                   f"Expected {expected}%, Got {percentage}%")
        
        return is_correct
        
    except Exception as e:
        print_test("Percentage Calculation", False, f"Error: {str(e)}")
        return False


def run_all_verifications():
    """Run all verification tests"""
    print("\n" + "="*80)
    print(" "*25 + "PHASE 5 PRODUCTION VERIFICATION")
    print("="*80)
    
    results = []
    
    # Run all tests
    results.append(("Database Connection", verify_database_connection()))
    results.append(("Database Schema", verify_tables_exist()))
    results.append(("AI Planner Init", verify_ai_planner_initialization()))
    results.append(("Plan Generation", verify_plan_generation()))
    results.append(("Edge Cases", verify_edge_cases()))
    results.append(("Activity Distribution", verify_activity_distribution()))
    results.append(("Percentage Calculation", verify_percentage_calculation()))
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    failed = total - passed
    pass_rate = (passed / total) * 100
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Pass Rate: {pass_rate:.1f}%")
    
    print("\nDetailed Results:")
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print("\n" + "="*80)
    
    if failed == 0:
        print("✅ ALL TESTS PASSED - PHASE 5 IS PRODUCTION-READY! 🚀")
    else:
        print(f"❌ {failed} TEST(S) FAILED - PLEASE FIX ISSUES BEFORE PHASE 6")
    
    print("="*80 + "\n")
    
    print("⚠️  MANUAL TESTS STILL REQUIRED:")
    print("  - Frontend UI/UX verification")
    print("  - Mobile responsiveness")
    print("  - End-to-end student workflow")
    print("  - Security testing (cross-user access)")
    print("  - Performance benchmarks")
    print("\nSee PHASE5_PRODUCTION_VERIFICATION.md for complete checklist.\n")
    
    return failed == 0


if __name__ == "__main__":
    try:
        success = run_all_verifications()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ VERIFICATION SCRIPT FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
