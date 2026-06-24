# 🧪 AI Study Companion - Complete Testing Guide

## Overview

This guide provides a systematic approach to testing all features of the AI Study Companion application.

---

## Prerequisites

Before testing, ensure:
- ✅ Backend server running on http://localhost:8000
- ✅ Frontend server running on http://localhost:3000
- ✅ Database migrations applied
- ✅ PDF ingestion completed (1,319 chunks loaded)
- ✅ Valid GEMINI_API_KEY configured

**Quick Health Check:**
```bash
curl http://localhost:8000/api/v1/tutor/health
```

---

## Test Plan Overview

| # | Test Category | Priority | Status |
|---|---------------|----------|--------|
| 1 | Basic Conversation | HIGH | ⏳ |
| 2 | RAG Retrieval | CRITICAL | ⏳ |
| 3 | Source Citations | HIGH | ⏳ |
| 4 | Out of Scope | HIGH | ⏳ |
| 5 | Context Awareness | MEDIUM | ⏳ |
| 6 | Follow-up Questions | MEDIUM | ⏳ |
| 7 | Socratic Mode | HIGH | ⏳ |
| 8 | Session Management | HIGH | ⏳ |
| 9 | Chat History Persistence | HIGH | ⏳ |
| 10 | Multi-Session Support | MEDIUM | ⏳ |
| 11 | Authentication | HIGH | ⏳ |
| 12 | Frontend UI | MEDIUM | ⏳ |
| 13 | Performance | HIGH | ⏳ |
| 14 | Retrieval Accuracy | CRITICAL | ⏳ |

---

## 1. ✅ Test: Basic Conversation

**Objective:** Verify the AI tutor can respond to greetings and basic queries.

### Test Cases:

#### TC 1.1: Greeting
```
Input: "Hello"
Expected: Friendly greeting without academic content
Verify:
  ✅ Response is welcoming
  ✅ No source citations (this is a greeting)
  ✅ Response time < 3 seconds
```

#### TC 1.2: Introduction
```
Input: "Who are you?"
Expected: Explanation of AI tutor role
Verify:
  ✅ Mentions Social Studies
  ✅ Mentions Socratic method
  ✅ No source citations needed
```

#### TC 1.3: Simple Academic Question
```
Input: "What is democracy?"
Expected: Clear definition with sources
Verify:
  ✅ Provides definition
  ✅ Includes source citations
  ✅ Response is clear and concise
```

**Status:** ⏳ Pending

---

## 2. ✅ Test: RAG Retrieval

**Objective:** Verify that relevant context is retrieved from PDFs.

### Test Cases:

#### TC 2.1: History Question
```
Input: "What were the causes of the French Revolution?"
Expected: Relevant historical context
Verify:
  ✅ Answer based on history PDF
  ✅ Sources cite "social_history.pdf"
  ✅ Multiple relevant points mentioned
```

#### TC 2.2: Geography Question
```
Input: "What is the monsoon climate?"
Expected: Geographic explanation
Verify:
  ✅ Answer based on geography PDF
  ✅ Sources cite "social_geography.pdf"
  ✅ Climate characteristics explained
```

#### TC 2.3: Economics Question
```
Input: "What is supply and demand?"
Expected: Economic concept explanation
Verify:
  ✅ Answer based on economics PDF
  ✅ Sources cite "social_economics.pdf"
  ✅ Concept clearly explained
```

#### TC 2.4: Politics Question
```
Input: "What are the three branches of government?"
Expected: Political structure explanation
Verify:
  ✅ Answer based on politics PDF
  ✅ Sources cite "social_politics.pdf"
  ✅ All three branches mentioned
```

**Status:** ⏳ Pending

---

## 3. ✅ Test: Source Citations

**Objective:** Verify that all academic responses include proper citations.

### Test Cases:

#### TC 3.1: Citation Format
```
Input: "What is capitalism?"
Expected: Answer with citations
Verify:
  ✅ "Sources:" section present
  ✅ PDF filename included
  ✅ Page number included
  ✅ Format: "📄 [PDF Name] (Page X)"
```

#### TC 3.2: Multiple Sources
```
Input: "How does climate affect economy?"
Expected: Answer citing multiple PDFs
Verify:
  ✅ Cites both geography and economics PDFs
  ✅ Each source properly formatted
  ✅ Answer integrates information from both
```

#### TC 3.3: No Sources for Non-Academic
```
Input: "Thank you!"
Expected: Polite response without citations
Verify:
  ✅ No "Sources:" section
  ✅ Friendly acknowledgment
```

**Status:** ⏳ Pending

---

## 4. ✅ Test: Out of Scope Questions

**Objective:** Verify proper handling of questions outside the curriculum.

### Test Cases:

#### TC 4.1: Science Question
```
Input: "What is quantum physics?"
Expected: Polite refusal
Verify:
  ✅ "I could not find this information in the Social Studies textbook"
  ✅ Offers to help with Social Studies topics
  ✅ No made-up information
```

#### TC 4.2: Math Question
```
Input: "Solve 2x + 5 = 15"
Expected: Polite refusal
Verify:
  ✅ Acknowledges limitation
  ✅ No attempt to answer
  ✅ Suggests Social Studies topics
```

#### TC 4.3: Personal Advice
```
Input: "What should I eat for lunch?"
Expected: Polite refusal
Verify:
  ✅ Redirects to academic topics
  ✅ Maintains professional tone
```

**Status:** ⏳ Pending

---

## 5. ✅ Test: Context Awareness

**Objective:** Verify the AI maintains conversation context.

### Test Sequence:

```
Message 1: "What is democracy?"
Expected: Full explanation of democracy

Message 2: "What are its main features?"
Expected: Should understand "its" refers to democracy
Verify:
  ✅ Continues democracy discussion
  ✅ Doesn't ask "What are you referring to?"
  ✅ Provides features of democracy
  ✅ Maintains source citations
```

**Status:** ⏳ Pending

---

## 6. ✅ Test: Follow-up Questions

**Objective:** Verify proper handling of related questions.

### Test Sequence:

```
Message 1: "What is the Industrial Revolution?"
Expected: Historical explanation

Message 2: "When did it happen?"
Expected: Time period of Industrial Revolution
Verify:
  ✅ Provides dates
  ✅ References previous context
  ✅ Includes sources
```

**Status:** ⏳ Pending

---

## 7. ✅ Test: Socratic Mode

**Objective:** Verify Socratic teaching method works correctly.

### Test Cases:

#### TC 7.1: Enable Socratic Mode
```
Input: "Can you ask me questions about democracy?"
Expected: Starts asking questions
Verify:
  ✅ Asks thought-provoking question
  ✅ Question is related to democracy
  ✅ Encourages critical thinking
```

#### TC 7.2: Answer to Socratic Question
```
Input: [User provides answer]
Expected: Evaluates and guides
Verify:
  ✅ Acknowledges correct parts
  ✅ Gently corrects misconceptions
  ✅ Asks follow-up question
  ✅ Doesn't give answer directly
```

#### TC 7.3: Disable Socratic Mode
```
Input: "Just tell me the answer"
Expected: Switches to explanation mode
Verify:
  ✅ Provides direct answer
  ✅ Stops asking questions
  ✅ Includes sources
```

**Status:** ⏳ Pending

---

## 8. ✅ Test: Session Management

**Objective:** Verify chat sessions are properly managed.

### Test Cases:

#### TC 8.1: Create New Session
```
Action: Click "New Chat"
Verify:
  ✅ Old conversation hidden
  ✅ New empty chat appears
  ✅ Session ID changes
  ✅ "Chat History" sidebar updates
```

#### TC 8.2: Switch Between Sessions
```
Action: Click on Session A, then Session B
Verify:
  ✅ Correct messages appear for each session
  ✅ No message mixing between sessions
  ✅ Context is session-specific
```

#### TC 8.3: Delete Session
```
Action: Delete a session
Verify:
  ✅ Session removed from sidebar
  ✅ Messages deleted from database
  ✅ Other sessions unaffected
```

**Status:** ⏳ Pending

---

## 9. ✅ Test: Chat History Persistence

**Objective:** Verify conversation history persists across page reloads.

### Test Procedure:

```
Step 1: Ask "What is democracy?"
Step 2: Receive answer
Step 3: Refresh page (F5)
Step 4: Check if message visible

Verify:
  ✅ Previous messages still visible
  ✅ Session restored automatically
  ✅ Can continue conversation
  ✅ Sources still displayed
```

**Alternative Test:**
```
Step 1: Close browser tab
Step 2: Reopen http://localhost:3000
Step 3: Login (if needed)
Step 4: Check chat history

Verify:
  ✅ All previous sessions listed
  ✅ Can open and view old conversations
  ✅ Messages intact
```

**Status:** ⏳ Pending

---

## 10. ✅ Test: Multi-Session Support

**Objective:** Verify multiple independent sessions can coexist.

### Test Procedure:

```
Step 1: Create Session A
  Ask: "What is democracy?"

Step 2: Create Session B  
  Ask: "What is the French Revolution?"

Step 3: Create Session C
  Ask: "What is monsoon climate?"

Step 4: Verify Independence
  Switch back to Session A
  Verify: Only democracy discussion visible
  
  Switch to Session B
  Verify: Only French Revolution discussion visible
  
  Switch to Session C
  Verify: Only monsoon discussion visible

Verify:
  ✅ Each session maintains its own context
  ✅ No message bleeding between sessions
  ✅ All sessions listed in sidebar
  ✅ Can continue any session independently
```

**Status:** ⏳ Pending

---

## 11. ✅ Test: Authentication

**Objective:** Verify protected routes require authentication.

### Test Cases:

#### TC 11.1: Access Without Login
```
Action: Open http://localhost:3000/chat (without logging in)
Expected: Redirect to login
Verify:
  ✅ Cannot access chat page
  ✅ Redirected to /login
  ✅ Helpful message shown
```

#### TC 11.2: API Access Without Token
```
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'

Expected: 401 Unauthorized
Verify:
  ✅ Returns 401 status code
  ✅ Error message: "Not authenticated"
```

#### TC 11.3: Valid Login
```
Action: Login with valid credentials
Verify:
  ✅ JWT token received
  ✅ Redirected to chat page
  ✅ Can send messages
  ✅ Token stored in localStorage
```

#### TC 11.4: Token Expiration
```
Action: Wait for token to expire (or manually set old token)
Verify:
  ✅ API calls return 401
  ✅ User redirected to login
  ✅ Helpful message shown
```

**Status:** ⏳ Pending

---

## 12. ✅ Test: Frontend UI

**Objective:** Verify the chat interface works correctly across devices.

### Test Cases:

#### TC 12.1: Loading State
```
Action: Send message
Verify During Loading:
  ✅ "Thinking..." indicator appears
  ✅ Input disabled
  ✅ Send button disabled
  ✅ Loading animation visible
```

#### TC 12.2: Auto-Scroll
```
Action: Send multiple messages until chat overflows
Verify:
  ✅ New messages automatically scroll into view
  ✅ Smooth scrolling behavior
  ✅ User can manually scroll up
  ✅ Auto-scroll resumes on new message
```

#### TC 12.3: Message Formatting
```
Action: Receive message with:
  - Bold text
  - Bullet points
  - Links
  - Code blocks (if applicable)

Verify:
  ✅ Markdown rendered correctly
  ✅ Formatting preserved
  ✅ Readable on all screen sizes
```

#### TC 12.4: Mobile Layout (375px)
```
Device: iPhone SE / Small phones
Verify:
  ✅ Text readable without zooming
  ✅ Input field accessible
  ✅ Send button clickable
  ✅ Sidebar collapses to hamburger menu
  ✅ No horizontal scroll
  ✅ Touch targets adequate (48x48px min)
```

#### TC 12.5: Tablet Layout (768px)
```
Device: iPad / Tablets
Verify:
  ✅ Sidebar visible
  ✅ Chat area uses available space
  ✅ Comfortable reading
  ✅ No UI breaking
```

#### TC 12.6: Desktop Layout (1024px+)
```
Device: Laptop / Desktop
Verify:
  ✅ Sidebar visible
  ✅ Chat area well-proportioned
  ✅ Maximum content width applied
  ✅ Professional appearance
```

**Status:** ⏳ Pending

---

## 13. ✅ Test: Performance

**Objective:** Verify acceptable response times.

### Test Cases:

#### TC 13.1: Simple Question
```
Input: "What is democracy?"
Measure: Time from send to first response character

Target: < 5 seconds
Good: 2-4 seconds
Excellent: < 2 seconds

Verify:
  ✅ Response within target
  ✅ No timeout errors
  ✅ Consistent across multiple tries
```

#### TC 13.2: Complex Question
```
Input: "Compare and contrast democracy and monarchy, discussing their historical origins, key features, and modern examples."

Target: < 8 seconds
Good: 4-7 seconds

Verify:
  ✅ Response complete
  ✅ Quality not sacrificed for speed
  ✅ All sources cited
```

#### TC 13.3: Load Testing (Optional)
```
Action: Send 10 questions rapidly
Verify:
  ✅ All responses received
  ✅ No errors
  ✅ Response quality maintained
  ✅ No server crashes
```

**Status:** ⏳ Pending

---

## 14. 🔴 Test: Retrieval Accuracy (CRITICAL)

**Objective:** Verify the RAG system retrieves correct information.

**This is the MOST IMPORTANT test.** Target accuracy: **85%+**

### Test Methodology:

Create 20 test questions (5 per category):
- 5 History questions
- 5 Geography questions
- 5 Politics questions
- 5 Economics questions

For each question, verify:
1. ✅ Correct source PDF cited
2. ✅ Answer is factually correct
3. ✅ Answer is relevant to the question

### History Questions (5):

#### Q1: French Revolution Causes
```
Question: "What were the main causes of the French Revolution?"
Expected Source: social_history.pdf
Expected Answer: Economic crisis, social inequality, Enlightenment ideas
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q2: Industrial Revolution
```
Question: "When did the Industrial Revolution begin and where?"
Expected Source: social_history.pdf
Expected Answer: Late 18th century, Britain
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q3: World War I
```
Question: "What triggered World War I?"
Expected Source: social_history.pdf
Expected Answer: Assassination of Archduke Franz Ferdinand
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q4: Colonial Period
```
Question: "What was colonialism and which countries were major colonial powers?"
Expected Source: social_history.pdf
Expected Answer: European expansion, Britain, France, Spain, Portugal
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q5: Renaissance
```
Question: "What was the Renaissance and where did it begin?"
Expected Source: social_history.pdf
Expected Answer: Cultural rebirth, 14th-17th century, Italy
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

**History Score: __/5 correct sources, __/5 correct answers**

---

### Geography Questions (5):

#### Q6: Monsoon Climate
```
Question: "What is a monsoon and which regions experience it?"
Expected Source: social_geography.pdf
Expected Answer: Seasonal wind pattern, South Asia, rainfall
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q7: Rivers
```
Question: "What are the major rivers of India?"
Expected Source: social_geography.pdf
Expected Answer: Ganges, Yamuna, Brahmaputra, etc.
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q8: Climate Zones
```
Question: "What are the different climate zones of the world?"
Expected Source: social_geography.pdf
Expected Answer: Tropical, temperate, polar, etc.
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q9: Natural Resources
```
Question: "What are renewable and non-renewable resources?"
Expected Source: social_geography.pdf
Expected Answer: Definitions and examples
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q10: Mountain Ranges
```
Question: "What are the major mountain ranges in Asia?"
Expected Source: social_geography.pdf
Expected Answer: Himalayas, Karakoram, Hindu Kush, etc.
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

**Geography Score: __/5 correct sources, __/5 correct answers**

---

### Politics Questions (5):

#### Q11: Democracy Definition
```
Question: "What is democracy and what are its key features?"
Expected Source: social_politics.pdf
Expected Answer: Rule by people, elections, rights, representation
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q12: Government Branches
```
Question: "What are the three branches of government?"
Expected Source: social_politics.pdf
Expected Answer: Legislative, Executive, Judicial
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q13: Constitution
```
Question: "What is a constitution?"
Expected Source: social_politics.pdf
Expected Answer: Supreme law, fundamental principles
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q14: Rights and Duties
```
Question: "What are fundamental rights?"
Expected Source: social_politics.pdf
Expected Answer: Basic rights guaranteed by constitution
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q15: Political Parties
```
Question: "What is the role of political parties in democracy?"
Expected Source: social_politics.pdf
Expected Answer: Representation, governance, opposition
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

**Politics Score: __/5 correct sources, __/5 correct answers**

---

### Economics Questions (5):

#### Q16: Supply and Demand
```
Question: "What is the law of supply and demand?"
Expected Source: social_economics.pdf
Expected Answer: Price relationship with supply and demand
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q17: Economic Systems
```
Question: "What are the different types of economic systems?"
Expected Source: social_economics.pdf
Expected Answer: Capitalism, socialism, mixed economy
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q18: GDP
```
Question: "What is GDP and why is it important?"
Expected Source: social_economics.pdf
Expected Answer: Gross Domestic Product, economic indicator
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q19: Inflation
```
Question: "What is inflation?"
Expected Source: social_economics.pdf
Expected Answer: Rising prices, purchasing power decrease
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

#### Q20: Trade
```
Question: "What is international trade and why do countries trade?"
Expected Source: social_economics.pdf
Expected Answer: Exchange of goods/services, comparative advantage
Verify:
  [ ] Correct source
  [ ] Correct answer
  [ ] Relevant content
```

**Economics Score: __/5 correct sources, __/5 correct answers**

---

### Accuracy Calculation:

```
Total Questions: 20

Correct Sources: __/20 = __%
Correct Answers: __/20 = __%
Overall Accuracy: __/20 = __%

Target: 85%+
```

### If Accuracy < 85%:

**Improvement Steps:**

1. **Improve Chunking:**
   - Current: 1000 chars, 200 overlap
   - Try: 1500 chars, 300 overlap
   - File: `backend/app/rag/ingestion/chunker.py`

2. **Increase Retrieval Count (top_k):**
   - Current: top_k = 4
   - Try: top_k = 6 or 8
   - File: `backend/app/rag/retriever/retriever_service.py`

3. **Improve Prompt:**
   - Add more explicit instructions
   - Emphasize source accuracy
   - File: `backend/app/rag/prompts/tutor_prompt.py`

4. **Re-run Ingestion:**
   ```bash
   cd backend
   rm -rf chroma_db/
   python app\rag\ingestion\ingest_all.py
   ```

**Status:** ⏳ Pending

---

## Testing Execution Plan

### Phase 1: Core Functionality (Day 1)
- [ ] Test 1: Basic Conversation
- [ ] Test 2: RAG Retrieval
- [ ] Test 3: Source Citations
- [ ] Test 14: Retrieval Accuracy (**CRITICAL**)

### Phase 2: Advanced Features (Day 2)
- [ ] Test 4: Out of Scope
- [ ] Test 5: Context Awareness
- [ ] Test 6: Follow-up Questions
- [ ] Test 7: Socratic Mode

### Phase 3: Data & Security (Day 3)
- [ ] Test 8: Session Management
- [ ] Test 9: Chat History Persistence
- [ ] Test 10: Multi-Session Support
- [ ] Test 11: Authentication

### Phase 4: UI & Performance (Day 4)
- [ ] Test 12: Frontend UI
- [ ] Test 13: Performance

---

## Test Results Summary

| Test # | Test Name | Status | Pass/Fail | Notes |
|--------|-----------|--------|-----------|-------|
| 1 | Basic Conversation | ⏳ | - | - |
| 2 | RAG Retrieval | ⏳ | - | - |
| 3 | Source Citations | ⏳ | - | - |
| 4 | Out of Scope | ⏳ | - | - |
| 5 | Context Awareness | ⏳ | - | - |
| 6 | Follow-up Questions | ⏳ | - | - |
| 7 | Socratic Mode | ⏳ | - | - |
| 8 | Session Management | ⏳ | - | - |
| 9 | Chat History | ⏳ | - | - |
| 10 | Multi-Session | ⏳ | - | - |
| 11 | Authentication | ⏳ | - | - |
| 12 | Frontend UI | ⏳ | - | - |
| 13 | Performance | ⏳ | - | - |
| 14 | Retrieval Accuracy | ⏳ | - | **CRITICAL** |

**Overall Status:** ⏳ Testing Not Started

---

## Quick Test Commands

### Backend Health Check
```bash
curl http://localhost:8000/api/v1/tutor/health
```

### Test Authentication
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Use returned token for subsequent requests
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is democracy?"}'
```

### Check Vector Store
```bash
# Should have 1319 chunks
ls -la backend/chroma_db/
```

---

## Troubleshooting Test Failures

### If RAG retrieval fails:
1. Check if PDFs are ingested: `ls backend/data/`
2. Check ChromaDB: `ls backend/chroma_db/`
3. Verify API key in `.env`
4. Re-run ingestion

### If authentication fails:
1. Check JWT_SECRET in `.env`
2. Verify database has users table
3. Check token expiration settings

### If performance is slow:
1. Check internet connection (API calls)
2. Monitor API rate limits
3. Consider caching frequent queries

---

## Next Steps After Testing

1. Document all failures
2. Create bug tickets for issues
3. Implement fixes
4. Re-test failed cases
5. Conduct user acceptance testing (UAT)
6. Deploy to production

---

**Good luck with testing! 🚀**
