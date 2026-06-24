"""
Question Quality Control and Validation Framework
==================================================

This module implements comprehensive quality checks for generated questions
to ensure educational value, factual accuracy, and assessment validity.

Key Features:
- Hallucination detection
- Educational quality metrics
- Bloom's Taxonomy validation
- Difficulty calibration verification
- Source attribution checking
"""
from typing import Dict, List, Tuple, Any
import re
import logging
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


# ============================================================================
# QUALITY METRICS AND THRESHOLDS
# ============================================================================

QUALITY_THRESHOLDS = {
    "min_question_length": 10,
    "max_question_length": 500,
    "min_answer_length": 1,
    "max_mcq_option_length": 200,
    "min_mcq_options": 4,
    "max_mcq_options": 4,
    "min_short_answer_words": 10,
    "max_short_answer_words": 60,
    "min_long_answer_words": 40,
    "max_long_answer_words": 200,
    "similarity_threshold": 0.75,  # For duplicate detection
}

VALID_DIFFICULTIES = {"Easy", "Medium", "Hard"}
VALID_BLOOM_LEVELS = {"Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"}
VALID_CATEGORIES = {"History", "Geography", "Politics", "Economics"}


# ============================================================================
# HALLUCINATION PREVENTION CHECKER
# ============================================================================

class HallucinationDetector:
    """
    Detects potential hallucinations by checking if question content
    can be traced back to source material.
    """
    
    @staticmethod
    def check_source_alignment(
        question_data: Dict[str, Any],
        source_chunks: List[Dict[str, Any]]
    ) -> Tuple[bool, str]:
        """
        Verify that question content aligns with source material.
        
        Strategy:
        - Check if answer text appears in source chunks
        - Verify key terms from question exist in sources
        - Flag questions with no source attribution
        
        Args:
            question_data: Generated question dictionary
            source_chunks: Original RAG chunks
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Extract question components
        question_text = question_data.get("question_text", "")
        correct_answer = question_data.get("correct_answer", "")
        model_answer = question_data.get("model_answer", "")
        
        # Check source attribution
        source_doc = question_data.get("source_document")
        source_page = question_data.get("source_page")
        
        if not source_doc or not source_page:
            return False, "Missing source attribution (document/page)"
        
        # Combine all source text
        all_source_text = " ".join([
            chunk.get("text", "").lower()
            for chunk in source_chunks
        ])
        
        if not all_source_text:
            return False, "No source text available for validation"
        
        # Check if answer content exists in source
        answer_to_check = model_answer if model_answer else correct_answer
        answer_lower = answer_to_check.lower()
        
        # For short answers, check exact or partial match
        if len(answer_lower.split()) <= 5:
            # Short answer - should appear verbatim or very close
            if answer_lower not in all_source_text:
                # Check for high similarity with any source chunk
                max_similarity = 0
                for chunk in source_chunks:
                    chunk_text = chunk.get("text", "").lower()
                    similarity = SequenceMatcher(None, answer_lower, chunk_text).ratio()
                    max_similarity = max(max_similarity, similarity)
                
                if max_similarity < 0.3:  # Low similarity threshold for short answers
                    logger.warning(
                        f"Answer '{answer_to_check[:50]}...' has low similarity "
                        f"({max_similarity:.2f}) with source material"
                    )
                    return False, "Answer not found in source material (potential hallucination)"
        else:
            # Long answer - check if key terms exist
            answer_words = set(answer_lower.split())
            # Remove common words
            common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
            key_words = answer_words - common_words
            
            # Check if at least 50% of key words exist in source
            found_words = sum(1 for word in key_words if word in all_source_text)
            coverage = found_words / len(key_words) if key_words else 0
            
            if coverage < 0.5:
                logger.warning(
                    f"Only {coverage:.1%} of answer key terms found in source material"
                )
                return False, f"Insufficient source coverage ({coverage:.1%}) - potential hallucination"
        
        return True, ""
    
    @staticmethod
    def check_factual_consistency(question_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Check for internal consistency and obvious factual errors.
        
        Args:
            question_data: Generated question dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        question_type = question_data.get("question_type", "")
        
        # MCQ-specific checks
        if question_type == "MCQ":
            options = question_data.get("options", [])
            correct_answer = question_data.get("correct_answer", "")
            
            # Check if correct answer is in options
            if correct_answer not in options:
                return False, "Correct answer not found in MCQ options"
            
            # Check for duplicate options
            if len(options) != len(set(options)):
                return False, "Duplicate options in MCQ"
        
        # Fill blanks checks
        elif question_type == "FILL_BLANKS":
            question_text = question_data.get("question_text", "")
            
            # Check for blank marker
            if "_____" not in question_text and "____" not in question_text:
                return False, "Fill in blank question missing blank marker"
            
            # Check for multiple blanks (should be only one)
            blank_count = question_text.count("_____") + question_text.count("____")
            if blank_count > 1:
                return False, f"Multiple blanks found ({blank_count}), should be exactly 1"
        
        return True, ""


# ============================================================================
# EDUCATIONAL QUALITY VALIDATOR
# ============================================================================

class EducationalQualityValidator:
    """
    Validates educational quality of generated questions.
    """
    
    @staticmethod
    def validate_difficulty_distribution(
        questions: List[Dict[str, Any]],
        target_distribution: Dict[str, float] = {"Easy": 0.3, "Medium": 0.5, "Hard": 0.2}
    ) -> Tuple[bool, str]:
        """
        Verify that difficulty distribution matches target.
        
        Args:
            questions: List of generated questions
            target_distribution: Expected difficulty ratios
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not questions:
            return False, "No questions to validate"
        
        # Count by difficulty
        difficulty_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
        for q in questions:
            diff = q.get("difficulty", "")
            if diff in difficulty_counts:
                difficulty_counts[diff] += 1
        
        total = len(questions)
        actual_distribution = {
            diff: count / total for diff, count in difficulty_counts.items()
        }
        
        # Check if distribution is within 20% tolerance
        tolerance = 0.2
        issues = []
        for diff, target_ratio in target_distribution.items():
            actual_ratio = actual_distribution.get(diff, 0)
            if abs(actual_ratio - target_ratio) > tolerance:
                issues.append(
                    f"{diff}: {actual_ratio:.1%} (expected {target_ratio:.1%})"
                )
        
        if issues:
            return False, f"Difficulty distribution off-target: {', '.join(issues)}"
        
        logger.info(f"✓ Difficulty distribution validated: {actual_distribution}")
        return True, ""
    
    @staticmethod
    def validate_bloom_taxonomy(question_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate Bloom's Taxonomy alignment.
        
        Args:
            question_data: Generated question
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        bloom_level = question_data.get("bloom_level", "")
        difficulty = question_data.get("difficulty", "")
        question_type = question_data.get("question_type", "")
        
        # Validate bloom level exists
        if bloom_level not in VALID_BLOOM_LEVELS:
            return False, f"Invalid Bloom's level: {bloom_level}"
        
        # Check alignment between difficulty and Bloom's level
        valid_alignments = {
            "Easy": ["Remember", "Understand"],
            "Medium": ["Understand", "Apply", "Analyze"],
            "Hard": ["Apply", "Analyze", "Evaluate"],
        }
        
        if bloom_level not in valid_alignments.get(difficulty, []):
            logger.warning(
                f"Bloom's level '{bloom_level}' may not align with "
                f"difficulty '{difficulty}'"
            )
        
        # Check question type alignment
        type_bloom_map = {
            "MCQ": ["Remember", "Understand", "Apply", "Analyze"],
            "FILL_BLANKS": ["Remember", "Understand"],
            "SHORT_ANSWER": ["Understand", "Apply"],
            "LONG_ANSWER": ["Understand", "Apply", "Analyze", "Evaluate"],
        }
        
        if bloom_level not in type_bloom_map.get(question_type, []):
            return False, (
                f"Bloom's level '{bloom_level}' not typical for "
                f"question type '{question_type}'"
            )
        
        return True, ""
    
    @staticmethod
    def check_question_independence(
        questions: List[Dict[str, Any]]
    ) -> Tuple[bool, List[str]]:
        """
        Check that questions are independent (no inter-dependencies).
        
        Args:
            questions: List of generated questions
            
        Returns:
            Tuple of (is_valid, list of issues)
        """
        issues = []
        
        for i, q1 in enumerate(questions):
            q1_text = q1.get("question_text", "").lower()
            
            for j, q2 in enumerate(questions[i+1:], start=i+1):
                q2_text = q2.get("question_text", "").lower()
                
                # Check for high similarity (potential duplicates)
                similarity = SequenceMatcher(None, q1_text, q2_text).ratio()
                if similarity > QUALITY_THRESHOLDS["similarity_threshold"]:
                    issues.append(
                        f"Questions {i+1} and {j+1} are too similar "
                        f"(similarity: {similarity:.1%})"
                    )
        
        return len(issues) == 0, issues
    
    @staticmethod
    def validate_concept_coverage(
        questions: List[Dict[str, Any]],
        min_unique_concepts: int = 3
    ) -> Tuple[bool, str]:
        """
        Verify questions cover multiple concepts, not just one.
        
        Args:
            questions: List of generated questions
            min_unique_concepts: Minimum number of distinct concepts
            
        Returns:
            Tuple of (is_valid, message)
        """
        # Extract key terms from all questions
        all_key_terms = set()
        
        for q in questions:
            text = q.get("question_text", "").lower()
            # Extract meaningful words (>4 characters, not common words)
            words = re.findall(r'\b\w{5,}\b', text)
            all_key_terms.update(words)
        
        unique_concepts = len(all_key_terms)
        
        if unique_concepts < min_unique_concepts:
            return False, (
                f"Only {unique_concepts} unique concepts found, "
                f"expected at least {min_unique_concepts}. Questions may be repetitive."
            )
        
        logger.info(f"✓ Concept coverage validated: {unique_concepts} unique terms")
        return True, ""


# ============================================================================
# COMPREHENSIVE QUESTION VALIDATOR
# ============================================================================

class QuestionQualityController:
    """
    Main quality control class that orchestrates all validation checks.
    """
    
    def __init__(self):
        self.hallucination_detector = HallucinationDetector()
        self.quality_validator = EducationalQualityValidator()
    
    def validate_single_question(
        self,
        question_data: Dict[str, Any],
        source_chunks: List[Dict[str, Any]]
    ) -> Tuple[bool, List[str]]:
        """
        Run all validation checks on a single question.
        
        Args:
            question_data: Generated question dictionary
            source_chunks: Original source material
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # 1. Basic structure validation
        required_fields = ["question_text", "difficulty", "category"]
        for field in required_fields:
            if field not in question_data or not question_data[field]:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            return False, errors
        
        # 2. Length validation
        question_text = question_data.get("question_text", "")
        if len(question_text) < QUALITY_THRESHOLDS["min_question_length"]:
            errors.append(f"Question too short: {len(question_text)} chars")
        if len(question_text) > QUALITY_THRESHOLDS["max_question_length"]:
            errors.append(f"Question too long: {len(question_text)} chars")
        
        # 3. Difficulty validation
        difficulty = question_data.get("difficulty", "")
        if difficulty not in VALID_DIFFICULTIES:
            errors.append(f"Invalid difficulty: {difficulty}")
        
        # 4. Category validation
        category = question_data.get("category", "")
        if category not in VALID_CATEGORIES:
            errors.append(f"Invalid category: {category}")
        
        # 5. Hallucination check
        is_aligned, msg = self.hallucination_detector.check_source_alignment(
            question_data, source_chunks
        )
        if not is_aligned:
            errors.append(f"Hallucination check failed: {msg}")
        
        # 6. Factual consistency check
        is_consistent, msg = self.hallucination_detector.check_factual_consistency(
            question_data
        )
        if not is_consistent:
            errors.append(f"Consistency check failed: {msg}")
        
        # 7. Bloom's Taxonomy validation
        if "bloom_level" in question_data:
            is_valid_bloom, msg = self.quality_validator.validate_bloom_taxonomy(
                question_data
            )
            if not is_valid_bloom:
                errors.append(f"Bloom's validation failed: {msg}")
        
        return len(errors) == 0, errors
    
    def validate_question_batch(
        self,
        questions: List[Dict[str, Any]],
        source_chunks: List[Dict[str, Any]],
        expected_count: int
    ) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Validate a batch of generated questions.
        
        Args:
            questions: List of generated questions
            source_chunks: Original source material
            expected_count: Expected number of questions
            
        Returns:
            Tuple of (valid_questions, error_messages)
        """
        valid_questions = []
        all_errors = []
        
        # Validate each question individually
        for i, question in enumerate(questions):
            is_valid, errors = self.validate_single_question(question, source_chunks)
            
            if is_valid:
                valid_questions.append(question)
            else:
                error_msg = f"Question {i+1}: {'; '.join(errors)}"
                all_errors.append(error_msg)
                logger.warning(error_msg)
        
        # Batch-level validations
        if valid_questions:
            # Check difficulty distribution
            is_valid_dist, msg = self.quality_validator.validate_difficulty_distribution(
                valid_questions
            )
            if not is_valid_dist:
                all_errors.append(f"Batch validation: {msg}")
            
            # Check question independence
            is_independent, issues = self.quality_validator.check_question_independence(
                valid_questions
            )
            if not is_independent:
                all_errors.extend([f"Independence check: {issue}" for issue in issues])
            
            # Check concept coverage
            is_covered, msg = self.quality_validator.validate_concept_coverage(
                valid_questions
            )
            if not is_covered:
                all_errors.append(f"Coverage check: {msg}")
        
        # Check if we have enough valid questions
        if len(valid_questions) < expected_count:
            all_errors.append(
                f"Only {len(valid_questions)} valid questions out of "
                f"{expected_count} required"
            )
        
        logger.info(
            f"✓ Validation complete: {len(valid_questions)}/{len(questions)} "
            f"questions passed, {len(all_errors)} issues found"
        )
        
        return valid_questions, all_errors


# ============================================================================
# QUALITY METRICS CALCULATOR
# ============================================================================

def calculate_quality_metrics(questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate quality metrics for a set of questions.
    
    Args:
        questions: List of validated questions
        
    Returns:
        Dictionary of quality metrics
    """
    if not questions:
        return {"error": "No questions to analyze"}
    
    # Difficulty distribution
    difficulty_dist = {"Easy": 0, "Medium": 0, "Hard": 0}
    for q in questions:
        diff = q.get("difficulty", "")
        if diff in difficulty_dist:
            difficulty_dist[diff] += 1
    
    total = len(questions)
    difficulty_percentages = {
        diff: (count / total * 100) for diff, count in difficulty_dist.items()
    }
    
    # Bloom's level distribution
    bloom_dist = {}
    for q in questions:
        bloom = q.get("bloom_level", "Unknown")
        bloom_dist[bloom] = bloom_dist.get(bloom, 0) + 1
    
    # Average question length
    avg_length = sum(len(q.get("question_text", "")) for q in questions) / total
    
    # Questions with source attribution
    sourced = sum(1 for q in questions if q.get("source_document"))
    source_coverage = (sourced / total * 100)
    
    metrics = {
        "total_questions": total,
        "difficulty_distribution": difficulty_percentages,
        "bloom_distribution": bloom_dist,
        "average_question_length": round(avg_length, 1),
        "source_attribution_coverage": round(source_coverage, 1),
        "quality_score": _calculate_overall_quality(questions)
    }
    
    return metrics


def _calculate_overall_quality(questions: List[Dict[str, Any]]) -> float:
    """Calculate overall quality score (0-100)"""
    if not questions:
        return 0.0
    
    score = 100.0
    
    # Deduct for missing difficulty
    missing_diff = sum(1 for q in questions if not q.get("difficulty"))
    score -= (missing_diff / len(questions)) * 20
    
    # Deduct for missing source attribution
    missing_source = sum(1 for q in questions if not q.get("source_document"))
    score -= (missing_source / len(questions)) * 20
    
    # Deduct for missing Bloom's level
    missing_bloom = sum(1 for q in questions if not q.get("bloom_level"))
    score -= (missing_bloom / len(questions)) * 10
    
    return max(0.0, round(score, 1))
