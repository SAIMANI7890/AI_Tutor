# 🧪 System Verification Guide

Complete verification testing for AI Study Companion.

---

## 🚀 Quick Start

### Option 1: Automated Verification (Recommended)

```bash
# Make sure server is running
cd backend
uvicorn app.main:app --reload

# In a new terminal, run verification
python verify_system.py
```

**Expected Output:**
```
==================================================================
        AI STUDY COMPANION - SYSTEM VERIFICATION
==================================================================

1. AUTHENTICATION TESTING
  ✓ PASS: Registration successful
  ✓ PASS: Login successful
  ✓ PASS: Invalid login rejected

2. RAG VERIFICATION (CRITICAL)
  ✓ PASS: Answer received
  ✓ PASS: Sources cited (politics PDF)
  ✓ PASS: ✅ CRITICAL: RAG guardrail working!

4. STUDY PLANNER VERIFICATION (CRITICAL)
  ✓ PASS: Plan created
  ✓ PASS: Revision days found
  ✓ PASS: Mock test days found
  ✓ PASS: Plan ends before exam ✓

5. EDGE CASES TESTING
  ✓ PASS: Past date rejected
  ✓ PASS: Empty chapters rejected

Total Tests: 19
Passed: 19
Failed: 0

✅ ALL TESTS PASSED!
System is ready for production.
```

---

### Option 2: Manual Verification

Follow the detailed plan in `VERIFICATION_PLAN.md`

---

## 📋 Test Categories

| Category | Tests | Critical | Status |
|----------|-------|----------|--------|
| Authentication | 4 | No | ⏳ |
| RAG Verification | 5 | **YES** | ⏳ |
| Chat Sessions | 2 | No | ⏳ |
| Study Planner | 5 | **YES** | ⏳ |
| Edge Cases | 3 | No | ⏳ |

---

## 🔴 Critical Tests

These MUST pass before deployment:

1. **RAG Out-of-Syllabus Guardrail**
   - System must refuse questions outside Social Studies
   - No hallucinations allowed

2. **Hard Chapter Prioritization**
   - Hard chapters must appear first in schedule

3. **Revision Days**
   - Must be inserted every 4 study days

4. **Mock Tests**
   - Must be inserted every 7 days

5. **Plan Ends Before Exam**
   - Last study date must be before exam date

---

## 📁 Files

```
verification/
├── VERIFICATION_README.md          # This file
├── VERIFICATION_PLAN.md            # Detailed manual plan
└── verify_system.py                # Automated script
```

---

## 🐛 Troubleshooting

### Server Not Running
```
Error: Connection refused
```
**Solution:**
```bash
cd backend
uvicorn app.main:app --reload
```

### Database Not Set Up
```
Error: No database connection
```
**Solution:**
```bash
cd backend
python -m alembic upgrade head
```

### RAG Not Ingested
```
Error: Tutor not ready
```
**Solution:**
```bash
cd backend
python app\rag\ingestion\ingest_all.py
```

---

## ✅ What to Check

### After Running Tests

1. **All Green (✓ PASS)?**
   - ✅ System ready for production

2. **Red Failures (✗ FAIL)?**
   - ❌ Fix issues before proceeding
   - Check logs for details

3. **Critical Failures (🔴)?**
   - 🚨 **BLOCKER** - Must fix immediately
   - Do not proceed to production

---

## 📊 Expected Results

### Perfect Score
```
Total Tests: 19
Passed: 19
Failed: 0
Success Rate: 100.0%

✅ ALL TESTS PASSED!
```

### With Minor Issues
```
Total Tests: 19
Passed: 17
Failed: 2
Success Rate: 89.5%

⚠ SOME TESTS FAILED
Review failures and fix issues.
```

### With Critical Issues
```
Total Tests: 19
Passed: 15
Failed: 4
Success Rate: 78.9%

🔴 CRITICAL FAILURES:
  - RAG Out-of-Syllabus
  - Plan Ends Before Exam

❌ CRITICAL FAILURES DETECTED!
Fix critical issues before proceeding.
```

---

## 🎯 Success Criteria

### Minimum Requirements
- [x] All authentication tests pass
- [x] RAG out-of-syllabus test passes (**CRITICAL**)
- [x] Study planner creates valid plans
- [x] Hard chapters prioritized
- [x] Revision days inserted
- [x] Mock tests inserted
- [x] Plan ends before exam
- [x] Edge cases handled

### Ideal State
- [x] 100% tests passing
- [x] No critical failures
- [x] All features working
- [x] System production-ready

---

## 🔍 Detailed Verification

For manual step-by-step verification, see:
- **VERIFICATION_PLAN.md** - Complete manual testing guide

For automated testing, run:
- **verify_system.py** - Automated test script

---

## 📞 Support

### If Tests Fail

1. **Check server logs**
   - Look for errors in uvicorn output

2. **Check database**
   - Verify migrations applied
   - Check data integrity

3. **Check RAG system**
   - Verify PDFs ingested
   - Check ChromaDB

4. **Review documentation**
   - PHASE3A_COMPLETE.md
   - PHASE3B_COMPLETE.md
   - TESTING_GUIDE.md

---

## 🎉 Next Steps

### After Verification Passes

1. **Deploy to Staging**
   - Test in staging environment
   - Verify with real users

2. **Frontend Integration**
   - Connect UI to APIs
   - Test end-to-end flow

3. **Production Deployment**
   - Deploy to production
   - Monitor performance

---

**Ready to verify? Run: `python verify_system.py`** 🚀
