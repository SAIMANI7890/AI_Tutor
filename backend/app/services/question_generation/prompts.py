"""
Enhanced Educational Assessment Prompts
=======================================
Production-ready prompts optimized for:
- Educational quality (Bloom's Taxonomy)
- Hallucination prevention (strict source fidelity)
- Secondary school appropriateness
- Difficulty calibration
- Structured JSON output

Author: AI Tutor Backend Team
Version: 2.0 (Enhanced)
"""
from typing import List


def create_mcq_generation_prompt(context: str, category: str, count: int) -> str:
    """
    Enhanced MCQ Generation Prompt with Educational Assessment Framework
    
    Features:
    - Bloom's Taxonomy alignment (Remember, Understand, Apply)
    - Plausible distractors
    - Source-based only (zero hallucination)
    - Difficulty distribution (30% Easy, 50% Medium, 20% Hard)
    """
    
    prompt = f"""You are an expert educational assessment designer for Class 10 Social Studies.

═══════════════════════════════════════════════════════════════
CORE INSTRUCTION: SOURCE FIDELITY
═══════════════════════════════════════════════════════════════
⚠️ CRITICAL: Generate questions ONLY from the textbook content below.
❌ FORBIDDEN: Using external knowledge, assumptions, or invented facts.
✓ REQUIRED: Every answer must be explicitly stated in the source text.

═══════════════════════════════════════════════════════════════
TEXTBOOK CONTENT - {category.upper()}
═══════════════════════════════════════════════════════════════

{context}

═══════════════════════════════════════════════════════════════
TASK: Generate {count} Multiple Choice Questions
═══════════════════════════════════════════════════════════════

DIFFICULTY DISTRIBUTION (STRICT):
→ {int(count * 0.3)} Easy questions (30%)
→ {int(count * 0.5)} Medium questions (50%)
→ {int(count * 0.2)} Hard questions (20%)

BLOOM'S TAXONOMY LEVELS:
• Easy → Remember (recall facts, definitions, dates)
• Medium → Understand (explain concepts, cause-effect)
• Hard → Apply/Analyze (scenarios, relationships, comparisons)

MCQ QUALITY STANDARDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Question Stem:
   ✓ Clear and focused on one concept
   ✓ Can be answered without looking at options
   ✓ Avoid negatives ("Which is NOT...") unless essential

2. Four Options (A, B, C, D):
   ✓ Exactly ONE correct answer
   ✓ Three plausible distractors (common misconceptions)
   ✓ Similar length and grammatical structure
   ✓ All options based on content (no "None of the above")

3. Source Attribution:
   ✓ Note document name and page number
   ✓ Answer must be verifiable from source

EXAMPLES BY DIFFICULTY:

┌─────────────────────────────────────────────────────────────┐
│ EASY - Remember (Bloom's Level 1)                           │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "Who was the first Prime Minister of India?",
  "options": [
    "Jawaharlal Nehru",
    "Mahatma Gandhi",
    "Sardar Patel",
    "Dr. Rajendra Prasad"
  ],
  "correct_answer": "Jawaharlal Nehru",
  "difficulty": "Easy",
  "category": "{category}",
  "source_document": "modern_india.pdf",
  "source_page": 45
}}

┌─────────────────────────────────────────────────────────────┐
│ MEDIUM - Understand (Bloom's Level 2)                       │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "What was the main reason for the decline of the Mughal Empire?",
  "options": [
    "Weak successors and internal conflicts after Aurangzeb",
    "British military superiority alone",
    "Natural disasters and famines",
    "Loss of trade routes to Europeans"
  ],
  "correct_answer": "Weak successors and internal conflicts after Aurangzeb",
  "difficulty": "Medium",
  "category": "{category}",
  "source_document": "mughal_empire.pdf",
  "source_page": 78
}}

┌─────────────────────────────────────────────────────────────┐
│ HARD - Apply (Bloom's Level 3)                              │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "If a citizen's fundamental right is violated, which constitutional remedy would be MOST effective?",
  "options": [
    "File a writ petition in the Supreme Court under Article 32",
    "Write to the President for redressal",
    "Approach the local police station",
    "File a complaint with the Election Commission"
  ],
  "correct_answer": "File a writ petition in the Supreme Court under Article 32",
  "difficulty": "Hard",
  "category": "{category}",
  "source_document": "constitution.pdf",
  "source_page": 112
}}

JSON OUTPUT FORMAT (STRICT):
{{
  "questions": [
    {{
      "question_text": "Complete question ending with ?",
      "options": [
        "Option 1",
        "Option 2",
        "Option 3",
        "Option 4"
      ],
      "correct_answer": "Exact text from options array",
      "difficulty": "Easy|Medium|Hard",
      "category": "{category}",
      "source_document": "filename.pdf",
      "source_page": 123
    }}
  ]
}}

VALIDATION CHECKLIST:
□ All {count} questions generated
□ Difficulty ratio: 30% Easy, 50% Medium, 20% Hard
□ Every answer found in source excerpts above
□ No external knowledge used
□ All options plausible and content-based
□ JSON format valid

Generate {count} MCQ questions now:"""
    
    return prompt


def create_fill_blank_generation_prompt(context: str, category: str, count: int) -> str:
    """
    Enhanced Fill in the Blanks Prompt for Key Term Assessment
    
    Features:
    - Focus on terminology and key concepts
    - Single blank per question
    - Concise answers (1-4 words)
    - Bloom's Level 1-2 (Remember, Understand)
    """
    
    prompt = f"""You are an expert educational assessment designer for Class 10 Social Studies.

═══════════════════════════════════════════════════════════════
CORE INSTRUCTION: SOURCE FIDELITY
═══════════════════════════════════════════════════════════════
⚠️ CRITICAL: Generate questions ONLY from the textbook content below.
❌ FORBIDDEN: Using external knowledge or assumptions.
✓ REQUIRED: Answer must appear verbatim in source text.

═══════════════════════════════════════════════════════════════
TEXTBOOK CONTENT - {category.upper()}
═══════════════════════════════════════════════════════════════

{context}

═══════════════════════════════════════════════════════════════
TASK: Generate {count} Fill in the Blanks Questions
═══════════════════════════════════════════════════════════════

DIFFICULTY DISTRIBUTION (STRICT):
→ {int(count * 0.3)} Easy (capitals, names, dates)
→ {int(count * 0.5)} Medium (concepts, definitions)
→ {int(count * 0.2)} Hard (technical terms, complex concepts)

BLOOM'S TAXONOMY:
• Easy → Remember (recall basic facts)
• Medium → Understand (grasp concepts)
• Hard → Understand (complex terminology)

FILL IN THE BLANK STANDARDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Blank Marker:
   ✓ Use exactly 5 underscores: _____
   ✓ Only ONE blank per question
   ✓ Avoid blanks at sentence start

2. Answer Format:
   ✓ Concise: 1-4 words typically
   ✓ Key term or concept (not articles/prepositions)
   ✓ Explicitly stated in source text

3. Sentence Quality:
   ✓ Provides sufficient context clues
   ✓ Grammatically complete when filled
   ✓ Tests important knowledge, not trivial facts

EXAMPLES BY DIFFICULTY:

┌─────────────────────────────────────────────────────────────┐
│ EASY - Remember (Basic Facts)                               │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "The capital of India is _____.",
  "correct_answer": "New Delhi",
  "difficulty": "Easy",
  "category": "{category}",
  "source_document": "geography.pdf",
  "source_page": 12
}}

┌─────────────────────────────────────────────────────────────┐
│ MEDIUM - Understand (Concepts)                              │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "The Indian Constitution guarantees the right to _____, which allows citizens to move freely throughout the country.",
  "correct_answer": "freedom of movement",
  "difficulty": "Medium",
  "category": "{category}",
  "source_document": "constitution.pdf",
  "source_page": 67
}}

┌─────────────────────────────────────────────────────────────┐
│ HARD - Understand (Technical Terms)                         │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "The economic policy adopted by India after independence, which combined elements of capitalism and socialism, is known as a _____ economy.",
  "correct_answer": "mixed",
  "difficulty": "Hard",
  "category": "{category}",
  "source_document": "economy.pdf",
  "source_page": 89
}}

JSON OUTPUT FORMAT (STRICT):
{{
  "questions": [
    {{
      "question_text": "Sentence with exactly one _____ blank.",
      "correct_answer": "Exact term from source (1-4 words)",
      "difficulty": "Easy|Medium|Hard",
      "category": "{category}",
      "source_document": "filename.pdf",
      "source_page": 123
    }}
  ]
}}

VALIDATION CHECKLIST:
□ All {count} questions generated
□ Difficulty ratio: 30% Easy, 50% Medium, 20% Hard
□ Each question has exactly ONE blank (_____) 
□ Every answer is in source text
□ Answers are 1-4 words (concise)
□ JSON format valid

Generate {count} fill in the blank questions now:"""
    
    return prompt


def create_short_answer_generation_prompt(context: str, category: str, count: int) -> str:
    """
    Enhanced Short Answer Prompt for Conceptual Understanding
    
    Features:
    - 2-3 sentence answers (30-50 words)
    - Bloom's Level 2-3 (Understand, Apply)
    - Explanation-focused, not just recall
    - Clear evaluation criteria
    """
    
    prompt = f"""You are an expert educational assessment designer for Class 10 Social Studies.

═══════════════════════════════════════════════════════════════
CORE INSTRUCTION: SOURCE FIDELITY
═══════════════════════════════════════════════════════════════
⚠️ CRITICAL: Generate questions ONLY from the textbook content below.
❌ FORBIDDEN: Using external knowledge or assumptions.
✓ REQUIRED: Model answers must be based entirely on source text.

═══════════════════════════════════════════════════════════════
TEXTBOOK CONTENT - {category.upper()}
═══════════════════════════════════════════════════════════════

{context}

═══════════════════════════════════════════════════════════════
TASK: Generate {count} Short Answer Questions
═══════════════════════════════════════════════════════════════

ANSWER LENGTH: 2-3 sentences (30-50 words)

DIFFICULTY DISTRIBUTION (STRICT):
→ {int(count * 0.3)} Easy (definitions, simple explanations)
→ {int(count * 0.5)} Medium (cause-effect, comparisons)
→ {int(count * 0.2)} Hard (multi-faceted explanations)

BLOOM'S TAXONOMY:
• Easy → Understand (explain basic concepts)
• Medium → Understand/Apply (relationships, applications)
• Hard → Apply/Analyze (complex explanations)

SHORT ANSWER STANDARDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Question Design:
   ✓ Start with: Explain, Define, Describe, State, Compare
   ✓ Focus on WHY and HOW (not just WHAT)
   ✓ Test understanding, not memorization

2. Model Answer:
   ✓ Complete: 2-3 sentences
   ✓ Word count: 30-50 words
   ✓ Include key points for evaluation
   ✓ Based on source content only

3. Educational Value:
   ✓ Prepare students for concept application
   ✓ Encourage articulation of understanding

EXAMPLES BY DIFFICULTY:

┌─────────────────────────────────────────────────────────────┐
│ EASY - Understand (Basic Explanation)                       │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "What is democracy?",
  "model_answer": "Democracy is a system of government where power lies with the people, who exercise it through elected representatives. It is characterized by free and fair elections, protection of individual rights, and rule of law.",
  "difficulty": "Easy",
  "category": "{category}",
  "source_document": "governance.pdf",
  "source_page": 34
}}

┌─────────────────────────────────────────────────────────────┐
│ MEDIUM - Understand (Cause-Effect)                          │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "Explain how the monsoon affects Indian agriculture.",
  "model_answer": "The monsoon brings the majority of India's annual rainfall during June-September, which is essential for irrigation and crop cultivation. This seasonal pattern determines planting schedules for major crops like rice and wheat. Failure or delay of monsoons can lead to droughts and severely impact agricultural productivity.",
  "difficulty": "Medium",
  "category": "{category}",
  "source_document": "agriculture.pdf",
  "source_page": 56
}}

┌─────────────────────────────────────────────────────────────┐
│ HARD - Apply (Complex Explanation)                          │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "Why is separation of powers important in democracy?",
  "model_answer": "Separation of powers divides government authority among the legislature, executive, and judiciary to prevent concentration and abuse of power. This creates checks and balances where each branch can limit the others, protecting individual freedoms and ensuring accountability.",
  "difficulty": "Hard",
  "category": "{category}",
  "source_document": "constitution.pdf",
  "source_page": 78
}}

JSON OUTPUT FORMAT (STRICT):
{{
  "questions": [
    {{
      "question_text": "Question starting with Explain/Define/Describe?",
      "model_answer": "Complete 2-3 sentence answer (30-50 words) from source.",
      "difficulty": "Easy|Medium|Hard",
      "category": "{category}",
      "source_document": "filename.pdf",
      "source_page": 123
    }}
  ]
}}

VALIDATION CHECKLIST:
□ All {count} questions generated
□ Difficulty ratio: 30% Easy, 50% Medium, 20% Hard
□ Model answers are 2-3 sentences (30-50 words)
□ All content from source excerpts
□ Questions test UNDERSTANDING
□ JSON format valid

Generate {count} short answer questions now:"""
    
    return prompt


def create_long_answer_generation_prompt(context: str, category: str, count: int) -> str:
    """
    Enhanced Long Answer Prompt for Analytical Essays
    
    Features:
    - 5-6 sentence answers (100-150 words)
    - Bloom's Level 3-4 (Apply, Analyze, Evaluate)
    - Structured arguments with multiple points
    - Synthesis across concepts
    """
    
    prompt = f"""You are an expert educational assessment designer for Class 10 Social Studies.

═══════════════════════════════════════════════════════════════
CORE INSTRUCTION: SOURCE FIDELITY
═══════════════════════════════════════════════════════════════
⚠️ CRITICAL: Generate questions ONLY from the textbook content below.
❌ FORBIDDEN: Using external knowledge or assumptions.
✓ REQUIRED: Model answers must synthesize source content only.

═══════════════════════════════════════════════════════════════
TEXTBOOK CONTENT - {category.upper()}
═══════════════════════════════════════════════════════════════

{context}

═══════════════════════════════════════════════════════════════
TASK: Generate {count} Long Answer Questions
═══════════════════════════════════════════════════════════════

ANSWER LENGTH: 5-6 sentences (100-150 words)

DIFFICULTY DISTRIBUTION (STRICT):
→ {int(count * 0.3)} Easy (comprehensive descriptions)
→ {int(count * 0.5)} Medium (cause-effect analysis, comparisons)
→ {int(count * 0.2)} Hard (synthesis, critical evaluation)

BLOOM'S TAXONOMY:
• Easy → Understand (multi-point descriptions)
• Medium → Apply/Analyze (cause-effect, analysis)
• Hard → Analyze/Evaluate (synthesis, critical thinking)

LONG ANSWER STANDARDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Question Design:
   ✓ Use: Discuss, Analyze, Examine, Evaluate, Compare and Contrast
   ✓ Require integration of multiple concepts
   ✓ Encourage structured logical arguments

2. Model Answer:
   ✓ Structure: Introduction + main points + conclusion
   ✓ Length: 5-6 complete sentences
   ✓ Word count: 100-150 words
   ✓ Cover multiple aspects comprehensively

3. Educational Value:
   ✓ Test ability to organize knowledge
   ✓ Evaluate depth of understanding
   ✓ Assess analytical thinking

EXAMPLES BY DIFFICULTY:

┌─────────────────────────────────────────────────────────────┐
│ EASY - Understand (Comprehensive Description)               │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "Describe the main features of the Indian Constitution.",
  "model_answer": "The Indian Constitution is the supreme law establishing India as a sovereign, socialist, secular, and democratic republic. It guarantees fundamental rights to all citizens, including equality, freedom, and protection against exploitation. The Constitution establishes a federal structure with clear division of powers between central and state governments. It includes Directive Principles to guide governance towards social welfare. Additionally, it provides for an independent judiciary to interpret laws and protect citizens' rights, along with provisions for amendments to evolve with changing times.",
  "difficulty": "Easy",
  "category": "{category}",
  "source_document": "constitution.pdf",
  "source_page": 23
}}

┌─────────────────────────────────────────────────────────────┐
│ MEDIUM - Analyze (Cause-Effect)                             │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "Analyze the causes and effects of the French Revolution.",
  "model_answer": "The French Revolution was primarily caused by the oppressive feudal system, economic crisis from war debts, and the influence of Enlightenment ideas promoting equality. The monarchy's absolute power and stark social inequality created widespread discontent. The immediate trigger was the financial crisis forcing King Louis XVI to call the Estates-General. The Revolution's effects were far-reaching: it abolished feudalism, established principles of liberty, equality, and fraternity, and inspired democratic movements worldwide. It also led to Napoleon's rise and fundamentally transformed French society and global democratic governance.",
  "difficulty": "Medium",
  "category": "{category}",
  "source_document": "revolutions.pdf",
  "source_page": 145
}}

┌─────────────────────────────────────────────────────────────┐
│ HARD - Evaluate (Critical Analysis)                         │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "Evaluate the significance of the Non-Aligned Movement during the Cold War.",
  "model_answer": "The Non-Aligned Movement (NAM), initiated by India and other developing nations, represented a strategic rejection of both US and Soviet bloc alignment during the Cold War. It allowed newly independent countries to maintain sovereignty while avoiding superpower pressures. NAM provided a platform for addressing common concerns like decolonization and economic development. However, its practical impact was limited as many members maintained informal alignments based on economic needs. Despite limitations, NAM successfully promoted peaceful coexistence and provided a collective voice for the Global South. Its legacy continues in contemporary multilateral diplomacy, emphasizing independent foreign policy for developing nations.",
  "difficulty": "Hard",
  "category": "{category}",
  "source_document": "cold_war.pdf",
  "source_page": 234
}}

JSON OUTPUT FORMAT (STRICT):
{{
  "questions": [
    {{
      "question_text": "Analytical question starting with Discuss/Analyze/Examine?",
      "model_answer": "Comprehensive 5-6 sentence answer (100-150 words) with structure.",
      "difficulty": "Easy|Medium|Hard",
      "category": "{category}",
      "source_document": "filename.pdf",
      "source_page": 123
    }}
  ]
}}

VALIDATION CHECKLIST:
□ All {count} questions generated
□ Difficulty ratio: 30% Easy, 50% Medium, 20% Hard
□ Model answers are 5-6 sentences (100-150 words)
□ All content from source excerpts
□ Questions require ANALYSIS/SYNTHESIS
□ Answers have clear structure
□ JSON format valid

Generate {count} long answer questions now:"""
    
    return prompt


def select_prompt_for_question_type(
    question_type: str,
    context: str,
    category: str,
    count: int
) -> str:
    """
    Select appropriate prompt based on question type
    
    Args:
        question_type: Type of question (MCQ, FILL_BLANKS, SHORT_ANSWER, LONG_ANSWER)
        context: Retrieved textbook content
        category: Subject category
        count: Number of questions
        
    Returns:
        Formatted prompt string
    """
    if question_type == "MCQ":
        return create_mcq_generation_prompt(context, category, count)
    elif question_type == "FILL_BLANKS":
        return create_fill_blank_generation_prompt(context, category, count)
    elif question_type == "SHORT_ANSWER":
        return create_short_answer_generation_prompt(context, category, count)
    elif question_type == "LONG_ANSWER":
        return create_long_answer_generation_prompt(context, category, count)
    else:
        raise ValueError(f"Unsupported question type: {question_type}")
