# Study Planner - Quick Start Guide

## ✅ Implementation Status

**Backend:** Complete (Phase 3.5)  
**Frontend:** Complete (Phase 5C & 5D)  
**Status:** Production-Ready

---

## 🚀 How to Test

### 1. **Start the Backend**

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

Backend runs on: `http://localhost:8000`

### 2. **Start the Frontend**

```bash
cd frontend
npm run dev
```

Frontend runs on: `http://localhost:3000`

### 3. **Access Study Planner**

1. **Login/Register:**
   - Go to `http://localhost:3000/login`
   - Login or create an account

2. **Navigate to Study Planner:**
   - Click "Social Studies" card from dashboard
   - OR directly go to: `http://localhost:3000/dashboard/social/study-plan`
   - OR use the top navigation: "Study Planner" button

### 4. **Create Your First Study Plan**

**Step 1: Select Exam Date**
- Click on the "Select exam date" button
- Choose a date in the future (e.g., 30 days from now)

**Step 2: Set Daily Study Hours**
- Enter hours you can study per day (e.g., 3)
- Range: 1-24 hours

**Step 3: Select Chapters**
- Expand category (e.g., History)
- Check individual chapters OR
- Click category checkbox to select all
- You can select from multiple categories

**Step 4: Generate**
- Click "Generate Study Plan" button
- Wait 2-5 seconds for generation
- Plan will appear automatically

### 5. **Use Your Study Plan**

**View Your Schedule:**
- See all study days organized as cards
- Blue cards = Study sessions
- Purple cards = Revision sessions
- Green cards = Mock Tests

**Track Progress:**
- Check the checkbox when you complete a day
- Watch your progress bar increase
- See completion percentage update

**Stats Dashboard:**
- 📅 Exam Date - Your target date
- ⏰ Days Remaining - Countdown
- 🎯 Daily Hours - Your commitment
- 📈 Progress - Completion percentage

---

## 📱 Navigation

Use the **top navigation bar** to switch between:
- 🏠 **Dashboard** - Main overview
- 💬 **AI Tutor Chat** - Ask questions
- 📅 **Study Planner** - Your study schedule ⭐
- 📝 **Examinations** - Practice tests

---

## 🎯 Features Highlights

### ✅ Intelligent Scheduling
- Automatically schedules study sessions
- Adds revision days every 4 study days
- Adds mock tests every 7 days
- Prioritizes harder chapters first

### ✅ Progress Tracking
- Real-time completion tracking
- Visual progress bar
- Statistics dashboard
- Completion badges

### ✅ Flexible Selection
- 40 chapters across 4 categories
- Select individual chapters
- Select entire categories
- Multiple category selection

### ✅ Responsive Design
- Works on mobile, tablet, desktop
- Touch-friendly checkboxes
- Optimized layouts for each screen size

---

## 🧪 Test Scenarios

### **Scenario 1: Quick Study Plan**
- Exam in 15 days
- 2 hours per day
- Select 3 chapters from History
- Expected: ~10 day plan with revisions

### **Scenario 2: Comprehensive Plan**
- Exam in 60 days
- 4 hours per day
- Select all History chapters (10)
- Expected: ~45 day plan with revisions and tests

### **Scenario 3: Multiple Categories**
- Exam in 30 days
- 3 hours per day
- 5 chapters from History + 5 from Geography
- Expected: ~25 day plan

### **Scenario 4: Progress Tracking**
- Create any plan
- Mark first 5 days as complete
- Watch progress bar increase
- Verify percentage calculation

---

## 🐛 Troubleshooting

### **Form doesn't submit:**
- Check that exam date is in the future
- Ensure daily hours is between 1-24
- Verify at least 1 chapter is selected
- Check browser console for errors

### **Plan doesn't load:**
- Verify backend is running on port 8000
- Check network tab for API errors
- Ensure you're logged in (valid JWT token)
- Try refreshing the page

### **Status update doesn't work:**
- Check backend connection
- Verify API endpoint is accessible
- Check browser console for errors
- Try clicking again

### **Backend not responding:**
```bash
# Check if backend is running
curl http://localhost:8000/docs

# Restart backend
cd backend
uvicorn app.main:app --reload
```

### **Frontend not loading:**
```bash
# Restart frontend
cd frontend
npm run dev
```

---

## 📊 API Testing (Optional)

### **Using cURL:**

**1. Login to get token:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

**2. Create study plan:**
```bash
curl -X POST http://localhost:8000/api/v1/study-plans \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "exam_date": "2026-07-15",
    "daily_study_hours": 3.0,
    "selected_chapter_ids": [1, 2, 3, 4, 5]
  }'
```

**3. Get study plan:**
```bash
curl -X GET http://localhost:8000/api/v1/study-plans/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### **Using FastAPI Docs:**

1. Go to `http://localhost:8000/docs`
2. Click "Authorize" button
3. Enter your JWT token
4. Try the `/study-plans` endpoints interactively

---

## 📝 Code Locations

### **Frontend Files:**
- **Page:** `frontend/src/app/dashboard/social/study-plan/page.tsx`
- **Form:** `frontend/src/components/study-plan/study-plan-form.tsx`
- **Card:** `frontend/src/components/study-plan/study-plan-card.tsx`
- **API:** `frontend/src/lib/study-plan-api.ts`
- **Types:** `frontend/src/types/study-plan.ts`
- **Data:** `frontend/src/data/chapters.ts`

### **Backend Files:**
- **API:** `backend/app/api/v1/endpoints/study_plans.py`
- **Service:** `backend/app/services/study_plan_service.py`
- **Planner:** `backend/app/study_planner/services/planner_service.py`
- **Models:** `backend/app/models/study_plan.py`
- **Schemas:** `backend/app/schemas/study_plan_api.py`
- **Chapters:** `backend/app/study_planner/config/chapters.py`

---

## 🎉 Success!

If you can:
1. ✅ Create a study plan
2. ✅ See it displayed with cards
3. ✅ Check/uncheck items
4. ✅ See progress bar update
5. ✅ Navigate between sections

**Your Study Planner is working perfectly!** 🎊

---

## 📚 Next Steps

1. **Test with real data:**
   - Create your actual exam study plan
   - Use real dates and chapters

2. **Track your progress:**
   - Mark completed sessions daily
   - Watch your progress grow

3. **Try different scenarios:**
   - Short exam periods
   - Long exam periods
   - Different chapter combinations

4. **Explore other features:**
   - Use AI Tutor for chapter help
   - Generate practice exams
   - View exam history

---

## 🤝 Support

**Found an issue?**
1. Check browser console for errors
2. Verify API endpoints in Network tab
3. Check backend logs
4. Review the implementation docs

**Need help?**
- Review: `PHASE5C_5D_STUDY_PLANNER_FRONTEND_COMPLETE.md`
- Check: `PHASE3.5_STUDY_PLANNER_VERIFICATION.md`
- API Docs: `http://localhost:8000/docs`

---

**Happy Studying! 📚✨**
