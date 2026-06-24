# AI Study Companion - Complete Setup Guide

This guide will walk you through setting up the complete AI Study Companion application from scratch.

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Python 3.12+** installed
- [ ] **Node.js 18+** installed
- [ ] **PostgreSQL 14+** installed and running
- [ ] **Git** installed (optional, for version control)
- [ ] **Code editor** (VS Code recommended)
- [ ] **Terminal/Command Prompt** access

### Verify Prerequisites

```bash
# Check Python version
python --version
# Should show: Python 3.12.x or higher

# Check Node.js version
node --version
# Should show: v18.x.x or higher

# Check npm version
npm --version
# Should show: 9.x.x or higher

# Check PostgreSQL
psql --version
# Should show: psql (PostgreSQL) 14.x or higher
```

## 🗄 Step 1: Database Setup

### 1.1 Start PostgreSQL Service

**Windows:**
```bash
# PostgreSQL should start automatically
# Or use Services app to start PostgreSQL service
```

**Linux/Mac:**
```bash
sudo service postgresql start
# or
sudo systemctl start postgresql
```

### 1.2 Create Database

**Option A - Using psql command line:**

```bash
# Connect to PostgreSQL
psql -U postgres

# In psql prompt:
CREATE DATABASE ai_study_companion;

# Create user (optional, if you want dedicated user)
CREATE USER study_admin WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE ai_study_companion TO study_admin;

# Exit psql
\q
```

**Option B - Using pgAdmin:**

1. Open pgAdmin
2. Right-click "Databases"
3. Create → Database
4. Name: `ai_study_companion`
5. Click "Save"

### 1.3 Note Your Database Credentials

Write down:
- Database name: `ai_study_companion`
- Username: `postgres` (or your custom user)
- Password: Your PostgreSQL password
- Host: `localhost`
- Port: `5432` (default)

## 🔧 Step 2: Backend Setup

### 2.1 Navigate to Backend Directory

```bash
cd ai-study-companion/backend
```

### 2.2 Create Virtual Environment

```bash
python -m venv venv
```

### 2.3 Activate Virtual Environment

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 2.4 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- FastAPI
- SQLAlchemy
- PostgreSQL driver
- JWT libraries
- And more...

### 2.5 Configure Environment Variables

**Create `.env` file:**

```bash
copy .env.example .env
```

**Edit `.env` file with your details:**

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ai_study_companion

# JWT Configuration
SECRET_KEY=your-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# API Configuration
API_V1_PREFIX=/api/v1
PROJECT_NAME=AI Study Companion

# CORS Origins
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Environment
ENVIRONMENT=development
```

**Generate a Secure SECRET_KEY:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and replace `SECRET_KEY` in `.env`

### 2.6 Initialize Database Tables

The tables will be created automatically when you first run the app, or you can use Alembic:

**Option A - Automatic (on first run):**
Tables are created when you start the server.

**Option B - Using Alembic:**
```bash
alembic upgrade head
```

### 2.7 Start Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 2.8 Verify Backend is Running

Open browser and visit:
- Main API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs
- Health Check: http://localhost:8000/health

You should see the API documentation interface.

**Keep this terminal running!** Open a new terminal for frontend setup.

## 💻 Step 3: Frontend Setup

### 3.1 Navigate to Frontend Directory

Open a **new terminal** and:

```bash
cd ai-study-companion/frontend
```

### 3.2 Install Node Dependencies

**Using npm:**
```bash
npm install
```

**Or using yarn:**
```bash
yarn install
```

**Or using pnpm:**
```bash
pnpm install
```

This will install:
- Next.js 15
- React 18
- Tailwind CSS
- shadcn/ui components
- Form libraries
- And more...

Installation may take 2-5 minutes.

### 3.3 Configure Environment Variables

**Create `.env.local` file:**

```bash
copy .env.local.example .env.local
```

**Edit `.env.local` file:**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 3.4 Start Frontend Development Server

```bash
npm run dev
```

Or:
```bash
yarn dev
```

You should see:
```
- ready started server on 0.0.0.0:3000
- Local:        http://localhost:3000
```

### 3.5 Verify Frontend is Running

Open browser and visit: http://localhost:3000

You should see the login page!

## ✅ Step 4: Test the Application

### 4.1 Register a New User

1. Open http://localhost:3000
2. Click "Sign up" link
3. Fill in the registration form:
   - Full Name: `Test User`
   - Email: `test@example.com`
   - Password: `TestPass123`
   - Confirm Password: `TestPass123`
4. Click "Create Account"

You should be redirected to the dashboard!

### 4.2 Test Dashboard

- You should see: "Welcome back, Test!"
- Social Studies card should be visible
- Click on your profile icon in top-right

### 4.3 Test Profile Page

1. Click your name in top-right
2. Select "Profile" from dropdown
3. Try editing your name
4. Click "Save Changes"

### 4.4 Test Logout

1. Click your name in top-right
2. Select "Logout"
3. You should be redirected to login page

### 4.5 Test Login

1. Use the same credentials to login:
   - Email: `test@example.com`
   - Password: `TestPass123`
2. You should be redirected to dashboard

## 🎉 Success!

If all tests passed, your application is fully set up and working!

## 📊 What's Running

You should have **two terminal windows** open:

### Terminal 1: Backend
```
Backend Server: http://localhost:8000
API Docs: http://localhost:8000/api/v1/docs
```

### Terminal 2: Frontend
```
Frontend App: http://localhost:3000
```

## 🛑 Stopping the Application

### Stop Frontend
Press `Ctrl + C` in the frontend terminal

### Stop Backend
Press `Ctrl + C` in the backend terminal

### Deactivate Python Virtual Environment
```bash
deactivate
```

## 🔄 Restarting the Application

### Start Backend
```bash
cd ai-study-companion/backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
uvicorn app.main:app --reload
```

### Start Frontend
```bash
cd ai-study-companion/frontend
npm run dev
```

## 🐛 Troubleshooting

### Issue: "Port 8000 already in use"

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:8000 | xargs kill -9
```

### Issue: "Port 3000 already in use"

**Run on different port:**
```bash
npm run dev -- -p 3001
```

Then update `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Issue: Database connection failed

1. Check PostgreSQL is running
2. Verify credentials in `.env`
3. Test connection:
```bash
psql -U postgres -d ai_study_companion
```

### Issue: Module not found (Python)

```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

### Issue: Module not found (Node.js)

```bash
# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

### Issue: "Cannot find module" in Next.js

```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

## 📚 Next Steps

Now that Phase 1 is complete, you can:

1. **Explore the codebase** - Understand the architecture
2. **Read the documentation** - Check `/backend/README.md` and `/frontend/README.md`
3. **Test the API** - Use the interactive docs at http://localhost:8000/api/v1/docs
4. **Customize the UI** - Modify colors in `tailwind.config.ts`
5. **Plan Phase 2** - Start designing the Study Planner feature

## 🚀 Ready for Development!

You're all set to start building amazing features for AI Study Companion!

---

**Questions?** Check the main README.md or individual component READMEs.
