"""
Examination Prompt Module — Public Entry Point
==============================================
Import from here rather than reaching into the question_generation sub-package.

Example
-------
    from app.prompts.examination_prompt import select_prompt

    prompt = select_prompt("MCQ", context, "History", count=5)
"""

# Re-export everything from the package __init__ so callers can choose
# either import path:
#   from app.prompts.examination_prompt import select_prompt
#   from app.prompts import select_prompt
from app.prompts import (  # noqa: F401
    select_prompt,
    SYSTEM_PROMPT,
    HALLUCINATION_PREVENTION_INSTRUCTION,
    DIFFICULTY_GUIDE,
    create_mcq_prompt,
    create_fill_blank_prompt,
    create_short_answer_prompt,
    create_long_answer_prompt,
    SUPPORTED_QUESTION_TYPES,
    DIFFICULTY_DISTRIBUTION,
    BLOOMS_LEVELS,
)
