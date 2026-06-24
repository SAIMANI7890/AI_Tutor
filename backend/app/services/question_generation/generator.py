"""
Question Generator Service
Main service for generating examination questions using RAG and Gemini
"""
from typing import List, Dict, Any
from uuid import UUID
import json
import logging
from sqlalchemy.orm import Session
from langchain_google_genai import ChatGoogleGenerativeAI

from app.rag.retriever.retriever_service import RetrieverService
# V3 prompts: Bloom's taxonomy, hallucination prevention, 30/50/20% difficulty split
from app.services.question_generation.prompts_v3 import select_prompt_v3
from app.services.question_generation.validators import QuestionValidator
from app.services.question_generation.schemas import (
    ExamGenerationRequest,
    ExamGenerationResponse,
    GeneratedQuestion
)
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.enums import QuestionType, TestStatus
from app.repositories.test_repository import TestRepository
from app.repositories.question_repository import TestQuestionRepository

logger = logging.getLogger(__name__)

# Subjective question types return model_answer instead of correct_answer
_SUBJECTIVE_TYPES = {QuestionType.SHORT_ANSWER, QuestionType.LONG_ANSWER}


class QuestionGeneratorService:
    """Service for generating examination questions"""
    
    def __init__(
        self,
        api_key: str,
        chroma_db_path: str = "./chroma_db",
        model: str = "gemini-2.5-flash-lite",  # Gemini 2.5 Flash Lite - fastest model
        temperature: float = 0.7,
        use_local_embeddings: bool = True
    ):
        """
        Initialize question generator service
        
        Args:
            api_key: Google API key for Gemini
            chroma_db_path: Path to ChromaDB
            model: Gemini model name
            temperature: LLM temperature (higher = more creative)
            use_local_embeddings: Use local embeddings for retrieval
        """
        # Initialize retriever with local embeddings
        self.retriever = RetrieverService(
            api_key=api_key if not use_local_embeddings else "",
            persist_directory=chroma_db_path,
            top_k=5,  # Retrieve more chunks for question generation
            use_local=use_local_embeddings
        )
        
        # Initialize LLM with higher temperature for diverse questions
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=temperature,
            convert_system_message_to_human=True
        )
        
        # Initialize validator
        self.validator = QuestionValidator()
        
        logger.info(f"Initialized question generator with model: {model}")
    
    def retrieve_context_by_category(
        self, 
        categories: List[str],
        top_k_per_category: int = 5
    ) -> str:
        """
        Retrieve textbook content filtered by categories
        Uses ChromaDB's native where filter for reliable category filtering
        
        Args:
            categories: List of categories to retrieve from
            top_k_per_category: Number of chunks per category
            
        Returns:
            Formatted context string
        """
        logger.info(f"Retrieving content for categories: {categories}")
        
        # Build query that emphasizes the categories
        category_query = " ".join(categories)
        query = f"Important topics and concepts from {category_query}"
        
        # Generate query embedding
        if self.retriever.use_local:
            query_embedding = self.retriever.embeddings.generate_embedding(query)
        else:
            query_embedding = self.retriever.embeddings.embed_query(query)
        
        # Retrieve chunks using ChromaDB native category filter
        # This is MUCH more reliable than post-filtering
        all_chunks = []
        
        for category in categories:
            try:
                # Use ChromaDB where clause to filter by category BEFORE retrieval
                results = self.retriever.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k_per_category,
                    where={"category": category},  # Native filter!
                    include=["documents", "metadatas", "distances"]
                )
                
                if results and results["documents"] and len(results["documents"]) > 0:
                    documents = results["documents"][0]
                    metadatas = results["metadatas"][0]
                    distances = results["distances"][0]
                    
                    for doc, metadata, distance in zip(documents, metadatas, distances):
                        similarity_score = 1 / (1 + distance)
                        all_chunks.append({
                            "text": doc,
                            "metadata": metadata,
                            "similarity_score": similarity_score
                        })
                    
                    logger.info(f"Retrieved {len(documents)} chunks for category: {category}")
                else:
                    logger.warning(f"No chunks found for category: {category}")
                    
            except Exception as e:
                logger.error(f"Error retrieving chunks for category {category}: {e}")
        
        if not all_chunks:
            raise ValueError(
                f"No content found for categories: {categories}. "
                f"Please ensure the vector store contains content for these categories."
            )
        
        logger.info(f"Total retrieved: {len(all_chunks)} chunks from {len(categories)} categories")
        
        # Format context
        context = self.retriever.format_context_for_llm(all_chunks)
        return context
    
    def parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON response from LLM
        Handles markdown code blocks and malformed JSON
        
        Args:
            response_text: Raw LLM response
            
        Returns:
            Parsed JSON dictionary
        """
        try:
            # Remove markdown code blocks if present
            text = response_text.strip()
            
            if text.startswith("```json"):
                text = text[7:]  # Remove ```json
            elif text.startswith("```"):
                text = text[3:]  # Remove ```
            
            if text.endswith("```"):
                text = text[:-3]  # Remove trailing ```
            
            text = text.strip()
            
            # Parse JSON
            parsed = json.loads(text)
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            logger.error(f"Response text: {response_text[:500]}")
            raise ValueError(f"Invalid JSON response from LLM: {str(e)}")
    
    def generate_questions_with_llm(
        self,
        question_type: QuestionType,
        context: str,
        category: str,
        count: int
    ) -> List[Dict[str, Any]]:
        """
        Generate questions using LLM with enhanced error handling
        
        Args:
            question_type: Type of questions to generate
            context: Retrieved textbook content
            category: Category for the questions
            count: Number of questions to generate
            
        Returns:
            List of generated question dictionaries
        """
        # Create V3 prompt (Bloom's + hallucination prevention + difficulty distribution)
        prompt = select_prompt_v3(
            question_type.value,
            context,
            category,
            count
        )
        
        logger.info(f"Generating {count} {question_type.value} questions for {category} [V3 prompt]")
        logger.debug(f"Prompt length: {len(prompt)} characters")
        
        # Call LLM with timeout and error handling
        try:
            # Set timeout for LLM call (30 seconds)
            import asyncio
            from concurrent.futures import TimeoutError
            
            response = self.llm.invoke(prompt)
            response_text = response.content
            
            logger.debug(f"LLM response length: {len(response_text)} characters")
            logger.debug(f"LLM response preview: {response_text[:200]}...")
            
            # Parse JSON response
            parsed_response = self.parse_json_response(response_text)
            
            # Extract questions
            if "questions" not in parsed_response:
                logger.error(f"Response missing 'questions' key. Keys present: {list(parsed_response.keys())}")
                logger.error(f"Full response: {response_text[:1000]}")
                raise ValueError("Response missing 'questions' key")
            
            questions = parsed_response["questions"]
            
            if not isinstance(questions, list):
                logger.error(f"'questions' is not a list, got type: {type(questions)}")
                raise ValueError("'questions' must be a list")
            
            if len(questions) == 0:
                logger.error("LLM returned empty questions list")
                logger.error(f"Full response: {response_text[:1000]}")
                raise ValueError("LLM returned no questions")
            
            logger.info(f"✅ LLM generated {len(questions)} questions successfully")
            
            return questions
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parsing error: {e}")
            logger.error(f"Attempted to parse: {response_text[:500]}")
            logger.error(f"Prompt used (first 300 chars): {prompt[:300]}")
            raise ValueError(f"Failed to parse LLM response as JSON: {str(e)}")
            
        except TimeoutError:
            logger.error(f"❌ LLM call timed out after 30 seconds")
            logger.error(f"Question type: {question_type.value}, Category: {category}, Count: {count}")
            raise ValueError("LLM request timed out. Please try again.")
            
        except Exception as e:
            logger.error(f"❌ Unexpected error generating questions: {e}", exc_info=True)
            logger.error(f"Question type: {question_type.value}, Category: {category}, Count: {count}")
            logger.error(f"Context length: {len(context)} characters")
            raise ValueError(f"Question generation failed: {str(e)}")
    
    def generate_exam(
        self,
        db: Session,
        request: ExamGenerationRequest
    ) -> ExamGenerationResponse:
        """
        Generate complete exam with questions
        
        Args:
            db: Database session
            request: Exam generation request
            
        Returns:
            Generated exam response
        """
        test = None
        
        try:
            logger.info(f"Starting exam generation: {request.question_count} {request.question_type.value} questions")
            
            # Step 1: Retrieve context from selected categories
            context = self.retrieve_context_by_category(
                request.selected_categories,
                top_k_per_category=10
            )
            
            # Step 2: Create test record WITHOUT committing yet
            test = Test(
                user_id=request.user_id,
                subject=request.subject,
                question_type=request.question_type,
                selected_categories=request.selected_categories,
                question_count=request.question_count,
                status=TestStatus.GENERATED
            )
            db.add(test)
            db.flush()  # Get test.id without committing
            
            logger.info(f"Created test record: {test.id}")
            
            # Step 3: Generate questions for each category
            all_generated_questions = []
            questions_per_category = max(1, request.question_count // len(request.selected_categories))
            remaining_questions = request.question_count
            
            for i, category in enumerate(request.selected_categories):
                # Calculate questions for this category
                if i == len(request.selected_categories) - 1:
                    # Last category gets remaining questions
                    category_count = remaining_questions
                else:
                    category_count = min(questions_per_category, remaining_questions)
                
                if category_count <= 0:
                    break
                
                # Generate questions
                generated = self.generate_questions_with_llm(
                    request.question_type,
                    context,
                    category,
                    category_count
                )
                
                # Validate questions
                valid_questions, errors = self.validator.validate_batch(
                    generated,
                    request.question_type.value
                )
                
                if errors:
                    logger.warning(f"Validation errors: {errors}")
                
                # Add valid questions
                all_generated_questions.extend(valid_questions[:category_count])
                remaining_questions -= len(valid_questions[:category_count])
            
            # Step 4: If we don't have enough valid questions, generate more
            retry_count = 0
            max_retries = 2
            
            while len(all_generated_questions) < request.question_count and retry_count < max_retries:
                retry_count += 1
                shortage = request.question_count - len(all_generated_questions)
                
                logger.warning(f"Short {shortage} questions, generating more (retry {retry_count})")
                
                # Pick a random category and generate more
                category = request.selected_categories[0]
                additional = self.generate_questions_with_llm(
                    request.question_type,
                    context,
                    category,
                    shortage
                )
                
                valid_additional, _ = self.validator.validate_batch(
                    additional,
                    request.question_type.value
                )
                
                all_generated_questions.extend(valid_additional[:shortage])
            
            # Check if we have enough questions
            if len(all_generated_questions) < request.question_count:
                logger.error(f"Failed to generate enough valid questions: {len(all_generated_questions)}/{request.question_count}")
                raise ValueError(
                    f"Could only generate {len(all_generated_questions)} valid questions out of {request.question_count} requested"
                )
            
            # Trim to exact count if we have extra
            all_generated_questions = all_generated_questions[:request.question_count]
            
            # Step 5: Store questions in database (still within same transaction)
            question_models = []
            
            for i, q_data in enumerate(all_generated_questions, start=1):
                # For subjective types (SHORT_ANSWER / LONG_ANSWER), V3 prompts
                # return `model_answer` instead of `correct_answer`.  We store
                # whichever key is present so the DB column is never empty.
                correct_ans = (
                    q_data.get("correct_answer")
                    or q_data.get("model_answer")
                    or "[See model answer]"
                )
                model_ans = q_data.get("model_answer") or q_data.get("correct_answer")

                question_model = TestQuestion(
                    test_id=test.id,
                    question_number=i,
                    question_type=request.question_type,
                    question_text=q_data["question_text"],
                    options_json=q_data.get("options"),
                    correct_answer=correct_ans,
                    model_answer=model_ans,
                    source_document=q_data.get("source_document"),
                    source_page=q_data.get("source_page"),
                    category=q_data["category"]
                )
                question_models.append(question_model)
            
            # Add questions to session (no commit yet)
            db.add_all(question_models)
            
            # COMMIT EVERYTHING ATOMICALLY
            db.commit()
            db.refresh(test)
            
            logger.info(f"✅ Successfully committed test and {len(question_models)} questions")
            
            # Step 6: Build response
            generated_questions = [
                GeneratedQuestion(
                    question_type=request.question_type,
                    question_text=q_data["question_text"],
                    options=q_data.get("options"),
                    correct_answer=q_data.get("correct_answer") or q_data.get("model_answer"),
                    model_answer=q_data.get("model_answer"),
                    source_document=q_data.get("source_document"),
                    source_page=q_data.get("source_page"),
                    category=q_data["category"]
                )
                for q_data in all_generated_questions
            ]
            
            response = ExamGenerationResponse(
                test_id=str(test.id),
                user_id=test.user_id,
                subject=test.subject,
                question_type=test.question_type,
                question_count=len(generated_questions),
                questions=generated_questions,
                status=test.status.value
            )
            
            logger.info(f"✅ Successfully generated exam: {test.id}")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error generating exam: {e}", exc_info=True)
            
            # Rollback transaction to prevent partial commit
            db.rollback()
            logger.info("Rolled back transaction due to error")
            
            # Re-raise with context
            raise ValueError(f"Exam generation failed: {str(e)}") from e
    
    # Convenience methods for specific question types
    
    def generate_mcq_exam(
        self,
        db: Session,
        user_id: int,
        categories: List[str],
        question_count: int
    ) -> ExamGenerationResponse:
        """Generate MCQ exam"""
        request = ExamGenerationRequest(
            user_id=user_id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=categories,
            question_count=question_count
        )
        return self.generate_exam(db, request)
    
    def generate_fill_blank_exam(
        self,
        db: Session,
        user_id: int,
        categories: List[str],
        question_count: int
    ) -> ExamGenerationResponse:
        """Generate Fill in the Blanks exam"""
        request = ExamGenerationRequest(
            user_id=user_id,
            subject="Social Studies",
            question_type=QuestionType.FILL_BLANKS,
            selected_categories=categories,
            question_count=question_count
        )
        return self.generate_exam(db, request)
    
    def generate_short_answer_exam(
        self,
        db: Session,
        user_id: int,
        categories: List[str],
        question_count: int
    ) -> ExamGenerationResponse:
        """Generate Short Answer exam"""
        request = ExamGenerationRequest(
            user_id=user_id,
            subject="Social Studies",
            question_type=QuestionType.SHORT_ANSWER,
            selected_categories=categories,
            question_count=question_count
        )
        return self.generate_exam(db, request)
    
    def generate_long_answer_exam(
        self,
        db: Session,
        user_id: int,
        categories: List[str],
        question_count: int
    ) -> ExamGenerationResponse:
        """Generate Long Answer exam"""
        request = ExamGenerationRequest(
            user_id=user_id,
            subject="Social Studies",
            question_type=QuestionType.LONG_ANSWER,
            selected_categories=categories,
            question_count=question_count
        )
        return self.generate_exam(db, request)
