# Phase 5 Production Verification Checklist

**Purpose:** Ensure Study Planner is truly production-ready, not just "it compiles"

**Date:** June 15, 2026  
**Status:** ⏳ PENDING VERIFICATION

---

## 🎯 Exit Criteria

Do NOT start Phase 6 until ALL of these are ✅:

- [ ] Study plan creation works
- [ ] Plans saved in DB correctly
- [ ] AI planner works (with Gemini)
- [ ] Fallback planner works (without Gemini)
- [ ] Task completion works
- [ ] Progress percentage accurate
- [ ] APIs properly secured
- [ ] Mobile responsive
- [ ] Data persists after refresh/login
- [ ] End-to-end student workflow tested

---

## 1️⃣ Database Verification

### Test 1.1: Study Plan Creation

**Action:**
1. Start backend: `uvicorn app.main:app --reload`
2. Login via frontend
3. Create a study plan

**Verify in PostgreSQL:**
```sql
-- Connect to database
psql -U postgres -d ai_study_companion

-- Check study plan created
SELECT 
    id, 
    user_id, 
    exam_date, 
    daily_study_hours, 
    created_at,
    updated_at
FROM study_plans
ORDER BY created_at DESC
LIMIT 1;
```

**Expected:**
- ✅ user_id matches your user
- ✅ exam_date stored correctly
- ✅ daily_study_hours stored correctly
- ✅ created_at populated
- ✅ updated_at populated

**Check study plan items:**
```sql
SELECT 
    id,
    study_plan_id,
    day_number,
    study_date,
    activity_type,
    chapter_name,
    status,
    completed_at
FROM study_plan_items
WHERE study_plan_id = (SELECT id FROM study_plans ORDER BY created_at DESC LIMIT 1)
ORDER BY day_number;
```

**Expected:**
- ✅ Multiple items created
- ✅ day_number sequential (1, 2, 3...)
- ✅ activity_type varies (Study, Revision, MockTest)
- ✅ status = 'Pending' by default
- ✅ completed_at = NULL initially

**Result:** [ ] PASS / [ ] FAIL

---

### Test 1.2: Task Completion Persistence

**Action:**
1. Mark 3 tasks as complete in frontend
2. Refresh browser (F5)
3. Restart backend
4. Login again

**Verify in PostgreSQL:**
```sql
SELECT 
    id,
    day_number,
    chapter_name,
    status,
    completed_at
FROM study_plan_items
WHERE study_plan_id = (SELECT id FROM study_plans ORDER BY created_at DESC LIMIT 1)
    AND status = 'Completed'
ORDER BY day_number;
```

**Expected:**
- ✅ Exactly 3 tasks with status = 'Completed'
- ✅ completed_at is populated (not NULL)
- ✅ completed_at is timezone-aware timestamp
- ✅ Data persists after refresh
- ✅ Data persists after backend restart

**Result:** [ ] PASS / [ ] FAIL

---

## 2️⃣ Study Plan Generation Verification

### Test 2.1: Normal Scenario (30 days, 3 hours, 10 chapters)

**Action:**
```
Exam Date: 30 days from today
Daily Hours: 3
Chapters: Select 10 chapters from different categories
```

**Verify:**
1. Plan generates successfully
2. Check distribution:
```sql
SELECT 
    activity_type,
    COUNT(*) as count
FROM study_plan_items
WHERE study_plan_id = (SELECT id FROM study_plans ORDER BY created_at DESC LIMIT 1)
GROUP BY activity_type;
```

**Expected:**
- ✅ Study days: 20-25
- ✅ Revision days: 4-6
- ✅ Mock test days: 3-4
- ✅ Total adds up to reasonable number
- ✅ Chapters distributed properly

**Result:** [ ] PASS / [ ] FAIL

---

### Test 2.2: Tight Schedule (7 days, 2 hours, 8 chapters)

**Action:**
```
Exam Date: 7 days from today
Daily Hours: 2
Chapters: Select 8 chapters
```

**Expected:**
- ✅ Plan generates (doesn't fail)
- ✅ Warning message about insufficient time
- ✅ Adapts to constraints
- ✅ No impossible schedule
- ✅ Reasonable chapter distribution

**Result:** [ ] PASS / [ ] FAIL

---

### Test 2.3: Invalid Date (Tomorrow)

**Action:**
```
Exam Date: Tomorrow
Daily Hours: 3
Chapters: Any
```

**Expected:**
- ❌ Request should be rejected
- ✅ Clear error message
- ✅ Form shows validation error
- ✅ No database entry created

**Result:** [ ] PASS / [ ] FAIL

---

### Test 2.4: Past Date

**Action:**
```
Exam Date: Yesterday
Daily Hours: 3
Chapters: Any
```

**Expected:**
- ❌ Date picker should prevent selection
- ✅ If bypassed, backend rejects
- ✅ Clear error message

**Result:** [ ] PASS / [ ] FAIL

---

## 3️⃣ AI Planner Verification

### Test 3.1: Gemini Generation Success

**Prerequisites:**
- Valid `GOOGLE_API_KEY` in backend `.env`
- Backend restarted

**Action:**
1. Create a study plan
2. Check backend logs

**Expected Logs:**
```
INFO  [ai_planner] Gemini LLM initialized successfully
INFO  [ai_planner] Attempting AI generation (attempt 1/2)
INFO  [ai_planner] AI generation successful
```

**Verify Response:**
- ✅ Returns valid JSON array
- ✅ No markdown code blocks
- ✅ No explanations
- ✅ Correct structure: `[{"day":1,"type":"study","task":"..."}]`
- ✅ Valid activity types (study/revision/mock_test)

**Check Plan Warning:**
```sql
SELECT 
    id,
    exam_date
FROM study_plans
WHERE id = (SELECT id FROM study_plans ORDER BY created_at DESC LIMIT 1);
```
- Note: Currently warnings aren't stored in DB, check frontend UI

**Result:** [ ] PASS / [ ] FAIL

---

### Test 3.2: Fallback Planner Test

**Action:**
1. Stop backend
2. Edit `backend/.env`: Set `GOOGLE_API_KEY=invalid_key_for_testing`
3. Restart backend
4. Create a study plan

**Expected Logs:**
```
ERROR [ai_planner] Failed to initialize Gemini: ...
INFO  [ai_planner] Attempting AI generation (attempt 1/2)
ERROR [ai_planner] Gemini invocation failed: ...
INFO  [ai_planner] Falling back to rule-based planner
```

**Verify:**
- ✅ Plan still generates successfully
- ✅ Uses rule-based algorithm
- ✅ No user-facing error
- ✅ Application does NOT crash
- ✅ Frontend shows plan normally

**⚠️ CRITICAL:** This test ensures the app NEVER fails!

**Restore:**
```bash
# Restore valid API key in .env
# Restart backend
```

**Result:** [ ] PASS / [ ] FAIL

---

## 4️⃣ API Verification

### Test 4.1: Using FastAPI Swagger

**Access:** `http://localhost:8000/docs`

#### POST /study-plans
```json
{
  "exam_date": "2027-03-20",
  "daily_study_hours": 3.0,
  "selected_chapter_ids": [1, 2, 3, 4, 5]
}
```

**Expected:**
- ✅ 201 Created
- ✅ Returns plan_id
- ✅ Returns items_count
- ✅ Authorization header required

**Result:** [ ] PASS / [ ] FAIL

---

#### GET /study-plans

**Expected:**
- ✅ 200 OK
- ✅ Returns list of plans
- ✅ Each plan has completion_percentage
- ✅ Ordered by newest first

**Result:** [ ] PASS / [ ] FAIL

---

#### GET /study-plans/progress

**Expected:**
- ✅ 200 OK
- ✅ Returns: total_tasks, completed_tasks, pending_tasks, skipped_tasks
- ✅ Returns: completion_percentage
- ✅ Returns: plan_id, exam_date

**Result:** [ ] PASS / [ ] FAIL

---

#### PATCH /study-plans/task/{task_id}

**Get a task_id first:**
```sql
SELECT id FROM study_plan_items LIMIT 1;
```

**Request:**
```json
{
  "status": "Completed"
}
```

**Expected:**
- ✅ 200 OK
- ✅ Returns updated status
- ✅ Returns completed_at timestamp
- ✅ Returns new completion_percentage
- ✅ Percentage increases correctly

**Result:** [ ] PASS / [ ] FAIL

---

## 5️⃣ Completion Percentage Verification

### Test 5.1: Percentage Accuracy

**Setup:** Create plan with exactly 10 tasks

**Test Cases:**

| Tasks Completed | Expected % | Actual % | Pass/Fail |
|-----------------|-----------|----------|-----------|
| 0 | 0% | | [ ] |
| 1 | 10% | | [ ] |
| 3 | 30% | | [ ] |
| 5 | 50% | | [ ] |
| 7 | 70% | | [ ] |
| 10 | 100% | | [ ] |

**Verify Both:**
1. Frontend display matches
2. Database value matches

```sql
-- Check in database
SELECT 
    id,
    (SELECT COUNT(*) FROM study_plan_items WHERE study_plan_id = sp.id) as total,
    (SELECT COUNT(*) FROM study_plan_items WHERE study_plan_id = sp.id AND status = 'Completed') as completed,
    ROUND((SELECT COUNT(*) FROM study_plan_items WHERE study_plan_id = sp.id AND status = 'Completed')::numeric / 
          (SELECT COUNT(*) FROM study_plan_items WHERE study_plan_id = sp.id)::numeric * 100, 2) as calculated_percentage
FROM study_plans sp
WHERE id = (SELECT id FROM study_plans ORDER BY created_at DESC LIMIT 1);
```

**Result:** [ ] PASS / [ ] FAIL

---

## 6️⃣ Security Verification

### Test 6.1: Cross-User Access Protection

**Setup:**
1. Login as User A
2. Create a study plan
3. Get a task_id from User A's plan
4. Logout
5. Register/Login as User B
6. Try to update User A's task

**Using cURL:**
```bash
# As User B, try to update User A's task
curl -X PATCH http://localhost:8000/api/v1/study-plans/task/{USER_A_TASK_ID} \
  -H "Authorization: Bearer USER_B_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "Completed"}'
```

**Expected:**
- ❌ 403 Forbidden OR 404 Not Found
- ✅ Task NOT updated
- ✅ Error message clear
- ✅ User B cannot access User A's data

**Result:** [ ] PASS / [ ] FAIL

---

### Test 6.2: API Protection Without JWT

**Action:**
```bash
curl -X GET http://localhost:8000/api/v1/study-plans
```

**Expected:**
- ❌ 401 Unauthorized
- ✅ Clear error message
- ✅ No data leaked

**Result:** [ ] PASS / [ ] FAIL

---

## 7️⃣ Frontend Verification

### Test 7.1: Loading State

**Action:**
1. Open Study Planner page
2. Fill form
3. Click "Generate Study Plan"
4. Observe immediately

**Expected:**
- ✅ Button disabled during generation
- ✅ Loading spinner shown
- ✅ "Generating your personalized study plan..." text
- ✅ Cannot submit multiple times
- ✅ Form fields disabled

**Result:** [ ] PASS / [ ] FAIL

---

### Test 7.2: Error State

**Action:**
1. Stop backend
2. Try to generate plan
3. Observe

**Expected:**
- ✅ Error alert shown
- ✅ Friendly message (not technical jargon)
- ✅ No white screen
- ✅ No console errors breaking UI
- ✅ Can retry after backend restarts

**Result:** [ ] PASS / [ ] FAIL

---

### Test 7.3: Empty State

**Action:**
1. Login as new user (no plans)
2. Navigate to Study Planner

**Expected:**
- ✅ Shows "No study plan created yet"
- ✅ Shows CTA button "Create Study Plan"
- ✅ Professional empty state design
- ✅ No loading spinner forever

**Result:** [ ] PASS / [ ] FAIL

---

### Test 7.4: Task Completion UX

**Action:**
1. View existing study plan
2. Click checkbox on a task
3. Observe behavior

**Expected:**
- ✅ Checkbox checks immediately (optimistic)
- ✅ Loading spinner appears briefly
- ✅ "Completed" badge appears
- ✅ Timestamp shows: "✓ Completed Jun 15, 2:30 PM"
- ✅ Progress bar updates
- ✅ Percentage increases
- ✅ Card background changes (faded)

**Result:** [ ] PASS / [ ] FAIL

---

## 8️⃣ Mobile Responsiveness

### Test 8.1: Different Screen Sizes

Test on these viewport sizes:

#### 320px (iPhone SE)
- [ ] No horizontal overflow
- [ ] Forms usable
- [ ] Buttons clickable (not too small)
- [ ] Text readable
- [ ] Cards stack vertically

#### 375px (iPhone 12)
- [ ] Professional appearance
- [ ] All features accessible
- [ ] No cut-off content

#### 768px (iPad)
- [ ] 2-column grid works
- [ ] Optimal spacing
- [ ] Navigation clear

#### 1024px+ (Desktop)
- [ ] 3-column grid works
- [ ] Progress dashboard fits
- [ ] Stats cards aligned

**How to Test:**
1. Chrome DevTools
2. Toggle Device Toolbar
3. Test each size
4. Rotate device (portrait/landscape)

**Result:** [ ] PASS / [ ] FAIL

---

## 9️⃣ Performance Verification

### Test 9.1: Generation Speed

**Measure with DevTools Network tab:**

#### Rule-Based Planner:
- Target: < 2 seconds
- Actual: _____ seconds
- [ ] PASS / [ ] FAIL

#### AI Planner (Gemini):
- Target: < 5 seconds
- Actual: _____ seconds
- [ ] PASS / [ ] FAIL

#### Task Update:
- Target: < 500ms
- Actual: _____ ms
- [ ] PASS / [ ] FAIL

#### Progress Load:
- Target: < 200ms
- Actual: _____ ms
- [ ] PASS / [ ] FAIL

**Result:** [ ] PASS / [ ] FAIL

---

## 🔟 End-to-End Student Workflow

### The Ultimate Test: Complete Student Journey

**Scenario:** New student preparing for exam

#### Step 1: Registration & Login
1. [ ] Register new account
2. [ ] Receive success message
3. [ ] Login with credentials
4. [ ] Redirected to dashboard

#### Step 2: Navigate to Study Planner
1. [ ] Click "Study Planner" in navigation
2. [ ] Page loads without errors
3. [ ] Shows empty state (first time)

#### Step 3: Create Study Plan
1. [ ] Select exam date (30 days from now)
2. [ ] Set daily hours (3)
3. [ ] Select 7-10 chapters from different categories
4. [ ] Click "Generate Study Plan"
5. [ ] Wait 2-5 seconds
6. [ ] Plan appears with all days

#### Step 4: View Schedule
1. [ ] See stats cards (exam date, days remaining, daily hours, progress)
2. [ ] See progress dashboard (0% initially)
3. [ ] See study plan items as cards
4. [ ] Cards show: day number, date, activity type, chapter name
5. [ ] All cards have checkboxes

#### Step 5: Mark Tasks Complete
1. [ ] Click checkbox on Day 1
2. [ ] See immediate feedback (optimistic update)
3. [ ] See "Completed" badge
4. [ ] See timestamp
5. [ ] See progress bar increase
6. [ ] Mark Days 2, 3, 4 complete
7. [ ] Progress shows 4/X completed

#### Step 6: Refresh Page
1. [ ] Press F5 to refresh
2. [ ] Still logged in
3. [ ] Study plan still visible
4. [ ] Completed tasks still checked
5. [ ] Progress percentage matches

#### Step 7: Logout
1. [ ] Click logout
2. [ ] Redirected to login page
3. [ ] Session cleared

#### Step 8: Login Again
1. [ ] Login with same credentials
2. [ ] Navigate to Study Planner
3. [ ] All data still present
4. [ ] Progress still accurate
5. [ ] Completed tasks still marked

#### Step 9: Check Database
```sql
SELECT 
    sp.id,
    sp.exam_date,
    COUNT(spi.id) as total_items,
    COUNT(CASE WHEN spi.status = 'Completed' THEN 1 END) as completed_items
FROM study_plans sp
JOIN study_plan_items spi ON sp.study_plan_id = spi.study_plan_id
WHERE sp.user_id = (SELECT id FROM users WHERE email = 'teststudent@example.com')
GROUP BY sp.id;
```

**Expected:**
- [ ] Data persists correctly
- [ ] Completed count matches frontend
- [ ] Timestamps recorded

**Result:** [ ] PASS / [ ] FAIL

---

## ✅ Final Checklist

### Core Functionality
- [ ] Study plan creation works
- [ ] Plans saved in DB correctly
- [ ] Task completion works
- [ ] Progress percentage accurate
- [ ] Data persists after refresh
- [ ] Data persists after logout/login
- [ ] Data persists after backend restart

### AI & Reliability
- [ ] AI planner works (with Gemini)
- [ ] Fallback planner works (without Gemini)
- [ ] Never crashes regardless of AI status
- [ ] Handles edge cases gracefully

### Security
- [ ] APIs properly secured
- [ ] JWT authentication required
- [ ] Cross-user access denied
- [ ] Authorization checks work

### User Experience
- [ ] Mobile responsive (320px to 1920px)
- [ ] Loading states clear
- [ ] Error states friendly
- [ ] Empty states helpful
- [ ] Optimistic updates smooth

### Performance
- [ ] Generation < 5 seconds
- [ ] Task updates < 500ms
- [ ] Page loads < 2 seconds
- [ ] No noticeable lag

### End-to-End
- [ ] Complete student workflow tested
- [ ] All features work together
- [ ] Professional appearance
- [ ] Production-ready

---

## 📊 Verification Results

**Date Verified:** __________  
**Verified By:** __________

**Total Tests:** 40+  
**Passed:** ___  
**Failed:** ___  
**Pass Rate:** ___%

### Critical Issues Found:
1. 
2. 
3. 

### Minor Issues Found:
1. 
2. 
3. 

---

## 🚦 Final Decision

### ✅ READY FOR PHASE 6
- [ ] All critical tests passed
- [ ] All security tests passed
- [ ] End-to-end workflow flawless
- [ ] Performance acceptable
- [ ] Mobile responsive
- [ ] Production-ready

### ❌ NOT READY - Issues to Fix:
- [ ] Critical issues found
- [ ] Security vulnerabilities
- [ ] Data integrity problems
- [ ] Performance issues
- [ ] UX problems

---

## 📝 Notes

**What worked well:**


**What needs improvement:**


**Recommendations before Phase 6:**


---

**Remember:** It's better to fix issues now than to carry them into Phase 6!
