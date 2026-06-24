# Educational Assessment Quality Framework V3.0
## Complete Question Generation Redesign for AI-Powered Examination System

**Document Version:** 3.0 (Production-Ready)  
**Target Audience:** Class 10 Secondary School Students  
**Subject:** Social Studies (History, Geography, Politics, Economics)  
**AI Model:** Google Gemini 1.5 Flash  
**Architecture:** RAG-based Question Generation

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Hallucination Prevention Strategy](#2-hallucination-prevention-strategy)
3. [Bloom's Taxonomy Mapping](#3-blooms-taxonomy-mapping)
4. [Difficulty Classification Framework](#4-difficulty-classification-framework)
5. [Enhanced System Prompt](#5-enhanced-system-prompt)
6. [Question Type Templates](#6-question-type-templates)
7. [Context Injection Strategy](#7-context-injection-strategy)
8. [JSON Output Schema](#8-json-output-schema)
9. [Validation Rules](#9-validation-rules)
10. [Quality Checklist](#10-quality-checklist)
11. [Implementation Guide](#11-implementation-guide)

---

## 1. System Architecture

### Current Flow (Enhanced)
```
Student Request
    ↓
Selected Categories (History, Geography, Politics, Economics)
    ↓
RAG Retrieval (ChromaDB + Local Embeddings)
    │
    ├→ Category Filtering
    ├→ Semantic Search (Top-K chunks)
    ├→ Context Formatting
    │
    ↓
Enhanced Prompt Construction
    │
    ├→ System Role Definition
    ├→ Source Fidelity Instructions
    ├→ Educational Framework (Bloom's + Difficulty)
    ├→ Few-Shot Examples
    ├→ Retrieved Context
    ├→ Output Format Specification
    │
    ↓
Gemini 1.5 Flash Generation
    ↓
JSON Response Parsing
    ↓
Multi-Layer Validation
    │
    ├→ JSON Schema Validation
    ├→ Source Attribution Check
    ├→ Difficulty Distribution Verification
    ├→ Educational Quality Assessment
    ├→ Hallucination Detection
    │
    ↓
Database Storage (PostgreSQL)
    ↓
Student Assessment Interface
```

### Quality Assurance Layers

**Layer 1: Pre-Generation**
- Context quality validation
- Sufficient content check
- Category verification

**Layer 2: Prompt Engineering**
- Explicit source-only instructions
- Structured output format
- Educational framework alignment

**Layer 3: Post-Generation**
- JSON structure validation
- Answer attribution verification
- Difficulty distribution check
- Educational quality scoring

---

## 2. Hallucination Prevention Strategy

### 5-Layer Defense System

#### Layer 1: Explicit Prompt Instructions
```
⚠️ CRITICAL RULE: Generate questions ONLY from provided textbook content
❌ FORBIDDEN: External knowledge, assumptions, or invented facts
✓ REQUIRED: Every answer must be explicitly stated in source text
✓ VERIFICATION: Include source_document and source_page for each question
```

#### Layer 2: Context Framing
```python
# Wrap retrieved content with clear boundaries
prompt = f"""
═══════════════════════════════════════════════════════════════
TEXTBOOK CONTENT - {category.upper()} (SOURCE OF TRUTH)
═══════════════════════════════════════════════════════════════

{retrieved_context}

═══════════════════════════════════════════════════════════════
END OF TEXTBOOK CONTENT
═══════════════════════════════════════════════════════════════

⚠️ Generate questions ONLY from the content above.
⚠️ Do NOT use any information not present in the text above.
"""
```

#### Layer 3: Source Attribution Requirement
Every generated question MUST include:
- `source_document`: Document filename from metadata
- `source_page`: Page number where answer is found

This forces the model to reference specific sources.

#### Layer 4: Post-Generation Validation
```python
def validate_source_attribution(question: dict, context_chunks: List[dict]) -> bool:
    """
    Verify that the answer exists in the provided context
    """
    answer = question['correct_answer'].lower()
    
    # Check if answer appears in any context chunk
    for chunk in context_chunks:
        if answer in chunk['text'].lower():
            return True
    
    # If answer not found, flag as potential hallucination
    return False
```

#### Layer 5: Semantic Verification (Advanced)
```python
from sentence_transformers import util

def semantic_similarity_check(answer: str, context: str, threshold=0.75) -> bool:
    """
    Check semantic similarity between answer and context
    """
    answer_embedding = embeddings.encode(answer)
    context_embedding = embeddings.encode(context)
    
    similarity = util.cos_sim(answer_embedding, context_embedding)
    return similarity.item() > threshold
```

### Hallucination Detection Patterns

**Common Hallucination Types:**

1. **External Dates**: Model adds dates not in context
2. **Assumed Relationships**: Inferring causation not stated
3. **Extended Lists**: Adding items beyond source list
4. **Modern Context**: Applying current events to historical content
5. **Overgeneralization**: Making claims broader than source

**Detection Strategy:**
```python
HALLUCINATION_INDICATORS = [
    "according to recent studies",  # Modern reference
    "it is well known that",        # Assumed knowledge
    "experts agree",                 # External authority
    "in general",                    # Overgeneralization
    "obviously",                     # Assumed truth
]

def detect_hallucination_patterns(question_text: str) -> List[str]:
    """Detect common hallucination language patterns"""
    detected = []
    for indicator in HALLUCINATION_INDICATORS:
        if indicator in question_text.lower():
            detected.append(indicator)
    return detected
```

---

## 3. Bloom's Taxonomy Mapping

### Question Type ↔ Bloom's Level Matrix

| Question Type | Primary Bloom's Levels | Cognitive Processes |
|---------------|----------------------|---------------------|
| **MCQ** | L1-L3 (Remember, Understand, Apply) | Recognition, Comprehension, Application |
| **Fill Blanks** | L1-L2 (Remember, Understand) | Recall, Terminology |
| **Short Answer** | L2-L3 (Understand, Apply) | Explanation, Application |
| **Long Answer** | L3-L5 (Apply, Analyze, Evaluate) | Analysis, Synthesis, Evaluation |

### Bloom's Taxonomy Levels (Full Breakdown)

**Level 1: Remember**
- **Verbs**: Define, List, Name, Identify, Recall, State
- **Assessment**: Recognition and recall of facts
- **Example**: "Who was the first Prime Minister of India?"

**Level 2: Understand**
- **Verbs**: Explain, Describe, Summarize, Compare, Classify
- **Assessment**: Comprehension of meanings
- **Example**: "Explain how the monsoon affects agriculture."

**Level 3: Apply**
- **Verbs**: Apply, Use, Demonstrate, Solve, Illustrate
- **Assessment**: Use knowledge in new situations
- **Example**: "If a citizen's right is violated, what remedy should they seek?"

**Level 4: Analyze**
- **Verbs**: Analyze, Examine, Differentiate, Compare, Contrast
- **Assessment**: Break down into parts, find patterns
- **Example**: "Analyze the causes of the French Revolution."

**Level 5: Evaluate**
- **Verbs**: Evaluate, Assess, Justify, Critique, Argue
- **Assessment**: Make judgments based on criteria
- **Example**: "Evaluate the significance of the Non-Aligned Movement."

### Implementation Strategy

```python
BLOOMS_TAXONOMY_MAP = {
    "MCQ": {
        "Easy": {"level": "L1", "verbs": ["identify", "recall", "name"]},
        "Medium": {"level": "L2", "verbs": ["explain", "compare", "classify"]},
        "Hard": {"level": "L3", "verbs": ["apply", "solve", "use"]}
    },
    "FILL_BLANKS": {
        "Easy": {"level": "L1", "verbs": ["recall", "name", "identify"]},
        "Medium": {"level": "L2", "verbs": ["define", "explain"]},
        "Hard": {"level": "L2", "verbs": ["classify", "summarize"]}
    },
    "SHORT_ANSWER": {
        "Easy": {"level": "L2", "verbs": ["explain", "describe"]},
        "Medium": {"level": "L2-L3", "verbs": ["compare", "apply", "demonstrate"]},
        "Hard": {"level": "L3-L4", "verbs": ["analyze", "examine", "differentiate"]}
    },
    "LONG_ANSWER": {
        "Easy": {"level": "L2-L3", "verbs": ["describe", "explain"]},
        "Medium": {"level": "L3-L4", "verbs": ["analyze", "examine", "compare"]},
        "Hard": {"level": "L4-L5", "verbs": ["evaluate", "assess", "critique"]}
    }
}
```

---

## 4. Difficulty Classification Framework

### Difficulty Levels Defined

**EASY (30% of questions)**
- **Cognitive Load**: Low
- **Bloom's Level**: L1-L2
- **Content Type**: Direct recall, basic definitions
- **Answer Location**: Explicit in single sentence/paragraph
- **Student Behavior**: Immediate recognition

**Examples:**
- "What is the capital of India?" (MCQ)
- "The Indian Constitution was adopted on _____." (Fill Blank)
- "Define democracy." (Short Answer)

**MEDIUM (50% of questions)**
- **Cognitive Load**: Moderate
- **Bloom's Level**: L2-L3
- **Content Type**: Concept understanding, relationships
- **Answer Location**: Requires synthesis from multiple sentences
- **Student Behavior**: Application of learned concepts

**Examples:**
- "What was the main cause of the French Revolution?" (MCQ)
- "The right to _____ allows citizens to move freely." (Fill Blank)
- "Explain how the monsoon affects agriculture." (Short Answer)

**HARD (20% of questions)**
- **Cognitive Load**: High
- **Bloom's Level**: L3-L5
- **Content Type**: Analysis, evaluation, synthesis
- **Answer Location**: Requires integration across multiple sources
- **Student Behavior**: Critical thinking and reasoning

**Examples:**
- "If a citizen's right is violated, what remedy is MOST effective?" (MCQ)
- "The economic policy combining capitalism and socialism is _____." (Fill Blank)
- "Evaluate the significance of the Non-Aligned Movement." (Long Answer)

### Automated Difficulty Classification

```python
def calculate_difficulty_score(question: dict) -> str:
    """
    Automatically classify question difficulty using multiple signals
    """
    score = 0
    
    # Signal 1: Question verb complexity
    hard_verbs = ["analyze", "evaluate", "assess", "compare", "synthesize"]
    medium_verbs = ["explain", "describe", "apply", "demonstrate"]
    easy_verbs = ["define", "list", "name", "identify", "recall"]
    
    q_text = question['question_text'].lower()
    
    if any(verb in q_text for verb in hard_verbs):
        score += 3
    elif any(verb in q_text for verb in medium_verbs):
        score += 2
    elif any(verb in q_text for verb in easy_verbs):
        score += 1
    
    # Signal 2: Answer length (longer = harder)
    answer_length = len(question.get('model_answer', question.get('correct_answer', '')).split())
    if answer_length > 80:
        score += 3
    elif answer_length > 30:
        score += 2
    else:
        score += 1
    
    # Signal 3: MCQ distractor complexity
    if question.get('options'):
        # Check if distractors are plausible (similar length to correct answer)
        correct_len = len(question['correct_answer'])
        avg_distractor_len = sum(len(opt) for opt in question['options']) / len(question['options'])
        if abs(correct_len - avg_distractor_len) / correct_len < 0.3:
            score += 2  # Plausible distractors = harder
    
    # Convert score to difficulty
    if score <= 3:
        return "Easy"
    elif score <= 6:
        return "Medium"
    else:
        return "Hard"
```

### Difficulty Distribution Enforcement

```python
def enforce_difficulty_distribution(
    questions: List[dict],
    target_easy: int,
    target_medium: int,
    target_hard: int
) -> List[dict]:
    """
    Ensure questions match target difficulty distribution
    30% Easy, 50% Medium, 20% Hard
    """
    # Group by difficulty
    by_difficulty = {
        "Easy": [q for q in questions if q['difficulty'] == "Easy"],
        "Medium": [q for q in questions if q['difficulty'] == "Medium"],
        "Hard": [q for q in questions if q['difficulty'] == "Hard"]
    }
    
    # Select target number from each difficulty
    selected = []
    selected.extend(by_difficulty["Easy"][:target_easy])
    selected.extend(by_difficulty["Medium"][:target_medium])
    selected.extend(by_difficulty["Hard"][:target_hard])
    
    return selected
```

---

## 5. Enhanced System Prompt

### Universal System Prompt (All Question Types)

```python
SYSTEM_PROMPT = """You are an expert educational assessment designer specializing in Class 10 Social Studies.

Your responsibilities:
