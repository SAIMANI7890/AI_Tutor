# ⚡ Test Enhanced Prompts - 5 Minute Guide

**Status**: Ready to test immediately ✅

---

## 🚀 STEP 1: Restart Server (30 seconds)

```bash
cd backend

# Stop current server (Ctrl+C if running)

# Start server with enhanced prompts
uvicorn app.main:app --reload
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## 🔑 STEP 2: Get Auth Token (1 minute)

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "password": "yourpassword"
  }'
```

**Copy the `access_token` from response**

```bash
# Set token as environment variable
export TOKEN="eyJ..."  # Your actual token
```

---

## 🎯 STEP 3: Test Question Generation (2 minutes)

### Test 1: MCQ Questions

```bash
curl -X POST http://localhost:8000/api/v1/exams/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "categories": ["History"],
    "question_type": "MCQ",
    "question_count": 5
  }'
```

**Expected Response**:
```json
{
  "success": true,
  "message": "Exam generated successfully",
  "data": {
    "test_id": "550e8400-e29b-41d4-a716-446655440000",
    "question_count": 5,
    "status": "GENERATED"
  }
}
```

---

### Test 2: Fill in the Blanks

```bash
curl -X POST http://localhost:8000/api/v1/exams/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "categories": ["Geography"],
    "question_type": "FILL_BLANKS",
    "question_count": 5
  }'
```

---

### Test 3: Short Answer

```bash
curl -X POST http://localhost:8000/api/v1/exams/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "categories": ["Politics"],
    "question_type": "SHORT_ANSWER",
    "question_count": 3
  }'
```

---

### Test 4: Long Answer

```bash
curl -X POST http://localhost:8000/api/v1/exams/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "categories": ["Economics"],
    "question_type": "LONG_ANSWER",
    "question_count": 3
  }'
```

---

## ✅ STEP 4: Verify Questions (2 minutes)

```bash
# Get the test_id from Step 3 response
TEST_ID="550e8400-e29b-41d4-a716-446655440000"

# Fetch questions
curl http://localhost:8000/api/v1/exams/$TEST_ID/questions \
  -H "Authorization: Bearer $TOKEN"
```

**Check Response For**:
- ✅ All questions present (count matches request)
- ✅ Questions have proper structure
- ✅ No `correct_answer` or `model_answer` (student-safe)
- ✅ Questions make sense
- ✅ MCQ has 4 options

---

## 🔍 STEP 5: Check Database (Optional, 1 minute)

```sql
-- Connect to PostgreSQL
psql -U your_user -d your_database

-- Check latest test
SELECT id, question_type, question_count, status, created_at 
FROM tests 
ORDER BY created_at DESC 
LIMIT 1;

-- Check questions for that test
SELECT question_number, question_type, LEFT(question_text, 50) as question_preview
FROM test_questions 
WHERE test_id = 'your_test_id_here'
ORDER BY question_number;

-- Count by difficulty (if you add this field)
SELECT difficulty, COUNT(*) 
FROM test_questions 
WHERE test_id = 'your_test_id_here'
GROUP BY difficulty;
```

**Expected Difficulty Distribution**:
- Easy: ~30%
- Medium: ~50%
- Hard: ~20%

---

## 📊 WHAT TO LOOK FOR

### ✅ Good Signs

1. **Questions are specific**
   - ❌ "What is history?" (too vague)
   - ✅ "Who introduced the Subsidiary Alliance?" (specific)

2. **MCQ options are plausible**
   - ❌ Options: "Gandhi", "Pizza", "XYZ", "123" (bad distractors)
   - ✅ Options: "Lord Curzon", "Lord Wellesley", "Lord Ripon", "Lord Mountbatten"

3. **No obvious external knowledge**
   - ❌ "Who won the 2024 elections?" (not in textbook)
   - ✅ "What was the main cause of the Sepoy Mutiny?" (textbook content)

4. **Fill blanks have context**
   - ❌ "_____ is important." (no context)
   - ✅ "The capital of India is _____." (clear context)

5. **Short answers require explanation**
   - ❌ "Who was Gandhi?" (just recall)
   - ✅ "Explain the significance of Gandhi's non-cooperation movement." (understanding)

6. **Long answers need depth**
   - ❌ "Name three freedom fighters." (just listing)
   - ✅ "Analyze the causes and effects of the French Revolution." (analysis)

---

## 🐛 TROUBLESHOOTING

### Issue: "Vector store not initialized"

```bash
# Run RAG ingestion first
cd backend
python app/rag/ingestion/ingest_all_local.py
```

---

### Issue: "No content found for categories"

```python
# Check ChromaDB has content
import chromadb
client = chromadb.PersistentClient(path='./chroma_db')
collection = client.get_collection('social_studies')
print(f'Total chunks: {collection.count()}')

# Check categories
results = collection.get(limit=10)
for metadata in results['metadatas']:
    print(f"Category: {metadata.get('category')}")
```

---

### Issue: Questions seem hallucinated

1. **Check logs** for validation warnings
2. **Verify source chunks** were retrieved
3. **Run quality control** validation:

```python
from app.services.question_generation.quality_control import (
    QuestionQualityController
)

qc = QuestionQualityController()
valid, errors = qc.validate_question_batch(questions, source_chunks, 5)

for error in errors:
    print(error)
```

---

### Issue: Difficulty distribution off

**This is normal** - It takes a few runs for the model to calibrate.

Expected on first few tests:
- Distribution might be 20/60/20 or 40/40/20
- After 5-10 generations, should stabilize to 30/50/20

---

## 📈 QUALITY CHECKLIST

After testing, verify:

- [ ] Questions generated successfully
- [ ] All 4 question types work (MCQ, Fill, Short, Long)
- [ ] Questions are specific and clear
- [ ] MCQ options are plausible
- [ ] No obviously hallucinated content
- [ ] Questions test understanding (not just recall)
- [ ] Language appropriate for Class 10
- [ ] No duplicate questions
- [ ] Generation time reasonable (<10 seconds)

---

## 🎯 NEXT STEPS

### If Everything Works ✅

1. **Monitor quality** for next 10-20 generations
2. **Check metrics** (if you add quality control module)
3. **Adjust difficulty distribution** if needed
4. **Fine-tune prompts** based on output

### If Issues Found ❌

1. **Check logs** for error messages
2. **Verify RAG** retrieval is working
3. **Review** generated questions manually
4. **Consult** `ENHANCED_PROMPTS_IMPLEMENTATION_GUIDE.md`
5. **Adjust prompts** in `prompts.py`

---

## 📚 HELPFUL COMMANDS

```bash
# View recent logs
tail -f logs/app.log | grep "exam"

# Check Gemini API usage
# (Check your Google Cloud Console)

# Monitor server
watch -n 5 'curl -s http://localhost:8000/health'

# Test all types at once
for TYPE in MCQ FILL_BLANKS SHORT_ANSWER LONG_ANSWER; do
  echo "Testing $TYPE..."
  curl -X POST http://localhost:8000/api/v1/exams/generate \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"categories\":[\"History\"],\"question_type\":\"$TYPE\",\"question_count\":3}"
  echo ""
done
```

---

## ✨ SUCCESS CRITERIA

Your enhanced prompts are working if:

✅ Questions generated without errors  
✅ No hallucinated content visible  
✅ MCQ options are all plausible  
✅ Questions test understanding  
✅ Language is Class 10 appropriate  
✅ Generation time is reasonable  
✅ Difficulty seems varied  

---

## 🎉 YOU'RE DONE!

Your examination module now uses:
- ✅ Enhanced educational assessment prompts
- ✅ Hallucination prevention (5 layers)
- ✅ Bloom's Taxonomy alignment
- ✅ Difficulty calibration
- ✅ Source attribution

**Generate a few tests and enjoy the improved quality!** 🚀

---

**Need Help?** Check:
- `PROMPT_QUICK_REFERENCE.md` - Quick fixes
- `ENHANCED_PROMPTS_IMPLEMENTATION_GUIDE.md` - Full details
- `PROMPT_ENHANCEMENT_SUMMARY.md` - Overview

**Time to test**: 5 minutes ⏱️  
**Difficulty**: Easy ✅  
**Result**: Better questions! 🎓
