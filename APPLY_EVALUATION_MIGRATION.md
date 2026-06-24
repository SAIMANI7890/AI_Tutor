# Apply Evaluation Module Migration

## Quick Start Guide

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Verify Current Migration Status
```bash
alembic current
```
Expected output: Should show revision `006` (or earlier)

### Step 3: Check Migration History
```bash
alembic history
```
You should see migration `007` listed.

### Step 4: Apply Migration
```bash
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade 006 -> 007, Create evaluations table
```

### Step 5: Verify Migration Applied
```bash
alembic current
```
Expected output: Should now show revision `007`

### Step 6: Verify Table Creation (Optional)
Connect to PostgreSQL and verify:
```sql
-- Check table exists
\dt evaluations

-- Check table structure
\d evaluations

-- Check indexes
\di evaluations*

-- Check constraints
\d+ evaluations
```

---

## Rollback (If Needed)

### Rollback to Previous Version
```bash
alembic downgrade -1
```

This will:
- Drop the evaluations table
- Drop all indexes
- Remove all constraints

### Verify Rollback
```bash
alembic current
```
Should show revision `006`

---

## Troubleshooting

### Issue: "Can't locate revision identified by '007'"
**Solution**: The migration file might not be in the versions directory. Verify:
```bash
ls alembic/versions/007_create_evaluations_table.py
```

### Issue: Foreign key constraint fails
**Solution**: Ensure these tables exist:
- users
- tests
- test_questions

Run earlier migrations if needed:
```bash
alembic upgrade head
```

### Issue: "Target database is not up to date"
**Solution**: Apply all pending migrations:
```bash
alembic upgrade head
```

### Issue: PostgreSQL connection error
**Solution**: 
1. Check `.env` file has correct DATABASE_URL
2. Verify PostgreSQL is running
3. Test connection manually

---

## Environment Variables Required

Ensure your `.env` file has:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

---

## Post-Migration Verification

### Test in Python
```python
from app.db.session import SessionLocal
from app.models.evaluation import Evaluation

# Create session
db = SessionLocal()

# Query evaluations table (should be empty)
count = db.query(Evaluation).count()
print(f"Evaluations count: {count}")  # Should print: 0

db.close()
```

---

## Migration File Location
`backend/alembic/versions/007_create_evaluations_table.py`

## Related Documentation
- Full implementation guide: `PHASE_7A_EVALUATION_DATABASE_LAYER.md`
- Architecture overview: `ARCHITECTURE.md`

---

**Status**: Ready to apply migration ✅
