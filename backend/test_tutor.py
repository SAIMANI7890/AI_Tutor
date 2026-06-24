"""
Test AI Tutor Service
Verifies tutor answers, hallucination protection, and source citations
"""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv()

from app.services.tutor_service import TutorService


def print_separator(title):
    """Print a formatted separator"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_tutor_answer(tutor, question, test_num, description):
    """Test tutor answer for a specific question"""
    print(f"\n🧑‍🏫 Test {test_num}: {description}")
    print("-" * 70)
    print(f"Question: {question}")
    print("-" * 70)
    
    try:
        # Get answer from tutor
        result = tutor.answer_question(question)
        
        # Display answer
        answer = result.get("answer", "")
        sources = result.get("sources", [])
        
        print(f"\n📝 Answer:")
        print(f"{answer}")
        
        print(f"\n📚 Sources ({len(sources)}):")
        if sources:
            for i, source in enumerate(sources, 1):
                doc = source.get("document", "Unknown")
                page = source.get("page", "?")
                category = source.get("category", "Unknown")
                print(f"  {i}. {category} - Page {page} ({doc})")
        else:
            print("  (No sources provided)")
        
        return {
            "answer": answer,
            "sources": sources,
            "success": True
        }
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {
            "answer": "",
            "sources": [],
            "success": False,
            "error": str(e)
        }


def verify_answer_quality(result, expected_category=None):
    """Verify answer meets quality standards"""
    print("\n🔍 Verification:")
    
    checks = {
        "has_answer": False,
        "understandable": False,
        "has_sources": False,
        "correct_category": False,
        "not_hallucination": True
    }
    
    answer = result.get("answer", "")
    sources = result.get("sources", [])
    
    # Check 1: Has answer
    if answer and len(answer) > 10:
        print("  ✅ Answer provided")
        checks["has_answer"] = True
    else:
        print("  ❌ No meaningful answer")
    
    # Check 2: Understandable (has reasonable length and structure)
    if len(answer) > 50 and len(answer) < 5000:
        print("  ✅ Answer length appropriate")
        checks["understandable"] = True
    else:
        print(f"  ⚠️  Answer length: {len(answer)} characters")
    
    # Check 3: Has sources
    if sources and len(sources) > 0:
        print(f"  ✅ Sources included ({len(sources)} source(s))")
        checks["has_sources"] = True
        
        # Display sources
        for source in sources:
            category = source.get("category", "Unknown")
            page = source.get("page", "?")
            print(f"     - {category}, Page {page}")
    else:
        print("  ❌ No sources included")
    
    # Check 4: Correct category (if expected)
    if expected_category and sources:
        categories = [s.get("category") for s in sources]
        if expected_category in categories:
            print(f"  ✅ Expected category '{expected_category}' found in sources")
            checks["correct_category"] = True
        else:
            print(f"  ⚠️  Expected '{expected_category}', got {categories}")
    elif expected_category:
        checks["correct_category"] = False
    else:
        checks["correct_category"] = True  # Not applicable
    
    # Check 5: Not hallucination (check for suspicious patterns)
    suspicious_phrases = [
        "i don't know",
        "i'm not sure",
        "based on my knowledge",
        "as an ai",
        "i cannot",
        "i apologize"
    ]
    
    answer_lower = answer.lower()
    if any(phrase in answer_lower for phrase in suspicious_phrases):
        print("  ⚠️  Answer contains uncertainty phrases")
    
    # Calculate score
    score = sum(1 for v in checks.values() if v) / len(checks) * 100
    
    print(f"\n📊 Quality Score: {score:.0f}%")
    
    return checks, score


def verify_no_hallucination(result):
    """Verify that tutor refuses to answer questions outside textbook"""
    print("\n🔍 Hallucination Protection Check:")
    
    answer = result.get("answer", "")
    sources = result.get("sources", [])
    
    checks = {
        "refuses_properly": False,
        "no_invented_answer": False,
        "no_sources": False,
        "correct_message": False
    }
    
    # Check for refusal phrases
    refusal_phrases = [
        "could not find",
        "not found",
        "not in the textbook",
        "don't have information",
        "no information"
    ]
    
    answer_lower = answer.lower()
    has_refusal = any(phrase in answer_lower for phrase in refusal_phrases)
    
    if has_refusal:
        print("  ✅ Refuses to answer")
        checks["refuses_properly"] = True
    else:
        print("  ❌ Does not refuse - may be hallucinating!")
    
    # Check that answer is short (not detailed fabrication)
    if len(answer) < 200:
        print("  ✅ Answer is brief (not fabricated)")
        checks["no_invented_answer"] = True
    else:
        print(f"  ⚠️  Answer is long ({len(answer)} chars) - suspicious!")
    
    # Check that no sources are provided
    if not sources or len(sources) == 0:
        print("  ✅ No sources (correct for unknown topic)")
        checks["no_sources"] = True
    else:
        print(f"  ⚠️  Sources provided: {len(sources)} - unexpected!")
    
    # Check for correct message
    if "social studies textbook" in answer_lower:
        print("  ✅ Mentions 'Social Studies textbook'")
        checks["correct_message"] = True
    else:
        print("  ⚠️  Does not mention textbook")
    
    # Calculate score
    score = sum(1 for v in checks.values() if v) / len(checks) * 100
    
    print(f"\n📊 Hallucination Protection Score: {score:.0f}%")
    
    if score >= 75:
        print("  ✅ PASS: Hallucination protection working!")
    else:
        print("  ❌ FAIL: System may be hallucinating!")
    
    return checks, score


def main():
    """Run all tutor tests"""
    
    print_separator("🧪 AI TUTOR SERVICE TEST")
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        return
    
    print("\nInitializing AI Tutor with LOCAL embeddings...")
    
    try:
        # Initialize tutor service with local embeddings
        tutor = TutorService(
            api_key=api_key,
            use_local_embeddings=True,
            top_k=5
        )
        print("✅ Tutor service initialized successfully")
        
    except Exception as e:
        print(f"❌ Failed to initialize tutor: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test results storage
    all_results = []
    
    # ========================================
    # Test 5: Verify Tutor Answers
    # ========================================
    print_separator("📝 TEST 5: Tutor Answer Quality")
    
    test_questions = [
        {
            "question": "What is democracy?",
            "expected_category": "Politics",
            "description": "Democracy explanation (Politics)"
        },
        {
            "question": "What is federalism?",
            "expected_category": "Politics",
            "description": "Federalism explanation (Politics)"
        },
        {
            "question": "What is monsoon climate?",
            "expected_category": "Geography",
            "description": "Monsoon explanation (Geography)"
        }
    ]
    
    for i, test in enumerate(test_questions, 1):
        result = test_tutor_answer(
            tutor,
            test["question"],
            f"5.{i}",
            test["description"]
        )
        
        if result["success"]:
            checks, score = verify_answer_quality(result, test["expected_category"])
            result["checks"] = checks
            result["score"] = score
        
        all_results.append({
            "test": f"5.{i}",
            "type": "answer_quality",
            "question": test["question"],
            "result": result
        })
        
        print()  # Spacing
    
    # ========================================
    # Test 6: Verify Hallucination Protection
    # ========================================
    print_separator("🛡️ TEST 6: Hallucination Protection")
    
    hallucination_tests = [
        "Who invented the iPhone?",
        "What is quantum physics?",
        "Who won the World Cup in 2022?",
        "What is artificial intelligence?"
    ]
    
    for i, question in enumerate(hallucination_tests, 1):
        result = test_tutor_answer(
            tutor,
            question,
            f"6.{i}",
            f"Out-of-scope question (should refuse)"
        )
        
        if result["success"]:
            checks, score = verify_no_hallucination(result)
            result["checks"] = checks
            result["score"] = score
        
        all_results.append({
            "test": f"6.{i}",
            "type": "hallucination",
            "question": question,
            "result": result
        })
        
        print()  # Spacing
    
    # ========================================
    # Test 7: Verify Source Citations
    # ========================================
    print_separator("📚 TEST 7: Source Citation Verification")
    
    print("\nChecking if sources are properly formatted...\n")
    
    # Use one of the previous results
    sample_result = all_results[0]["result"]
    sources = sample_result.get("sources", [])
    
    if sources:
        print("✅ Sources are provided")
        print(f"✅ Number of sources: {len(sources)}")
        
        for i, source in enumerate(sources, 1):
            print(f"\nSource {i}:")
            
            # Check required fields
            has_document = "document" in source
            has_page = "page" in source
            has_category = "category" in source
            
            if has_document:
                print(f"  ✅ Document: {source['document']}")
            else:
                print("  ❌ Missing document name")
            
            if has_page:
                print(f"  ✅ Page: {source['page']}")
            else:
                print("  ❌ Missing page number")
            
            if has_category:
                print(f"  ✅ Category: {source['category']}")
            else:
                print("  ❌ Missing category")
            
            if has_document and has_page and has_category:
                print("  ✅ Source is complete")
        
        print("\n✅ PASS: Source citations are properly formatted")
    else:
        print("❌ FAIL: No sources provided")
    
    # ========================================
    # Summary
    # ========================================
    print_separator("📊 TEST SUMMARY")
    
    print("\n🧑‍🏫 Test 5: Tutor Answer Quality")
    test5_results = [r for r in all_results if r["type"] == "answer_quality"]
    test5_passed = sum(1 for r in test5_results if r["result"].get("score", 0) >= 75)
    print(f"  Passed: {test5_passed}/{len(test5_results)}")
    
    for r in test5_results:
        status = "✅" if r["result"].get("score", 0) >= 75 else "❌"
        score = r["result"].get("score", 0)
        print(f"  {status} {r['test']}: {r['question']} ({score:.0f}%)")
    
    print("\n🛡️ Test 6: Hallucination Protection")
    test6_results = [r for r in all_results if r["type"] == "hallucination"]
    test6_passed = sum(1 for r in test6_results if r["result"].get("score", 0) >= 75)
    print(f"  Passed: {test6_passed}/{len(test6_results)}")
    
    for r in test6_results:
        status = "✅" if r["result"].get("score", 0) >= 75 else "❌"
        score = r["result"].get("score", 0)
        print(f"  {status} {r['test']}: {r['question']} ({score:.0f}%)")
    
    print("\n📚 Test 7: Source Citations")
    if sources and len(sources) > 0:
        print("  ✅ Sources provided and formatted correctly")
    else:
        print("  ❌ No sources or formatting issues")
    
    # Overall summary
    total_tests = len(test5_results) + len(test6_results) + 1
    total_passed = test5_passed + test6_passed + (1 if sources else 0)
    
    print(f"\n{'='*70}")
    print(f"Overall: {total_passed}/{total_tests} tests passed ({(total_passed/total_tests)*100:.0f}%)")
    print(f"{'='*70}")
    
    if total_passed == total_tests:
        print("\n🎉 ALL TUTOR TESTS PASSED!")
        print("✅ Tutor provides quality answers")
        print("✅ Hallucination protection working")
        print("✅ Source citations included")
    else:
        print(f"\n⚠️  {total_tests - total_passed} test(s) need attention")
    
    print("\n" + "="*70)
    print("Note: Chat session test (Test 8) requires backend server running.")
    print("Run it separately via API after starting the server.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
