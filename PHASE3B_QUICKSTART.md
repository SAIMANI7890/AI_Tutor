# 🚀 Phase 3B: Quick Start Guide

Get started with Study Planner APIs in 5 minutes!

---

## Step 1: Start the Server ⏱️ 30 seconds

```bash
cd backend
uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## Step 2: View API Documentation ⏱️ 1 minute

Open your browser:
```
http://localhost:8000/docs
```

You'll see:
- ✅ All 6 study plan endpoints
- ✅ Interactive try-it-out feature
- ✅ Request/response examples
- ✅ Authentication setup

---

## Step 3: Test with cURL ⏱️ 2 minutes

### 3.1 Login to Get Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Copy the `access_token` from the response.**

### 3.2 Create a Study Plan

```bash
export TOKEN="your_access_token_here"

curl -X POST "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exam_date": "2026-03-15",
    "daily_study_hours": 3,
    "selected_chapter_ids": [1, 2, 3, 4]
  }'
```

**Expected response:**
```json
{
  "success": true,
  "message": "Study plan generated successfully",
  "data": {
    "plan_id": 1,
    "total_days": 28,
    "items_count": 34
  }
}
```

### 3.3 List Your Plans

```bash
curl -X GET "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer $TOKEN"
```

### 3.4 Get Plan Details

```bash
curl -X GET "http://localhost:8000/api/v1/study-plans/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Step 4: Run Tests (Optional) ⏱️ 1 minute

```bash
cd backend
pytest tests/api/test_study_plans_api.py -v
```

**Expected:** 40+ tests passing ✅

---

## 🎯 You're Done!

You now have a working Study Planner API. You can:

### Test All Endpoints

1. **Create Plan:** `POST /api/v1/study-plans/`
2. **List Plans:** `GET /api/v1/study-plans/`
3. **Get Details:** `GET /api/v1/study-plans/{id}`
4. **Update Status:** `PATCH /api/v1/study-plans/{id}/items/{item_id}`
5. **Delete Plan:** `DELETE /api/v1/study-plans/{id}`
6. **Get Summary:** `GET /api/v1/study-plans/{id}/summary`

### Read Documentation

- **PHASE3B_COMPLETE.md** - Full documentation
- **PHASE3B_API_EXAMPLES.md** - Complete examples
- **Swagger UI** - http://localhost:8000/docs

---

## 🔥 Quick Examples

### Complete Workflow (Copy & Paste)

```bash
# 1. Login
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  | jq -r '.data.access_token')

# 2. Create Plan
PLAN_ID=$(curl -s -X POST "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exam_date": "2026-03-15",
    "daily_study_hours": 3,
    "selected_chapter_ids": [1,2,3,4]
  }' | jq -r '.data.plan_id')

echo "Created Plan ID: $PLAN_ID"

# 3. View Plan
curl -X GET "http://localhost:8000/api/v1/study-plans/$PLAN_ID" \
  -H "Authorization: Bearer $TOKEN" | jq

# 4. Get Summary
curl -X GET "http://localhost:8000/api/v1/study-plans/$PLAN_ID/summary" \
  -H "Authorization: Bearer $TOKEN" | jq

# 5. Mark First Item as Completed
ITEM_ID=$(curl -s -X GET "http://localhost:8000/api/v1/study-plans/$PLAN_ID" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.data.items[0].id')

curl -X PATCH "http://localhost:8000/api/v1/study-plans/$PLAN_ID/items/$ITEM_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "Completed"}' | jq

# 6. Check Progress Again
curl -X GET "http://localhost:8000/api/v1/study-plans/$PLAN_ID/summary" \
  -H "Authorization: Bearer $TOKEN" | jq
```

---

## 🐛 Troubleshooting

### Server Won't Start
```bash
# Check if port 8000 is already in use
netstat -ano | findstr :8000

# Kill the process or use a different port
uvicorn app.main:app --reload --port 8001
```

### Database Error
```bash
# Make sure migrations are applied
python -m alembic upgrade head
```

### Authentication Error
```bash
# Make sure you have a test user
# Register a new user first
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

---

## 📚 Next Steps

1. **Explore Swagger UI** - Test all endpoints interactively
2. **Read API Examples** - See complete request/response examples
3. **Run Full Test Suite** - Verify everything works
4. **Integrate Frontend** - Start building the UI!

---

## ✅ Success Checklist

- [ ] Server running on port 8000
- [ ] Can access Swagger UI
- [ ] Can login and get token
- [ ] Can create a study plan
- [ ] Can list plans
- [ ] Can view plan details
- [ ] Can update item status
- [ ] Can delete a plan

---

**Happy Coding! 🎉**
