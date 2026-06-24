# ⚡ Enhanced Prompts - Quick Reference Card

**Version**: 2.0 | **Date**: June 15, 2026

---

## 🎯 KEY FEATURES

```
✅ Zero Hallucination     ✅ Bloom's Taxonomy
✅ 30/50/20 Difficulty   ✅ Source Attribution
✅ JSON Output           ✅ Educational Quality
```

---

## 📋 UPDATED FILES

```bash
backend/app/services/question_generation/
├── prompts.py              ✅ ENHANCED (V2.0)
├── enhanced_prompts.py     ✅ NEW (Alternative)
└── quality_control.py      ✅ NEW (Validation)
```

---

## 🔄 MIGRATION STEPS

### Option 1: Use Enhanced Prompts (Recommended)

```python
# In generator.py, change import:
from app.services.question_generation.enhanced_prompts import (
    select_enhanced_prompt,
    format_context_for_assessment
)

# Update generation:
formatted_context = format_context_for_assessment(chunks, category)
prompt = select_enhanced_prompt(question_type, formatted_context, category, count)
```

### Option 2: Keep Existing, Enhanced

Your existing `prompts.py` is now V2.0 enhanced!  
No code changes needed - just restart server.

---

## 📊 DIFFICULTY DISTRIBUTION

```
┌──────────────────────────────────────┐
│  30% Easy    →  Remember/Understand  │
│  50% Medium  →  Understand/Apply     │
│  20% Hard    →  Apply/Analyze        │
└──────────────────────────────────────┘
```

---

## 🎓 BLOOM'S TAXONOMY QUICK MAP

| Level | Verbs | Question Types |
|-------|-------|----------------|
| **Remember** | Define, List, Name | MCQ (Easy), Fill Blanks |
| **Understand** | Explain, Describe | All types (Easy-Medium) |
| **Apply** | Apply, Solve, Use | MCQ/Short Answer (Medium-Hard) |
| **Analyze** | Analyze, Compare | Long Answer (Hard) |

---

## 📝 JSON SCHEMA (All Types)

```json
{
  "questions": [{
    "question_text": "string (10-500 chars)",
    "correct_answer": "string (MCQ/Fill)",
    "model_answer": "string (Short/Long)",
    "options": ["A", "B", "C", "D"],  // MCQ only
    "difficulty": "Easy|Medium|Hard",
    "category": "History|Geography|Politics|Economics",
    "source_document": "filename.pdf",
    "source_page": 123
  }]
}
```

---

## ✅ VALIDATION CHECKLIST

```bash
□ All questions generated (count matches)
□ Difficulty: ~30% Easy, ~50% Medium, ~20% Hard
□ Every question has source_document + source_page
□ JSON format valid
□ No duplicates (similarity < 75%)
□ Answers in source material
```

---

## 🔍 TEST COMMANDS

```bash
# Generate MCQ test
curl -X POST http://localhost:8000/api/v1/exams/generate \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"categories":["History"],"question_type":"MCQ","question_count":10}'

# Check quality
python -c "
from app.services.question_generation.quality_control import calculate_quality_metrics
metrics = calculate_quality_metrics(questions)
print(f'Quality: {metrics[\"quality_score\"]}/100')
"
```

---

## 🐛 TROUBLESHOOTING

### Issue: Hallucinated Content
**Fix**: Check source validation in quality_control.py

### Issue: Wrong Difficulty Distribution
**Fix**: Prompts now explicitly specify count per level

### Issue: Duplicate Questions
**Fix**: Use similarity check in quality_control.py

### Issue: JSON Parse Error
**Fix**: Enhanced prompts include "no markdown" reminder

---

## 📈 QUALITY TARGETS

| Metric | Target |
|--------|--------|
| Source Attribution | 100% |
| Hallucination Rate | <5% |
| Difficulty Distribution | 30/50/20 ±10% |
| JSON Validity | 100% |

---

## 🚀 QUICK START

```python
# 1. Import enhanced prompts
from app.services.question_generation.prompts import (
    create_mcq_generation_prompt
)

# 2. Format context
context = format_context_with_sources(rag_chunks)

# 3. Generate prompt
prompt = create_mcq_generation_prompt(context, "History", 10)

# 4. Call LLM
response = llm.invoke(prompt)

# 5. Validate
from app.services.question_generation.quality_control import (
    QuestionQualityController
)
qc = QuestionQualityController()
valid_questions, errors = qc.validate_question_batch(
    questions, rag_chunks, 10
)
```

---

## 📚 DOCUMENTATION

- **Full Guide**: `ENHANCED_PROMPTS_IMPLEMENTATION_GUIDE.md`
- **Code**: `app/services/question_generation/enhanced_prompts.py`
- **Validation**: `app/services/question_generation/quality_control.py`

---

## ✨ WHAT'S NEW IN V2.0

1. ✅ Visual emphasis on source fidelity (═══, ⚠️, ❌, ✓)
2. ✅ Explicit Bloom's Taxonomy levels
3. ✅ Strict difficulty distribution (30/50/20)
4. ✅ 3 examples per difficulty level
5. ✅ Enhanced validation checklist
6. ✅ Better structured prompts
7. ✅ Quality control module
8. ✅ Comprehensive documentation

---

**Ready to use!** Just restart your server to apply changes.

**Questions?** Check `ENHANCED_PROMPTS_IMPLEMENTATION_GUIDE.md`
