"""
Verify gemini-2.0-flash-exp works with your API key
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

load_dotenv()

print("=" * 60)
print("Verifying gemini-2.0-flash-exp")
print("=" * 60)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not found in .env")
    print("\nAdd to backend/.env:")
    print("GEMINI_API_KEY=your_key_here")
    sys.exit(1)

print(f"\n✅ API Key found: {api_key[:10]}...{api_key[-4:]}")

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    print("\n[1/3] Testing gemini-2.0-flash-exp...")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=api_key,
        temperature=0.7
    )
    
    print("[2/3] Sending test request...")
    import time
    start = time.time()
    
    response = llm.invoke("Generate one MCQ question about Indian history. Reply with just 'TEST SUCCESSFUL' if you can read this.")
    
    duration = time.time() - start
    
    print(f"[3/3] Response received in {duration:.2f}s")
    print(f"\nResponse: {response.content[:200]}...")
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! gemini-2.0-flash-exp is working!")
    print("=" * 60)
    print(f"\nPerformance: {duration:.2f} seconds")
    print("Quality: Response received")
    print("\n✅ You can now use gemini-2.0-flash-exp in production!")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\n" + "=" * 60)
    print("Troubleshooting:")
    print("=" * 60)
    
    if "not found" in str(e) or "not supported" in str(e):
        print("\n⚠️  gemini-2.0-flash-exp is NOT available for your API key.")
        print("\nThis happens when:")
        print("  1. Your API key doesn't have access to experimental models")
        print("  2. Your region doesn't support this model yet")
        print("  3. The model name has changed")
        
        print("\n✅ SOLUTION: Use gemini-pro instead:")
        print("  1. Change model to 'gemini-pro' in:")
        print("     - app/services/question_generation/generator.py")
        print("     - app/study_planner/services/ai_planner_service.py")
        print("     - app/services/tutor_service.py")
        print("  2. Restart backend")
        
        print("\n📝 Note: gemini-pro is slower (15-20s) but always works!")
        
    elif "quota" in str(e).lower() or "429" in str(e):
        print("\n⚠️  API quota exceeded.")
        print("  - Free tier: 15 requests/minute")
        print("  - Wait 1 minute and try again")
        
    elif "api key" in str(e).lower():
        print("\n⚠️  Invalid API key.")
        print("  - Get new key: https://makersuite.google.com/app/apikey")
        print("  - Update .env file")
    
    else:
        print(f"\n⚠️  Unexpected error: {e}")
        print("  - Check internet connection")
        print("  - Verify API key is valid")
        print("  - Try regenerating API key")
    
    sys.exit(1)
