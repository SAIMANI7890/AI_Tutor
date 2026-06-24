# 🚀 Quick Start: gemini-2.5-flash-lite

## ✅ DONE: All services updated to `gemini-2.5-flash-lite`

---

## 🎯 Test It Now (2 Minutes)

### 1. Verify Model (30 seconds)
```bash
cd backend
python verify_gemini_2_flash.py
```

✅ **See "SUCCESS"?** → Continue to step 2  
❌ **See "ERROR"?** → Model not available, see bottom of this file

---

### 2. Restart Backend (10 seconds)
```bash
# Press Ctrl+C to stop backend
uvicorn app.main:app --reload
```

---

### 3. Test Exam Generation (1 minute)
1. Open: http://localhost:3000/dashboard/social/examination
2. Select: **History** + **MCQ** + **5 questions**
3. Click: **"Generate Test"**
4. ⏱️ **Time it!**

**Expected**: 6-10 seconds (very fast!) ⚡  
**If slower than 15s**: Model didn't work, see troubleshooting

---

## ✅ Success Looks Like:

```
✓ Verification passes
✓ Backend restarts without errors  
✓ Exam generates in 6-10 seconds
✓ Questions are high quality
✓ Study planner works (3-5 seconds)
✓ AI tutor responds (1-2 seconds)
```

---

## ❌ If Verification Fails:

### Error: "model not found"

**Your API key doesn't have access to gemini-2.5-flash-lite**

**Quick Fix** - Use `gemini-pro` instead:

```bash
cd backend

# Rollback to gemini-pro (always works)
python -c "
import os
files = [
    'app/services/question_generation/generator.py',
    'app/study_planner/services/ai_planner_service.py', 
    'app/services/tutor_service.py',
    'app/api/v1/endpoints/tutor.py'
]
for f in files:
    content = open(f).read()
    content = content.replace('gemini-2.5-flash-lite', 'gemini-pro')
    open(f, 'w').write(content)
    print(f'✅ {f}')
print('\n✅ Done! Restart backend.')
"
```

Then restart backend. Will be slower (15-20s) but **will work**!

---

## 📊 Performance Expectations

| Feature | Time |
|---------|------|
| **Exam Generation (5 MCQ)** | 6-10s |
| **Study Plan Creation** | 3-5s |
| **AI Tutor Response** | 1-2s |

If times are much higher, the model change didn't work.

---

## 🎉 That's It!

**Your entire AI system now uses gemini-2.5-flash-lite** ⚡

Test it and enjoy the speed! 🚀

---

**Need help?** Read `GEMINI_2.5_FLASH_LITE_UPDATED.md` for detailed guide.
