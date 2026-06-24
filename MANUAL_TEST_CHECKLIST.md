# 📋 Manual Testing Checklist

Quick reference checklist for manual testing. Print this and check off as you test.

---

## Pre-Test Setup

- [ ] Backend server running on http://localhost:8000
- [ ] Frontend server running on http://localhost:3000
- [ ] Database migrations applied
- [ ] PDF ingestion completed (1,319 chunks)
- [ ] Health check passes: `curl http://localhost:8000/api/v1/tutor/health`

---

## Test 1: Basic Conversation ✅

- [ ] **TC 1.1:** Send "Hello" → Gets friendly greeting
- [ ] **TC 1.2:** Send "Who are you?" → Explains AI tutor role
- [ ] **TC 1.3:** Send "What is democracy?" → Gets definition with sources

**Notes:**
_____________________________________________

---

## Test 2: RAG Retrieval ✅

- [ ] **TC 2.1:** "What were the causes of the French Revolution?" → Cites history PDF
- [ ] **TC 2.2:** "What is the monsoon climate?" → Cites geography PDF
- [ ] **TC 2.3:** "What is supply and demand?" → Cites economics PDF
- [ ] **TC 2.4:** "What are the three branches of government?" → Cites politics PDF

**Notes:**
_____________________________________________

---

## Test 3: Source Citations ✅

- [ ] **TC 3.1:** Sources section present with PDF name and page
- [ ] **TC 3.2:** Question citing multiple PDFs shows all sources
- [ ] **TC 3.3:** Non-academic questions (greetings) have no sources

**Notes:**
_____________________________________________

---

## Test 4: Out of Scope Questions ✅

- [ ] **TC 4.1:** "What is quantum physics?" → Politely refuses
- [ ] **TC 4.2:** "Solve 2x + 5 = 15" → Redirects to Social Studies
- [ ] **TC 4.3:** "What should I eat?" → Stays professional

**Notes:**
_____________________________________________

---

## Test 5: Context Awareness ✅

- [ ] **TC 5.1:** Ask "What is democracy?"
- [ ] **TC 5.2:** Follow up: "What are its main features?"
- [ ] Verify: Second answer continues democracy discussion without asking "What?"

**Notes:**
_____________________________________________

---

## Test 6: Follow-up Questions ✅

- [ ] **TC 6.1:** Ask "What is the Industrial Revolution?"
- [ ] **TC 6.2:** Follow up: "When did it happen?"
- [ ] Verify: Provides dates, references previous context

**Notes:**
_____________________________________________

---

## Test 7: Socratic Mode ✅

- [ ] **TC 7.1:** Say "Can you ask me questions about democracy?"
- [ ] Verify: Starts asking questions instead of explaining
- [ ] **TC 7.2:** Answer the question
- [ ] Verify: Evaluates answer, asks follow-up, doesn't give direct answer
- [ ] **TC 7.3:** Say "Just tell me the answer"
- [ ] Verify: Switches to explanation mode

**Notes:**
_____________________________________________

---

## Test 8: Session Management ✅

- [ ] **TC 8.1:** Click "New Chat" → Old conversation hidden, new empty chat
- [ ] **TC 8.2:** Click on old session in sidebar → Correct messages appear
- [ ] **TC 8.3:** Delete a session → Removed from sidebar, others unaffected

**Notes:**
_____________________________________________

---

## Test 9: Chat History Persistence ✅

- [ ] **TC 9.1:** Ask "What is democracy?"
- [ ] **TC 9.2:** Refresh page (F5)
- [ ] Verify: Previous messages still visible
- [ ] **TC 9.3:** Close browser, reopen → History intact

**Notes:**
_____________________________________________

---

## Test 10: Multi-Session Support ✅

- [ ] **TC 10.1:** Create Session A: "What is democracy?"
- [ ] **TC 10.2:** Create Session B: "What is the French Revolution?"
- [ ] **TC 10.3:** Create Session C: "What is monsoon climate?"
- [ ] **TC 10.4:** Switch back to each session
- [ ] Verify: Each maintains its own context, no message mixing

**Notes:**
_____________________________________________

---

## Test 11: Authentication ✅

- [ ] **TC 11.1:** Open /chat without login → Redirects to login
- [ ] **TC 11.2:** API call without token → Returns 401
- [ ] **TC 11.3:** Login with valid credentials → Gets token, accesses chat
- [ ] **TC 11.4:** Use expired token → Returns 401, redirects to login

**Notes:**
_____________________________________________

---

## Test 12: Frontend UI ✅

### Loading State
- [ ] **TC 12.1:** Send message → "Thinking..." appears, input disabled

### Auto-Scroll
- [ ] **TC 12.2:** Send multiple messages → New messages scroll into view

### Message Formatting
- [ ] **TC 12.3:** Markdown (bold, lists, links) renders correctly

### Mobile Layout (375px)
- [ ] **TC 12.4:** Text readable, no horizontal scroll, sidebar collapses

### Tablet Layout (768px)
- [ ] **TC 12.5:** Sidebar visible, comfortable reading

### Desktop Layout (1024px+)
- [ ] **TC 12.6:** Full layout, professional appearance

**Notes:**
_____________________________________________

---

## Test 13: Performance ✅

- [ ] **TC 13.1:** "What is democracy?" → Response < 5 seconds ⏱️ ___s
- [ ] **TC 13.2:** Complex question → Response < 8 seconds ⏱️ ___s
- [ ] **TC 13.3:** 10 rapid questions → All complete without errors

**Notes:**
_____________________________________________

---

## Test 14: Retrieval Accuracy 🔴 CRITICAL

### History (5 questions)
- [ ] Q1: French Revolution causes → history PDF ✓
- [ ] Q2: Industrial Revolution → history PDF ✓
- [ ] Q3: World War I trigger → history PDF ✓
- [ ] Q4: Colonialism → history PDF ✓
- [ ] Q5: Renaissance → history PDF ✓

**Score: ___/5**

### Geography (5 questions)
- [ ] Q6: Monsoon → geography PDF ✓
- [ ] Q7: Major rivers → geography PDF ✓
- [ ] Q8: Climate zones → geography PDF ✓
- [ ] Q9: Resources → geography PDF ✓
- [ ] Q10: Mountains → geography PDF ✓

**Score: ___/5**

### Politics (5 questions)
- [ ] Q11: Democracy → politics PDF ✓
- [ ] Q12: Government branches → politics PDF ✓
- [ ] Q13: Constitution → politics PDF ✓
- [ ] Q14: Rights → politics PDF ✓
- [ ] Q15: Political parties → politics PDF ✓

**Score: ___/5**

### Economics (5 questions)
- [ ] Q16: Supply & demand → economics PDF ✓
- [ ] Q17: Economic systems → economics PDF ✓
- [ ] Q18: GDP → economics PDF ✓
- [ ] Q19: Inflation → economics PDF ✓
- [ ] Q20: Trade → economics PDF ✓

**Score: ___/5**

### Accuracy Calculation
```
Total Correct Sources: ___/20 = ___%
Total Correct Answers: ___/20 = ___%
Overall Accuracy: ___/20 = ___%

Target: 85%+
Status: [ ] PASS  [ ] FAIL
```

**Notes:**
_____________________________________________

---

## Overall Test Summary

**Date:** _____________  
**Tester:** _____________  
**Version:** _____________

### Results
- Tests Passed: ___/14
- Tests Failed: ___/14
- Critical Issues: ___
- Minor Issues: ___

### Critical Test Status
- [ ] Test 2: RAG Retrieval
- [ ] Test 14: Retrieval Accuracy (85%+)

### Overall Status
- [ ] ✅ READY FOR PRODUCTION
- [ ] ⚠️ NEEDS IMPROVEMENTS
- [ ] ❌ NOT READY

### Next Steps
_____________________________________________
_____________________________________________
_____________________________________________

---

## Sign Off

**Tester Signature:** _____________  
**Date:** _____________  

**Reviewer Signature:** _____________  
**Date:** _____________
