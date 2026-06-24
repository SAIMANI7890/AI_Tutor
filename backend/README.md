# AI Study Companion - Backend

FastAPI backend for the AI Study Companion application.

## Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Primary database
- **Alembic**: Database migrations
- **JWT**: Authentication
- **Bcrypt**: Password hashing

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   └── auth.py       # Authentication endpoints
│   │   │   └── router.py         # Main API router
│   │   └── dependencies.py       # API dependencies
│   ├── core/
│   │   ├── config.py             # App configuration
│   │   └── security.py           # Security utilities
│   ├── db/
│   │   ├── base.py               # Base model
│   │   └── session.py            # Database session
│   ├── models/
│   │   └── user.py               # User model
│   ├── schemas/
│   │   ├── response.py           # Standard responses
│   │   └── user.py               # User schemas
│   ├── services/
│   │   └── user_service.py       # User business logic
│   └── main.py                   # Application entry point
├── alembic/                      # Database migrations
├── .env.example                  # Environment variables template
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Setup Instructions

### Prerequisites

- Python 3.12+
- PostgreSQL 14+
- pip or virtualenv

### Installation

1. **Create virtual environment:**

```bash
python -m venv venv
```

2. **Activate virtual environment:**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Setup PostgreSQL:**

Create a PostgreSQL database:

```sql
CREATE DATABASE ai_study_companion;
```

5. **Configure environment:**

Copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

Edit `.env` and update:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/ai_study_companion
SECRET_KEY=your-secret-key-min-32-characters-long
```

Generate a secure SECRET_KEY:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

6. **Initialize database:**

```bash
alembic upgrade head
```

Or if you're not using Alembic migrations, the tables will be created automatically on first run.

### Running the Server

**Development mode:**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode:**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## API Endpoints

### Authentication

#### Register User
```
POST /api/v1/auth/register
Content-Type: application/json

{
  "full_name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "confirm_password": "SecurePass123"
}
```

#### Login
```
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

#### Get Current User
```
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

#### Update Profile
```
PUT /api/v1/auth/me
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "full_name": "Jane Doe"
}
```

## Database Schema

### Users Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | PRIMARY KEY |
| full_name | String(255) | NOT NULL |
| email | String(255) | UNIQUE, NOT NULL, INDEXED |
| password_hash | String(255) | NOT NULL |
| created_at | DateTime | DEFAULT NOW() |
| updated_at | DateTime | DEFAULT NOW(), ON UPDATE NOW() |

## Testing

To test the API, use the interactive docs at `/api/v1/docs` or use tools like:
- Postman
- curl
- httpie

Example curl request:

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

## Deployment

### Render / Railway

1. Create a new Web Service
2. Connect your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables from `.env`
6. Deploy!

## Security

- Passwords are hashed using bcrypt
- JWT tokens expire after 24 hours (configurable)
- CORS is configured for frontend origins
- SQL injection protection via SQLAlchemy ORM
- Input validation using Pydantic

## Future Enhancements

Phase 2+:
- Study planner endpoints
- Examination generation
- RAG integration
- AI tutor chat
- Progress tracking

## License

Proprietary - AI Study Companion
