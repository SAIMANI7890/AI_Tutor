# AI Study Companion - Architecture Documentation

## 📐 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                      (Browser / Mobile)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (Next.js 15)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │   Pages      │  │  Components  │  │   State Management  │  │
│  │  - Login     │  │  - UI        │  │   - Auth Context    │  │
│  │  - Register  │  │  - Layout    │  │   - TanStack Query  │  │
│  │  - Dashboard │  │  - Forms     │  │                     │  │
│  │  - Profile   │  │              │  │                     │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Services & API Client                       │  │
│  │              - Axios with interceptors                   │  │
│  │              - JWT token management                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST API / JWT
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Layer (v1)                        │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │  │
│  │  │   Auth     │  │  Future    │  │   Middleware     │   │  │
│  │  │ Endpoints  │  │  Features  │  │   - CORS         │   │  │
│  │  │            │  │            │  │   - Error Handle │   │  │
│  │  └────────────┘  └────────────┘  └──────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Business Logic Layer                        │  │
│  │  ┌────────────────┐  ┌────────────────┐                 │  │
│  │  │ User Service   │  │ Future Services│                 │  │
│  │  │ - Create       │  │                │                 │  │
│  │  │ - Auth         │  │                │                 │  │
│  │  │ - Update       │  │                │                 │  │
│  │  └────────────────┘  └────────────────┘                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 Data Access Layer                        │  │
│  │  ┌────────────┐  ┌────────────┐  ┌─────────────────┐    │  │
│  │  │ SQLAlchemy │  │   Models   │  │    Schemas      │    │  │
│  │  │    ORM     │  │  - User    │  │  - Validation   │    │  │
│  │  │            │  │  - Future  │  │  - Serialization│    │  │
│  │  └────────────┘  └────────────┘  └─────────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ SQL Queries
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATABASE (PostgreSQL)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │  users       │  │   Future     │  │    Indexes          │  │
│  │  - id        │  │   Tables     │  │    - email          │  │
│  │  - full_name │  │              │  │    - created_at     │  │
│  │  - email     │  │              │  │                     │  │
│  │  - password  │  │              │  │                     │  │
│  │  - timestamps│  │              │  │                     │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 🏗 Architecture Patterns

### 1. **Clean Architecture**

The application follows clean architecture principles with clear separation of concerns:

#### Frontend Layers:
1. **Presentation Layer** - React components, pages
2. **Application Layer** - Contexts, hooks, state management
3. **Domain Layer** - Types, interfaces, business logic
4. **Infrastructure Layer** - API clients, services

#### Backend Layers:
1. **API Layer** - FastAPI routes, endpoints
2. **Service Layer** - Business logic, use cases
3. **Data Access Layer** - SQLAlchemy models, repositories
4. **Infrastructure Layer** - Database, external services

### 2. **RESTful API Design**

- Resource-based URLs
- HTTP methods (GET, POST, PUT, DELETE)
- Status codes
- JSON payloads
- Versioned API (`/api/v1/`)

### 3. **JWT Authentication Flow**

```
┌──────────┐                          ┌──────────┐
│  Client  │                          │  Server  │
└────┬─────┘                          └────┬─────┘
     │                                     │
     │  1. POST /auth/register             │
     │  (email, password, name)            │
     │────────────────────────────────────>│
     │                                     │
     │  2. Hash password & create user     │
     │                                     │
     │  3. Generate JWT token              │
     │                                     │
     │  4. Return token + user data        │
     │<────────────────────────────────────│
     │                                     │
     │  5. Store token in localStorage     │
     │                                     │
     │  6. GET /auth/me                    │
     │  Authorization: Bearer <token>      │
     │────────────────────────────────────>│
     │                                     │
     │  7. Verify token & decode           │
     │                                     │
     │  8. Return user data                │
     │<────────────────────────────────────│
     │                                     │
```

## 🗂 Directory Structure Explained

### Backend Structure

```
backend/
├── app/
│   ├── api/                    # API layer
│   │   ├── v1/                 # API version 1
│   │   │   ├── endpoints/      # Route handlers
│   │   │   │   └── auth.py     # Authentication endpoints
│   │   │   └── router.py       # Main router
│   │   └── dependencies.py     # Shared dependencies
│   │
│   ├── core/                   # Core utilities
│   │   ├── config.py           # Configuration management
│   │   └── security.py         # Security utilities
│   │
│   ├── db/                     # Database layer
│   │   ├── base.py             # Base model class
│   │   └── session.py          # Database session
│   │
│   ├── models/                 # SQLAlchemy models
│   │   └── user.py             # User model
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py             # User schemas
│   │   └── response.py         # Response schemas
│   │
│   ├── services/               # Business logic
│   │   └── user_service.py     # User service
│   │
│   └── main.py                 # Application entry
│
├── alembic/                    # Database migrations
│   ├── versions/               # Migration files
│   ├── env.py                  # Alembic config
│   └── script.py.mako          # Migration template
│
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
└── README.md                   # Backend docs
```

**Key Design Decisions:**

- **API Versioning**: `/api/v1/` allows future version changes
- **Service Layer**: Business logic separated from routes
- **Dependency Injection**: FastAPI's Depends() for clean code
- **Schema Validation**: Pydantic for request/response validation

### Frontend Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── login/              # Login page
│   │   ├── register/           # Register page
│   │   ├── dashboard/          # Dashboard page
│   │   ├── profile/            # Profile page
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   └── globals.css         # Global styles
│   │
│   ├── components/             # React components
│   │   ├── ui/                 # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── label.tsx
│   │   │   └── dropdown-menu.tsx
│   │   ├── layout/             # Layout components
│   │   │   ├── dashboard-header.tsx
│   │   │   └── protected-route.tsx
│   │   └── providers.tsx       # Context providers
│   │
│   ├── contexts/               # React contexts
│   │   └── auth.context.tsx    # Auth context
│   │
│   └── lib/                    # Utilities
│       ├── services/           # API services
│       │   └── auth.service.ts
│       ├── api.ts              # Axios instance
│       ├── types.ts            # TypeScript types
│       └── utils.ts            # Utility functions
│
├── public/                     # Static files
├── .env.local.example          # Environment template
├── next.config.js              # Next.js config
├── tailwind.config.ts          # Tailwind config
├── tsconfig.json               # TypeScript config
├── package.json                # Dependencies
└── README.md                   # Frontend docs
```

**Key Design Decisions:**

- **App Router**: Next.js 15's modern routing
- **Component Library**: shadcn/ui for consistency
- **Context API**: Authentication state management
- **Service Layer**: API calls abstracted from components
- **Type Safety**: TypeScript for all files

## 🔐 Security Architecture

### Authentication & Authorization

1. **Password Security**
   - Bcrypt hashing (12 rounds)
   - Salted passwords
   - No plain text storage

2. **JWT Token Security**
   - HS256 algorithm
   - 24-hour expiration
   - Stored in localStorage
   - Bearer token in headers

3. **API Security**
   - CORS configuration
   - Input validation
   - SQL injection prevention (ORM)
   - XSS protection

### Data Flow Security

```
User Input → Validation (Zod) → API Call (Axios) 
→ Backend Validation (Pydantic) → Business Logic 
→ Database (SQLAlchemy ORM) → Response → Frontend
```

## 📊 Data Models

### User Model

```python
class User(Base):
    __tablename__ = "users"
    
    id: int (PK)
    full_name: str(255)
    email: str(255) [UNIQUE, INDEXED]
    password_hash: str(255)
    created_at: datetime [DEFAULT: NOW()]
    updated_at: datetime [DEFAULT: NOW(), AUTO UPDATE]
```

**Relationships (Future):**
- `study_plans` - One-to-Many
- `examinations` - One-to-Many
- `progress_records` - One-to-Many

## 🚀 Scalability Considerations

### Current Phase 1 Architecture
- Single server deployment
- PostgreSQL for relational data
- JWT for stateless authentication

### Future Scaling (Phase 2+)

1. **Horizontal Scaling**
   - Load balancer
   - Multiple backend instances
   - Session store (Redis)

2. **Database Scaling**
   - Read replicas
   - Connection pooling
   - Query optimization

3. **Caching Layer**
   - Redis for session data
   - API response caching
   - CDN for static assets

4. **Microservices (Phase 3+)**
   - Auth service
   - Study planner service
   - AI service (RAG/LangGraph)
   - Examination service

## 🧪 Testing Strategy

### Backend Testing
- Unit tests (pytest)
- Integration tests (TestClient)
- API endpoint tests
- Database tests

### Frontend Testing
- Component tests (Jest)
- Integration tests
- E2E tests (Playwright)

### Test Coverage Goals
- Backend: >80%
- Frontend: >70%

## 📈 Performance Optimization

### Backend
- Database indexing
- Query optimization
- Connection pooling
- Async operations (FastAPI)

### Frontend
- Code splitting (Next.js)
- Image optimization
- Lazy loading
- Bundle size optimization

## 🔄 CI/CD Pipeline (Future)

```
Developer Push → GitHub → CI Tests → Build → 
Deploy to Staging → Manual Approval → 
Deploy to Production → Health Checks
```

## 📚 Technology Choices Rationale

### Why Next.js 15?
- Server-side rendering
- App Router for modern patterns
- Great developer experience
- Vercel deployment integration

### Why FastAPI?
- Modern Python framework
- Async support
- Auto-generated docs
- Type hints support
- Fast performance

### Why PostgreSQL?
- ACID compliance
- Mature ecosystem
- Great for relational data
- JSON support for flexibility

### Why JWT?
- Stateless authentication
- Scalable
- Standard protocol
- Easy to implement

## 🔮 Future Architecture Evolution

### Phase 2: AI Integration
- LangChain for AI workflows
- Vector database (Pinecone/Weaviate)
- OpenAI API integration

### Phase 3: Real-time Features
- WebSocket support
- Real-time notifications
- Live chat with AI tutor

### Phase 4: Analytics
- User behavior tracking
- Progress analytics
- A/B testing framework

---

This architecture provides a solid foundation for growth while maintaining code quality and developer productivity.
