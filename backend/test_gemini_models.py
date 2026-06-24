"""
Test which Gemini models are available
"""
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env")
        exit(1)
    
    print("Testing available Gemini models...\n")
    
    models_to_test = [
        "gemini-pro",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-2.0-flash-exp",
        "models/gemini-1.5-flash",
        "models/gemini-pro",
    ]
    
    for model_name in models_to_test:
        try:
            print(f"Testing: {model_name}...", end=" ")
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=0.7
            )
            response = llm.invoke("Say 'Hello'")
            print(f"✅ WORKS - Response: {response.content[:50]}")
        except Exception as e:
            error_msg = str(e)
            if "not found" in error_msg or "not supported" in error_msg:
                print(f"❌ NOT AVAILABLE")
            else:
                print(f"⚠️  ERROR: {error_msg[:100]}")
    
    print("\n" + "="*60)
    print("Recommendation: Use the first model that works!")
    print("="*60)

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Run: pip install langchain-google-genai")
