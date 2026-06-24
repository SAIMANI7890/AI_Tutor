"""
Verify Gemini API Key
Tests if the API key is valid by making a simple request
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

def verify_gemini_key():
    """Test Gemini API key validity"""
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    print("=" * 60)
    print("Gemini API Key Verification")
    print("=" * 60)
    
    # Check if key exists
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        print("\nPlease add it to backend/.env:")
        print("GEMINI_API_KEY=your-key-here")
        return False
    
    # Display key info (masked)
    if len(api_key) < 10:
        print(f"❌ API Key is too short: {len(api_key)} characters")
        print("   Expected: 39 characters starting with 'AIzaSy'")
        return False
    
    masked_key = api_key[:10] + "*" * (len(api_key) - 14) + api_key[-4:]
    print(f"API Key found: {masked_key}")
    print(f"Length: {len(api_key)} characters")
    
    # Expected format
    if not api_key.startswith("AIzaSy"):
        print("⚠️  Warning: Key doesn't start with 'AIzaSy' (expected format)")
    
    if len(api_key) != 39:
        print(f"⚠️  Warning: Key length is {len(api_key)}, expected 39")
    
    print("\nTesting API key...")
    print("-" * 60)
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Test 1: List models
        print("Test 1: Listing available models...")
        models = genai.list_models()
        model_count = len(list(models))
        print(f"✅ Successfully connected! Found {model_count} models")
        
        # Test 2: Find embedding model
        print("\nTest 2: Finding embedding model...")
        embedding_models = [m for m in genai.list_models() if 'embed' in m.name.lower()]
        if embedding_models:
            embedding_model = embedding_models[0].name
            print(f"Found embedding model: {embedding_model}")
            
            # Test embedding generation
            print("Generating test embedding...")
            result = genai.embed_content(
                model=embedding_model,
                content="This is a test message",
                task_type="retrieval_document"
            )
            embedding = result['embedding']
            print(f"✅ Successfully generated embedding (dimension: {len(embedding)})")
        else:
            print("⚠️  No embedding model found, but API key is valid")
        
        # Test 3: Generate text
        print("\nTest 3: Finding text generation model...")
        text_models = [m for m in genai.list_models() if 'generateContent' in [method for method in m.supported_generation_methods]]
        if text_models:
            text_model = text_models[0].name
            print(f"Found text model: {text_model}")
            print("Generating test text...")
            model = genai.GenerativeModel(text_model)
            response = model.generate_content("Say 'Hello' in one word")
            print(f"✅ Successfully generated text: '{response.text.strip()}'")
        else:
            print("⚠️  No text generation model found, but API key is valid")
        
        print("\n" + "=" * 60)
        print("✅ GEMINI API KEY IS VALID!")
        print("=" * 60)
        print("\nYour API key is working correctly.")
        print("You can proceed with PDF ingestion.")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ API Key Verification Failed!")
        print(f"\nError: {error_msg}")
        
        # Provide helpful hints
        print("\n" + "-" * 60)
        print("Troubleshooting:")
        print("-" * 60)
        
        if "API key not valid" in error_msg or "API_KEY_INVALID" in error_msg:
            print("❌ The API key is invalid.")
            print("\nTo fix:")
            print("1. Visit: https://makersuite.google.com/app/apikey")
            print("2. Sign in with your Google account")
            print("3. Click 'Create API Key'")
            print("4. Copy the COMPLETE key")
            print("5. Update backend/.env file:")
            print("   GEMINI_API_KEY=<paste-your-key-here>")
            print("\nMake sure to copy the entire key with no spaces!")
            
        elif "quota" in error_msg.lower():
            print("❌ API quota exceeded.")
            print("You may have hit the free tier limit.")
            print("Wait a few minutes or upgrade your plan.")
            
        elif "permission" in error_msg.lower():
            print("❌ Permission denied.")
            print("Make sure the API key has proper permissions.")
            
        else:
            print("❌ Unexpected error.")
            print("Check your internet connection and try again.")
        
        print("\n" + "=" * 60)
        return False


if __name__ == "__main__":
    verify_gemini_key()
