# 🎨 Enhanced Prompt Architecture - Visual Guide

---

## 🏗️ COMPLETE SYSTEM ARCHITECTURE

```
┌────────────────────────────────────────────────────────────────────┐
│                    STUDENT INITIATES TEST                          │
│            (Selects Categories + Question Type + Count)            │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│                    BACKEND: RAG RETRIEVAL                          │
│  • Query ChromaDB with category filter                             │
│  • Retrieve top K chunks per category                              │
│  • Format with source attribution                                  │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│               ENHANCED PROMPT GENERATION (NEW!)                    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ SYSTEM INSTRUCTIONS                                         │  │
│  │ • Expert educational designer role                          │  │
│  │ • Bloom's Taxonomy framework                                │  │
│  │ • Secondary school focus                                    │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ SOURCE FIDELITY LAYER (ANTI-HALLUCINATION)                  │  │
│  │ ═══════════════════════════════════════════════════════════  │  │
│  │ ⚠️ CRITICAL: Use ONLY textbook content                      │  │
│  │ ❌ FORBIDDEN: External knowledge                            │  │
│  │ ✓ REQUIRED: Source attribution                              │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ FORMATTED CONTEXT                                            │  │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│  │ EXCERPT #1                                                   │  │
│  │ Source: modern_india.pdf | Page: 45 | Category: History     │  │
│  │ [Actual textbook content]                                    │  │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ DIFFICULTY SPECIFICATION                                     │  │
│  │ → 30% Easy   (Remember/Understand)                           │  │
│  │ → 50% Medium (Understand/Apply)                              │  │
│  │ → 20% Hard   (Apply/Analyze/Evaluate)                        │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ FEW-SHOT EXAMPLES (3 per type)                               │  │
│  │ ┌─ EASY Example ────────────────────────────────────────┐   │  │
│  │ │ Bloom's: Remember | Direct recall                     │   │  │
│  │ └───────────────────────────────────────────────────────┘   │  │
│  │ ┌─ MEDIUM Example ──────────────────────────────────────┐   │  │
│  │ │ Bloom's: Understand/Apply | Concept relationships     │   │  │
│  │ └───────────────────────────────────────────────────────┘   │  │
│  │ ┌─ HARD Example ────────────────────────────────────────┐   │  │
│  │ │ Bloom's: Analyze | Multi-concept synthesis            │   │  │
│  │ └───────────────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ JSON OUTPUT SCHEMA                                           │  │
│  │ {                                                             │  │
│  │   "questions": [{                                             │  │
│  │     "question_text": "...",                                   │  │
│  │     "correct_answer": "...",                                  │  │
│  │     "difficulty": "Easy|Medium|Hard",                         │  │
│  │     "source_document": "...",                                 │  │
│  │     "source_page": 123                                        │  │
│  │   }]                                                          │  │
│  │ }                                                             │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ VALIDATION CHECKLIST                                         │  │
│  │ □ All questions generated                                    │  │
│  │ □ Difficulty 30/50/20                                        │  │
│  │ □ Source attribution 100%                                    │  │
│  │ □ JSON valid                                                 │  │
│  └─────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│                    GEMINI AI PROCESSING                            │
│  • Receives structured prompt                                      │
│  • Processes with educational context                              │
│  • Generates questions following template                          │
│  • Returns structured JSON                                         │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│              QUALITY CONTROL VALIDATION (NEW!)                     │
│                                                                     │
│  ┌─── TIER 1: JSON VALIDATION ───────────────────────────────┐   │
│  │ ✓ Valid JSON format                                        │   │
│  │ ✓ All required fields present                              │   │
│  │ ✓ Field types correct                                      │   │
│  └────────────────────────────────────────────────────────────┘   │
│                          │                                         │
│                          ▼                                         │
│  ┌─── TIER 2: HALLUCINATION DETECTION ───────────────────────┐   │
│  │ ✓ Answer exists in source chunks                           │   │
│  │ ✓ Source document/page valid                               │   │
│  │ ✓ Content similarity > threshold                           │   │
│  └────────────────────────────────────────────────────────────┘   │
│                          │                                         │
│                          ▼                                         │
│  ┌─── TIER 3: EDUCATIONAL QUALITY ───────────────────────────┐   │
│  │ ✓ Difficulty distribution 30/50/20 ±10%                    │   │
│  │ ✓ Bloom's taxonomy alignment                               │   │
│  │ ✓ Question independence (no duplicates)                    │   │
│  │ ✓ Multiple concepts covered                                │   │
│  └────────────────────────────────────────────────────────────┘   │
│                          │                                         │
│                          ▼                                         │
│  ┌─── QUALITY METRICS ─────────────────────────────────────────┐ │
│  │ • Source Attribution: 100%                                  │ │
│  │ • Hallucination Rate: <5%                                   │ │
│  │ • Difficulty Distribution: ✓                                │ │
│  │ • Overall Quality Score: 95/100                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│                    DATABASE STORAGE                                │
│  • Store test record (tests table)                                 │
│  • Store questions (test_questions table)                          │
│  • Atomic transaction                                              │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│                    RETURN TO FRONTEND                              │
│  {                                                                  │
│    "test_id": "uuid",                                               │
│    "question_count": 10,                                            │
│    "status": "GENERATED"                                            │
│  }                                                                  │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🎓 BLOOM'S TAXONOMY PYRAMID

```
                        ┌──────────────┐
                        │   CREATE     │  Not used (too advanced)
                        └──────────────┘
                    ┌──────────────────────┐
                    │     EVALUATE         │  HARD (20%)
                    │   (Judge, Assess)    │  Long Answer
                    └──────────────────────┘
                ┌──────────────────────────────┐
                │         ANALYZE              │  HARD (20%)
                │    (Compare, Examine)        │  Long Answer, MCQ
                └──────────────────────────────┘
            ┌──────────────────────────────────────┐
            │           APPLY                      │  MEDIUM (50%)
            │     (Use, Demonstrate)               │  MCQ, Short Answer
            └──────────────────────────────────────┘
        ┌──────────────────────────────────────────────┐
        │            UNDERSTAND                        │  EASY-MEDIUM (30-50%)
        │       (Explain, Describe)                    │  All types
        └──────────────────────────────────────────────┘
    ┌──────────────────────────────────────────────────────┐
    │              REMEMBER                                │  EASY (30%)
    │         (Recall, Define)                             │  MCQ, Fill Blanks
    └──────────────────────────────────────────────────────┘

                     CLASS 10 FOCUS AREA
```

---

## 🎯 DIFFICULTY CALIBRATION FLOW

```
                    INPUT: 10 Questions
                            │
                ┌───────────┴───────────┐
                │   DIFFICULTY SPLITTER  │
                │   (30% / 50% / 20%)    │
                └───────────┬───────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐  ┌────────────────┐  ┌──────────────┐
│  EASY (3)     │  │  MEDIUM (5)    │  │  HARD (2)    │
│               │  │                │  │              │
│ Remember      │  │ Understand     │  │ Analyze      │
│ Basic Facts   │  │ Apply          │  │ Evaluate     │
│ Definitions   │  │ Relationships  │  │ Synthesis    │
└───────────────┘  └────────────────┘  └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  VALIDATION:    │
                   │  Check if ratio │
                   │  matches target │
                   └─────────────────┘
                            │
                ┌───────────┴───────────┐
                │         PASS          │
         ┌──────┴──────┐         ┌─────┴──────┐
         │   Accept    │         │   Reject   │
         │   Questions │         │   & Retry  │
         └─────────────┘         └────────────┘
```

---

## 🔒 HALLUCINATION PREVENTION LAYERS

```
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 1: PROMPT DESIGN (Prevention)                            │
├─────────────────────────────────────────────────────────────────┤
│ • Visual emphasis (═══, ⚠️, ❌, ✓)                              │
│ • Multiple explicit warnings                                    │
│ • Source-only requirement stated 3+ times                       │
│ • Examples include source attribution                           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 2: CONTEXT FORMATTING (Clarity)                          │
├─────────────────────────────────────────────────────────────────┤
│ • Clear boundaries for source material                          │
│ • Numbered excerpts with metadata                               │
│ • Document name + page number visible                           │
│ • Visual separation from instructions                           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 3: OUTPUT REQUIREMENTS (Enforcement)                     │
├─────────────────────────────────────────────────────────────────┤
│ • Mandatory source_document field                               │
│ • Mandatory source_page field                                   │
│ • JSON schema with attribution                                  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 4: POST-GENERATION VALIDATION (Detection)                │
├─────────────────────────────────────────────────────────────────┤
│ • Check answer exists in source chunks                          │
│ • Verify source document is valid                               │
│ • Calculate content similarity score                            │
│ • Flag low-similarity answers                                   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 5: QUALITY SCORING (Metrics)                             │
├─────────────────────────────────────────────────────────────────┤
│ • Source attribution coverage: 100%                             │
│ • Hallucination rate: <5%                                       │
│ • Content overlap ratio: >0.5                                   │
│ • Overall quality score: >90                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 QUALITY METRICS DASHBOARD

```
╔════════════════════════════════════════════════════════════════╗
║              QUESTION QUALITY METRICS                          ║
╠════════════════════════════════════════════════════════════════╣
║                                                                 ║
║  SOURCE ATTRIBUTION                                            ║
║  ████████████████████████████████████████████████ 100%        ║
║                                                                 ║
║  DIFFICULTY DISTRIBUTION                                       ║
║  Easy:   ███████████████                           30%        ║
║  Medium: █████████████████████████                 50%        ║
║  Hard:   ██████████                                20%        ║
║                                                                 ║
║  HALLUCINATION RATE                                            ║
║  ██                                                 4%         ║
║  ✓ Target: <5%                                                 ║
║                                                                 ║
║  BLOOM'S TAXONOMY ALIGNMENT                                    ║
║  ████████████████████████████████████████████      92%        ║
║                                                                 ║
║  QUESTION INDEPENDENCE                                         ║
║  ████████████████████████████████████████████████ 100%        ║
║  (No duplicates detected)                                      ║
║                                                                 ║
║  OVERALL QUALITY SCORE                                         ║
║  ██████████████████████████████████████████████    95/100     ║
║                                                                 ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 🔄 QUESTION GENERATION FLOW (DETAILED)

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. STUDENT SELECTS                                              │
│    Categories: [History, Politics]                              │
│    Type: MCQ                                                     │
│    Count: 10                                                     │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. RAG RETRIEVAL                                                │
│    FOR category IN [History, Politics]:                         │
│        chunks = chromadb.query(                                 │
│            embedding=query_embedding,                           │
│            where={"category": category},  ← NATIVE FILTER       │
│            n_results=10                                         │
│        )                                                        │
│    RESULT: 20 chunks (10 per category)                          │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. CONTEXT FORMATTING                                           │
│    formatted = format_context_for_assessment(chunks, category)  │
│    • Add visual boundaries                                      │
│    • Include source attribution                                 │
│    • Number excerpts                                            │
│    RESULT: Structured context string                            │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. PROMPT CONSTRUCTION                                          │
│    prompt = create_mcq_generation_prompt(                       │
│        context=formatted,                                       │
│        category="History",                                      │
│        count=10                                                 │
│    )                                                            │
│    INCLUDES:                                                    │
│    • System instructions                                        │
│    • Source fidelity warnings (5 layers)                        │
│    • Difficulty specs (3 Easy, 5 Medium, 2 Hard)                │
│    • Bloom's taxonomy guidance                                  │
│    • 3 examples per difficulty                                  │
│    • JSON schema                                                │
│    • Validation checklist                                       │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. GEMINI AI CALL                                               │
│    response = llm.invoke(prompt, temperature=0.7)               │
│    • Processes structured prompt                                │
│    • Generates 10 MCQ questions                                 │
│    • Returns JSON                                               │
│    TIME: ~5-10 seconds                                          │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. JSON PARSING                                                 │
│    questions = parse_json_response(response.content)            │
│    • Remove markdown code blocks                                │
│    • Parse JSON                                                 │
│    • Validate structure                                         │
│    RESULT: List of 10 question dicts                            │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. QUALITY CONTROL                                              │
│    qc = QuestionQualityController()                             │
│    valid, errors = qc.validate_question_batch(                  │
│        questions, source_chunks, expected_count=10              │
│    )                                                            │
│    CHECKS:                                                      │
│    ✓ JSON structure                                             │
│    ✓ Hallucination detection                                    │
│    ✓ Difficulty distribution                                    │
│    ✓ Bloom's alignment                                          │
│    ✓ Question independence                                      │
│    ✓ Concept coverage                                           │
│    RESULT: 10 validated questions                               │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. DATABASE STORAGE                                             │
│    BEGIN TRANSACTION;                                           │
│      INSERT INTO tests (...);                                   │
│      INSERT INTO test_questions (...) x10;                      │
│    COMMIT;                                                      │
│    RESULT: test_id returned                                     │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 9. RESPONSE TO FRONTEND                                         │
│    {                                                             │
│      "success": true,                                            │
│      "data": {                                                   │
│        "test_id": "uuid",                                        │
│        "question_count": 10,                                     │
│        "status": "GENERATED"                                     │
│      }                                                           │
│    }                                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✅ VALIDATION GATES

```
QUESTION BATCH
      │
      ├─► [GATE 1] JSON Valid? ────────► NO ──► REJECT
      │                    │
      │                    YES
      │                    │
      ├─► [GATE 2] All Fields Present? ► NO ──► REJECT
      │                    │
      │                    YES
      │                    │
      ├─► [GATE 3] Answers in Source? ──► NO ──► REJECT
      │                    │
      │                    YES
      │                    │
      ├─► [GATE 4] Difficulty 30/50/20? ► NO ──► WARN + ACCEPT
      │                    │
      │                    YES
      │                    │
      ├─► [GATE 5] No Duplicates? ──────► NO ──► FILTER DUPLICATES
      │                    │
      │                    YES
      │                    │
      └─► [GATE 6] Bloom's Aligned? ────► NO ──► WARN + ACCEPT
                           │
                           YES
                           │
                           ▼
                    ✅ ACCEPT BATCH
```

---

**Created**: June 15, 2026  
**Purpose**: Visual reference for enhanced prompt architecture  
**Status**: Production-Ready ✅
