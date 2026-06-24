# 🧪 Complete System Verification Plan

Comprehensive testing checklist for all implemented features.

---

## 📋 Test Categories

1. ✅ Authentication Testing
2. ✅ RAG Verification (CRITICAL)
3. ✅ Chat Session Verification
4. ✅ Study Planner Verification (CRITICAL)
5. ✅ Edge Cases Testing

---

## 1️⃣ Authentication Testing

### 1.1 Registration Test

**Objective:** Verify new user registration works correctly

#### Test Steps:
```bash
# Register new user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "securepass123",
    "full_name": "New Test User"
  }'
```

#### Verify:
- [ ] ✅ Status code: 201 Created
- [ ] ✅ Response contains `access_token`
- [ ] ✅ Response contains user data
- [ ] ✅ User saved in database
- [ ] ✅ Password is hashed (not stored as plain text)
- [ ] ✅ JWT token works for protected routes

**Expected Response:**
```json
{
  "success": true,
  "message": "Registration successful",
  "data": {
    "access_token": "eyJhbGc...",
    "user": {
      "id": 1,
      "email": "newuser@example.com",
      "full_name": "New Test User"
    }
  }
}
```

---

### 1.2 Login Test - Valid Credentials

#### Test Steps:
```bash
# Login with valid credentials
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "securepass123"
  }'
```

#### Verify:
- [ ] ✅ Status code: 200 OK
- [ ] ✅ Token generated
- [ ] ✅ Token can access protected routes
- [ ] ✅ User data returned

---

### 1.3 Login Test - Invalid Credentials

#### Test Steps:
```bash
# Login with wrong password
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "wrongpassword"
  }'
```

#### Verify:
- [ ] ✅ Status code: 401 Unauthorized
- [ ] ✅ Error message: "Incorrect email or password"
- [ ] ✅ No token generated
- [ ] ✅ Invalid login rejected

**Expected Response:**
```json
{
  "detail": "Incorrect email or password"
}
```

---

### 1.4 Authorization Test - Cross-User Access

**Objective:** Verify users cannot access each other's data

#### Test Steps:
```bash
# User A creates study plan
USER_A_TOKEN="..."
PLAN_ID=$(curl -s -X POST "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer $USER_A_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exam_date": "2026-03-15",
    "daily_study_hours": 3,
    "selected_chapter_ids": [1,2,3]
  }' | jq -r '.data.plan_id')

# User B tries to access User A's plan
USER_B_TOKEN="..."
curl -X GET "http://localhost:8000/api/v1/study-plans/$PLAN_ID" \
  -H "Authorization: Bearer $USER_B_TOKEN"
```

#### Verify:
- [ ] ✅ Status code: 403 Forbidden
- [ ] ✅ Error message about permissions
- [ ] ✅ User A can access their plan
- [ ] ✅ User B cannot access User A's plan

**Expected Response:**
```json
{
  "detail": "You do not have permission to access this study plan"
}
```

---

## 2️⃣ RAG Verification (CRITICAL)

**⚠️ This is critical - Every future module depends on RAG working correctly!**

### 2.1 Test Retrieval Accuracy

#### Test 1: Democracy Question
```bash
curl -X POST "http://localhost:8000/api/v1/tutor/query" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is democracy?"}'
```

#### Verify:
- [ ] ✅ Answer comes from PDF content
- [ ] ✅ Sources section present
- [ ] ✅ Cites `social_politics.pdf`
- [ ] ✅ No hallucinations (answer is factual)
- [ ] ✅ Response mentions key features: elections, rights, representation

---

#### Test 2: Federalism Question
```bash
curl -X POST "http://localhost:8000/api/v1/tutor/query" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain federalism"}'
```

#### Verify:
- [ ] ✅ Answer from politics PDF
- [ ] ✅ Sources cited
- [ ] ✅ Explains federal structure
- [ ] ✅ No made-up information

---

#### Test 3: Monsoon Climate Question
```bash
curl -X POST "http://localhost:8000/api/v1/tutor/query" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is monsoon climate?"}'
```

#### Verify:
- [ ] ✅ Answer from geography PDF
- [ ] ✅ Cites `social_geography.pdf`
- [ ] ✅ Explains monsoon patterns
- [ ] ✅ Mentions seasonal winds/rainfall

---

#### Test 4: French Revolution Question
```bash
curl -X POST "http://localhost:8000/api/v1/tutor/query" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "What were the causes of the French Revolution?"}'
```

#### Verify:
- [ ] ✅ Answer from history PDF
- [ ] ✅ Cites `social_history.pdf`
- [ ] ✅ Mentions economic crisis, inequality, Enlightenment
- [ ] ✅ Historically accurate

---

### 2.2 Out-of-Syllabus Test (CRITICAL RAG Guardrail)

#### Test: Quantum Computing (NOT in Social Studies)
```bash
curl -X POST "http://localhost:8000/api/v1/tutor/query" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is quantum computing?"}'
```

#### Verify:
- [ ] 🔴 **CRITICAL:** Response says "I could not find this information in the Social Studies textbook"
- [ ] ✅ Does NOT provide answer about quantum computing
- [ ] ✅ No hallucinations
- [ ] ✅ Stays within Social Studies domain

**Expected Response:**
```
I could not find this information in the Social Studies textbook. 
I can only help with Social Studies topics like History, Geography, 
Politics, and Economics.
```

**⚠️ If Gemini answers anyway, RAG guardrails need improvement!**

---

## 3️⃣ Chat Session Verification

### 3.1 Create Multiple Sessions

#### Test Steps:
```bash
# Create Session A
SESSION_A=$(curl -s -X POST "http://localhost:8000/api/v1/chat/sessions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Session A"}' | jq -r '.data.id')

# Send message to Session A
curl -X POST "http://localhost:8000/api/v1/chat/$SESSION_A/messages" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is democracy?"}'

# Create Session B
SESSION_B=$(curl -s -X POST "http://localhost:8000/api/v1/chat/sessions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Session B"}' | jq -r '.data.id')

# Send message to Session B
curl -X POST "http://localhost:8000/api/v1/chat/$SESSION_B/messages" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is monsoon climate?"}'
```

#### Verify:
- [ ] ✅ Both sessions created with unique IDs
- [ ] ✅ Messages stored correctly in each session
- [ ] ✅ Sessions are separated (no message mixing)
- [ ] ✅ History loads correctly for each session

---

### 3.2 Session History Persistence

```bash
# Get Session A messages
curl -X GET "http://localhost:8000/api/v1/chat/$SESSION_A/messages" \
  -H "Authorization: Bearer $TOKEN"

# Get Session B messages
curl -X GET "http://localhost:8000/api/v1/chat/$SESSION_B/messages" \
  -H "Authorization: Bearer $TOKEN"
```

#### Verify:
- [ ] ✅ Session A contains democracy discussion
- [ ] ✅ Session B contains monsoon discussion
- [ ] ✅ No cross-contamination
- [ ] ✅ All messages preserved

---

## 4️⃣ Study Planner Verification (CRITICAL)

**⚠️ Most important test - Validates entire Phase 3A + 3B**

### 4.1 Normal Plan Generation

#### Test Steps:
```bash
curl -X POST "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exam_date": "2026-03-15",
    "daily_study_hours": 3,
    "selected_chapter_ids": [1, 2, 3, 11, 21]
  }'
```

#### Verify:
- [ ] ✅ Status code: 201 Created
- [ ] ✅ Plan generated successfully
- [ ] ✅ `plan_id` returned
- [ ] ✅ `total_days` reasonable (should be ~30)
- [ ] ✅ `items_count` > 0
- [ ] ✅ Timeline makes sense

**Expected Response:**
```json
{
  "success": true,
  "message": "Study plan generated successfully",
  "data": {
    "plan_id": 1,
    "total_days": 28,
    "items_count": 34,
    "exam_date": "2026-03-15",
    "daily_study_hours": 3.0
  }
}
```

---

### 4.2 Hard Chapter Priority Test

#### Test Steps:
```bash
# Create plan with mixed difficulties
curl -X POST "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exam_date": "2026-03-15",
    "daily_study_hours": 3,
    "selected_chapter_ids": [
      9,  # Easy: Ancient Civilizations
      11, # Medium: Climate
      1   # Hard: French Revolution
    ]
  }'

# Get plan details
curl -X GET "http://localhost:8000/api/v1/study-plans/PLAN_ID" \
  -H "Authorization: Bearer $TOKEN"
```

#### Verify:
- [ ] ✅ Hard chapters (French Revolution) appear earlier in schedule
- [ ] ✅ Easy chapters (Ancient Civilizations) appear later
- [ ] ✅ Hard chapters get more study sessions
- [ ] ✅ Difficulty-based prioritization working

**Check items array:**
```
Day 1: French Revolution (Hard)     ✅
Day 2: French Revolution (Hard)     ✅
Day 3: Climate (Medium)              ✅
Day 4: Ancient Civilizations (Easy)  ✅
```

---

### 4.3 Revision Days Verification

#### Test Steps:
```bash
# Create longer plan to see revision pattern
curl -X POST "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exam_date": "2026-04-15",
    "daily_study_hours": 3,
    "selected_chapter_ids": [1, 2, 3, 4, 5, 11, 12, 21]
  }'

# Get plan details
curl -X GET "http://localhost:8000/api/v1/study-plans/PLAN_ID" \
  -H "Authorization: Bearer $TOKEN"
```

#### Verify:
- [ ] ✅ Revision days exist
- [ ] ✅ Revision appears every 4 study days (approximately)
- [ ] ✅ Revision items have `activity_type: "Revision"`
- [ ] ✅ Revision items have `chapter_id: null`

**Pattern to check:**
```
Day 1: Study
Day 2: Study
Day 3: Study
Day 4: Study
Day 5: Revision  ✅ (Every 4 study days)
Day 6: Study
...
```

---

### 4.4 Mock Tests Verification

#### Verify in same plan:
- [ ] ✅ Mock test days exist
- [ ] ✅ Mock test appears every 7 days (approximately)
- [ ] ✅ Mock test items have `activity_type: "MockTest"`
- [ ] ✅ Mock test items have `chapter_id: null`

**Pattern to check:**
```
Day 1: Study
Day 2: Study
...
Day 7: MockTest  ✅ (Every 7 days)
Day 14: MockTest ✅
Day 21: MockTest ✅
```

---

### 4.5 Plan Ends Before Exam

#### Verify:
```bash
# Get plan details
curl -X GET "http://localhost:8000/api/v1/study-plans/PLAN_ID" \
  -H "Authorization: Bearer $TOKEN"
```

#### Check:
- [ ] ✅ Last item's `study_date` < `exam_date`
- [ ] ✅ Plan never schedules study on exam day
- [ ] ✅ All items fit within available time

**Example:**
```json
{
  "exam_date": "2026-03-15",
  "items": [
    ...
    {
      "day_number": 28,
      "study_date": "2026-03-14"  ✅ (Before exam)
    }
  ]
}
```

---

## 5️⃣ Edge Cases Testing

### 5.1 Past Date Rejection

#### Test Steps:
```bash
curl -X POST "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exam_date": "2024-01-01",
    "daily_study_hours": 3,
    "selected_chapter_ids": [1, 2, 3]
  }'
```

#### Verify:
- [ ] ✅ Status code: 400 Bad Request
- [ ] ✅ Error message: "Exam date must be in the future"
- [ ] ✅ No plan created

**Expected Response:**
```json
{
  "detail": "Validation failed: Exam date must be in the future"
}
```

---

### 5.2 No Chapters Selected

#### Test Steps:
```bash
curl -X POST "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exam_date": "2026-03-15",
    "daily_study_hours": 3,
    "selected_chapter_ids": []
  }'
```

#### Verify:
- [ ] ✅ Status code: 422 Unprocessable Entity
- [ ] ✅ Validation error about empty chapters
- [ ] ✅ No plan created

---

### 5.3 Impossible Schedule

#### Test Steps:
```bash
curl -X POST "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exam_date": "2026-02-12",
    "daily_study_hours": 1,
    "selected_chapter_ids": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
  }'
```

#### Verify:
- [ ] ✅ Plan created (but with warning)
- [ ] ✅ Warning message about insufficient time
- [ ] ✅ Warning: "Insufficient time: Need X hours but only Y hours available"

**Expected Response:**
```json
{
  "success": true,
  "message": "Study plan generated successfully",
  "data": {
    "plan_id": 1,
    "warnings": [
      "Insufficient time: Need 80.0 hours but only 20.0 hours available. 
       Consider increasing daily hours or reducing chapters."
    ]
  }
}
```

---

## 📊 Test Execution Summary

### Checklist Overview

| Category | Tests | Status |
|----------|-------|--------|
| Authentication | 4 | ⏳ |
| RAG Verification | 5 | ⏳ |
| Chat Sessions | 2 | ⏳ |
| Study Planner | 5 | ⏳ |
| Edge Cases | 3 | ⏳ |
| **Total** | **19** | **⏳** |

---

## 🎯 Critical Success Criteria

### Must Pass (Blockers):
1. ✅ RAG out-of-syllabus guardrail works
2. ✅ Hard chapter prioritization works
3. ✅ Revision days inserted correctly
4. ✅ Mock tests inserted correctly
5. ✅ Plan ends before exam
6. ✅ Authorization prevents cross-user access

### Should Pass (Important):
7. ✅ All authentication flows work
8. ✅ Chat sessions separate correctly
9. ✅ Edge cases handled gracefully

---

## 🔍 How to Run This Verification

### Option 1: Manual Testing (Recommended First)
1. Start server: `uvicorn app.main:app --reload`
2. Follow each test in order
3. Check boxes as you verify
4. Document any failures

### Option 2: Automated Script
```bash
# Run verification script
python verify_system.py
```

### Option 3: Postman Collection
Import the Postman collection and run all tests sequentially.

---

## 📝 Test Results Template

```
=== VERIFICATION TEST RESULTS ===
Date: ___________
Tester: ___________

1. Authentication: [PASS/FAIL]
   - Registration: ✅/❌
   - Login Valid: ✅/❌
   - Login Invalid: ✅/❌
   - Authorization: ✅/❌

2. RAG Verification: [PASS/FAIL]
   - Democracy: ✅/❌
   - Federalism: ✅/❌
   - Monsoon: ✅/❌
   - French Revolution: ✅/❌
   - Out-of-Syllabus: ✅/❌ (CRITICAL)

3. Chat Sessions: [PASS/FAIL]
   - Multiple Sessions: ✅/❌
   - History Persistence: ✅/❌

4. Study Planner: [PASS/FAIL]
   - Normal Plan: ✅/❌
   - Hard Priority: ✅/❌
   - Revision Days: ✅/❌
   - Mock Tests: ✅/❌
   - Plan Ends Before Exam: ✅/❌

5. Edge Cases: [PASS/FAIL]
   - Past Date: ✅/❌
   - No Chapters: ✅/❌
   - Impossible Schedule: ✅/❌

Overall Status: [PASS/FAIL]
Critical Failures: _____
```

---

**Ready to verify? Start with Authentication tests!** 🚀
