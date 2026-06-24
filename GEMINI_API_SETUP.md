# Gemini API Setup Guide

## Why You Need This

The Study Planner uses Google's Gemini AI to generate intelligent, personalized study schedules. Without a valid API key, the system will automatically fall back to the rule-based planner (which still works great!).

---

## Getting Your Gemini API Key

### Step 1: Go to Google AI Studio
Visit: https://aistudio.google.com/app/apikey

### Step 2: Sign in with Google Account
Use any Google account

### Step 3: Create API Key
1. Click "Get API Key" or "Create API Key"
2. Select "Create API key in new project" (or use existing project)
3. Copy the generated key
4. **Important:** Keep this key secret!

**Example key format:**
```
AIzaSyD-1234567890abcdefghijklmnopqrstuvwxyz
```

---

## Adding API Key to Your Project

### Method 1: Environment File (Recommended)

**Edit:** `backend/.env`

```env
# AI Configuration
GEMINI_API_KEY=AIzaSyD-your-actual-key-here
```

**Replace** `AIzaSyD-your-actual-key-here` with your actual key!

### Method 2: Environment Variable

**Windows:**
```cmd
set GEMINI_API_KEY=AIzaSyD-your-actual-key-here
```

**Mac/Linux:**
```bash
export GEMINI_API_KEY=AIzaSyD-your-actual-key-here
```

---

## Verifying Your Setup

### Step 1: Restart Backend
```bash
cd backend
# Stop backend if running (Ctrl+C)
uvicorn app.main:app --reload
```

### Step 2: Check Logs
You should see:
```
INFO  [ai_planner] Gemini LLM initialized successfully
```

**If you see:**
```
WARNING [ai_planner] GEMINI_API_KEY not configured - will use fallback planner
```
→ Your key is not set correctly

### Step 3: Run Verification Script
```bash
cd backend
python verify_phase5_production.py
```

**Look for:**
```
✅ PASS - AI Planner Init
      Gemini LLM Initialized     AI planner ready
```

---

## Testing AI Generation

### Method 1: Via Frontend
1. Open Study Planner
2. Create a study plan
3. Wait 2-5 seconds
4. Check backend logs for "AI generation successful"

### Method 2: Via Python Script
```bash
cd backend
python verify_ai_planner.py
```

**Expected output:**
```
🤖 TEST 1: AI-Powered Generation
✅ Plan generated successfully!

📊 Plan Summary:
   Total Days: 30
   ...
   
🎉 Generated using: AI (Gemini)
```

---

## Troubleshooting

### Issue: "GEMINI_API_KEY not configured"

**Solution 1:** Check `.env` file
```bash
cd backend
cat .env | grep GEMINI_API_KEY
```
- Should show: `GEMINI_API_KEY=AIzaSy...`
- If empty or missing, add your key

**Solution 2:** Restart backend
- Changes to `.env` require restart
- Stop backend (Ctrl+C)
- Start again: `uvicorn app.main:app --reload`

---

### Issue: "Failed to initialize Gemini: API key invalid"

**Possible causes:**
1. **Wrong key format**
   - Should start with `AIzaSy`
   - Should be ~39 characters
   - No spaces or quotes

2. **Expired or revoked key**
   - Generate a new key
   - Update `.env`
   - Restart backend

3. **API not enabled**
   - Go to: https://console.cloud.google.com/
   - Enable "Generative Language API"

---

### Issue: "API quota exceeded"

**Symptoms:**
- Plans generate but then stop working
- Error: "429 Resource exhausted"

**Solutions:**
1. **Wait:** Free tier resets daily
2. **Upgrade:** Enable billing in Google Cloud
3. **Fallback works:** System automatically uses rule-based planner

---

## API Key Best Practices

### ✅ DO:
- Keep your key secret
- Add `.env` to `.gitignore`
- Use different keys for dev/prod
- Monitor usage in Google Cloud Console
- Revoke old keys

### ❌ DON'T:
- Commit keys to git
- Share keys publicly
- Use production keys in development
- Hardcode keys in source code

---

## Fallback System

**Good news:** Even without Gemini, your app works perfectly!

### When Fallback Activates:
- No API key configured
- Invalid API key
- Network issues
- API quota exceeded
- Gemini service down

### What Happens:
1. System detects AI unavailable
2. Automatically switches to rule-based planner
3. Generates valid study plan
4. User experience unaffected
5. Warning logged (but not shown to user)

**Bottom line:** Your app NEVER crashes due to AI issues! 🎉

---

## Free Tier Limits

**Google Gemini Free Tier:**
- 60 requests per minute
- 1,500 requests per day
- Plenty for development and testing!

**For production:**
- Monitor usage
- Consider enabling billing
- Implement rate limiting

---

## Testing Without API Key

**Want to test fallback system?**

1. Comment out API key in `.env`:
```env
# GEMINI_API_KEY=AIzaSy...
```

2. Restart backend

3. Create study plan

4. Verify:
   - Plan still generates ✅
   - Uses rule-based algorithm ✅
   - No errors ✅

5. Restore API key when done

---

## Support

**Still having issues?**

1. Check backend logs: Look for AI planner errors
2. Run verification: `python verify_phase5_production.py`
3. Test AI script: `python verify_ai_planner.py`
4. Check API key format: Should start with `AIzaSy`
5. Try new API key: Generate fresh key

**Remember:** Fallback ensures your app always works! 🚀
