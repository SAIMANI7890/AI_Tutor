"""
Enhanced Question Validation System V3.0
========================================
Multi-layer validation for educational assessment quality

VALIDATION LAYERS:
1. Schema Validation - JSON structure and required fields
2. Source Attribution - Answer verification against context
3. Difficulty Distribution - 30% Easy, 50% Medium, 20% Hard
4. Educational Quality - Bloom's taxonomy alignment
5. Hallucination Detection - Pattern-based screening

Author: AI Tutor Backend Team
Version: 3.0
"""
import re
import json
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass


# ============================================================================
# VALIDATION RESULT CLASSES
# ============================================================================

@dataclass
class ValidationResult:
    """Result of question validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    quality_score: float  # 0.0 to 1.0
    

@dataclass
class BatchValidationResult:
    """Result of batch question validation"""
    valid_questions: List[dict]
    invalid_questions: List[dict]
    validation_results: List[ValidationResult]
    difficulty_distribution: Dict[str, int]
    overall_quality_score: float


# ============================================================================
# HALLUCINATION DETECTION
# ============================================================================

class HallucinationDetector:
    """Detect potential hallucinations in generated questions"""
    
    # Phrases that indicate external knowledge or assumptions
    HALLUCINATION_INDICATORS = [
        r"according to recent studies",
        r"it is well known that",
        r"experts agree",
        r"in general",
        r"obviously",
        r"clearly",
        r"as everyone knows",
        r"research shows",
        r"studies indicate",
        r"it has been proven",
        r"nowadays",
        r"in modern times",
        r"today",
        r"currently",
        r"in recent years",
        r"latest research",
        r"new evidence suggests",
    ]
    
    @classmethod
    def detect_patterns(cls, text: str) -> List[str]:
        """
        Detect hallucination indicator patterns in text
        
        Args:
            text: Question text or answer to check
            
        Returns:
            List of detected hallucination indicators
        """
        detected = []
        text_lower = text.lower()
        
        for pattern in cls.HALLUCINATION_INDICATORS:
            if re.search(pattern, text_lower):
                detected.append(pattern)
        
        return detected
    
    @classmethod
    def check_source_attribution(
        cls,
        answer: str,
        context_chunks: List[str],
        fuzzy_match: bool = True,
        min_similarity: float = 0.8
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify if answer exists in provided context
        
        Args:
            answer: The correct answer to verify
            context_chunks: List of source text chunks
            fuzzy_match: Allow approximate matching
            min_similarity: Minimum similarity threshold (0-1)
            
        Returns:
            (is_found, matching_chunk) tuple
        """
        answer_lower = answer.lower().strip()
        
        for chunk in context_chunks:
            chunk_lower = chunk.lower()
            
            # Exact match check
            if answer_lower in chunk_lower:
                return True, chunk
            
            # Fuzzy match check (if enabled)
            if fuzzy_match:
                # Calculate simple token overlap
                answer_tokens = set(answer_lower.split())
                chunk_tokens = set(chunk_lower.split())
                
                if len(answer_tokens) == 0:
                    continue
                    
                overlap = len(answer_tokens & chunk_tokens)
                similarity = overlap / len(answer_tokens)
                
                if similarity >= min_similarity:
                    return True, chunk
        
        return False, None


# ============================================================================
# SCHEMA VALIDATOR
# ============================================================================

class SchemaValidator:
    """Validate JSON schema for different question types"""
    
    REQUIRED_FIELDS_BY_TYPE = {
        "MCQ": [
            "question_text",
            "options",
            "correct_answer",
            "difficulty",
            "category",
            "source_document",
            "source_page"
        ],
        "FILL_BLANKS": [
            "question_text",
            "correct_answer",
            "difficulty",
            "category",
            "source_document",
            "source_page"
        ],
        "SHORT_ANSWER": [
            "question_text",
            "model_answer",
            "difficulty",
            "category",
            "source_document",
            "source_page"
        ],
        "LONG_ANSWER": [
            "question_text",
            "model_answer",
            "difficulty",
            "category",
            "source_document",
            "source_page"
        ]
    }
    
    @classmethod
    def validate(cls, question: dict, question_type: str) -> ValidationResult:
        """
        Validate question schema
        
        Args:
            question: Question dictionary
            question_type: Type of question (MCQ, FILL_BLANKS, etc.)
            
        Returns:
            ValidationResult with errors and warnings
        """
        errors = []
        warnings = []
        
        # Check required fields
        required_fields = cls.REQUIRED_FIELDS_BY_TYPE.get(question_type, [])
        for field in required_fields:
            if field not in question:
                errors.append(f"Missing required field: {field}")
            elif not question[field]:
                errors.append(f"Empty field: {field}")
        
        # Type-specific validation
        if question_type == "MCQ":
            errors.extend(cls._validate_mcq(question))
        elif question_type == "FILL_BLANKS":
            errors.extend(cls._validate_fill_blank(question))
        elif question_type == "SHORT_ANSWER":
            errors.extend(cls._validate_short_answer(question))
        elif question_type == "LONG_ANSWER":
            errors.extend(cls._validate_long_answer(question))
        
        # Check difficulty value
        if "difficulty" in question:
            if question["difficulty"] not in ["Easy", "Medium", "Hard"]:
                errors.append(f"Invalid difficulty: {question['difficulty']}")
        
        is_valid = len(errors) == 0
        quality_score = 1.0 if is_valid else 0.0
        
        return ValidationResult(is_valid, errors, warnings, quality_score)
    
    @staticmethod
    def _validate_mcq(question: dict) -> List[str]:
        """MCQ-specific validation"""
        errors = []
        
        # Check options
        if "options" in question:
            options = question["options"]
            
            if not isinstance(options, list):
                errors.append("Options must be a list")
            elif len(options) != 4:
                errors.append(f"MCQ must have exactly 4 options, got {len(options)}")
            elif len(set(options)) != len(options):
                errors.append("Options contain duplicates")
            
            # Check correct answer is in options
            if "correct_answer" in question:
                if question["correct_answer"] not in options:
                    errors.append("Correct answer not found in options")
        
        return errors
    
    @staticmethod
    def _validate_fill_blank(question: dict) -> List[str]:
        """Fill in the blank validation"""
        errors = []
        
        if "question_text" in question:
            text = question["question_text"]
            blank_count = text.count("_____")
            
            if blank_count == 0:
                errors.append("Fill blank question missing blank marker (_____)")
            elif blank_count > 1:
                errors.append(f"Fill blank should have exactly 1 blank, found {blank_count}")
        
        # Check answer length
        if "correct_answer" in question:
            answer = question["correct_answer"]
            word_count = len(answer.split())
            
            if word_count > 5:
                errors.append(f"Fill blank answer too long ({word_count} words), should be 1-4 words")
        
        return errors
    
    @staticmethod
    def _validate_short_answer(question: dict) -> List[str]:
        """Short answer validation"""
        errors = []
        warnings = []
        
        if "model_answer" in question:
            answer = question["model_answer"]
            word_count = len(answer.split())
            sentence_count = len([s for s in answer.split('.') if s.strip()])
            
            if word_count < 20:
                warnings.append(f"Short answer may be too brief ({word_count} words, target 30-50)")
            elif word_count > 70:
                warnings.append(f"Short answer may be too long ({word_count} words, target 30-50)")
            
            if sentence_count < 2:
                warnings.append(f"Short answer should have 2-3 sentences, found {sentence_count}")
        
        return errors
    
    @staticmethod
    def _validate_long_answer(question: dict) -> List[str]:
        """Long answer validation"""
        errors = []
        warnings = []
        
        if "model_answer" in question:
            answer = question["model_answer"]
            word_count = len(answer.split())
            sentence_count = len([s for s in answer.split('.') if s.strip()])
            
            if word_count < 80:
                warnings.append(f"Long answer may be too brief ({word_count} words, target 100-150)")
            elif word_count > 180:
                warnings.append(f"Long answer may be too long ({word_count} words, target 100-150)")
            
            if sentence_count < 4:
                warnings.append(f"Long answer should have 5-6 sentences, found {sentence_count}")
        
        return errors


# ============================================================================
# EDUCATIONAL QUALITY VALIDATOR
# ============================================================================

class EducationalQualityValidator:
    """Validate educational quality and Bloom's taxonomy alignment"""
    
    BLOOMS_VERBS = {
        "L1_Remember": ["define", "list", "name", "identify", "recall", "state", "label", "match"],
        "L2_Understand": ["explain", "describe", "summarize", "compare", "classify", "discuss", "interpret"],
        "L3_Apply": ["apply", "use", "demonstrate", "solve", "illustrate", "show", "calculate"],
        "L4_Analyze": ["analyze", "examine", "differentiate", "compare", "contrast", "investigate"],
        "L5_Evaluate": ["evaluate", "assess", "justify", "critique", "argue", "judge", "defend"]
    }
    
    @classmethod
    def assess_quality(cls, question: dict, question_type: str) -> Tuple[float, List[str]]:
        """
        Assess educational quality of a question
        
        Args:
            question: Question dictionary
            question_type: Type of question
            
        Returns:
            (quality_score, feedback) tuple where score is 0-1
        """
        score = 1.0
        feedback = []
        
        # Check for appropriate question verbs
        question_text = question.get("question_text", "").lower()
        blooms_level = question.get("blooms_level", "")
        difficulty = question.get("difficulty", "")
        
        # Verify Bloom's level matches difficulty
        expected_blooms = cls._expected_blooms_for_difficulty(difficulty, question_type)
        if blooms_level and blooms_level not in expected_blooms:
            score -= 0.2
            feedback.append(f"Bloom's level {blooms_level} may not match {difficulty} difficulty")
        
        # Check for educational value indicators
        if question_type == "MCQ":
            # Check if it's testing understanding vs recall
            if any(verb in question_text for verb in cls.BLOOMS_VERBS["L1_Remember"]):
                if difficulty == "Hard":
                    score -= 0.1
                    feedback.append("Hard MCQ should test higher-order thinking, not just recall")
        
        # Check answer quality
        if question_type in ["SHORT_ANSWER", "LONG_ANSWER"]:
            model_answer = question.get("model_answer", "")
            if model_answer:
                # Check for structured answer
                if "." not in model_answer:
                    score -= 0.2
                    feedback.append("Answer should be in complete sentences")
                
                # Check for explanation vs just listing
                if question_type == "LONG_ANSWER" and len(model_answer.split()) < 80:
                    score -= 0.15
                    feedback.append("Long answer needs more comprehensive explanation")
        
        return max(0.0, score), feedback
    
    @staticmethod
    def _expected_blooms_for_difficulty(difficulty: str, question_type: str) -> List[str]:
        """Get expected Bloom's levels for difficulty"""
        mapping = {
            ("Easy", "MCQ"): ["L1_Remember", "L2_Understand"],
            ("Medium", "MCQ"): ["L2_Understand", "L3_Apply"],
            ("Hard", "MCQ"): ["L3_Apply", "L4_Analyze"],
            ("Easy", "FILL_BLANKS"): ["L1_Remember"],
            ("Medium", "FILL_BLANKS"): ["L1_Remember", "L2_Understand"],
            ("Hard", "FILL_BLANKS"): ["L2_Understand"],
            ("Easy", "SHORT_ANSWER"): ["L2_Understand"],
            ("Medium", "SHORT_ANSWER"): ["L2_Understand", "L3_Apply"],
            ("Hard", "SHORT_ANSWER"): ["L3_Apply", "L4_Analyze"],
            ("Easy", "LONG_ANSWER"): ["L2_Understand", "L3_Apply"],
            ("Medium", "LONG_ANSWER"): ["L3_Apply", "L4_Analyze"],
            ("Hard", "LONG_ANSWER"): ["L4_Analyze", "L5_Evaluate"]
        }
        return mapping.get((difficulty, question_type), [])


# ============================================================================
# MAIN VALIDATOR CLASS
# ============================================================================

class QuestionValidatorV3:
    """
    Main validator combining all validation layers
    """
    
    def __init__(self):
        self.schema_validator = SchemaValidator()
        self.hallucination_detector = HallucinationDetector()
        self.quality_validator = EducationalQualityValidator()
    
    def validate_question(
        self,
        question: dict,
        question_type: str,
        context_chunks: Optional[List[str]] = None
    ) -> ValidationResult:
        """
        Comprehensive validation of a single question
        
        Args:
            question: Question dictionary to validate
            question_type: Type of question (MCQ, FILL_BLANKS, etc.)
            context_chunks: Source text chunks for attribution check
            
        Returns:
            ValidationResult with all checks
        """
        all_errors = []
        all_warnings = []
        scores = []
        
        # Layer 1: Schema Validation
        schema_result = self.schema_validator.validate(question, question_type)
        all_errors.extend(schema_result.errors)
        all_warnings.extend(schema_result.warnings)
        scores.append(schema_result.quality_score)
        
        # Layer 2: Hallucination Detection
        question_text = question.get("question_text", "")
        hallucination_patterns = self.hallucination_detector.detect_patterns(question_text)
        if hallucination_patterns:
            all_warnings.append(f"Potential hallucination indicators: {', '.join(hallucination_patterns)}")
            scores.append(0.8)
        else:
            scores.append(1.0)
        
        # Layer 3: Source Attribution (if context provided)
        if context_chunks:
            answer_key = "model_answer" if question_type in ["SHORT_ANSWER", "LONG_ANSWER"] else "correct_answer"
            answer = question.get(answer_key, "")
            
            if answer:
                is_found, _ = self.hallucination_detector.check_source_attribution(
                    answer, context_chunks
                )
                if not is_found:
                    all_errors.append("Answer not found in provided source context")
                    scores.append(0.0)
                else:
                    scores.append(1.0)
        
        # Layer 4: Educational Quality
        quality_score, quality_feedback = self.quality_validator.assess_quality(
            question, question_type
        )
        all_warnings.extend(quality_feedback)
        scores.append(quality_score)
        
        # Calculate overall score
        overall_score = sum(scores) / len(scores) if scores else 0.0
        is_valid = len(all_errors) == 0
        
        return ValidationResult(is_valid, all_errors, all_warnings, overall_score)
    
    def validate_batch(
        self,
        questions: List[dict],
        question_type: str,
        context_chunks: Optional[List[str]] = None,
        target_distribution: Optional[Dict[str, float]] = None
    ) -> BatchValidationResult:
        """
        Validate a batch of questions with difficulty distribution check
        
        Args:
            questions: List of question dictionaries
            question_type: Type of questions
            context_chunks: Source text for attribution
            target_distribution: Expected difficulty distribution (default: 30% Easy, 50% Medium, 20% Hard)
            
        Returns:
            BatchValidationResult with valid/invalid questions separated
        """
        if target_distribution is None:
            target_distribution = {"Easy": 0.3, "Medium": 0.5, "Hard": 0.2}
        
        valid_questions = []
        invalid_questions = []
        validation_results = []
        difficulty_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
        
        # Validate each question
        for question in questions:
            result = self.validate_question(question, question_type, context_chunks)
            validation_results.append(result)
            
            if result.is_valid:
                valid_questions.append(question)
                difficulty = question.get("difficulty", "Medium")
                difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
            else:
                invalid_questions.append(question)
        
        # Check difficulty distribution
        total_valid = len(valid_questions)
        if total_valid > 0:
            actual_distribution = {
                diff: count / total_valid
                for diff, count in difficulty_counts.items()
            }
            
            # Calculate distribution error
            distribution_error = sum(
                abs(actual_distribution.get(diff, 0) - target_distribution.get(diff, 0))
                for diff in ["Easy", "Medium", "Hard"]
            )
            
            # If distribution is off by more than 20%, add warning
            if distribution_error > 0.2:
                for result in validation_results:
                    result.warnings.append(
                        f"Difficulty distribution off target: {actual_distribution}"
                    )
        
        # Calculate overall quality score
        quality_scores = [r.quality_score for r in validation_results if r.is_valid]
        overall_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        
        return BatchValidationResult(
            valid_questions=valid_questions,
            invalid_questions=invalid_questions,
            validation_results=validation_results,
            difficulty_distribution=difficulty_counts,
            overall_quality_score=overall_quality
        )
