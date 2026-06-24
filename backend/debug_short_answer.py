"""
Debug Short Answer Question Generation
Helps diagnose why Short Answer questions are failing validation
"""
import os
import sys
import json
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from app.services.question_generation.prompts_v3 import create_short_answer_prompt_v3
from app.services.question_generation.validators import QuestionValidator
from langchain_google_genai import ChatGoogleGenerativeAI

# Sample context (simulated textbook content)
SAMPLE_CONTEXT = """
Chapter: Modern India (1947-Present)

Independence and Partition:
India gained independence from British rule on August 15, 1947. The country was partitioned into India and Pakistan, causing massive migration and violence. Jawaharlal Nehru became the first Prime Minister of India, while Dr. Rajendra Prasad became the first President.

The Constitution:
The Constituent Assembly drafted the Constitution of India, which came into effect on January 26, 1950. Dr. B.R. Ambedkar chaired the Drafting Committee. The Constitution established India as a sovereign, socialist, secular, and democratic republic.

Fundamental Rights:
The Constitution guarantees fundamental rights to all citizens, including the right to equality, freedom of speech and expression, freedom of religion, and protection against discrimination. These rights can be enforced through courts if violated by the state.

Economic Planning:
India adopted a mixed economy model combining elements of capitalism and socialism. The Planning Commission was established in 1950 to oversee Five-Year Plans for economic development. The first Five-Year Plan (1951-56) focused on agriculture and irrigation to address food shortages.
"""

def test_short_answer_generation():
    """Test Short Answer generation with diagnostic output"""
    
    print("=" * 70)
    print("🔍 Short Answer Generation Diagnostic Tool")
    print("=" * 70)
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in .env file")
        return
    
    print(f"\n✅ API Key found: {api_key[:10]}...")
    
    # Initialize LLM
    print("\n📡 Initializing Gemini model: gemini-2.5-flash-lite")
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        print("✅ Model initialized successfully")
    except Exception as e:
        print(f"❌ Model initialization failed: {e}")
        return
    
    # Generate prompt
    print("\n📝 Generating Short Answer prompt...")
    prompt = create_short_answer_prompt_v3(
        context=SAMPLE_CONTEXT,
        category="History",
        count=3
    )
    
    print(f"✅ Prompt generated ({len(prompt)} characters)")
    print("\n" + "-" * 70)
    print("PROMPT PREVIEW (first 500 chars):")
    print("-" * 70)
    print(prompt[:500] + "...")
    
    # Call LLM
    print("\n" + "=" * 70)
    print("⏳ Calling Gemini API... (this may take 5-10 seconds)")
    print("=" * 70)
    
    try:
        response = llm.invoke(prompt)
        response_text = response.content
        
        print(f"\n✅ Response received ({len(response_text)} characters)")
        
        # Show raw response
        print("\n" + "=" * 70)
        print("📄 RAW LLM RESPONSE:")
        print("=" * 70)
        print(response_text)
        print("=" * 70)
        
        # Try to parse JSON
        print("\n🔧 Attempting to parse JSON...")
        
        # Clean up response
        text = response_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        try:
            parsed = json.loads(text)
            print("✅ JSON parsed successfully!")
            
            # Check for questions
            if "questions" in parsed:
                questions = parsed["questions"]
                print(f"\n✅ Found {len(questions)} questions in response")
                
                # Validate each question
                print("\n" + "=" * 70)
                print("🔍 VALIDATION ANALYSIS:")
                print("=" * 70)
                
                for i, q in enumerate(questions, 1):
                    print(f"\n--- Question {i} ---")
                    
                    # Check required fields
                    has_question_text = 'question_text' in q
                    has_model_answer = 'model_answer' in q
                    has_category = 'category' in q
                    
                    print(f"✓ Has question_text: {has_question_text}")
                    print(f"✓ Has model_answer: {has_model_answer}")
                    print(f"✓ Has category: {has_category}")
                    
                    if has_question_text:
                        question_text = q['question_text']
                        print(f"\nQuestion: {question_text}")
                        print(f"✓ Length: {len(question_text)} characters")
                        
                        if len(question_text) < 10:
                            print("\n⚠️  VALIDATION WILL FAIL: Question too short!")
                        else:
                            print("✅ Question length is valid")
                    
                    if has_model_answer:
                        model_answer = q['model_answer']
                        word_count = len(model_answer.split())
                        
                        print(f"\nModel Answer: {model_answer}")
                        print(f"✓ Length: {len(model_answer)} characters")
                        print(f"✓ Word count: {word_count} words")
                        
                        if word_count < 10:
                            print(f"\n⚠️  VALIDATION WILL FAIL: Answer too short ({word_count} words, need 10+)!")
                        elif word_count > 60:
                            print(f"\n⚠️  WARNING: Answer is long ({word_count} words, expected 20-40)")
                        else:
                            print("\n✅ Answer length is valid")
                    
                    if has_category:
                        category = q['category']
                        valid_categories = {'History', 'Geography', 'Politics', 'Economics'}
                        is_valid_category = category in valid_categories
                        
                        print(f"\nCategory: {category}")
                        print(f"✓ Valid category: {is_valid_category}")
                        
                        if not is_valid_category:
                            print(f"\n⚠️  VALIDATION WILL FAIL: Invalid category! Must be one of {valid_categories}")
                        else:
                            print("✅ Category is valid")
                
                # Final summary - use actual validator
                print("\n" + "=" * 70)
                print("📊 ACTUAL VALIDATOR TEST:")
                print("=" * 70)
                
                validator = QuestionValidator()
                valid_questions, errors = validator.validate_batch(questions, "SHORT_ANSWER")
                
                print(f"Total questions generated: {len(questions)}")
                print(f"Valid questions (by actual validator): {len(valid_questions)}")
                print(f"Invalid questions: {len(errors)}")
                
                if errors:
                    print("\n❌ VALIDATION ERRORS:")
                    for error in errors:
                        print(f"  • {error}")
                
                if len(valid_questions) == 0:
                    print("\n❌ PROBLEM IDENTIFIED: All questions are invalid!")
                    print("\nMost likely issues:")
                    print("  • Model answers too short (< 10 words)")
                    print("  • Missing required fields")
                    print("  • Invalid category names")
                    print("\n💡 SOLUTION: Check validator requirements vs LLM output")
                else:
                    print(f"\n✅ {len(valid_questions)} questions passed validation!")
                    print("\nGeneration working correctly! 🎉")
                
            else:
                print("❌ Response missing 'questions' key!")
                print(f"Keys found: {list(parsed.keys())}")
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print("\nCleaned text that failed to parse:")
            print("-" * 70)
            print(text[:500])
            print("-" * 70)
        
    except Exception as e:
        print(f"\n❌ LLM call failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_short_answer_generation()
    
    print("\n" + "=" * 70)
    print("🏁 Diagnostic Complete")
    print("=" * 70)
