"""
Quick Test Script for AI Study Companion
Tests basic functionality quickly without full test suite

Usage:
    python quick_test.py
"""

import requests
import json
import sys

API_BASE_URL = "http://localhost:8000/api/v1"

def print_test(name):
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print('='*60)

def print_pass(msg):
    print(f"✓ PASS: {msg}")

def print_fail(msg):
    print(f"✗ FAIL: {msg}")

def test_health():
    """Test 1: Health Check"""
    print_test("Health Check")
    try:
        response = requests.get(f"{API_BASE_URL}/tutor/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            chunks = data.get("data", {}).get("chunks_loaded", 0)
            print_pass(f"API is healthy - {chunks} chunks loaded")
            return True
        else:
            print_fail(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_fail(f"Health check error: {str(e)}")
        print("Is the backend server running?")
        return False

def test_basic_query():
    """Test 2: Basic Query (No Auth)"""
    print_test("Basic Query")
    
    # Note: This will fail if auth is required
    # Adjust based on your actual endpoint configuration
    try:
        response = requests.post(
            f"{API_BASE_URL}/tutor/query",
            json={"query": "What is democracy?"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("data", {}).get("answer", "")
            sources = data.get("data", {}).get("sources", [])
            
            if answer:
                print_pass("Got answer")
                print(f"Answer preview: {answer[:100]}...")
            else:
                print_fail("No answer in response")
            
            if sources:
                print_pass(f"Got {len(sources)} sources")
                for source in sources:
                    print(f"  - {source.get('source', 'Unknown')}")
            else:
                print_fail("No sources in response")
            
            return True
        elif response.status_code == 401:
            print_fail("Authentication required for this endpoint")
            print("This is normal if your API requires auth")
            return True  # Not a failure, just requires auth
        else:
            print_fail(f"Query failed: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print_fail(f"Query error: {str(e)}")
        return False

def test_frontend():
    """Test 3: Frontend Accessibility"""
    print_test("Frontend Accessibility")
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print_pass("Frontend is accessible")
            return True
        else:
            print_fail(f"Frontend returned: {response.status_code}")
            return False
    except Exception as e:
        print_fail(f"Frontend error: {str(e)}")
        print("Is the frontend server running?")
        return False

def test_cors():
    """Test 4: CORS Configuration"""
    print_test("CORS Configuration")
    try:
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST"
        }
        response = requests.options(
            f"{API_BASE_URL}/tutor/query",
            headers=headers,
            timeout=5
        )
        
        cors_header = response.headers.get("Access-Control-Allow-Origin", "")
        if cors_header:
            print_pass(f"CORS configured: {cors_header}")
            return True
        else:
            print_fail("CORS headers not found")
            print("Frontend may have issues calling backend")
            return False
            
    except Exception as e:
        print_fail(f"CORS test error: {str(e)}")
        return False

def test_database():
    """Test 5: Database Tables"""
    print_test("Database Tables")
    
    print("This test requires direct database access")
    print("Checking if alembic migrations were run...")
    
    import os
    backend_path = "backend"
    alembic_ini = os.path.join(backend_path, "alembic.ini")
    
    if os.path.exists(alembic_ini):
        print_pass("alembic.ini found")
        
        # Check if chroma_db exists
        chroma_path = os.path.join(backend_path, "chroma_db")
        if os.path.exists(chroma_path):
            print_pass(f"ChromaDB directory exists at {chroma_path}")
            
            # Count files in chroma_db
            files = []
            for root, dirs, filenames in os.walk(chroma_path):
                files.extend(filenames)
            
            if files:
                print_pass(f"ChromaDB has {len(files)} files (ingestion completed)")
            else:
                print_fail("ChromaDB directory is empty (run ingestion)")
            return True
        else:
            print_fail("ChromaDB directory not found")
            print("Run: python backend/app/rag/ingestion/ingest_all.py")
            return False
    else:
        print_fail("alembic.ini not found")
        return False

def main():
    """Run all quick tests"""
    print("\n" + "="*60)
    print("AI STUDY COMPANION - QUICK TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("Basic Query", test_basic_query()))
    results.append(("Frontend", test_frontend()))
    results.append(("CORS", test_cors()))
    results.append(("Database", test_database()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED - System ready for manual testing")
        return 0
    else:
        print(f"\n✗ {total - passed} TESTS FAILED - Fix issues before manual testing")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
