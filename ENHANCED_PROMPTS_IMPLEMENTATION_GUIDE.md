# 🎓 Enhanced Educational Assessment Prompts - Implementation Guide

**Version**: 2.0  
**Date**: June 15, 2026  
**Status**: Production-Ready

---

## 📋 OVERVIEW

This guide documents the enhanced prompt engineering framework for generating high-quality educational assessments that:

✅ **Prevent hallucination** - Strict source fidelity  
✅ **Align with Bloom's Taxonomy** - Cognitive level tracking  
✅ **Calibrate difficulty** - 30% Easy, 50% Medium, 20% Hard  
✅ **Ensure educational quality** - Secondary school appropriate  
✅ **Provide structured output** - Valid JSON with source attribution  

---

## 🎯 KEY IMPROVEMENTS OVER V1

| Aspect | V1 (Original) | V2 (Enhanced) |
|--------|--------------|---------------|
| **Hallucination Prevention** | Basic warning | Multi-layered with visual emphasis |
| **Bloom's Taxonomy** | Not included | Explicit level assignment |
| **Difficulty Distribution** | Not enforced | Strict 30/50/20 ratio |
| **Examples** | 1 per type | 3 per type (Easy/Medium/Hard) |
| **Source Attribution** | Basic | Document + page required |
| **Validation Checklist** | None | Comprehensive checklist |
| **Visual Design** | Plain text | Box borders, symbols, structure |
| **Educational Theory** | Implicit | Explicit Bloom's levels |

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                  PROMPT ENGINEERING FRAMEWORK                │
└─────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  SYSTEM       │   │  CONTEXT      │   │  TASK         │
│  INSTRUCTIONS │   │  FORMATTING   │   │  SPECIFICATION│
└───────────────┘   └───────────────┘   └───────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  EXAMPLES        │
                    │  (Few-Shot)      │
                    └──────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  OUTPUT SCHEMA   │
                    │  (JSON)          │
                    └──────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  VALIDATION      │
                    │  CHECKLIST       │
                    └──────────────────┘
```

---

## 📚 BLOOM'S TAXONOMY MAPPING

### Question Type Distribution

```
┌─────────────────────────────────────────────────────────────┐
│ MCQ (Multiple Choice Questions)                             │
├─────────────────────────────────────────────────────────────┤
│ Easy (30%)    → Remember    (recall facts, definitions)     │
│ Medium (50%)  → Understand  (explain concepts)              │
│ Hard (20%)    → Apply       (scenarios, application)        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ FILL IN THE BLANKS                                          │
├─────────────────────────────────────────────────────────────┤
│ Easy (30%)    → Remember    (basic facts)                   │
│ Medium (50%)  → Understand  (concepts)                      │
│ Hard (20%)    → Understand  (technical terms)               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ SHORT ANSWER (2-3 sentences)                                │
├─────────────────────────────────────────────────────────────┤
│ Easy (30%)    → Understand  (simple explanations)           │
│ Medium (50%)  → Apply       (cause-effect, comparisons)     │
│ Hard (20%)    → Analyze     (complex explanations)          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ LONG ANSWER (5-6 sentences)                                 │
├─────────────────────────────────────────────────────────────┤
│ Easy (30%)    → Understand  (comprehensive descriptions)    │
│ Medium (50%)  → Analyze     (cause-effect, analysis)        │
│ Hard (20%)    → Evaluate    (synthesis, critical thinking)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔒 HALLUCINATION PREVENTION STRATEGY

### Multi-Layer Approach

**Layer 1: Visual Emphasis**
```
═══════════════════════════════════════════════════════════════
CORE INSTRUCTION: SOURCE FIDELITY
═══════════════════════════════════════════════════════════════
⚠️ CRITICAL: Generate questions ONLY from textbook content
❌ FORBIDDEN: External knowledge, assumptions, invented facts
✓ REQUIRED: Every answer explicitly in source text
```

**Layer 2: Context Formatting**
- Clear boundary markers for source material
- Numbered excerpts with attribution
- Visual separation from instructions

**Layer 3: Validation Requirements**
- Mandatory source_document field
- Mandatory source_page field
- Answers must be verifiable

**Layer 4: Examples**
- All examples include source attribution
- Demonstrate expected format

**Layer 5: Checklist**
- Final reminder to check source alignment
- No external knowledge reminder

---

## 📝 JSON OUTPUT SCHEMA

### Standard Format (All Question Types)

```json
{
  "questions": [
    {
      "question_text": "Complete question with proper grammar?",
      "correct_answer": "For MCQ/Fill Blanks",
      "model_answer": "For Short/Long Answer",
      "options": ["A", "B", "C", "D"],  // MCQ only
      "difficulty": "Easy|Medium|Hard",
      "category": "History|Geography|Politics|Economics",
      "source_document": "filename.pdf",
      "source_page": 123
    }
  ]
}
```

### Field Specifications

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `question_text` | string | ✅ | 10-500 chars |
| `correct_answer` | string | MCQ/Fill Blanks | 1-200 chars |
| `model_answer` | string | Short/Long | 30-200 words |
| `options` | array[4] | MCQ only | 4 strings, 1-200 chars each |
| `difficulty` | enum | ✅ | Easy\|Medium\|Hard |
| `category` | string | ✅ | Valid category |
| `source_document` | string | ✅ | Filename from context |
| `source_page` | integer | ✅ | Page number from context |

---

## 🎯 DIFFICULTY CALIBRATION GUIDE

### Easy (30% of questions)

**Cognitive Level**: Remember, Basic Understand  
**Characteristics**:
- Direct factual recall
- Definitions of key terms
- Basic concept explanations
- Straightforward cause-effect
- Well-known facts (capitals, dates, names)

**Verbs**: Define, List, Name, Identify, State, What is...

**MCQ Example**:
```
Q: Who was the first Prime Minister of India?
A: Jawaharlal Nehru
```

---

### Medium (50% of questions)

**Cognitive Level**: Understand, Apply  
**Characteristics**:
- Concept relationships
- Cause-and-effect analysis
- Comparisons and contrasts
- Application to scenarios
- Multi-step reasoning

**Verbs**: Explain, Describe, Compare, Apply, How, Why

**MCQ Example**:
```
Q: What was the main reason for Mughal Empire decline?
A: Weak successors and internal conflicts
```

---

### Hard (20% of questions)

**Cognitive Level**: Apply, Analyze, Evaluate  
**Characteristics**:
- Multi-concept synthesis
- Critical analysis
- Evaluation of significance
- Complex scenarios
- Technical terminology

**Verbs**: Analyze, Evaluate, Examine, Discuss, Assess

**MCQ Example**:
```
Q: If a fundamental right is violated, which remedy is most effective?
A: Writ petition under Article 32
```

---

## 🔄 IMPLEMENTATION WORKFLOW

### Step 1: Context Preparation
```python
from app.services.question_generation.prompts import (
    create_mcq_generation_prompt
)

# Format context with clear boundaries
formatted_context = format_context_with_attribution(rag_chunks)
```

### Step 2: Prompt Selection
```python
# Select appropriate prompt for question type
prompt = create_mcq_generation_prompt(
    context=formatted_context,
    category="History",
    count=10
)
```

### Step 3: LLM Invocation
```python
# Call Gemini with enhanced prompt
response = llm.invoke(prompt)
questions = parse_json_response(response.content)
```

### Step 4: Validation
```python
# Validate against source material
valid_questions = []
for q in questions:
    if validate_source_alignment(q, rag_chunks):
        valid_questions.append(q)
```

### Step 5: Quality Check
```python
# Check difficulty distribution
check_difficulty_distribution(valid_questions)
# Expected: ~30% Easy, ~50% Medium, ~20% Hard
```

---

## ✅ VALIDATION CHECKLIST

### Pre-Generation Checks
- [ ] RAG context retrieved successfully
- [ ] Context formatted with source attribution
- [ ] Category is valid (History/Geography/Politics/Economics)
- [ ] Question count specified (1-10)
- [ ] Question type selected (MCQ/Fill Blanks/Short/Long)

### Post-Generation Checks
- [ ] All requested questions generated
- [ ] JSON format is valid
- [ ] Difficulty distribution: ~30% Easy, ~50% Medium, ~20% Hard
- [ ] All questions have `source_document` and `source_page`
- [ ] No duplicate questions (similarity check)
- [ ] Answers verifiable in source material
- [ ] Question text length 10-500 characters
- [ ] Options (MCQ) are unique and plausible

### Educational Quality Checks
- [ ] Questions test understanding, not just recall
- [ ] Bloom's levels appropriate for difficulty
- [ ] Language appropriate for Class 10 (ages 14-16)
- [ ] Multiple concepts covered
- [ ] No trivial or trick questions
- [ ] Model answers (Short/Long) are structured

---

## 🐛 COMMON ISSUES & SOLUTIONS

### Issue 1: Hallucinated Content

**Symptom**: Answers not found in source material

**Solution**:
```python
# Use stricter validation
def validate_answer_in_source(answer, source_text):
    answer_lower = answer.lower()
    source_lower = source_text.lower()
    
    # Check for exact or high similarity match
    if answer_lower not in source_lower:
        similarity = calculate_similarity(answer, source_text)
        if similarity < 0.5:
            return False, "Answer not in source"
    return True, ""
```

---

### Issue 2: Difficulty Distribution Off-Target

**Symptom**: Too many Easy or Hard questions

**Solution**:
```python
# Explicitly specify in prompt
count_easy = int(count * 0.3)
count_medium = int(count * 0.5)
count_hard = int(count * 0.2)

# Add to prompt:
f"Generate EXACTLY {count_easy} Easy, {count_medium} Medium, {count_hard} Hard"
```

---

### Issue 3: Duplicate Questions

**Symptom**: Similar questions generated

**Solution**:
```python
from difflib import SequenceMatcher

def check_similarity(q1, q2, threshold=0.75):
    ratio = SequenceMatcher(None, q1, q2).ratio()
    return ratio > threshold

# Filter duplicates
unique_questions = []
for q in questions:
    is_duplicate = any(
        check_similarity(q['question_text'], existing['question_text'])
        for existing in unique_questions
    )
    if not is_duplicate:
        unique_questions.append(q)
```

---

### Issue 4: Poor MCQ Distractors

**Symptom**: Obviously wrong options

**Solution**:
- Enhanced prompt emphasizes "plausible distractors"
- Examples show good vs. bad distractors
- Validation checks for option similarity

---

## 📊 QUALITY METRICS

### Target Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Source Attribution | 100% | All questions have source_document |
| Difficulty Distribution | 30/50/20 | ±10% tolerance |
| Bloom's Alignment | 90%+ | Manual review |
| No Hallucinations | 95%+ | Validation checks |
| Question Independence | 100% | Similarity < 75% |
| JSON Validity | 100% | Parse success rate |

### Measurement Code

```python
def calculate_quality_score(questions):
    total_questions = len(questions)
    
    # Source attribution
    sourced = sum(1 for q in questions if q.get('source_document'))
    source_score = (sourced / total_questions) * 100
    
    # Difficulty distribution
    diff_dist = get_difficulty_distribution(questions)
    dist_score = check_distribution_match(diff_dist, {
        "Easy": 0.3, "Medium": 0.5, "Hard": 0.2
    })
    
    # Overall quality
    quality_score = (source_score * 0.4) + (dist_score * 0.6)
    
    return {
        "source_attribution": source_score,
        "difficulty_distribution": diff_dist,
        "overall_quality": quality_score
    }
```

---

## 🚀 DEPLOYMENT CHECKLIST

### Before Deployment
- [ ] Enhanced prompts file created
- [ ] Validation module tested
- [ ] Quality control integrated
- [ ] Example questions generated and reviewed
- [ ] Error handling implemented
- [ ] Logging configured

### Testing
- [ ] Generate 10 MCQ questions - verify quality
- [ ] Generate 10 Fill Blanks - verify quality
- [ ] Generate 5 Short Answer - verify quality
- [ ] Generate 5 Long Answer - verify quality
- [ ] Check difficulty distribution across 100 questions
- [ ] Validate no hallucinations in 50 questions
- [ ] Measure generation time (should be <10s)

### Monitoring
- [ ] Track hallucination rate (target: <5%)
- [ ] Monitor difficulty distribution (target: 30/50/20 ±10%)
- [ ] Track source attribution coverage (target: 100%)
- [ ] Measure user feedback on question quality
- [ ] Log validation failures

---

## 📖 USAGE EXAMPLES

### Example 1: Generate MCQ Questions

```python
from app.services.question_generation.prompts import (
    create_mcq_generation_prompt
)
from langchain_google_genai import ChatGoogleGenerativeAI

# Setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=api_key,
    temperature=0.7
)

# Prepare context
rag_chunks = retriever.retrieve("History topics", top_k=10)
formatted_context = format_context_for_assessment(rag_chunks, "History")

# Generate prompt
prompt = create_mcq_generation_prompt(
    context=formatted_context,
    category="History",
    count=10
)

# Call LLM
response = llm.invoke(prompt)
questions = json.loads(response.content)

# Validate
valid_questions = validate_questions(questions, rag_chunks)
```

### Example 2: Check Quality

```python
from app.services.question_generation.quality_control import (
    QuestionQualityController
)

qc = QuestionQualityController()

# Validate batch
valid_questions, errors = qc.validate_question_batch(
    questions=generated_questions,
    source_chunks=rag_chunks,
    expected_count=10
)

# Calculate metrics
metrics = calculate_quality_metrics(valid_questions)

print(f"Quality Score: {metrics['quality_score']}")
print(f"Difficulty Distribution: {metrics['difficulty_distribution']}")
```

---

## 🎓 EDUCATIONAL BEST PRACTICES

### Principle 1: Cognitive Load
- Easy questions build confidence
- Medium questions develop skills
- Hard questions challenge thinking

### Principle 2: Formative Assessment
- Questions should reveal understanding gaps
- Model answers provide learning points
- Source attribution enables review

### Principle 3: Constructive Alignment
- Questions align with learning objectives
- Difficulty matches curriculum progression
- Bloom's levels scaffold cognitive development

### Principle 4: Authenticity
- Questions reflect real-world applications
- Context from actual curriculum materials
- Age-appropriate language and examples

---

## 📚 REFERENCES

1. **Bloom's Taxonomy**: Anderson & Krathwohl (2001) - A Taxonomy for Learning, Teaching, and Assessing
2. **Assessment Design**: Wiggins & McTighe (2005) - Understanding by Design
3. **Educational Measurement**: Miller et al. (2009) - Measurement and Assessment in Teaching
4. **Prompt Engineering**: Wei et al. (2023) - Chain-of-Thought Prompting
5. **RAG Systems**: Lewis et al. (2020) - Retrieval-Augmented Generation

---

## ✅ CONCLUSION

The enhanced prompt framework provides:

✅ **Hallucination Prevention** - Multi-layer source fidelity  
✅ **Educational Quality** - Bloom's Taxonomy alignment  
✅ **Reliable Difficulty** - 30/50/20 distribution  
✅ **Comprehensive Examples** - All scenarios covered  
✅ **Structured Output** - Valid JSON with attribution  
✅ **Quality Assurance** - Validation framework

**Status**: Production-Ready  
**Next Steps**: Deploy, Monitor, Iterate based on metrics

---

**Document Version**: 2.0  
**Last Updated**: June 15, 2026  
**Maintained By**: AI Tutor Backend Team
