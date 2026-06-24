"""
AI Evaluation Service
Evaluates student answers using RAG and Gemini AI
"""
from typing import Dict, Any, Optional
import json
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from app.rag.retriever.retriever_service import RetrieverService

logger = logging.getLogger(__name__)


class AIEvaluationService:
    """Service for AI-powered answer evaluation"""
    
    def __init__(
        self,
        api_key: str,
        chroma_db_path: str = "./chroma_db",
        top_k: int = 5,
        model: str = "gemini-2.5-flash-lite",
        temperature: float = 0.3,
        use_local_embeddings: bool = True
    ):
        """
        Initialize AI evaluation service
        
        Args:
            api_key: Google API key for Gemini
            chroma_db_path: Path to ChromaDB
            top_k: Number of chunks to retrieve
            model: Gemini model name
            temperature: LLM temperature (lower = more consistent)
            use_local_embeddings: Use local embeddings for retrieval
        """
        # Initialize retriever with local embeddings
        self.retriever = RetrieverService(
            api_key=api_key if not use_local_embeddings else "",
            persist_directory=chroma_db_path,
            top_k=top_k,
            use_local=use_local_embeddings
        )
        
        # Initialize LLM with lower temperature for consistent evaluation
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=temperature,
            convert_system_message_to_human=True
        )
        
        logger.info(f"Initialized AI evaluation service with model: {model}")
    
    def generate_model_answer(
        self,
        question: str,
        context: str
    ) -> str:
        """
        Generate ideal model answer from textbook content
        
        Args:
            question: The question to answer
            context: Retrieved textbook content
            
        Returns:
            Model answer text
        """
        prompt = f"""You are a Social Studies teacher generating the ideal answer based strictly on the provided textbook content.

TEXTBOOK CONTENT:
{context}

QUESTION:
{question}

INSTRUCTIONS:
1. Answer based ONLY on the textbook content provided above
2. Do NOT use external knowledge
3. Keep the answer appropriate for secondary school students
4. Maximum 150 words
5. Be factually correct and easy to understand
6. Focus on key concepts from the textbook

Generate a concise, accurate model answer:"""
        
        try:
            logger.info("Generating model answer")
            response = self.llm.invoke(prompt)
            model_answer = response.content.strip()
            
            logger.info(f"Model answer generated ({len(model_answer)} characters)")
            return model_answer
            
        except Exception as e:
            logger.error(f"Error generating model answer: {e}")
            raise
    
    def evaluate_answer(
        self,
        question: str,
        student_answer: str,
        model_answer: str,
        context: str,
        total_marks: int = 5
    ) -> Dict[str, Any]:
        """
        Evaluate student answer against model answer and textbook content
        
        Args:
            question: The question asked
            student_answer: Student's submitted answer
            model_answer: Ideal model answer
            context: Retrieved textbook content
            total_marks: Total marks for the question
            
        Returns:
            Evaluation dictionary with marks, feedback, strengths, and improvements
        """
        prompt = f"""You are an expert Social Studies teacher evaluating a student's answer.

TEXTBOOK CONTENT:
{context}

QUESTION:
{question}

MODEL ANSWER:
{model_answer}

STUDENT'S ANSWER:
{student_answer}

EVALUATION CRITERIA:
1. Correctness: Is the answer factually correct according to the textbook?
2. Completeness: Does it cover the key points?
3. Clarity: Is it well-explained and easy to understand?
4. Coverage: Are important concepts mentioned?

SCORING SCALE (out of {total_marks}):
- 0 = Completely incorrect or irrelevant
- 1 = Very poor answer with major misconceptions
- 2 = Partially correct but missing many key points
- 3 = Mostly correct with some gaps
- 4 = Good answer covering most key points
- {total_marks} = Excellent answer covering all key points clearly

IMPORTANT RULES:
- Do NOT reward hallucinated information (facts not in the textbook)
- Do NOT penalize minor grammar/spelling mistakes
- Focus on conceptual understanding
- Compare with both the model answer and textbook content
- Be fair but accurate in assessment

Return your evaluation in the following JSON format ONLY (no additional text):
{{
    "marks_awarded": <number from 0 to {total_marks}>,
    "total_marks": {total_marks},
    "feedback": "<2-3 sentences of constructive feedback>",
    "strengths": [
        "<strength 1>",
        "<strength 2>"
    ],
    "improvements": [
        "<improvement suggestion 1>",
        "<improvement suggestion 2>"
    ]
}}

Evaluate now:"""
        
        try:
            logger.info("Evaluating student answer")
            response = self.llm.invoke(prompt)
            response_text = response.content.strip()
            
            # Parse JSON response
            evaluation = self._parse_evaluation_response(response_text)
            
            # Validate marks
            if evaluation["marks_awarded"] > total_marks:
                logger.warning(f"Marks awarded ({evaluation['marks_awarded']}) exceeded total ({total_marks}), capping")
                evaluation["marks_awarded"] = total_marks
            
            if evaluation["marks_awarded"] < 0:
                logger.warning(f"Marks awarded ({evaluation['marks_awarded']}) is negative, setting to 0")
                evaluation["marks_awarded"] = 0
            
            logger.info(f"Evaluation complete: {evaluation['marks_awarded']}/{total_marks} marks")
            
            return evaluation
            
        except Exception as e:
            logger.error(f"Error evaluating answer: {e}")
            raise
    
    def _parse_evaluation_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON evaluation response from LLM
        
        Args:
            response_text: Raw LLM response
            
        Returns:
            Parsed evaluation dictionary
            
        Raises:
            ValueError: If JSON parsing fails
        """
        try:
            # Remove markdown code blocks if present
            text = response_text.strip()
            
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            
            if text.endswith("```"):
                text = text[:-3]
            
            text = text.strip()
            
            # Parse JSON
            evaluation = json.loads(text)
            
            # Validate required fields
            required_fields = ["marks_awarded", "total_marks", "feedback", "strengths", "improvements"]
            missing_fields = [field for field in required_fields if field not in evaluation]
            
            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")
            
            # Validate types
            if not isinstance(evaluation["marks_awarded"], (int, float)):
                raise ValueError("marks_awarded must be a number")
            
            if not isinstance(evaluation["total_marks"], (int, float)):
                raise ValueError("total_marks must be a number")
            
            if not isinstance(evaluation["feedback"], str):
                raise ValueError("feedback must be a string")
            
            if not isinstance(evaluation["strengths"], list):
                raise ValueError("strengths must be a list")
            
            if not isinstance(evaluation["improvements"], list):
                raise ValueError("improvements must be a list")
            
            # Convert to int if needed
            evaluation["marks_awarded"] = int(evaluation["marks_awarded"])
            evaluation["total_marks"] = int(evaluation["total_marks"])
            
            return evaluation
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse evaluation JSON: {e}")
            logger.error(f"Response text: {response_text[:500]}")
            raise ValueError(f"Invalid JSON response from AI: {str(e)}")
        except Exception as e:
            logger.error(f"Error parsing evaluation: {e}")
            raise ValueError(f"Failed to parse evaluation: {str(e)}")
    
    def evaluate_with_rag(
        self,
        question: str,
        student_answer: str,
        chapter_name: Optional[str] = None,
        total_marks: int = 5
    ) -> Dict[str, Any]:
        """
        Complete evaluation workflow with RAG
        
        1. Retrieve relevant textbook content
        2. Generate model answer
        3. Evaluate student answer
        
        Args:
            question: The question asked
            student_answer: Student's submitted answer
            chapter_name: Optional chapter name for filtered retrieval
            total_marks: Total marks for the question
            
        Returns:
            Complete evaluation including model answer
        """
        try:
            # Step 1: Retrieve relevant textbook content
            logger.info(f"Retrieving context for: {question[:50]}...")
            
            # Build query that emphasizes chapter if provided
            if chapter_name:
                query = f"{chapter_name}: {question}"
            else:
                query = question
            
            chunks = self.retriever.retrieve(query, top_k=5)
            
            if not chunks:
                raise ValueError(
                    "Could not find relevant textbook content for this question. "
                    "Please ensure the question is related to the Social Studies syllabus."
                )
            
            # Format context
            context = self.retriever.format_context_for_llm(chunks)
            
            # Step 2: Generate model answer
            model_answer = self.generate_model_answer(question, context)
            
            # Step 3: Evaluate student answer
            evaluation = self.evaluate_answer(
                question=question,
                student_answer=student_answer,
                model_answer=model_answer,
                context=context,
                total_marks=total_marks
            )
            
            # Add model answer to evaluation
            evaluation["model_answer"] = model_answer
            
            # Add sources
            sources = self.retriever.get_sources(chunks)
            evaluation["sources"] = sources
            
            logger.info(
                f"Complete evaluation: {evaluation['marks_awarded']}/{evaluation['total_marks']} "
                f"marks, {len(sources)} sources"
            )
            
            return evaluation
            
        except Exception as e:
            logger.error(f"Error in evaluation workflow: {e}")
            raise
