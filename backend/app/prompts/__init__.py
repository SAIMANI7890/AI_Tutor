"""
Examination Prompt Module
=========================
Canonical entry point for all examination question generation prompts.

This module re-exports the production V3 prompt system which provides:
  • Bloom's Taxonomy alignment (L1 Remember → L5 Evaluate)
  • 5-Layer Hallucination Prevention Protocol
  • Difficulty Distribution: 30% Easy | 50% Medium | 20% Hard
  • Source Attribution Verification
  • Few-Shot Examples for each question type
  • Quality Pre-Submission Checklists

Usage
-----
    from app.prompts.examination_prompt import select_prompt, SYSTEM_PROMPT

    prompt = select_prompt(
        question_type="MCQ",
        context="<retrieved textbook chunks>",
        category="History",
        count=5,
    )

Public API
----------
    select_prompt(question_type, context, category, count) -> str
    SYSTEM_PROMPT                                           -> str
    HALLUCINATION_PREVENTION_INSTRUCTION                    -> str
    DIFFICULTY_GUIDE                                        -> str
    create_mcq_prompt(context, category, count)             -> str
    create_fill_blank_prompt(context, category, count)      -> str
    create_short_answer_prompt(context, category, count)    -> str
    create_long_answer_prompt(context, category, count)     -> str
"""

from app.services.question_generation.prompts_v3 import (
    # Selector — recommended entry point for the generator
    select_prompt_v3 as select_prompt,

    # Building blocks (useful for testing / custom prompts)
    SYSTEM_PROMPT,
    HALLUCINATION_PREVENTION_INSTRUCTION,
    DIFFICULTY_GUIDE,

    # Per-type factory functions
    create_mcq_prompt_v3 as create_mcq_prompt,
    create_fill_blank_prompt_v3 as create_fill_blank_prompt,
    create_short_answer_prompt_v3 as create_short_answer_prompt,
    create_long_answer_prompt_v3 as create_long_answer_prompt,
)

__all__ = [
    "select_prompt",
    "SYSTEM_PROMPT",
    "HALLUCINATION_PREVENTION_INSTRUCTION",
    "DIFFICULTY_GUIDE",
    "create_mcq_prompt",
    "create_fill_blank_prompt",
    "create_short_answer_prompt",
    "create_long_answer_prompt",
]


# ---------------------------------------------------------------------------
# Convenience constants — useful for documentation and tests
# ---------------------------------------------------------------------------

SUPPORTED_QUESTION_TYPES = ("MCQ", "FILL_BLANKS", "SHORT_ANSWER", "LONG_ANSWER")

DIFFICULTY_DISTRIBUTION = {
    "Easy":   0.30,   # Bloom's L1-L2: Remember, Understand
    "Medium": 0.50,   # Bloom's L2-L3: Understand, Apply
    "Hard":   0.20,   # Bloom's L3-L5: Apply, Analyze, Evaluate
}

BLOOMS_LEVELS = {
    "L1_Remember":  "Direct recall of facts from source",
    "L2_Understand": "Comprehension and paraphrasing of concepts",
    "L3_Apply":     "Application of knowledge to new situations",
    "L4_Analyze":   "Breaking down concepts into components",
    "L5_Evaluate":  "Making judgements based on criteria",
}
