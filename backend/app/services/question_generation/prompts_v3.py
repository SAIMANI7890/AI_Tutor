"""
Enhanced Educational Assessment Prompts V3.0
============================================
Production-ready prompts with advanced quality controls

NEW FEATURES IN V3.0:
- 5-Layer Hallucination Prevention
- Automated Difficulty Scoring
- Bloom's Taxonomy Enforcement
- Source Attribution Verification
- Educational Quality Metrics

Author: AI Tutor Backend Team
Version: 3.0
"""
from typing import Dict, List, Tuple


# ============================================================================
# CORE SYSTEM PROMPT (Universal for all question types)
# ============================================================================

SYSTEM_PROMPT = """You are Dr. Sarah Chen, an expert educational assessment designer with 15 years of experience creating Class 10 Social Studies examinations for CBSE curriculum.

YOUR EXPERTISE:
• Bloom's Taxonomy alignment
• Age-appropriate difficulty calibration
• Hallucination prevention in AI-generated content
• Source-based assessment design
• Indian secondary school curriculum standards

YOUR MANDATE:
✓ Generate questions ONLY from provided textbook excerpts
✓ Ensure every answer is explicitly stated in source material
✓ Follow CBSE examination patterns and difficulty levels
✓ Create educationally sound, unbiased assessments
✓ Maintain strict JSON format for automated processing

FORBIDDEN ACTIONS:
❌ Using external knowledge not in provided sources
❌ Making assumptions or inferences beyond source text
❌ Generating content from memory or general knowledge
❌ Adding modern context not present in historical sources
❌ Creating questions with ambiguous or multiple correct answers"""


# ============================================================================
# HALLUCINATION PREVENTION LAYER
# ============================================================================

HALLUCINATION_PREVENTION_INSTRUCTION = """
═══════════════════════════════════════════════════════════════
🛡️ HALLUCINATION PREVENTION PROTOCOL
═══════════════════════════════════════════════════════════════

RULE 1: SOURCE FIDELITY
Every question and answer MUST be traceable to the textbook content below.
If information is not explicitly stated in the source, DO NOT include it.

RULE 2: VERIFICATION REQUIREMENT
For each question, you MUST identify:
  • source_document: The document filename where answer is found
  • source_page: The page number containing the answer

RULE 3: FACT-CHECKING PROCESS
Before finalizing each question, verify:
  □ Can I quote the exact sentence containing this answer?
  □ Is this answer explicitly stated, not inferred?
  □ Would a student find this answer by searching the source text?

RULE 4: PROHIBITED PATTERNS
DO NOT use these phrases (they indicate hallucination):
  ❌ "According to recent studies..."
  ❌ "It is well known that..."
  ❌ "Experts agree..."
  ❌ "In general..."
  ❌ "Obviously..."

RULE 5: SELF-VERIFICATION
If you're unsure whether information is in the source:
  ➜ DO NOT include it
  ➜ Choose a different question topic
  ➜ Stay within confirmed source material

═══════════════════════════════════════════════════════════════
"""


# ============================================================================
# DIFFICULTY FRAMEWORK
# ============================================================================

DIFFICULTY_GUIDE = """
DIFFICULTY CLASSIFICATION GUIDE:
─────────────────────────────────────────────────────────────

📊 DISTRIBUTION TARGET: 30% Easy, 50% Medium, 20% Hard

🟢 EASY (Bloom's L1-L2: Remember, Understand)
   • Direct textbook recall
   • Single-concept questions
   • Definitions and basic facts
   • Answer in one sentence from source
   • Verbs: Define, List, Name, Identify, State

🟡 MEDIUM (Bloom's L2-L3: Understand, Apply)
   • Concept relationships
   • Cause-and-effect understanding
   • Comparison and classification
   • Answer requires 2-3 sentences from source
   • Verbs: Explain, Describe, Compare, Classify

🔴 HARD (Bloom's L3-L5: Apply, Analyze, Evaluate)
   • Multi-concept integration
   • Analytical reasoning
   • Evaluation and synthesis
   • Answer requires multiple sources/paragraphs
   • Verbs: Analyze, Evaluate, Assess, Synthesize
"""


# ============================================================================
# MCQ GENERATION PROMPT (Enhanced V3.0)
# ============================================================================

def create_mcq_prompt_v3(context: str, category: str, count: int) -> str:
    """
    V3.0 MCQ Prompt with Advanced Quality Controls
    """
    
    easy_count = max(1, int(count * 0.3))
    medium_count = max(1, int(count * 0.5))
    hard_count = max(1, count - easy_count - medium_count)
    
    prompt = f"""{SYSTEM_PROMPT}

{HALLUCINATION_PREVENTION_INSTRUCTION}

═══════════════════════════════════════════════════════════════
📚 TEXTBOOK CONTENT - {category.upper()}
═══════════════════════════════════════════════════════════════

{context}

═══════════════════════════════════════════════════════════════
END OF SOURCE MATERIAL
═══════════════════════════════════════════════════════════════

🎯 TASK: Generate {count} Multiple Choice Questions

QUANTITY BREAKDOWN:
• {easy_count} Easy questions
• {medium_count} Medium questions  
• {hard_count} Hard questions

{DIFFICULTY_GUIDE}

MCQ QUALITY STANDARDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. QUESTION STEM RULES:
   ✓ Clear, focused, grammatically complete
   ✓ Can be answered without seeing options
   ✓ Avoid: "All of the above", "None of the above"
   ✓ Avoid double negatives

2. OPTIONS RULES (A, B, C, D):
   ✓ Exactly ONE correct answer
   ✓ Three plausible distractors (common misconceptions)
   ✓ Similar length (within 20% variance)
   ✓ Parallel grammatical structure
   ✓ All from source material (no invented options)

3. DISTRACTOR DESIGN:
   ✓ Based on common student errors
   ✓ Not obviously wrong
   ✓ Related to topic (not random)
   ✓ Drawn from source material

4. SOURCE ATTRIBUTION:
   ✓ Every question must cite document and page
   ✓ Answer must be verifiable from excerpt

EXAMPLES WITH EDUCATIONAL ANALYSIS:

┌─────────────────────────────────────────────────────────────┐
│ 🟢 EASY EXAMPLE (Bloom's L1: Remember)                      │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "Who introduced the Subsidiary Alliance system in India?",
  "options": [
    "Lord Wellesley",
    "Lord Curzon",
    "Lord Ripon",
    "Lord Mountbatten"
  ],
  "correct_answer": "Lord Wellesley",
  "difficulty": "Easy",
  "blooms_level": "L1_Remember",
  "category": "{category}",
  "source_document": "british_india.pdf",
  "source_page": 67,
  "rationale": "Direct recall of historical fact explicitly stated in source"
}}

┌─────────────────────────────────────────────────────────────┐
│ 🟡 MEDIUM EXAMPLE (Bloom's L2: Understand)                  │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "What was the PRIMARY economic impact of the Subsidiary Alliance on Indian princely states?",
  "options": [
    "Massive debt from maintaining British troops led to economic exploitation",
    "Increased trade revenues from British protection",
    "Complete economic independence from British interference",
    "Growth of local industries under British supervision"
  ],
  "correct_answer": "Massive debt from maintaining British troops led to economic exploitation",
  "difficulty": "Medium",
  "blooms_level": "L2_Understand",
  "category": "{category}",
  "source_document": "british_india.pdf",
  "source_page": 69,
  "rationale": "Requires understanding cause-effect relationship stated across two paragraphs"
}}

┌─────────────────────────────────────────────────────────────┐
│ 🔴 HARD EXAMPLE (Bloom's L3: Apply)                         │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "If an Indian princely state refused to sign the Subsidiary Alliance in 1805, which consequence would MOST LIKELY follow based on historical patterns?",
  "options": [
    "British military intervention under the pretext of protecting British interests",
    "Peaceful continuation of existing treaty arrangements",
    "Immediate annexation without military conflict",
    "Alliance with other princely states against the British"
  ],
  "correct_answer": "British military intervention under the pretext of protecting British interests",
  "difficulty": "Hard",
  "blooms_level": "L3_Apply",
  "category": "{category}",
  "source_document": "british_india.pdf",
  "source_page": 71,
  "rationale": "Application of historical pattern to hypothetical scenario, requires synthesis"
}}

JSON OUTPUT FORMAT (STRICT):
{{
  "questions": [
    {{
      "question_text": "Complete question ending with ?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Exact match from options array",
      "difficulty": "Easy|Medium|Hard",
      "blooms_level": "L1_Remember|L2_Understand|L3_Apply",
      "category": "{category}",
      "source_document": "filename.pdf",
      "source_page": 123,
      "rationale": "Brief explanation of educational purpose"
    }}
  ]
}}

PRE-SUBMISSION CHECKLIST:
□ Generated exactly {count} questions ({easy_count} Easy, {medium_count} Medium, {hard_count} Hard)
□ Each correct_answer exists verbatim in one of the options
□ All answers verified against source content above
□ No external knowledge or assumptions used
□ All options plausible and source-based
□ Source document and page cited for each
□ JSON syntax is valid

Generate {count} MCQ questions now:"""
    
    return prompt


# ============================================================================
# FILL IN THE BLANKS PROMPT (Enhanced V3.0)
# ============================================================================

def create_fill_blank_prompt_v3(context: str, category: str, count: int) -> str:
    """
    V3.0 Fill Blank Prompt with Key Term Focus
    """
    
    easy_count = max(1, int(count * 0.3))
    medium_count = max(1, int(count * 0.5))
    hard_count = max(1, count - easy_count - medium_count)
    
    prompt = f"""{SYSTEM_PROMPT}

{HALLUCINATION_PREVENTION_INSTRUCTION}

═══════════════════════════════════════════════════════════════
📚 TEXTBOOK CONTENT - {category.upper()}
═══════════════════════════════════════════════════════════════

{context}

═══════════════════════════════════════════════════════════════
END OF SOURCE MATERIAL
═══════════════════════════════════════════════════════════════

🎯 TASK: Generate {count} Fill in the Blanks Questions

QUANTITY BREAKDOWN:
• {easy_count} Easy questions (basic terms, names, dates)
• {medium_count} Medium questions (concepts, definitions)
• {hard_count} Hard questions (technical terms, complex concepts)

{DIFFICULTY_GUIDE}

FILL IN THE BLANK STANDARDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. BLANK FORMAT:
   ✓ Use exactly: _____ (5 underscores)
   ✓ Only ONE blank per question
   ✓ Blank should be a key term/concept (not articles/prepositions)
   ✓ Avoid blanks at sentence start

2. ANSWER FORMAT:
   ✓ Concise: 1-4 words typically
   ✓ Must appear verbatim in source text
   ✓ Should be important knowledge (not trivial)

3. CONTEXT CLUES:
   ✓ Sentence provides enough context to identify answer
   ✓ Grammatically complete when filled
   ✓ Not ambiguous (only one logical answer)

EXAMPLES WITH EDUCATIONAL ANALYSIS:

┌─────────────────────────────────────────────────────────────┐
│ 🟢 EASY EXAMPLE (Bloom's L1: Remember)                      │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "The first Prime Minister of India was _____.",
  "correct_answer": "Jawaharlal Nehru",
  "difficulty": "Easy",
  "blooms_level": "L1_Remember",
  "category": "{category}",
  "source_document": "modern_india.pdf",
  "source_page": 45,
  "rationale": "Basic historical fact recall"
}}

┌─────────────────────────────────────────────────────────────┐
│ 🟡 MEDIUM EXAMPLE (Bloom's L2: Understand)                  │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "The fundamental right that protects citizens from arbitrary arrest is the right to _____.",
  "correct_answer": "life and personal liberty",
  "difficulty": "Medium",
  "blooms_level": "L2_Understand",
  "category": "{category}",
  "source_document": "constitution.pdf",
  "source_page": 89,
  "rationale": "Requires understanding of constitutional rights terminology"
}}

┌─────────────────────────────────────────────────────────────┐
│ 🔴 HARD EXAMPLE (Bloom's L2: Understand Complex Terms)      │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "The economic system adopted by India after independence, which combines features of both capitalism and socialism, is known as a _____ economy.",
  "correct_answer": "mixed",
  "difficulty": "Hard",
  "blooms_level": "L2_Understand",
  "category": "{category}",
  "source_document": "economy.pdf",
  "source_page": 112,
  "rationale": "Technical economic terminology requiring conceptual understanding"
}}

JSON OUTPUT FORMAT (STRICT):
{{
  "questions": [
    {{
      "question_text": "Sentence with exactly one _____ blank.",
      "correct_answer": "Exact term from source (1-4 words)",
      "difficulty": "Easy|Medium|Hard",
      "blooms_level": "L1_Remember|L2_Understand",
      "category": "{category}",
      "source_document": "filename.pdf",
      "source_page": 123,
      "rationale": "Brief explanation"
    }}
  ]
}}

PRE-SUBMISSION CHECKLIST:
□ Generated exactly {count} questions ({easy_count} Easy, {medium_count} Medium, {hard_count} Hard)
□ Each question has exactly ONE blank (_____) 
□ All answers are 1-4 words
□ Every answer found verbatim in source text
□ Questions test important concepts (not trivial facts)
□ JSON syntax is valid

Generate {count} fill in the blank questions now:"""
    
    return prompt


# ============================================================================
# SHORT ANSWER PROMPT (Enhanced V3.0)
# ============================================================================

def create_short_answer_prompt_v3(context: str, category: str, count: int) -> str:
    """
    V3.0 Short Answer Prompt for Conceptual Understanding
    """
    
    easy_count = max(1, int(count * 0.3))
    medium_count = max(1, int(count * 0.5))
    hard_count = max(1, count - easy_count - medium_count)
    
    prompt = f"""{SYSTEM_PROMPT}

{HALLUCINATION_PREVENTION_INSTRUCTION}

═══════════════════════════════════════════════════════════════
📚 TEXTBOOK CONTENT - {category.upper()}
═══════════════════════════════════════════════════════════════

{context}

═══════════════════════════════════════════════════════════════
END OF SOURCE MATERIAL
═══════════════════════════════════════════════════════════════

🎯 TASK: Generate {count} Short Answer Questions

QUANTITY BREAKDOWN:
• {easy_count} Easy questions (definitions, simple explanations)
• {medium_count} Medium questions (cause-effect, comparisons)
• {hard_count} Hard questions (multi-faceted analysis)

TARGET LENGTH: 2-3 sentences (30-50 words)

{DIFFICULTY_GUIDE}

SHORT ANSWER STANDARDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. QUESTION DESIGN:
   ✓ Start with: Explain, Define, Describe, State, Compare, Discuss
   ✓ Focus on WHY and HOW (not just WHAT)
   ✓ Test understanding, not memorization
   ✓ Should have clear evaluation criteria

2. MODEL ANSWER:
   ✓ Length: 2-3 complete sentences
   ✓ Word count: 30-50 words
   ✓ Directly from source content
   ✓ Include key points for scoring
   ✓ Clear and concise

3. EDUCATIONAL VALUE:
   ✓ Prepares for concept application
   ✓ Develops articulation skills
   ✓ Tests comprehension depth

EXAMPLES WITH EDUCATIONAL ANALYSIS:

┌─────────────────────────────────────────────────────────────┐
│ 🟢 EASY EXAMPLE (Bloom's L2: Understand)                    │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "What is the significance of fundamental rights in the Indian Constitution?",
  "model_answer": "Fundamental rights are basic human rights guaranteed to all citizens by the Constitution. They protect individual freedoms such as equality, speech, and religion. These rights can be enforced through courts if violated.",
  "difficulty": "Easy",
  "blooms_level": "L2_Understand",
  "category": "{category}",
  "source_document": "constitution.pdf",
  "source_page": 78,
  "rationale": "Basic explanation requiring comprehension of constitutional concept"
}}

┌─────────────────────────────────────────────────────────────┐
│ 🟡 MEDIUM EXAMPLE (Bloom's L2-L3: Understand/Apply)         │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "Explain how the monsoon system affects agricultural practices in India.",
  "model_answer": "The monsoon brings 75% of India's annual rainfall during June-September, determining the planting and harvesting schedules for major crops. Farmers depend on timely monsoon arrival for kharif crops like rice and cotton. Failure or delay of monsoons can cause droughts, severely impacting agricultural productivity and rural livelihoods.",
  "difficulty": "Medium",
  "blooms_level": "L2_Understand",
  "category": "{category}",
  "source_document": "agriculture.pdf",
  "source_page": 134,
  "rationale": "Requires understanding cause-effect relationship between climate and agriculture"
}}

┌─────────────────────────────────────────────────────────────┐
│ 🔴 HARD EXAMPLE (Bloom's L3-L4: Apply/Analyze)              │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "Why is the separation of powers important for maintaining democracy?",
  "model_answer": "Separation of powers divides government authority among legislature, executive, and judiciary to prevent concentration and abuse of power. Each branch can check and balance the others, ensuring accountability. This protects individual freedoms and prevents authoritarian rule by any single branch.",
  "difficulty": "Hard",
  "blooms_level": "L3_Apply",
  "category": "{category}",
  "source_document": "governance.pdf",
  "source_page": 89,
  "rationale": "Requires analyzing institutional relationships and their democratic purpose"
}}

JSON OUTPUT FORMAT (STRICT):
{{
  "questions": [
    {{
      "question_text": "Question starting with Explain/Define/Describe?",
      "model_answer": "Complete 2-3 sentence answer from source (30-50 words).",
      "difficulty": "Easy|Medium|Hard",
      "blooms_level": "L2_Understand|L3_Apply|L4_Analyze",
      "category": "{category}",
      "source_document": "filename.pdf",
      "source_page": 123,
      "rationale": "Brief explanation"
    }}
  ]
}}

PRE-SUBMISSION CHECKLIST:
□ Generated exactly {count} questions ({easy_count} Easy, {medium_count} Medium, {hard_count} Hard)
□ Model answers are 2-3 sentences (30-50 words)
□ All content from source material
□ Questions test UNDERSTANDING (not just recall)
□ Answers provide clear evaluation criteria
□ JSON syntax is valid

Generate {count} short answer questions now:"""
    
    return prompt


# ============================================================================
# LONG ANSWER PROMPT (Enhanced V3.0)
# ============================================================================

def create_long_answer_prompt_v3(context: str, category: str, count: int) -> str:
    """
    V3.0 Long Answer Prompt for Analytical Essays
    """
    
    easy_count = max(1, int(count * 0.3))
    medium_count = max(1, int(count * 0.5))
    hard_count = max(1, count - easy_count - medium_count)
    
    prompt = f"""{SYSTEM_PROMPT}

{HALLUCINATION_PREVENTION_INSTRUCTION}

═══════════════════════════════════════════════════════════════
📚 TEXTBOOK CONTENT - {category.upper()}
═══════════════════════════════════════════════════════════════

{context}

═══════════════════════════════════════════════════════════════
END OF SOURCE MATERIAL
═══════════════════════════════════════════════════════════════

🎯 TASK: Generate {count} Long Answer Questions

QUANTITY BREAKDOWN:
• {easy_count} Easy questions (comprehensive descriptions)
• {medium_count} Medium questions (cause-effect analysis)
• {hard_count} Hard questions (synthesis, evaluation)

TARGET LENGTH: 5-6 sentences (100-150 words)

{DIFFICULTY_GUIDE}

LONG ANSWER STANDARDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. QUESTION DESIGN:
   ✓ Use: Discuss, Analyze, Examine, Evaluate, Compare and Contrast
   ✓ Require integration of multiple concepts
   ✓ Encourage structured logical arguments
   ✓ Test higher-order thinking

2. MODEL ANSWER:
   ✓ Structure: Introduction + main points + conclusion
   ✓ Length: 5-6 complete sentences
   ✓ Word count: 100-150 words
   ✓ Cover multiple aspects comprehensively
   ✓ Based entirely on source synthesis

3. EDUCATIONAL VALUE:
   ✓ Test ability to organize knowledge
   ✓ Evaluate depth of understanding
   ✓ Assess analytical thinking
   ✓ Prepare for board exams

EXAMPLES WITH EDUCATIONAL ANALYSIS:

┌─────────────────────────────────────────────────────────────┐
│ 🟢 EASY EXAMPLE (Bloom's L2-L3: Understand/Apply)           │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "Describe the main features of the Indian Constitution.",
  "model_answer": "The Indian Constitution is the supreme law that establishes India as a sovereign, socialist, secular, and democratic republic. It guarantees fundamental rights to all citizens, including equality, freedom, and protection against exploitation. The Constitution creates a federal structure with clear division of powers between central and state governments. It includes Directive Principles of State Policy to guide governance toward social welfare. The document provides for an independent judiciary to interpret laws and protect citizens' rights. Additionally, it contains provisions for amendments to evolve with changing societal needs.",
  "difficulty": "Easy",
  "blooms_level": "L2_Understand",
  "category": "{category}",
  "source_document": "constitution.pdf",
  "source_page": 23,
  "rationale": "Comprehensive description requiring organization of multiple constitutional features"
}}

┌─────────────────────────────────────────────────────────────┐
│ 🟡 MEDIUM EXAMPLE (Bloom's L3-L4: Apply/Analyze)            │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "Analyze the causes and consequences of the French Revolution.",
  "model_answer": "The French Revolution was triggered by multiple interconnected causes. The oppressive feudal system and absolute monarchy created severe social inequality between estates. Economic crisis from war debts and poor harvests led to widespread poverty and hunger. Enlightenment ideas promoting liberty and equality inspired calls for reform. The immediate trigger was the financial crisis forcing King Louis XVI to convene the Estates-General. The Revolution's consequences were profound: it abolished feudalism and established principles of liberty, equality, and fraternity that spread across Europe. It also led to Napoleon's rise and fundamentally transformed political systems worldwide.",
  "difficulty": "Medium",
  "blooms_level": "L4_Analyze",
  "category": "{category}",
  "source_document": "revolutions.pdf",
  "source_page": 145,
  "rationale": "Requires analysis of cause-effect relationships and historical significance"
}}

┌─────────────────────────────────────────────────────────────┐
│ 🔴 HARD EXAMPLE (Bloom's L4-L5: Analyze/Evaluate)           │
└─────────────────────────────────────────────────────────────┘
{{
  "question_text": "Evaluate the significance of India's Non-Aligned Movement during the Cold War era.",
  "model_answer": "The Non-Aligned Movement (NAM), initiated by India under Nehru's leadership, represented a strategic rejection of both US and Soviet bloc alignment during the Cold War. It allowed newly independent nations to maintain sovereignty while avoiding superpower pressures and conflicts. NAM provided a platform for addressing common concerns like decolonization, economic development, and peaceful coexistence. However, its practical impact was limited as economic dependencies often forced informal alignments with superpowers. Despite these limitations, NAM successfully promoted dialogue between developing nations and gave them a collective voice in international affairs. Its legacy continues in contemporary multilateral diplomacy, emphasizing the importance of independent foreign policy for developing nations.",
  "difficulty": "Hard",
  "blooms_level": "L5_Evaluate",
  "category": "{category}",
  "source_document": "cold_war.pdf",
  "source_page": 234,
  "rationale": "Requires critical evaluation of movement's achievements and limitations with historical context"
}}

JSON OUTPUT FORMAT (STRICT):
{{
  "questions": [
    {{
      "question_text": "Analytical question starting with Discuss/Analyze/Evaluate?",
      "model_answer": "Comprehensive 5-6 sentence answer (100-150 words) with clear structure.",
      "difficulty": "Easy|Medium|Hard",
      "blooms_level": "L2_Understand|L3_Apply|L4_Analyze|L5_Evaluate",
      "category": "{category}",
      "source_document": "filename.pdf",
      "source_page": 123,
      "rationale": "Brief explanation"
    }}
  ]
}}

PRE-SUBMISSION CHECKLIST:
□ Generated exactly {count} questions ({easy_count} Easy, {medium_count} Medium, {hard_count} Hard)
□ Model answers are 5-6 sentences (100-150 words)
□ All content synthesized from source material
□ Questions require ANALYSIS/SYNTHESIS/EVALUATION
□ Answers have clear structure (intro + points + conclusion)
□ JSON syntax is valid

Generate {count} long answer questions now:"""
    
    return prompt


# ============================================================================
# PROMPT SELECTOR (Updated for V3.0)
# ============================================================================

def select_prompt_v3(
    question_type: str,
    context: str,
    category: str,
    count: int
) -> str:
    """
    Select appropriate V3.0 prompt based on question type
    
    Args:
        question_type: Type of question (MCQ, FILL_BLANKS, SHORT_ANSWER, LONG_ANSWER)
        context: Retrieved textbook content
        category: Subject category
        count: Number of questions
        
    Returns:
        Formatted V3.0 prompt string
    """
    if question_type == "MCQ":
        return create_mcq_prompt_v3(context, category, count)
    elif question_type == "FILL_BLANKS":
        return create_fill_blank_prompt_v3(context, category, count)
    elif question_type == "SHORT_ANSWER":
        return create_short_answer_prompt_v3(context, category, count)
    elif question_type == "LONG_ANSWER":
        return create_long_answer_prompt_v3(context, category, count)
    else:
        raise ValueError(f"Unsupported question type: {question_type}")
