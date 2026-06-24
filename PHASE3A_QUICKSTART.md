# 🚀 Phase 3A: Quick Start Guide

## Get Started in 5 Minutes

---

## Step 1: Apply Database Migration ⏱️ 30 seconds

```bash
cd backend
python -m alembic upgrade head
```

**Expected output:**
```
INFO [alembic.runtime.migration] Running upgrade 002 -> 003, create study plan tables
```

---

## Step 2: Run Tests ⏱️ 1 minute

```bash
# Run all tests
pytest tests/study_planner/ -v

# Or run specific tests
pytest tests/study_planner/test_planner_service.py -v
pytest tests/study_planner/test_chapters.py -v
```

**Expected:** 55+ tests passing ✅

---

## Step 3: Run Examples ⏱️ 1 minute

```bash
python -m app.study_planner.example_usage
```

**You'll see:**
- 5 working examples
- Generated study plans
- Algorithm demonstrations

---

## Step 4: Try It Yourself ⏱️ 2 minutes

Create a file `test_planner.py`:

```python
from datetime import date, timedelta
from app.study_planner.services.planner_service import planner_service

# Generate a study plan
exam_date = date.today() + timedelta(days=30)
plan = planner_service.generate_study_plan(
    exam_date=exam_date,
    daily_study_hours=3.0,
    selected_chapter_ids=[1, 2, 11]  # French Rev, Industrial Rev, Climate
)

# Print results
print(f"✅ Plan generated!")
print(f"Total Days: {plan.total_days}")
print(f"Study Days: {len([d for d in plan.days if d.activity_type.value == 'Study'])}")

# Show first 5 days
print("\nFirst 5 Days:")
for day in plan.days[:5]:
    activity = day.activity_type.value
    chapter = day.chapter_name or "N/A"
    print(f"  Day {day.day_number}: {activity} - {chapter} ({day.allocated_hours}h)")
```

Run it:
```bash
python test_planner.py
```

---

## ✅ You're Done!

The study planner foundation is working. You can now:

### Explore the Code
- `app/study_planner/config/chapters.py` - 40 chapters configured
- `app/study_planner/services/planner_service.py` - Core algorithm
- `app/study_planner/schemas/study_plan.py` - Data schemas
- `app/models/study_plan.py` - Database models

### Read Documentation
- `PHASE3A_COMPLETE.md` - Full documentation
- `app/study_planner/example_usage.py` - 5 examples

### Next Steps
- Integrate with your application
- Build APIs (Phase 3B)
- Build frontend (Phase 3C)

---

## 🎯 Quick Reference

### Generate a Plan
```python
from app.study_planner.services.planner_service import planner_service
from datetime import date, timedelta

plan = planner_service.generate_study_plan(
    exam_date=date.today() + timedelta(days=30),
    daily_study_hours=3.0,
    selected_chapter_ids=[1, 2, 11]
)
```

### Get Plan Summary
```python
summary = planner_service.get_plan_summary(plan)
print(f"Study Days: {summary['study_days']}")
print(f"Revision Days: {summary['revision_days']}")
print(f"Mock Tests: {summary['mock_test_days']}")
```

### Browse Chapters
```python
from app.study_planner.config.chapters import (
    get_all_chapters,
    get_chapters_by_category,
    get_chapter_by_id
)

# Get all chapters
all_chapters = get_all_chapters()

# Get by category
history_chapters = get_chapters_by_category("History")

# Get specific chapter
chapter = get_chapter_by_id(1)
```

---

## 🐛 Troubleshooting

### Migration Fails
```
Error: revision 002 not found
```
**Solution:** Run previous migrations first
```bash
python -m alembic upgrade head
```

### Tests Fail
```
ModuleNotFoundError: No module named 'app'
```
**Solution:** Run from backend directory
```bash
cd backend
pytest tests/study_planner/ -v
```

### Import Errors
```
ImportError: cannot import name 'planner_service'
```
**Solution:** Ensure you're in backend directory and Python path is correct

---

## 📊 What You Built

✅ Database Models (2 tables)  
✅ Chapter Configuration (40 chapters)  
✅ Scheduling Service (intelligent algorithm)  
✅ Validation Schemas (type-safe)  
✅ Unit Tests (55+ tests)  
✅ Database Migration (ready to apply)  
✅ Example Usage (5 examples)  

**Total:** ~2,000 lines of production-ready code

---

## 🎉 Success!

You now have a working study planner foundation that can:
- Generate realistic study schedules
- Prioritize hard chapters first
- Insert revision days automatically
- Insert mock tests automatically
- Validate inputs and provide warnings
- Handle edge cases gracefully

**Ready for Phase 3B: API Integration!**
