# 🗺️ AI Study Companion - Project Map

## 📁 Complete File Structure

```
ai-study-companion/
│
├── 📄 README.md                    # Main project documentation
├── 📄 QUICKSTART.md                # 10-minute setup guide
├── 📄 SETUP.md                     # Detailed setup instructions
├── 📄 ARCHITECTURE.md              # System design & architecture
├── 📄 PHASE1_COMPLETE.md           # Phase 1 completion report
├── 📄 PROJECT_MAP.md               # This file
│
├── 🔧 backend/                     # FastAPI Backend
│   ├── 📄 README.md                # Backend documentation
│   ├── 📄 requirements.txt         # Python dependencies
│   ├── 📄 .env.example             # Environment template
│   ├── 📄 .gitignore               # Git ignore rules
│   ├── 📄 alembic.ini              # Alembic configuration
│   │
│   ├── 📁 alembic/                 # Database migrations
│   │   ├── 📄 env.py               # Migration environment
│   │   └── 📄 script.py.mako       # Migration template
│   │
│   └── 📁 app/                     # Application code
│       ├── 📄 __init__.py
│       ├── 📄 main.py              # FastAPI app entry point
│       │
│       ├── 📁 api/                 # API layer
│       │   ├── 📄 __init__.py
│       │   ├── 📄 dependencies.py  # API dependencies
│       │   └── 📁 v1/              # API version 1
│       │       ├── 📄 __init__.py
│       │       ├── 📄 router.py    # Main API router
│       │       └── 📁 endpoints/   # API endpoints
│       │           ├── 📄 __init__.py
│       │           └── 📄 auth.py  # Auth endpoints
│       │
│       ├── 📁 core/                # Core utilities
│       │   ├── 📄 __init__.py
│       │   ├── 📄 config.py        # App configuration
│       │   └── 📄 security.py      # Security functions
│       │
│       ├── 📁 db/                  # Database layer
│       │   ├── 📄 __init__.py
│       │   ├── 📄 base.py          # Base model
│       │   └── 📄 session.py       # DB session
│       │
│       ├── 📁 models/              # SQLAlchemy models
│       │   ├── 📄 __init__.py
│       │   └── 📄 user.py          # User model
│       │
│       ├── 📁 schemas/             # Pydantic schemas
│       │   ├── 📄 __init__.py
│       │   ├── 📄 user.py          # User schemas
│       │   └── 📄 response.py      # Response schemas
│       │
│       └── 📁 services/            # Business logic
│           ├── 📄 __init__.py
│           └── 📄 user_service.py  # User service
│
└── 💻 frontend/                    # Next.js Frontend
    ├── 📄 README.md                # Frontend documentation
    ├── 📄 package.json             # Node dependencies
    ├── 📄 tsconfig.json            # TypeScript config
    ├── 📄 next.config.js           # Next.js config
    ├── 📄 tailwind.config.ts       # Tailwind config
    ├── 📄 postcss.config.js        # PostCSS config
    ├── 📄 .env.local.example       # Environment template
    ├── 📄 .gitignore               # Git ignore rules
    │
    └── 📁 src/                     # Source code
        ├── 📁 app/                 # Next.js App Router
        │   ├── 📄 layout.tsx       # Root layout
        │   ├── 📄 page.tsx         # Home page
        │   ├── 📄 globals.css      # Global styles
        │   │
        │   ├── 📁 login/           # Login page
        │   │   └── 📄 page.tsx
        │   │
        │   ├── 📁 register/        # Registration page
        │   │   └── 📄 page.tsx
        │   │
        │   ├── 📁 dashboard/       # Dashboard page
        │   │   └── 📄 page.tsx
        │   │
        │   └── 📁 profile/         # Profile page
        │       └── 📄 page.tsx
        │
        ├── 📁 components/          # React components
        │   ├── 📄 providers.tsx    # App providers
        │   │
        │   ├── 📁 ui/              # UI components
        │   │   ├── 📄 button.tsx
        │   │   ├── 📄 card.tsx
        │   │   ├── 📄 input.tsx
        │   │   ├── 📄 label.tsx
        │   │   └── 📄 dropdown-menu.tsx
        │   │
        │   └── 📁 layout/          # Layout components
        │       ├── 📄 dashboard-header.tsx
        │       └── 📄 protected-route.tsx
        │
        ├── 📁 contexts/            # React contexts
        │   └── 📄 auth.context.tsx # Auth context
        │
        └── 📁 lib/                 # Library code
            ├── 📄 utils.ts         # Utility functions
            ├── 📄 api.ts           # Axios instance
            ├── 📄 types.ts         # TypeScript types
            │
            └── 📁 services/        # API services
                └── 📄 auth.service.ts
```

## 🎯 Key Files Explained

### Documentation Files (Root)

| File | Purpose | When to Read |
|------|---------|--------------|
| `README.md` | Main overview | First time |
| `QUICKSTART.md` | Fast setup | To get started quickly |
| `SETUP.md` | Detailed setup | Having setup issues |
| `ARCHITECTURE.md` | System design | Understanding architecture |
| `PHASE1_COMPLETE.md` | Features list | Checking what's done |
| `PROJECT_MAP.md` | This file | Finding files |

### Backend Core Files

| File | Purpose | Contains |
|------|---------|----------|
| `main.py` | App entry | FastAPI app, CORS, routes |
| `config.py` | Settings | Environment vars, config |
| `security.py` | Auth utils | JWT, password hashing |
| `user.py` (model) | Database | User table definition |
| `user.py` (schema) | Validation | Request/response schemas |
| `auth.py` | API routes | Login, register endpoints |
| `user_service.py` | Business logic | User operations |

### Frontend Core Files

| File | Purpose | Contains |
|------|---------|----------|
| `layout.tsx` | Root layout | HTML structure, providers |
| `page.tsx` (app) | Home | Redirect to login |
| `page.tsx` (login) | Login page | Login form |
| `page.tsx` (register) | Register page | Registration form |
| `page.tsx` (dashboard) | Dashboard | Main app interface |
| `page.tsx` (profile) | Profile | User profile page |
| `auth.context.tsx` | Auth state | User state management |
| `auth.service.ts` | API calls | Auth API functions |
| `dashboard-header.tsx` | Header | App header component |

## 🔗 File Relationships

### Backend Flow
```
main.py
  ↓ includes
router.py (v1)
  ↓ includes
auth.py (endpoints)
  ↓ uses
user_service.py
  ↓ uses
user.py (model)
  ↓ connects to
PostgreSQL Database
```

### Frontend Flow
```
page.tsx (root)
  ↓ redirects to
page.tsx (login)
  ↓ uses
auth.context.tsx
  ↓ calls
auth.service.ts
  ↓ uses
api.ts (axios)
  ↓ calls
Backend API
```

## 📊 Component Dependencies

### Backend Dependencies
```
FastAPI
├── SQLAlchemy → PostgreSQL
├── Pydantic → Validation
├── Python-Jose → JWT
├── Passlib → Bcrypt
└── Alembic → Migrations
```

### Frontend Dependencies
```
Next.js 15
├── React 18 → UI
├── Tailwind CSS → Styling
├── shadcn/ui → Components
├── React Hook Form → Forms
├── Zod → Validation
├── TanStack Query → Data fetching
└── Axios → HTTP client
```

## 🗄️ Database Schema

```sql
users
├── id (PK)
├── full_name
├── email (UNIQUE, INDEXED)
├── password_hash
├── created_at
└── updated_at
```

## 🔐 Authentication Flow

```
1. User submits form
   ↓
2. Frontend validates (Zod)
   ↓
3. API call (Axios)
   ↓
4. Backend validates (Pydantic)
   ↓
5. Service layer processes
   ↓
6. Database operation
   ↓
7. JWT token generated
   ↓
8. Token returned to frontend
   ↓
9. Token stored (localStorage)
   ↓
10. User redirected to dashboard
```

## 🎨 UI Component Hierarchy

```
layout.tsx (Root)
└── Providers
    └── AuthProvider
        ├── Login Page
        │   └── Card
        │       ├── Input (email)
        │       ├── Input (password)
        │       └── Button
        │
        ├── Register Page
        │   └── Card
        │       ├── Input (name)
        │       ├── Input (email)
        │       ├── Input (password)
        │       ├── Input (confirm)
        │       └── Button
        │
        ├── Dashboard Page
        │   ├── DashboardHeader
        │   │   └── DropdownMenu
        │   └── Card (Social Studies)
        │       └── Button
        │
        └── Profile Page
            ├── DashboardHeader
            └── Card
                ├── Input (name)
                ├── Input (email - disabled)
                └── Button (Edit/Save)
```

## 📍 Important Directories

### Where to Add...

**New API Endpoint**
- `backend/app/api/v1/endpoints/`
- Update `router.py`

**New Database Model**
- `backend/app/models/`
- Import in `db/base.py`

**New Service Function**
- `backend/app/services/`

**New Frontend Page**
- `frontend/src/app/[route]/page.tsx`

**New UI Component**
- `frontend/src/components/ui/`

**New React Component**
- `frontend/src/components/[feature]/`

**New API Service**
- `frontend/src/lib/services/`

## 🔍 Quick File Finder

Need to find where...

| Task | File Location |
|------|---------------|
| Change API URL | `frontend/.env.local` |
| Change database | `backend/.env` |
| Add new route | `backend/app/api/v1/router.py` |
| Add new page | `frontend/src/app/[name]/page.tsx` |
| Change colors | `frontend/tailwind.config.ts` |
| Update user model | `backend/app/models/user.py` |
| Auth logic | `frontend/src/contexts/auth.context.tsx` |
| Password hashing | `backend/app/core/security.py` |
| Form validation | Component using `zod` schema |
| API response format | `backend/app/schemas/response.py` |

## 🧩 Module Purposes

### Backend Modules

- `api/` - HTTP endpoints
- `core/` - Configuration & utilities
- `db/` - Database connection
- `models/` - Database tables
- `schemas/` - Data validation
- `services/` - Business logic

### Frontend Modules

- `app/` - Pages & routes
- `components/` - Reusable UI
- `contexts/` - Global state
- `lib/` - Utilities & services

## 📦 Package Management

### Backend
```bash
# Install all
pip install -r requirements.txt

# Add new package
pip install package-name
pip freeze > requirements.txt
```

### Frontend
```bash
# Install all
npm install

# Add new package
npm install package-name
```

## 🎓 Learning Path

### New to Project?
1. Read `README.md`
2. Follow `QUICKSTART.md`
3. Read `ARCHITECTURE.md`
4. Explore code in this order:
   - Backend `main.py`
   - Backend `auth.py`
   - Frontend `auth.context.tsx`
   - Frontend `login/page.tsx`

### Adding Features?
1. Check `ARCHITECTURE.md`
2. Find relevant service in `PROJECT_MAP.md`
3. Add backend endpoint
4. Add frontend UI
5. Connect with service

## 🚀 Deployment Files

### Backend (Render/Railway)
- `requirements.txt` - Dependencies
- `.env` - Configuration
- `main.py` - Entry point

### Frontend (Vercel)
- `package.json` - Dependencies
- `.env.local` - Configuration
- `next.config.js` - Build config

## 📈 Project Stats

- **Total Files**: 50+
- **Lines of Code**: ~5,500
- **Backend Files**: 20+
- **Frontend Files**: 25+
- **Documentation**: 6 files
- **Setup Time**: ~10 minutes
- **Tech Stack**: 15+ technologies

---

**Use this map to navigate the project efficiently!** 🗺️
