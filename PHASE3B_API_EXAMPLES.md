# 📚 Phase 3B: Study Plans API - Examples

Complete examples of all Study Plans API endpoints with requests and responses.

---

## 🔐 Authentication

All endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

---

## 📍 Base URL

```
http://localhost:8000/api/v1/study-plans
```

---

## 1️⃣ Create Study Plan

**POST** `/api/v1/study-plans/`

Generate and save a new study plan.

### Request

```http
POST /api/v1/study-plans/
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "exam_date": "2026-03-15",
  "daily_study_hours": 3.0,
  "selected_chapter_ids": [1, 2, 3, 4, 11, 12, 21, 22]
}
```

### Response (201 Created)

```json
{
  "success": true,
  "message": "Study plan generated successfully",
  "data": {
    "plan_id": 1,
    "total_days": 28,
    "items_count": 34,
    "exam_date": "2026-03-15",
    "daily_study_hours": 3.0
  }
}
```

### Error Responses

**400 Bad Request - Past Exam Date**
```json
{
  "success": false,
  "message": "Validation failed: Exam date must be in the future",
  "errors": []
}
```

**400 Bad Request - Invalid Chapter IDs**
```json
{
  "success": false,
  "message": "One or more invalid chapter IDs provided",
  "errors": []
}
```

**401 Unauthorized**
```json
{
  "detail": "Not authenticated"
}
```

### cURL Example

```bash
curl -X POST "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "exam_date": "2026-03-15",
    "daily_study_hours": 3.0,
    "selected_chapter_ids": [1, 2, 3, 4]
  }'
```

---

## 2️⃣ List Study Plans

**GET** `/api/v1/study-plans/`

Get all study plans for the authenticated user.

### Request

```http
GET /api/v1/study-plans/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Response (200 OK)

```json
{
  "success": true,
  "message": "Study plans retrieved successfully",
  "data": {
    "plans": [
      {
        "id": 1,
        "exam_date": "2026-03-15",
        "daily_study_hours": 3.0,
        "created_at": "2026-02-10T10:30:00",
        "updated_at": "2026-02-15T14:20:00",
        "completion_percentage": 65.5,
        "total_items": 34,
        "completed_items": 22
      },
      {
        "id": 2,
        "exam_date": "2026-04-20",
        "daily_study_hours": 4.0,
        "created_at": "2026-02-08T09:00:00",
        "updated_at": "2026-02-08T09:00:00",
        "completion_percentage": 0.0,
        "total_items": 28,
        "completed_items": 0
      }
    ],
    "total_count": 2
  }
}
```

### Response - Empty List (200 OK)

```json
{
  "success": true,
  "message": "Study plans retrieved successfully",
  "data": {
    "plans": [],
    "total_count": 0
  }
}
```

### cURL Example

```bash
curl -X GET "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 3️⃣ Get Study Plan Details

**GET** `/api/v1/study-plans/{plan_id}`

Get complete details of a specific study plan including all items.

### Request

```http
GET /api/v1/study-plans/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Response (200 OK)

```json
{
  "success": true,
  "message": "Study plan retrieved successfully",
  "data": {
    "id": 1,
    "user_id": 5,
    "exam_date": "2026-03-15",
    "daily_study_hours": 3.0,
    "created_at": "2026-02-10T10:30:00",
    "updated_at": "2026-02-15T14:20:00",
    "completion_percentage": 65.5,
    "total_items": 34,
    "completed_items": 22,
    "items": [
      {
        "id": 1,
        "study_plan_id": 1,
        "day_number": 1,
        "study_date": "2026-02-10",
        "activity_type": "Study",
        "chapter_id": 1,
        "chapter_name": "French Revolution",
        "allocated_hours": 2.5,
        "status": "Completed",
        "created_at": "2026-02-10T10:30:00"
      },
      {
        "id": 2,
        "study_plan_id": 1,
        "day_number": 2,
        "study_date": "2026-02-11",
        "activity_type": "Study",
        "chapter_id": 2,
        "chapter_name": "Industrial Revolution",
        "allocated_hours": 3.0,
        "status": "Completed",
        "created_at": "2026-02-10T10:30:00"
      },
      {
        "id": 3,
        "study_plan_id": 1,
        "day_number": 3,
        "study_date": "2026-02-12",
        "activity_type": "Study",
        "chapter_id": 3,
        "chapter_name": "World War I",
        "allocated_hours": 3.0,
        "status": "Pending",
        "created_at": "2026-02-10T10:30:00"
      },
      {
        "id": 4,
        "study_plan_id": 1,
        "day_number": 4,
        "study_date": "2026-02-13",
        "activity_type": "Revision",
        "chapter_id": null,
        "chapter_name": null,
        "allocated_hours": 3.0,
        "status": "Pending",
        "created_at": "2026-02-10T10:30:00"
      }
    ]
  }
}
```

### Error Responses

**404 Not Found**
```json
{
  "detail": "Study plan not found"
}
```

**403 Forbidden - Not Owner**
```json
{
  "detail": "You do not have permission to access this study plan"
}
```

### cURL Example

```bash
curl -X GET "http://localhost:8000/api/v1/study-plans/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 4️⃣ Update Study Item Status

**PATCH** `/api/v1/study-plans/{plan_id}/items/{item_id}`

Mark a study item as Completed, Pending, or Skipped.

### Request - Mark as Completed

```http
PATCH /api/v1/study-plans/1/items/3
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "status": "Completed"
}
```

### Response (200 OK)

```json
{
  "success": true,
  "message": "Status updated successfully",
  "data": {
    "item_id": 3,
    "day_number": 3,
    "status": "Completed",
    "chapter_name": "World War I",
    "activity_type": "Study"
  }
}
```

### Request - Mark as Skipped

```http
PATCH /api/v1/study-plans/1/items/5
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "status": "Skipped"
}
```

### Response (200 OK)

```json
{
  "success": true,
  "message": "Status updated successfully",
  "data": {
    "item_id": 5,
    "day_number": 5,
    "status": "Skipped",
    "chapter_name": "Climate and Weather Patterns",
    "activity_type": "Study"
  }
}
```

### Error Responses

**404 Not Found - Invalid Item**
```json
{
  "detail": "Study plan item not found"
}
```

**422 Validation Error - Invalid Status**
```json
{
  "detail": [
    {
      "loc": ["body", "status"],
      "msg": "value is not a valid enumeration member; permitted: 'Pending', 'Completed', 'Skipped'",
      "type": "type_error.enum"
    }
  ]
}
```

### cURL Examples

```bash
# Mark as Completed
curl -X PATCH "http://localhost:8000/api/v1/study-plans/1/items/3" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"status": "Completed"}'

# Mark as Skipped
curl -X PATCH "http://localhost:8000/api/v1/study-plans/1/items/5" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"status": "Skipped"}'
```

---

## 5️⃣ Delete Study Plan

**DELETE** `/api/v1/study-plans/{plan_id}`

Delete a study plan and all its items (cascade delete).

### Request

```http
DELETE /api/v1/study-plans/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Response (200 OK)

```json
{
  "success": true,
  "message": "Plan deleted successfully",
  "data": {
    "plan_id": 1
  }
}
```

### Error Responses

**404 Not Found**
```json
{
  "detail": "Study plan not found"
}
```

**403 Forbidden - Not Owner**
```json
{
  "detail": "Study plan not found"
}
```

### cURL Example

```bash
curl -X DELETE "http://localhost:8000/api/v1/study-plans/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 6️⃣ Get Study Plan Summary (Bonus)

**GET** `/api/v1/study-plans/{plan_id}/summary`

Get quick summary statistics for a study plan.

### Request

```http
GET /api/v1/study-plans/1/summary
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Response (200 OK)

```json
{
  "success": true,
  "message": "Summary retrieved successfully",
  "data": {
    "plan_id": 1,
    "exam_date": "2026-03-15",
    "days_until_exam": 33,
    "total_items": 34,
    "completed_items": 22,
    "pending_items": 10,
    "skipped_items": 2,
    "completion_percentage": 64.71
  }
}
```

### cURL Example

```bash
curl -X GET "http://localhost:8000/api/v1/study-plans/1/summary" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🔒 Security Notes

### Authentication
- All endpoints require a valid JWT token
- Token must be included in the `Authorization` header
- Format: `Bearer <token>`

### Authorization
- Users can only access their own study plans
- Attempting to access another user's plan returns 403 Forbidden
- Plan ownership is automatically validated

### Data Validation
- Exam date must be in the future
- Daily hours must be between 1 and 12
- At least one chapter must be selected
- Chapter IDs must be valid

---

## 🧪 Testing with Postman

### Setup

1. **Create Environment Variables:**
   - `base_url`: `http://localhost:8000/api/v1`
   - `token`: Your JWT token (get from login endpoint)

2. **Set Authorization:**
   - Type: Bearer Token
   - Token: `{{token}}`

### Collection Structure

```
Study Plans API
├── 1. Create Plan
├── 2. List Plans
├── 3. Get Plan Details
├── 4. Update Item Status
│   ├── Mark Completed
│   ├── Mark Pending
│   └── Mark Skipped
├── 5. Delete Plan
└── 6. Get Summary
```

---

## 📊 Response Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (no token) |
| 403 | Forbidden (not owner) |
| 404 | Not Found |
| 422 | Unprocessable Entity (schema validation) |
| 500 | Internal Server Error |

---

## 🎯 Common Use Cases

### 1. Create and Track a Plan

```bash
# Step 1: Create plan
curl -X POST "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exam_date": "2026-03-15",
    "daily_study_hours": 3,
    "selected_chapter_ids": [1,2,3,4]
  }'

# Step 2: Get plan details
curl -X GET "http://localhost:8000/api/v1/study-plans/1" \
  -H "Authorization: Bearer $TOKEN"

# Step 3: Mark first day as completed
curl -X PATCH "http://localhost:8000/api/v1/study-plans/1/items/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "Completed"}'

# Step 4: Check progress
curl -X GET "http://localhost:8000/api/v1/study-plans/1/summary" \
  -H "Authorization: Bearer $TOKEN"
```

### 2. Manage Multiple Plans

```bash
# List all plans
curl -X GET "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer $TOKEN"

# Delete old plan
curl -X DELETE "http://localhost:8000/api/v1/study-plans/1" \
  -H "Authorization: Bearer $TOKEN"

# Create new plan
curl -X POST "http://localhost:8000/api/v1/study-plans/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exam_date": "2026-04-20",
    "daily_study_hours": 4,
    "selected_chapter_ids": [5,6,7,8]
  }'
```

---

## 📚 Interactive API Documentation

Visit the auto-generated Swagger UI:

```
http://localhost:8000/docs
```

Features:
- Try out all endpoints
- See request/response schemas
- Test authentication
- View all examples

---

**Happy Testing! 🚀**
