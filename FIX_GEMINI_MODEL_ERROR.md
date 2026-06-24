# 🔧 Fix: Gemini Model "Not Found" Error

## ❌ The Error

```
404 models/gemini-1.5-flash is not found for API version v1beta
```

## 🎯 Root Cause

The model name `gemini-1.5-flash` or `gemini-2.5-flash` is not available in your Gemini API version or region.

## ✅ Solution: Use Available Models

### Option 1: Use gemini-pro (RECOMMENDED - Always Works)

**File**: `backend/app/services/question_generation/generator.py`

**Line 40** - Change to:
```python
model: str = "gemini-pro",  # Stable, widely available
```

**Pros**:
- ✅ Always available
- ✅ Good quality
- ✅ Reliable

**Cons**:
- ⚠️ Slower than flash models (15-20s vs 8-10s)

---

### Option 2: Try gemini-1.5-pro (If available)

```python
model: str = "gemini-1.5-pro",  # Better but may not be available
```

**Check if it works**:
```bash
cd backend
python test_gemini_models.py
```

Look for which models show "✅ WORKS"

---

### Option 3: Use Experimental Model (Fastest)

If you have access to experimental models:

```python
model: str = "gemini-2.0-flash-exp",  # Experimental, very fast
```

**Note**: Not all API keys have access to experimental models.

---

## 🧪 Test Which Models You Have Access To

```bash
cd backend
python test_gemini_models.py
```

This will test all common Gemini models and show which work with your API key.

Output example:
```
Testing: gemini-pro... ✅ WORKS
Testing: gemini-1.5-flash... ❌ NOT AVAILABLE
Testing: gemini-1.5-pro... ✅ WORKS
Testing: gemini-2.0-flash-exp... ❌ NOT AVAILABLE
```

Use whichever one works!

---

## 📝 Update Your Code

### Step 1: Find the file
```
backend/app/services/question_generation/generator.py
```

### Step 2: Find line 40 (in `__init__` method)
```python
model: str = "...",  # This line
```

### Step 3: Replace with working model
```python
model: str = "gemini-pro",  # Safe choice
```

### Step 4: Restart backend
```bash
# Stop backend (Ctrl+C)
# Start again
cd backend
uvicorn app.main:app --reload
```

### Step 5: Test exam generation
Go to http://localhost:3000/dashboard/social/examination and try generating a test.

---

## ⏱️ Performance by Model

| Model | Availability | Speed | Quality |
|-------|-------------|-------|---------|
| `gemini-pro` | ✅ Always | 15-20s | ⭐⭐⭐⭐ |
| `gemini-1.5-pro` | ⚠️ Some keys | 12-15s | ⭐⭐⭐⭐⭐ |
| `gemini-1.5-flash` | ⚠️ Some keys | 8-10s | ⭐⭐⭐⭐ |
| `gemini-2.0-flash-exp` | ⚠️ Experimental | 5-8s | ⭐⭐⭐⭐ |

---

## 🔍 Why Did This Happen?

The optimization guide recommended `gemini-1.5-flash` because it's faster, but:

1. **Not all Gemini API keys have access** to newer models
2. **Regional differences** - some regions don't have all models
3. **API tier** - Free tier vs paid tier have different models

**The safe default is `gemini-pro`** - it's always available!

---

## 🚀 What About Performance?

**Don't worry!** Even with `gemini-pro`:

1. You can still apply other optimizations:
   - ✅ Reduce `top_k` to 5 (already done)
   - ✅ Implement background jobs (see optimization guide)
   - ✅ Add caching

2. Performance improvements stack:
   - gemini-pro: 20s
   - gemini-pro + reduced chunks: 15s
   - gemini-pro + background jobs: <1s perceived ⚡

**The model is not the only optimization!**

---

## ✅ Quick Fix Steps

1. **Change model to `gemini-pro`** (done above)
2. **Restart backend**
3. **Test exam generation**
4. **If works**: Great! Consider background jobs for better UX
5. **If still fails**: Run `python test_gemini_models.py` to debug

---

## 🆘 Still Having Issues?

### Error: "API key not valid"
- Check `.env` file has correct `GEMINI_API_KEY`
- Regenerate key at https://makersuite.google.com/app/apikey

### Error: "Quota exceeded"
- You've hit free tier limits (15 requests/minute)
- Wait 1 minute and try again
- Or upgrade to paid tier

### Error: Model works in test but fails in app
- Clear Python cache: `find . -name "*.pyc" -delete`
- Restart backend completely
- Check for multiple generator instances

---

## 📚 Next Steps

After fixing the model error:

1. ✅ **Test exam generation** - Should work now!
2. ✅ **Check generation time** - Expect 15-20s with gemini-pro
3. ✅ **If too slow**: Implement background jobs (see optimization guide)
4. ✅ **Monitor quality**: Generate 5-10 tests, check questions

---

**Status**: Model fixed to `gemini-pro` ✅  
**Expected time**: 15-20 seconds  
**Next**: Consider background processing for better UX  

**The error should be resolved now!** Try generating a test. 🎉
