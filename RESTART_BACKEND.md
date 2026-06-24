# ⚠️ RESTART BACKEND SERVER

## The backend server MUST be restarted for the new API endpoint to work!

### How to Restart:

#### Option 1: Stop and Restart
1. Go to your terminal running the backend
2. Press `Ctrl+C` to stop the server
3. Run again:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Option 2: If using auto-reload
The `--reload` flag should auto-restart when files change, but sometimes it doesn't pick up new endpoints.
**Manually restart to be safe!**

---

## After Restarting:

1. ✅ Backend should start without errors
2. ✅ You should see logs about routes being registered
3. ✅ Navigate to `http://localhost:3000/dashboard/social/evaluation`
4. ✅ The page should load (possibly showing "No submitted tests" if you haven't submitted any)

---

## If You See "No submitted tests found":

This is **NORMAL** if you haven't submitted any tests with long-answer questions yet!

### To test the full workflow:

1. **Go to Examinations** → `/dashboard/social/examination`
2. **Generate a new exam**:
   - Select any category (e.g., "History")
   - Choose question type: **LONG_ANSWER**
   - Set question count: 3-5 questions
   - Click "Generate Exam"
3. **Answer the questions** (write actual answers, not just "test")
4. **Submit the exam**
5. **Go back to Evaluation** → `/dashboard/social/evaluation`
6. **You should now see your submitted test** with "Evaluate" buttons

---

## Troubleshooting:

### Still getting 500 error?
- Check backend terminal for error messages
- Look for Python traceback in the logs
- Ensure database migrations are applied: `alembic upgrade head`

### Backend won't start?
- Check for syntax errors in the evaluations.py file
- Verify all imports are correct
- Check if port 8000 is already in use

### Tests not showing up?
- Verify you submitted a test with LONG_ANSWER questions
- Check test status is SUBMITTED (not GENERATED)
- Check you actually answered the long-answer questions

---

**After restarting, the evaluation page should work!** 🚀
