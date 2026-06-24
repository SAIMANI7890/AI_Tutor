"""
Enhanced Question Generation Prompts - Educational Assessment Framework
========================================================================

This module implements a sophisticated prompt engineering strategy for generating
high-quality educational assessments aligned with Bloom's Taxonomy and 
secondary school curriculum standards.

Key Features:
- Bloom's Taxonomy alignment
- Hallucination prevention
- Difficulty calibration (Easy 30%, Medium 50%, Hard 20%)
- Multi-concept coverage
- Source attribution
- Educational best practices
"""
from typing import Dict, List


# ============================================================================
# SYSTEM PROMPT - Core Instructions for the AI
# ============================================================================

SYSTEM_PROMPT = """You are an expert educational assessment designer specializing in creating high-quality examination questions for Class 10 (secondary school) students in Social Studies.

YOUR ROLE:
- Create pedagogically sound questions that test understanding, not just recall
- Align questions with Bloom's Taxonomy (Remember, Understand, Apply, Analyze)
- Ensure all content is strictly derived from provided textbook excerpts
- Follow secondary school assessment standards
- Design questions that promote deep learning

CORE PRINCIPLES:
1. **Source Fidelity**: Generate questions ONLY from the provided textbook content. Never use external knowledge or make assumptions.
2. **Educational Value**: Each question should test conceptual understanding, not mere memorization.
3. **Age Appropriateness**: Language and complexity must match Class 10 student level (14-16 years old).
4. **Cognitive Diversity**: Mix different cognitive levels according to difficulty distribution.
5. **Factual Accuracy**: Every answer must be explicitly stated or clearly inferrable from the source text.

STRICTLY FORBIDDEN:
❌ Inventing facts not in the source material
❌ Using information from your general knowledge
❌ Creating questions that cannot be answered from the provided context
❌ Generating ambiguous or trick questions
❌ Using outdated or incorrect information

OUTPUT REQUIREMENTS:
- Return valid JSON only (no markdown, no explanations)
- Include source attribution (document name, page number)
- Classify difficulty accurately (Easy, Medium, Hard)
- Ensure questions are independent (no inter-dependencies)
- Avoid repetitive question patterns"""


# ============================================================================
# CONTEXT FORMATTING STRATEGY
# ============================================================================

def format_context_for_assessment(chunks: List[Dict], category: str) -> str:
    """
    Format retrieved RAG chunks into a structured context for question generation.
    
    Strategy:
    - Group by document and page for logical flow
    - Add clear source markers for attribution
    - Include metadata for hallucination prevention
    - Provide sufficient context for understanding
    
    Args:
        chunks: Retrieved chunks from RAG system
        category: Subject category (History, Geography, Politics, Economics)
        
    Returns:
        Formatted context string optimized for LLM consumption
    """
    if not chunks:
        return ""
    
    context_parts = [
        f"TEXTBOOK EXCERPTS - {category.upper()}",
        "=" * 70,
        "",
        "INSTRUCTIONS: Use ONLY the information below to generate questions.",
        "Each excerpt is marked with its source document and page number.",
        "Do not use any information outside these excerpts.",
        ""
    ]
    
    for i, chunk in enumerate(chunks, start=1):
        metadata = chunk.get("metadata", {})
        text = chunk.get("text", "")
        
        source_info = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXCERPT #{i}
Source: {metadata.get('document_name', 'Unknown')}
Page: {metadata.get('page_number', 'N/A')}
Category: {metadata.get('category', category)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{text}
"""
        context_parts.append(source_info)
    
    context_parts.append("\n" + "=" * 70)
    context_parts.append("END OF TEXTBOOK EXCERPTS")
    context_parts.append("")
    
    return "\n".join(context_parts)


# ============================================================================
# BLOOM'S TAXONOMY MAPPING
# ============================================================================

BLOOMS_TAXONOMY_GUIDE = """
BLOOM'S TAXONOMY FOR QUESTION DESIGN:

Level 1 - REMEMBER (Knowledge):
  Verbs: Define, List, Name, Identify, State, Label
  Difficulty: Easy
  Question Types: MCQ (factual), Fill in Blanks, Short Answer (definitions)
  Example: "Who was the first Prime Minister of India?"

Level 2 - UNDERSTAND (Comprehension):
  Verbs: Explain, Describe, Summarize, Interpret, Compare, Classify
  Difficulty: Easy to Medium
  Question Types: MCQ (conceptual), Short Answer, Long Answer
  Example: "Explain the main features of the Indian Constitution."

Level 3 - APPLY (Application):
  Verbs: Apply, Demonstrate, Solve, Use, Illustrate, Calculate
  Difficulty: Medium
  Question Types: MCQ (scenario-based), Short Answer, Long Answer
  Example: "How would democratic principles apply to resolving a local dispute?"

Level 4 - ANALYZE (Analysis):
  Verbs: Analyze, Compare, Contrast, Examine, Differentiate, Investigate
  Difficulty: Medium to Hard
  Question Types: Long Answer, Short Answer, MCQ (analytical)
  Example: "Analyze the causes and effects of the French Revolution."

DISTRIBUTION FOR CLASS 10:
- 30% Easy (Remember + basic Understand)
- 50% Medium (Understand + Apply)
- 20% Hard (Analyze + complex Apply)
"""


# ============================================================================
# MCQ GENERATION PROMPT
# ============================================================================

def create_enhanced_mcq_prompt(context: str, category: str, count: int) -> str:
    """
    Generate MCQ prompt with educational assessment best practices.
    
    Strategy:
    - Bloom's Level 1-3 focus (Remember, Understand, Apply)
    - Plausible distractors (wrong options)
    - No "all of the above" or "none of the above"
    - Clear, unambiguous stems
    - Options of similar length and structure
    """
    
    prompt = f"""{SYSTEM_PROMPT}

{BLOOMS_TAXONOMY_GUIDE}

{context}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK: Generate {count} Multiple Choice Questions (MCQs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CATEGORY: {category}
STUDENT LEVEL: Class 10 (Ages 14-16)
COGNITIVE FOCUS: Remember, Understand, Apply

DIFFICULTY DISTRIBUTION (REQUIRED):
- {int(count * 0.3)} Easy questions (Bloom's Level 1-2, direct recall/basic understanding)
- {int(count * 0.5)} Medium questions (Bloom's Level 2-3, concept application)
- {int(count * 0.2)} Hard questions (Bloom's Level 3-4, analysis/synthesis)

MCQ BEST PRACTICES:
1. **Question Stem**: 
   - Clear, complete, and focused on one concept
   - Avoid negative phrasing unless absolutely necessary
   - Can be answered without looking at options (if possible)

2. **Options**:
   - Exactly 4 options (A, B, C, D)
   - All options must be plausible (no obviously wrong "joke" options)
   - Similar length and grammatical structure
   - Only ONE correct answer
   - Distractors should reflect common misconceptions

3. **Difficulty Calibration**:
   - Easy: Direct textbook facts, definitions, single-concept recall
   - Medium: Requires understanding relationships, cause-effect, comparisons
   - Hard: Requires analysis, synthesis of multiple concepts, application

4. **Source Attribution**:
   - Use information from the excerpts above
   - Note the specific document name and page number
   - If answer spans multiple excerpts, cite the primary source

QUESTION DESIGN CHECKLIST:
✓ Does the question have educational value?
✓ Is the answer explicitly stated or clearly inferrable from the source?
✓ Are all distractors plausible and based on content?
✓ Is the language age-appropriate for Class 10?
✓ Does the question test understanding, not just memorization?
✓ Are options free from clues (length patterns, grammar mismatches)?

FEW-SHOT EXAMPLES:

EXAMPLE 1 - Easy (Bloom's Level 1 - Remember):
{{
  "question_text": "Who introduced the Doctrine of Lapse in India?",
  "options": [
    "Lord Dalhousie",
    "Lord Wellesley",
    "Lord Curzon",
    "Lord Mountbatten"
  ],
  "correct_answer": "Lord Dalhousie",
  "difficulty": "Easy",
  "bloom_level": "Remember",
  "category": "{category}",
  "source_document": "modern_india.pdf",
  "source_page": 45,
  "explanation": "Direct factual recall from textbook."
}}

EXAMPLE 2 - Medium (Bloom's Level 2 - Understand):
{{
  "question_text": "What was the primary objective of the Non-Cooperation Movement launched by Mahatma Gandhi?",
  "options": [
    "To achieve complete independence through non-violent resistance",
    "To demand better economic policies from the British",
    "To establish a separate Muslim state",
    "To reform the Indian social structure"
  ],
  "correct_answer": "To achieve complete independence through non-violent resistance",
  "difficulty": "Medium",
  "bloom_level": "Understand",
  "category": "{category}",
  "source_document": "freedom_struggle.pdf",
  "source_page": 78,
  "explanation": "Requires understanding of historical movements and their goals."
}}

EXAMPLE 3 - Hard (Bloom's Level 3 - Apply):
{{
  "question_text": "If the Indian Constitution's federal structure were to be applied to resolve a resource conflict between two states, which provision would be MOST relevant?",
  "options": [
    "Article 263 - Interstate Council for coordination",
    "Article 370 - Special status provisions",
    "Article 356 - President's Rule",
    "Article 368 - Amendment procedures"
  ],
  "correct_answer": "Article 263 - Interstate Council for coordination",
  "difficulty": "Hard",
  "bloom_level": "Apply",
  "category": "{category}",
  "source_document": "indian_constitution.pdf",
  "source_page": 112,
  "explanation": "Requires applying constitutional knowledge to a practical scenario."
}}

JSON OUTPUT SCHEMA:
{{
  "questions": [
    {{
      "question_text": "Clear, complete question here?",
      "options": [
        "Option A - First plausible answer",
        "Option B - Second plausible answer",
        "Option C - Third plausible answer",
        "Option D - Fourth plausible answer"
      ],
      "correct_answer": "Option A - First plausible answer",
      "difficulty": "Easy|Medium|Hard",
      "bloom_level": "Remember|Understand|Apply|Analyze",
      "category": "{category}",
      "source_document": "document_name.pdf",
      "source_page": 45,
      "explanation": "Brief note on why this tests the concept (internal use)"
    }}
  ]
}}

CRITICAL REMINDERS:
- Generate EXACTLY {count} questions
- Maintain difficulty distribution: 30% Easy, 50% Medium, 20% Hard
- ALL content must be from the excerpts above
- Return ONLY valid JSON (no markdown code blocks)
- Each question must be independently answerable
- Avoid repetitive patterns across questions

Generate the questions now:"""
    
    return prompt


# ============================================================================
# FILL IN THE BLANKS PROMPT
# ============================================================================

def create_enhanced_fill_blank_prompt(context: str, category: str, count: int) -> str:
    """
    Generate Fill in the Blanks prompt optimized for key term assessment.
    
    Strategy:
    - Test key vocabulary and concepts
    - Blank should be a significant word, not trivial
    - Context should provide sufficient clues
    - Answer should be 1-4 words typically
    """
    
    prompt = f"""{SYSTEM_PROMPT}

{BLOOMS_TAXONOMY_GUIDE}

{context}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK: Generate {count} Fill in the Blanks Questions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CATEGORY: {category}
STUDENT LEVEL: Class 10 (Ages 14-16)
COGNITIVE FOCUS: Remember, Understand (Bloom's Level 1-2)

DIFFICULTY DISTRIBUTION (REQUIRED):
- {int(count * 0.3)} Easy (Well-known terms, capitals, dates, names)
- {int(count * 0.5)} Medium (Concepts, definitions, relationships)
- {int(count * 0.2)} Hard (Technical terms, complex concepts)

FILL IN THE BLANK BEST PRACTICES:
1. **Blank Placement**:
   - Mark blank with exactly 5 underscores: _____
   - Place blank in a position that tests key knowledge
   - Avoid blanks at the beginning of sentences (harder to parse)
   - Only ONE blank per question

2. **Answer Format**:
   - Should be 1-4 words typically (concise)
   - Must be explicitly mentioned in the source text
   - Should be a significant term, not articles/prepositions
   - Accept reasonable variations (e.g., "democracy" vs "democratic system")

3. **Context Quality**:
   - Sentence should provide sufficient clues
   - Should test terminology, not just completion ability
   - Grammatically correct when blank is filled

4. **Difficulty Calibration**:
   - Easy: Common terms, widely known facts (capitals, famous people)
   - Medium: Important concepts, definitions, key relationships
   - Hard: Technical terminology, complex concepts, lesser-known facts

FEW-SHOT EXAMPLES:

EXAMPLE 1 - Easy (Bloom's Level 1):
{{
  "question_text": "The capital of India is _____.",
  "correct_answer": "New Delhi",
  "difficulty": "Easy",
  "bloom_level": "Remember",
  "category": "{category}",
  "source_document": "indian_geography.pdf",
  "source_page": 12,
  "explanation": "Basic geographical fact recall."
}}

EXAMPLE 2 - Medium (Bloom's Level 2):
{{
  "question_text": "The Indian Constitution guarantees six fundamental rights, including the right to _____ which allows citizens to challenge unlawful detention.",
  "correct_answer": "Constitutional Remedies",
  "difficulty": "Medium",
  "bloom_level": "Understand",
  "category": "{category}",
  "source_document": "constitution_basics.pdf",
  "source_page": 67,
  "explanation": "Tests understanding of constitutional rights and their purposes."
}}

EXAMPLE 3 - Hard (Bloom's Level 2):
{{
  "question_text": "The economic policy followed by India immediately after independence, which involved government control over major industries, is known as _____.",
  "correct_answer": "Mixed Economy",
  "difficulty": "Hard",
  "bloom_level": "Understand",
  "category": "{category}",
  "source_document": "economic_development.pdf",
  "source_page": 89,
  "explanation": "Tests knowledge of technical economic terminology."
}}

JSON OUTPUT SCHEMA:
{{
  "questions": [
    {{
      "question_text": "Complete sentence with _____ in the middle or end.",
      "correct_answer": "The missing word or phrase (1-4 words)",
      "difficulty": "Easy|Medium|Hard",
      "bloom_level": "Remember|Understand",
      "category": "{category}",
      "source_document": "document_name.pdf",
      "source_page": 45,
      "explanation": "Why this blank tests important knowledge"
    }}
  ]
}}

CRITICAL REMINDERS:
- Generate EXACTLY {count} questions
- Maintain difficulty distribution: 30% Easy, 50% Medium, 20% Hard
- Each blank should test a KEY term or concept
- Answer must be explicitly in the source excerpts
- Use exactly _____ (5 underscores) for blanks
- Return ONLY valid JSON (no markdown)

Generate the questions now:"""
    
    return prompt


# ============================================================================
# SHORT ANSWER PROMPT
# ============================================================================

def create_enhanced_short_answer_prompt(context: str, category: str, count: int) -> str:
    """
    Generate Short Answer prompt for explanation and definition questions.
    
    Strategy:
    - 2-3 sentence answers (30-50 words)
    - Test understanding, not just recall
    - Require explanation, not just listing
    - Clear evaluation criteria
    """
    
    prompt = f"""{SYSTEM_PROMPT}

{BLOOMS_TAXONOMY_GUIDE}

{context}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK: Generate {count} Short Answer Questions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CATEGORY: {category}
STUDENT LEVEL: Class 10 (Ages 14-16)
COGNITIVE FOCUS: Understand, Apply (Bloom's Level 2-3)
EXPECTED ANSWER LENGTH: 2-3 sentences (30-50 words)

DIFFICULTY DISTRIBUTION (REQUIRED):
- {int(count * 0.3)} Easy (Simple explanations, definitions)
- {int(count * 0.5)} Medium (Concept relationships, comparisons, cause-effect)
- {int(count * 0.2)} Hard (Multi-faceted explanations, analysis)

SHORT ANSWER BEST PRACTICES:
1. **Question Design**:
   - Begin with action verbs: Explain, Define, Describe, Compare, State
   - Focus on WHY and HOW, not just WHAT
   - Should require understanding, not just memorization
   - Clear and specific about what's being asked

2. **Model Answer**:
   - 2-3 complete sentences
   - 30-50 words typically
   - Include key points that demonstrate understanding
   - Based entirely on source excerpts
   - Serve as evaluation rubric for teachers

3. **Difficulty Calibration**:
   - Easy: Simple definitions, basic explanations
   - Medium: Cause-effect, comparisons, multi-point descriptions
   - Hard: Complex concepts, analysis, synthesis of ideas

4. **Educational Value**:
   - Should prepare students for concept application
   - Encourage articulation of understanding
   - Bridge between recall and analysis

FEW-SHOT EXAMPLES:

EXAMPLE 1 - Easy (Bloom's Level 2 - Understand):
{{
  "question_text": "What is democracy?",
  "model_answer": "Democracy is a system of government in which power is vested in the people, who exercise it directly or through elected representatives. It is characterized by free and fair elections, protection of individual rights, and rule of law.",
  "difficulty": "Easy",
  "bloom_level": "Understand",
  "category": "{category}",
  "source_document": "political_systems.pdf",
  "source_page": 34,
  "explanation": "Tests basic understanding of a fundamental political concept.",
  "key_points": ["power from people", "elected representatives", "free elections", "rights protection"]
}}

EXAMPLE 2 - Medium (Bloom's Level 2-3):
{{
  "question_text": "Explain how the monsoon system affects Indian agriculture.",
  "model_answer": "The monsoon brings the majority of India's annual rainfall during June-September, which is critical for irrigation and crop cultivation. This seasonal pattern determines planting and harvesting schedules for major crops like rice and wheat. Failure or delay of monsoons can lead to droughts and severely impact agricultural productivity.",
  "difficulty": "Medium",
  "bloom_level": "Understand",
  "category": "{category}",
  "source_document": "indian_climate.pdf",
  "source_page": 56,
  "explanation": "Requires understanding of cause-effect relationships between climate and agriculture.",
  "key_points": ["seasonal rainfall", "irrigation importance", "crop scheduling", "drought risk"]
}}

EXAMPLE 3 - Hard (Bloom's Level 3 - Apply):
{{
  "question_text": "Why is the separation of powers important in a democratic government?",
  "model_answer": "Separation of powers divides government authority among the legislature, executive, and judiciary to prevent concentration of power and potential abuse. This system creates checks and balances where each branch can limit the others, protecting individual freedoms. It ensures accountability and prevents tyranny by distributing decision-making authority.",
  "difficulty": "Hard",
  "bloom_level": "Apply",
  "category": "{category}",
  "source_document": "governance_principles.pdf",
  "source_page": 78,
  "explanation": "Requires analysis of democratic principles and their practical importance.",
  "key_points": ["power distribution", "checks and balances", "prevents abuse", "ensures accountability"]
}}

JSON OUTPUT SCHEMA:
{{
  "questions": [
    {{
      "question_text": "Clear question starting with Explain/Define/Describe/etc.?",
      "model_answer": "Complete answer in 2-3 sentences (30-50 words) based on source material.",
      "difficulty": "Easy|Medium|Hard",
      "bloom_level": "Understand|Apply",
      "category": "{category}",
      "source_document": "document_name.pdf",
      "source_page": 45,
      "explanation": "Why this tests conceptual understanding",
      "key_points": ["point 1", "point 2", "point 3"]
    }}
  ]
}}

CRITICAL REMINDERS:
- Generate EXACTLY {count} questions
- Maintain difficulty distribution: 30% Easy, 50% Medium, 20% Hard
- Model answers must be 2-3 sentences, 30-50 words
- All content from source excerpts only
- Questions should test UNDERSTANDING, not just recall
- Include key_points for evaluation guidance
- Return ONLY valid JSON

Generate the questions now:"""
    
    return prompt


# ============================================================================
# LONG ANSWER PROMPT
# ============================================================================

def create_enhanced_long_answer_prompt(context: str, category: str, count: int) -> str:
    """
    Generate Long Answer prompt for comprehensive essay-type questions.
    
    Strategy:
    - 5-6 sentence answers (100-150 words)
    - Test analysis, synthesis, evaluation
    - Require structured arguments
    - Multi-concept integration
    """
    
    prompt = f"""{SYSTEM_PROMPT}

{BLOOMS_TAXONOMY_GUIDE}

{context}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK: Generate {count} Long Answer Questions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CATEGORY: {category}
STUDENT LEVEL: Class 10 (Ages 14-16)
COGNITIVE FOCUS: Analyze, Evaluate (Bloom's Level 3-4)
EXPECTED ANSWER LENGTH: 5-6 sentences (100-150 words)

DIFFICULTY DISTRIBUTION (REQUIRED):
- {int(count * 0.3)} Easy (Comprehensive descriptions with multiple points)
- {int(count * 0.5)} Medium (Analysis of causes/effects, comparisons)
- {int(count * 0.2)} Hard (Synthesis across concepts, critical evaluation)

LONG ANSWER BEST PRACTICES:
1. **Question Design**:
   - Use verbs: Discuss, Analyze, Examine, Evaluate, Compare and Contrast
   - Should require integration of multiple concepts
   - Encourage structured, logical argumentation
   - Clear about scope and expectations

2. **Model Answer**:
   - 5-6 complete sentences
   - 100-150 words
   - Structured with introduction, main points, conclusion
   - Cover multiple aspects comprehensively
   - Based entirely on source material

3. **Difficulty Calibration**:
   - Easy: Multi-point descriptions, comprehensive listings
   - Medium: Cause-effect analysis, comparisons, historical narratives
   - Hard: Critical analysis, synthesis, evaluation of significance

4. **Assessment Value**:
   - Test ability to organize and present knowledge
   - Evaluate depth of understanding
   - Assess analytical and critical thinking skills
   - Check for conceptual integration

FEW-SHOT EXAMPLES:

EXAMPLE 1 - Easy (Bloom's Level 2-3):
{{
  "question_text": "Describe the main features of the Indian Constitution.",
  "model_answer": "The Indian Constitution is the supreme law of India, establishing the country as a sovereign, socialist, secular, and democratic republic. It guarantees fundamental rights to all citizens, including equality, freedom, and protection against exploitation. The Constitution establishes a federal structure with clear division of powers between the central and state governments. It includes Directive Principles of State Policy to guide governance towards social welfare. The Constitution also provides for an independent judiciary to interpret laws and protect citizens' rights. Additionally, it includes provisions for amendments, allowing it to evolve with changing times while maintaining its core principles.",
  "difficulty": "Easy",
  "bloom_level": "Understand",
  "category": "{category}",
  "source_document": "constitution_structure.pdf",
  "source_page": 23,
  "explanation": "Requires comprehensive description of multiple constitutional features.",
  "key_points": ["supreme law", "fundamental rights", "federal structure", "directive principles", "independent judiciary", "amendment provisions"]
}}

EXAMPLE 2 - Medium (Bloom's Level 3):
{{
  "question_text": "Analyze the causes and effects of the French Revolution.",
  "model_answer": "The French Revolution was primarily caused by the oppressive feudal system, economic crisis from war debts, and the influence of Enlightenment ideas promoting equality and liberty. The monarchy's absolute power and the stark inequality between social classes created widespread discontent among the common people. The immediate trigger was the financial crisis that forced King Louis XVI to call the Estates-General. The Revolution's effects were far-reaching, abolishing feudalism and establishing the principles of liberty, equality, and fraternity. It inspired democratic movements worldwide and led to the rise of Napoleon Bonaparte. The Revolution fundamentally transformed French society and influenced the development of modern democratic governance systems globally.",
  "difficulty": "Medium",
  "bloom_level": "Analyze",
  "category": "{category}",
  "source_document": "european_revolutions.pdf",
  "source_page": 145,
  "explanation": "Requires analysis of multiple causes and their interconnected effects.",
  "key_points": ["feudal oppression", "economic crisis", "Enlightenment influence", "feudalism abolished", "democratic principles", "global impact"]
}}

EXAMPLE 3 - Hard (Bloom's Level 4):
{{
  "question_text": "Evaluate the significance of the Non-Aligned Movement in the context of the Cold War era.",
  "model_answer": "The Non-Aligned Movement (NAM), initiated by India and other developing nations, represented a strategic rejection of both US and Soviet bloc alignment during the Cold War. It allowed newly independent countries to maintain sovereignty while avoiding the pressures of choosing between superpowers. NAM provided a platform for developing nations to address common concerns like decolonization, economic development, and racial discrimination. However, its practical impact was limited as many member nations still maintained informal alignments based on economic and military needs. Despite these limitations, NAM successfully promoted the concept of peaceful coexistence and provided a collective voice for the Global South in international affairs. Its legacy continues in contemporary multilateral diplomacy, emphasizing the importance of independent foreign policy for developing nations.",
  "difficulty": "Hard",
  "bloom_level": "Evaluate",
  "category": "{category}",
  "source_document": "cold_war_dynamics.pdf",
  "source_page": 234,
  "explanation": "Requires critical evaluation of historical significance with balanced perspective.",
  "key_points": ["strategic independence", "sovereignty preservation", "developing nations platform", "practical limitations", "peaceful coexistence", "lasting legacy"]
}}

JSON OUTPUT SCHEMA:
{{
  "questions": [
    {{
      "question_text": "Clear analytical/evaluative question starting with Discuss/Analyze/Examine?",
      "model_answer": "Comprehensive answer in 5-6 sentences (100-150 words) with clear structure and multiple points.",
      "difficulty": "Easy|Medium|Hard",
      "bloom_level": "Understand|Apply|Analyze|Evaluate",
      "category": "{category}",
      "source_document": "document_name.pdf",
      "source_page": 45,
      "explanation": "Why this tests higher-order thinking",
      "key_points": ["point 1", "point 2", "point 3", "point 4", "point 5"]
    }}
  ]
}}

CRITICAL REMINDERS:
- Generate EXACTLY {count} questions
- Maintain difficulty distribution: 30% Easy, 50% Medium, 20% Hard
- Model answers must be 5-6 sentences, 100-150 words
- All content from source excerpts only
- Questions should require ANALYSIS and SYNTHESIS
- Structure answers with clear progression of ideas
- Include key_points for comprehensive evaluation
- Return ONLY valid JSON

Generate the questions now:"""
    
    return prompt


# ============================================================================
# PROMPT SELECTOR
# ============================================================================

def select_enhanced_prompt(
    question_type: str,
    formatted_context: str,
    category: str,
    count: int
) -> str:
    """
    Select the appropriate enhanced prompt based on question type.
    
    Args:
        question_type: MCQ, FILL_BLANKS, SHORT_ANSWER, or LONG_ANSWER
        formatted_context: Pre-formatted textbook excerpts
        category: Subject category
        count: Number of questions to generate
        
    Returns:
        Complete prompt string optimized for educational quality
    """
    prompt_map = {
        "MCQ": create_enhanced_mcq_prompt,
        "FILL_BLANKS": create_enhanced_fill_blank_prompt,
        "SHORT_ANSWER": create_enhanced_short_answer_prompt,
        "LONG_ANSWER": create_enhanced_long_answer_prompt,
    }
    
    prompt_generator = prompt_map.get(question_type)
    if not prompt_generator:
        raise ValueError(f"Unsupported question type: {question_type}")
    
    return prompt_generator(formatted_context, category, count)
