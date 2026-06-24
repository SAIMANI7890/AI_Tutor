# 🚀 AI Study Companion - Quick Start Guide

**Get up and running in 10 minutes!**

## Prerequisites

✅ Python 3.12+  
✅ Node.js 18+  
✅ PostgreSQL 14+

## Setup Steps

### 1️⃣ Database (2 minutes)

```bash
# Create database
psql -U postgres
CREATE DATABASE ai_study_companion;
\q
```

### 2️⃣ Backend (3 minutes)

```bash
# Navigate and setup
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your database credentials

# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Copy output to SECRET_KEY in .env

# Start server
uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000

### 3️⃣ Frontend (3 minutes)

**Open new terminal:**

```bash
# Navigate and setup
cd frontend
npm install

# Configure environment
copy .env.local.example .env.local
# Content should be:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Start server
npm run dev
```

✅ Frontend running at: http://localhost:3000

## First Test (2 minutes)

1. **Open browser**: http://localhost:3000
2. **Register**: Click "Sign up"
   - Name: Test User
   - Email: test@example.com
   - Password: TestPass123
3. **Explore**: View dashboard and profile
4. **Logout & Login**: Test authentication

## Quick Commands

### Start Everything

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Stop Everything

Press `Ctrl + C` in both terminals

## URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/api/v1/docs |
| Health Check | http://localhost:8000/health |

## Common Issues

### Port already in use?
```bash
# Change frontend port
npm run dev -- -p 3001

# Kill process on Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Database connection error?
- Check PostgreSQL is running
- Verify credentials in backend/.env
- Test: `psql -U postgres -d ai_study_companion`

### Module not found?
```bash
# Backend
pip install -r requirements.txt

# Frontend
rm -rf node_modules
npm install
```

## Project Structure

```
ai-study-companion/
├── backend/          # FastAPI + PostgreSQL
│   ├── app/          # Application code
│   ├── alembic/      # Database migrations
│   └── .env          # Configuration
│
├── frontend/         # Next.js 15
│   ├── src/          # Source code
│   └── .env.local    # Configuration
│
└── docs/             # Documentation
```

## What's Implemented?

✅ User registration and login  
✅ JWT authentication  
✅ Protected dashboard  
✅ Profile management  
✅ Responsive design  
✅ Social Studies subject card  

## What's NOT Implemented Yet?

⏳ Study planner (Phase 2)  
⏳ AI tutor (Phase 2)  
⏳ Examinations (Phase 2)  
⏳ Progress tracking (Phase 2)  

## Tech Stack

**Frontend**: Next.js 15, TypeScript, Tailwind CSS, shadcn/ui  
**Backend**: FastAPI, SQLAlchemy, PostgreSQL  
**Auth**: JWT, Bcrypt

## Need Help?

📖 **Detailed Setup**: Read `SETUP.md`  
🏗️ **Architecture**: Read `ARCHITECTURE.md`  
📋 **Features**: Read `PHASE1_COMPLETE.md`  
📚 **Main Docs**: Read `README.md`

## API Examples

### Register User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "confirm_password": "SecurePass123"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

## Development Workflow

1. **Start backend** in terminal 1
2. **Start frontend** in terminal 2
3. **Open browser** at http://localhost:3000
4. **Make changes** - both servers auto-reload
5. **Test** in browser
6. **Commit** changes to git

## Production Deployment

### Backend (Render/Railway)
1. Connect repository
2. Set build: `pip install -r requirements.txt`
3. Set start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables

### Frontend (Vercel)
1. Connect repository
2. Root: `frontend`
3. Framework: Next.js
4. Add `NEXT_PUBLIC_API_URL` env var

## Success Criteria

✅ Backend server running without errors  
✅ Frontend loads at localhost:3000  
✅ Can register new user  
✅ Can login  
✅ Dashboard displays  
✅ Profile page works  
✅ Can logout  

## Next Steps

1. ✅ Complete Phase 1 setup
2. 📖 Read architecture documentation
3. 🎨 Customize UI colors/branding
4. 🚀 Start planning Phase 2 features
5. 💡 Explore the codebase

---

**You're ready to build!** 🎉

For detailed information, see the other documentation files.
