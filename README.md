# AI Study Companion

An AI-powered educational web application designed to be a complete AI tuition teacher for secondary school students.

## 🎯 Project Overview

AI Study Companion helps students study independently without attending traditional tuition classes. Currently focusing on **Social Studies**, with plans to expand to more subjects.

### Phase 1 Status: ✅ COMPLETE

**Implemented Features:**
- ✅ Complete project architecture
- ✅ User authentication system (JWT)
- ✅ PostgreSQL database integration
- ✅ User registration and login
- ✅ Protected dashboard
- ✅ Profile management
- ✅ Responsive design (mobile/tablet/desktop)
- ✅ Modern UI with shadcn/ui
- ✅ Production-ready structure

**Not Yet Implemented (Future Phases):**
- ⏳ Study Planner
- ⏳ Examination Generator
- ⏳ Evaluation System
- ⏳ Revision System
- ⏳ Progress Tracking
- ⏳ AI Tutor Chat
- ⏳ RAG-based Knowledge Retrieval

## 🛠 Tech Stack

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **React Hook Form + Zod** - Form validation
- **TanStack Query** - Data fetching
- **Axios** - HTTP client

### Backend
- **FastAPI** - Python web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Alembic** - Database migrations
- **JWT** - Authentication
- **Bcrypt** - Password hashing
- **LangChain** - RAG framework (Phase 2)
- **Google Gemini** - LLM (Phase 2)
- **ChromaDB** - Vector database (Phase 2)

### Deployment
- **Vercel** - Frontend hosting
- **Render/Railway** - Backend hosting

## 📁 Project Structure

```
ai-study-companion/
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/             # App router pages
│   │   │   ├── login/       # Login page
│   │   │   ├── register/    # Registration page
│   │   │   ├── dashboard/   # Main dashboard
│   │   │   └── profile/     # Profile page
│   │   ├── components/      # React components
│   │   │   ├── ui/          # shadcn/ui components
│   │   │   └── layout/      # Layout components
│   │   ├── contexts/        # React contexts
│   │   └── lib/             # Utilities and services
│   ├── package.json
│   └── README.md
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── api/             # API routes
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/            # Core utilities
│   │   ├── db/              # Database config
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── main.py          # App entry point
│   ├── alembic/             # Database migrations
│   ├── requirements.txt
│   └── README.md
│
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- **Node.js 18+**
- **PostgreSQL 14+**
- **npm/yarn/pnpm**
- **Git**
- **Google Gemini API Key** (Phase 2 - [Get it here](https://makersuite.google.com/app/apikey))

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
```

3. **Activate virtual environment:**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Create PostgreSQL database:**
```sql
CREATE DATABASE ai_study_companion;
```

6. **Configure environment:**
```bash
copy .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/ai_study_companion
SECRET_KEY=your-secure-secret-key-min-32-chars
GEMINI_API_KEY=your-google-gemini-api-key
```

Generate SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Get Gemini API Key: https://makersuite.google.com/app/apikey

7. **Run database migrations:**
```bash
alembic upgrade head
```

8. **Run PDF ingestion (Phase 2):**
```bash
# Place your PDFs in backend/data/ first
python app/rag/ingestion/ingest_all.py
```

9. **Run the server:**
```bash
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Configure environment:**
```bash
copy .env.local.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

4. **Run the development server:**
```bash
npm run dev
```

Frontend runs at: http://localhost:3000

## 📱 Features

### Phase 1: Authentication & Foundation
- User registration with validation
- Secure login with JWT tokens
- Password hashing with bcrypt
- Protected routes
- Dashboard with subject cards
- Profile management

### Phase 2: RAG + AI Tutor (NEW!)
- **AI Tutor Chat** - Ask questions about Social Studies
- **RAG System** - Retrieval-Augmented Generation
- **Source Citations** - Every answer cites textbook sources
- **Zero Hallucination** - Only uses textbook content
- **Chat Sessions** - Multiple conversation support
- **PDF Ingestion** - Automatic processing of textbooks
- **Vector Search** - Semantic similarity matching

### UI/UX
- Educational theme (Blue/Indigo)
- Smooth animations
- Mobile-first responsive design
- Loading states
- Error handling
- Success notifications

## 🗄 Database Schema

### Users Table (Phase 1)

| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | PRIMARY KEY |
| full_name | String(255) | NOT NULL |
| email | String(255) | UNIQUE, NOT NULL, INDEXED |
| password_hash | String(255) | NOT NULL |
| created_at | DateTime | DEFAULT NOW() |
| updated_at | DateTime | DEFAULT NOW(), AUTO UPDATE |

### Chat Sessions Table (Phase 2)

| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | PRIMARY KEY |
| user_id | Integer | FOREIGN KEY → users |
| title | String(255) | DEFAULT 'New Conversation' |
| created_at | DateTime | DEFAULT NOW() |
| updated_at | DateTime | DEFAULT NOW() |

### Chat Messages Table (Phase 2)

| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | PRIMARY KEY |
| session_id | Integer | FOREIGN KEY → chat_sessions |
| role | String(50) | NOT NULL |
| message | Text | NOT NULL |
| sources | Text | JSON string |
| created_at | DateTime | DEFAULT NOW() |

## 🔐 Security

- JWT token-based authentication
- Password hashing with bcrypt (12 rounds)
- CORS configuration
- Input validation with Pydantic
- SQL injection protection via ORM
- XSS protection
- Secure HTTP-only approach for production

## 📊 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login user | No |
| GET | `/api/v1/auth/me` | Get current user | Yes |
| PUT | `/api/v1/auth/me` | Update profile | Yes |

### API Response Format

**Success:**
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

**Error:**
```json
{
  "success": false,
  "message": "Error message",
  "errors": ["details"]
}
```

## 🚢 Deployment

### Backend (Render/Railway)

1. Create new Web Service
2. Connect repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy

### Frontend (Vercel)

1. Connect GitHub repository
2. Set framework preset: Next.js
3. Set root directory: `frontend`
4. Add environment variable: `NEXT_PUBLIC_API_URL`
5. Deploy

## 🧪 Testing

### Backend
Access interactive API docs:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

### Frontend
Test in browser:
- Development: http://localhost:3000
- Use Chrome DevTools for debugging

## 📚 Future Roadmap

### Phase 3: Study Planning
- AI-powered study schedules
- Custom learning paths
- Topic recommendations
- Progress tracking

### Phase 4: Examination System
- Question generation
- Multiple question types
- Automated grading
- Performance analytics

### Phase 5: Advanced Features
- LangGraph agents
- Revision system
- Evaluation system
- Parent dashboard
- Multi-subject support

## 🤝 Development Guidelines

### Code Quality
- Write clean, documented code
- Follow TypeScript/Python type hints
- Use meaningful variable names
- Keep functions small and focused

### Git Workflow
- Create feature branches
- Write descriptive commit messages
- Review code before merging
- Keep main branch stable

### Architecture Principles
- Separation of concerns
- DRY (Don't Repeat Yourself)
- SOLID principles
- API-first design

## 📚 Documentation

### Phase 1 Documentation
- `PHASE1_COMPLETE.md` - Phase 1 features
- `SETUP.md` - Detailed setup guide
- `ARCHITECTURE.md` - System architecture

### Phase 2 Documentation (NEW!)
- `PHASE2_COMPLETE.md` - Phase 2 features
- `PHASE2_SETUP.md` - RAG setup guide
- `PHASE2_SUMMARY.md` - Delivery summary
- `backend/README_PHASE2.md` - Technical reference

## 📝 License

Proprietary - AI Study Companion

## 👥 Contributors

Development Team - Phase 1 & 2 Implementation

## 📞 Support

For issues or questions:
1. Check documentation in `/backend/README.md` and `/frontend/README.md`
2. Review API docs at `/api/v1/docs`
3. Check browser console for frontend errors
4. Review backend logs for API errors

---

**Phase 1 Complete** ✅ | **Phase 2 Complete** ✅ | **Next: Phase 3 Development** 🚀

### 🎉 What's New in Phase 2?

**AI Tutor is now LIVE!**

- Chat with an AI tutor about Social Studies
- Get accurate answers from textbooks
- See source citations for every answer
- Zero hallucinations - only textbook content!

**Quick Start for Phase 2:**
1. Get Gemini API key
2. Place PDFs in `backend/data/`
3. Run: `python app/rag/ingestion/ingest_all.py`
4. Start chatting at `/dashboard/social/chat`

See `PHASE2_SETUP.md` for complete instructions!
