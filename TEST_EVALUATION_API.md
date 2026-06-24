# Testing the Evaluation API - Quick Guide

## 🚀 Quick Start

### Step 1: Start the Backend Server

```bash
cd backend
uvicorn app.main:app --reload
```

Server will start at: `http://localhost:8000`

---

## 🧪 Test Sequence

### 1. Health Check (No Auth Required)

```bash
curl -X GET http://localhost:8000/api/v1/evaluations/health/check
```

**Expected Response**:
```json
{
  "success": true,
  "message": "AI Evaluation service is ready",
  "data": {
    "status": "healthy",
    "chunks_loaded": 1234,
    "model": "gemini-2.5-flash-lite",
    "service": "evaluation"
  }
}
```

---

### 2. Register/Login to Get Auth Token

**Register**:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test Student",
    "email": "student@test.com",
    "password": "password123"
  }'
```

**Or Login**:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "password": "password123"
  }'
```

**Save the token** from the response:
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {...}
  }
}
```

**Export token** (for easier testing):
```bash
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### 3. Evaluate an Answer

```bash
curl -X POST http://localhost:8000/api/v1/evaluations/evaluate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is democracy?",
    "student_answer": "Democracy is a form of government where the people have the power to choose their leaders through free and fair elections. It allows citizens to participate in decision-making and protects individual freedoms.",
    "chapter_name": "Democracy",
    "total_marks": 5
  }'
```

**Expected Response**:
```json
{
  "success": true,
  "message": "Answer evaluated successfully",
  "data": {
    "evaluation_id": "uuid-here",
    "question": "What is democracy?",
    "student_answer": "Democracy is a form of government...",
    "model_answer": "Democracy is a system of government...",
    "marks_awarded": 4,
    "total_marks": 5,
    "feedback": "Good understanding of the concept. You correctly identified the key features of democracy including elections and citizen participation.",
    "strengths": [
      "Correctly explained the role of elections",
      "Mentioned citizen participation",
      "Clear and concise explanation"
    ],
    "improvements": [
      "Could mention rule of law",
      "Add examples of democratic rights"
    ],
    "chapter_name": "Democracy",
    "percentage": 80.0,
    "created_at": "2026-06-17T10:30:00Z"
  }
}
```

---

### 4. Get All User Evaluations

```bash
curl -X GET http://localhost:8000/api/v1/evaluations \
  -H "Authorization: Bearer $TOKEN"
```

**With Pagination**:
```bash
curl -X GET "http://localhost:8000/api/v1/evaluations?limit=10&offset=0" \
  -H "Authorization: Bearer $TOKEN"
```

---

### 5. Get Specific Evaluation

```bash
# Replace {evaluation_id} with actual UUID from previous response
curl -X GET http://localhost:8000/api/v1/evaluations/{evaluation_id} \
  -H "Authorization: Bearer $TOKEN"
```

---

### 6. Get Chapter Evaluations

```bash
curl -X GET http://localhost:8000/api/v1/evaluations/chapter/Democracy \
  -H "Authorization: Bearer $TOKEN"
```

---

### 7. Get Overall Performance Stats

```bash
curl -X GET http://localhost:8000/api/v1/evaluations/stats/performance \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response**:
```json
{
  "success": true,
  "message": "Performance statistics retrieved successfully",
  "data": {
    "user_id": 1,
    "total_evaluations": 5,
    "total_marks_obtained": 20,
    "total_marks_possible": 25,
    "overall_percentage": 80.0,
    "chapters_covered": 2,
    "recent_evaluations": [...]
  }
}
```

---

### 8. Get All Chapters Performance

```bash
curl -X GET http://localhost:8000/api/v1/evaluations/stats/chapters \
  -H "Authorization: Bearer $TOKEN"
```

---

### 9. Get Specific Chapter Performance

```bash
curl -X GET http://localhost:8000/api/v1/evaluations/stats/chapter/Democracy \
  -H "Authorization: Bearer $TOKEN"
```

---

### 10. Delete Evaluation

```bash
# Replace {evaluation_id} with actual UUID
curl -X DELETE http://localhost:8000/api/v1/evaluations/{evaluation_id} \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🧪 Test Scenarios

### Scenario 1: Excellent Answer
```json
{
  "question": "What are the main features of democracy?",
  "student_answer": "Democracy has several key features: 1) Free and fair elections where citizens vote for their leaders, 2) Rule of law where everyone is equal before the law, 3) Protection of fundamental rights like freedom of speech and expression, 4) Independent judiciary, and 5) Accountability of government to the people.",
  "chapter_name": "Democracy",
  "total_marks": 10
}
```

Expected: 9-10 marks

---

### Scenario 2: Poor Answer
```json
{
  "question": "Explain the concept of separation of powers.",
  "student_answer": "Government has power.",
  "chapter_name": "Government",
  "total_marks": 5
}
```

Expected: 0-1 marks

---

### Scenario 3: Partial Answer
```json
{
  "question": "What is the role of the judiciary in a democracy?",
  "student_answer": "The judiciary interprets laws and resolves disputes.",
  "chapter_name": "Democracy",
  "total_marks": 5
}
```

Expected: 2-3 marks (missing key points like independence, protecting rights)

---

### Scenario 4: Answer with Hallucination
```json
{
  "question": "What is the capital of India?",
  "student_answer": "The capital of India is Mumbai, which is also the largest city.",
  "chapter_name": "Geography",
  "total_marks": 2
}
```

Expected: 0 marks (factually incorrect)

---

## 🐛 Common Issues & Solutions

### Issue 1: "GEMINI_API_KEY not configured"
**Solution**: Set API key in `.env` file:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

---

### Issue 2: "Vector store not initialized"
**Solution**: Run ingestion first:
```bash
cd backend
python app/rag/ingestion/ingest_all_local.py
```

---

### Issue 3: "Invalid authentication credentials"
**Solution**: 
1. Check token is valid (not expired)
2. Ensure Bearer prefix: `Bearer <token>`
3. Re-login to get fresh token

---

### Issue 4: "No content found for question"
**Solution**:
1. Ensure question is related to Social Studies syllabus
2. Check chapter_name matches content in vector store
3. Verify RAG system has been ingested

---

### Issue 5: "Failed to parse LLM response"
**Solution**:
- Usually retry will work (Gemini may occasionally return malformed JSON)
- Check logs for actual response
- Reduce question complexity if persistent

---

## 📊 Expected Behavior

### Model Answer Generation
- Should be 50-150 words
- Based strictly on textbook content
- No external knowledge
- Appropriate for secondary school students

### Evaluation Feedback
- 2-3 sentences of constructive feedback
- Focuses on conceptual understanding
- Does not penalize grammar mistakes
- Compares with textbook and model answer

### Marks Distribution
- **0**: Completely wrong/irrelevant
- **1**: Very poor with misconceptions
- **2**: Partially correct, missing many points
- **3**: Mostly correct with gaps
- **4**: Good answer covering most points
- **5**: Excellent, covering all key points

### Strengths & Improvements
- Each should have 1-3 items
- Specific and actionable
- Based on textbook content
- Constructive tone

---

## 🔍 Debugging

### Enable Debug Logging

In `backend/app/main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Logs

```bash
tail -f logs/app.log
```

### Key Log Messages
- "Retrieving context for: ..."
- "Model answer generated (X characters)"
- "Evaluation complete: X/Y marks"
- "Evaluation stored: {id}"

---

## 📈 Performance Testing

### Single Evaluation
```bash
time curl -X POST http://localhost:8000/api/v1/evaluations/evaluate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @test_evaluation.json
```

Expected: 3-8 seconds (depending on RAG retrieval and Gemini response)

### Load Testing (with ApacheBench)
```bash
# 10 requests, 2 concurrent
ab -n 10 -c 2 -H "Authorization: Bearer $TOKEN" \
   -p test_evaluation.json -T application/json \
   http://localhost:8000/api/v1/evaluations/evaluate
```

---

## ✅ Success Criteria

- [x] Health check returns healthy
- [x] Authentication works
- [x] Evaluation returns structured response
- [x] Marks are between 0 and total_marks
- [x] Model answer generated from textbook
- [x] Feedback is constructive
- [x] Strengths and improvements are relevant
- [x] Performance stats calculate correctly
- [x] Chapter filtering works
- [x] Authorization prevents access to others' evaluations

---

## 🎯 Next Steps

1. Test all endpoints manually
2. Create automated integration tests
3. Test with various question types
4. Verify performance metrics
5. Test error scenarios
6. Frontend integration

---

**Happy Testing!** 🧪
