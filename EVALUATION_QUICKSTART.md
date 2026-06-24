# Evaluation Module - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Verify Backend is Running
```bash
cd backend
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend should be running at: `http://localhost:8000`

### Step 2: Start Frontend
```bash
cd frontend
npm run dev
```

Frontend should be running at: `http://localhost:3000`

### Step 3: Test the Feature
1. **Login** to your account at `http://localhost:3000`
2. **Navigate** to Dashboard → Evaluation (in the navigation bar)
3. **Submit an evaluation**:
   - Enter a question: "What is democracy?"
   - Enter your answer: "Democracy is a form of government where citizens have the power to vote..."
   - (Optional) Select a chapter: "Democracy and Its Features"
   - Click "Evaluate Answer"
4. **View results** with AI feedback, model answer, and score
5. **Check history** by clicking "View History"
6. **Explore chapter performance** on the history page

---

## 📍 Routes

| Route | Description |
|-------|-------------|
| `/dashboard/social/evaluation` | Submit answers for evaluation |
| `/dashboard/social/evaluation/history` | View evaluation history and performance |

---

## 🔑 Key Features to Test

### Main Evaluation Page
- ✅ Form validation (try submitting empty fields)
- ✅ Loading states with rotating messages
- ✅ Result display with score, feedback, strengths, improvements
- ✅ Model answer generation
- ✅ Navigation to history

### History Page
- ✅ Search evaluations by question text
- ✅ Filter by chapter
- ✅ Filter by score range (Excellent/Good/Needs Improvement)
- ✅ Sort by newest, oldest, highest score, lowest score
- ✅ View full evaluation details in modal
- ✅ Delete evaluations (with confirmation)
- ✅ Chapter performance cards with statistics

### Mobile Testing
- ✅ Test on mobile viewport (320px, 375px)
- ✅ Tables convert to cards on mobile
- ✅ All buttons and interactions work on touch

---

## 🎯 Sample Questions to Try

### History
- "Explain the causes of the French Revolution"
- "What were the main events of World War II?"
- "Describe the impact of colonialism on India"

### Geography
- "What are monsoons and how do they affect India?"
- "Explain the importance of the Himalayan mountain range"
- "Describe different types of soil found in India"

### Politics
- "What is democracy and its key features?"
- "Explain the three branches of government"
- "What are fundamental rights?"

### Economics
- "Explain the law of supply and demand"
- "What is GDP and how is it calculated?"
- "Describe the impact of globalization"

---

## 🐛 Troubleshooting

### Backend Issues
**Error**: "Connection refused" or "Network Error"
- ✅ Check backend is running on port 8000
- ✅ Verify `.env` file has correct database settings
- ✅ Run `alembic upgrade head` to apply migrations

**Error**: "Evaluation service not initialized"
- ✅ Check that textbook PDFs are loaded in the RAG system
- ✅ Verify Gemini API key is set in `.env`
- ✅ Check backend logs for RAG initialization errors

### Frontend Issues
**Error**: "Module not found"
- ✅ Run `npm install` in the frontend directory
- ✅ Restart the development server

**Issue**: Components not styling correctly
- ✅ Verify Tailwind CSS is working: check other pages
- ✅ Clear browser cache and reload

**Issue**: API calls failing
- ✅ Check browser console for errors
- ✅ Verify API URL in `frontend/src/lib/api.ts`
- ✅ Check authentication token is valid

### Common Issues
**Empty history**: No evaluations showing
- ✅ Submit at least one evaluation first
- ✅ Check that user is logged in
- ✅ Verify backend returns data: check Network tab

**Chapter performance not showing**
- ✅ Submit evaluations with chapter names
- ✅ Wait for the API call to complete (check loading state)

---

## 📊 Expected Behavior

### Evaluation Flow
1. User submits question + answer
2. Loading state appears (15-30 seconds)
3. Backend:
   - Generates model answer from textbook
   - Evaluates student answer
   - Calculates score and feedback
4. Results displayed with:
   - Score: X / 5 (percentage)
   - Status badge: Excellent/Good/Needs Improvement
   - Feedback paragraph
   - Strengths (bullet points)
   - Improvements (bullet points)
   - Model answer

### Score Status Logic
- **Excellent**: 80% and above (Green)
- **Good**: 60-79% (Blue)
- **Needs Improvement**: Below 60% (Amber)

---

## 🔍 What to Look For

### User Experience
- ✅ Smooth transitions between states
- ✅ Clear error messages if something fails
- ✅ Loading indicators during API calls
- ✅ Intuitive navigation between pages
- ✅ Professional, student-friendly design
- ✅ Mobile-responsive on all screen sizes

### Data Integrity
- ✅ Evaluations persist in database
- ✅ Scores calculated correctly
- ✅ Filters work as expected
- ✅ Delete removes evaluation from list
- ✅ Chapter performance updates after new evaluations

### Performance
- ✅ Page loads quickly
- ✅ Filters apply instantly (client-side)
- ✅ No lag when switching between pages
- ✅ Smooth scrolling in modals

---

## ✅ Testing Checklist

Copy this checklist and mark items as you test:

### Basic Functionality
- [ ] Submit evaluation with all fields filled
- [ ] Submit evaluation without chapter (optional field)
- [ ] View evaluation results
- [ ] Navigate to history page
- [ ] View chapter performance cards

### Filters & Search
- [ ] Search by question text
- [ ] Filter by chapter
- [ ] Filter by score range
- [ ] Sort by newest
- [ ] Sort by oldest
- [ ] Sort by highest score
- [ ] Sort by lowest score

### Actions
- [ ] View evaluation details in modal
- [ ] Close modal
- [ ] Delete evaluation (confirm)
- [ ] Cancel delete
- [ ] Navigate back to evaluation page

### Responsive Design
- [ ] Desktop view (1024px+)
- [ ] Tablet view (768px)
- [ ] Mobile view (375px)
- [ ] Small mobile (320px)

### Edge Cases
- [ ] Empty history (no evaluations)
- [ ] Error handling (disconnect backend and try)
- [ ] Very long question text
- [ ] Very long answer text
- [ ] Special characters in text

---

## 🎓 User Scenarios

### Scenario 1: First Time User
1. User clicks "Evaluation" in navigation
2. Sees form with instructions
3. Enters sample question and answer
4. Clicks "Evaluate Answer"
5. Waits for loading (sees rotating messages)
6. Views results with excitement
7. Clicks "View History" to see saved evaluation

### Scenario 2: Regular User
1. User has 10+ evaluations already
2. Opens history page
3. Searches for specific topic using search bar
4. Filters by chapter to focus on weak areas
5. Sorts by lowest score to identify improvement areas
6. Clicks "View" on a low-scoring evaluation
7. Reviews model answer and improvements
8. Goes back to main page to try again

### Scenario 3: Progress Tracker
1. User opens history page
2. Scrolls to chapter performance section
3. Reviews average scores per chapter
4. Identifies weak chapters (below 60%)
5. Plans to study those chapters
6. Submits new evaluations for weak chapters
7. Tracks improvement over time

---

## 📱 Mobile-Specific Features

When testing on mobile devices:
- Navigation shows icon-only on small screens
- Tables convert to cards with key information
- Dialogs take full screen for better readability
- Buttons are touch-friendly (larger tap targets)
- Forms stack vertically for easy input
- Chapter performance cards stack in single column

---

## 🆘 Support

If you encounter issues:
1. Check this troubleshooting guide first
2. Review browser console for errors
3. Check backend logs for API errors
4. Verify all dependencies are installed
5. Ensure database migrations are applied

---

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Evaluations complete in 15-30 seconds
- ✅ Results show meaningful feedback from AI
- ✅ Model answers match textbook content
- ✅ History page loads instantly with filters
- ✅ Chapter performance shows accurate statistics
- ✅ Mobile experience is smooth and responsive
- ✅ No console errors in browser

---

**Ready to go!** 🚀

Start with Step 1 above and test the complete flow. The module is production-ready!
