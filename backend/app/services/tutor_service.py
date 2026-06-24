"""
AI Tutor Service
Handles AI-powered tutoring using RAG
"""
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from app.rag.retriever.retriever_service import RetrieverService
from app.rag.prompts.tutor_prompt import (
    create_tutor_prompt, 
    GREETING_PROMPT, 
    is_greeting
)
import logging

logger = logging.getLogger(__name__)


class TutorService:
    """Service for AI tutoring with RAG"""
    
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
        Initialize tutor service
        
        Args:
            api_key: Google API key (for text generation)
            chroma_db_path: Path to ChromaDB
            top_k: Number of chunks to retrieve
            model: Gemini model name
            temperature: LLM temperature (lower = more focused)
            use_local_embeddings: Use local embeddings for retrieval (default: True)
        """
        # Initialize retriever with local embeddings (no API limits!)
        self.retriever = RetrieverService(
            api_key=api_key if not use_local_embeddings else "",
            persist_directory=chroma_db_path,
            top_k=top_k,
            use_local=use_local_embeddings
        )
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=temperature,
            convert_system_message_to_human=True
        )
        
        logger.info(f"Initialized tutor service with model: {model}")
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Answer a student's question using RAG
        
        Args:
            question: Student's question
            
        Returns:
            Dictionary containing answer and sources
        """
        try:
            # Check if it's a greeting
            if is_greeting(question):
                response = self.llm.invoke(GREETING_PROMPT)
                return {
                    "answer": response.content,
                    "sources": []
                }
            
            # Retrieve relevant context
            logger.info(f"Retrieving context for: {question}")
            chunks = self.retriever.retrieve(question)
            
            if not chunks:
                return {
                    "answer": "I could not find this information in the Social Studies textbook.",
                    "sources": []
                }
            
            # Format context for LLM
            context = self.retriever.format_context_for_llm(chunks)
            
            # Create prompt
            prompt = create_tutor_prompt(context, question)
            
            # Get answer from LLM
            logger.info("Generating answer from LLM")
            response = self.llm.invoke(prompt)
            answer = response.content
            
            # Check if the answer is a refusal (hallucination protection)
            # If the AI refuses to answer, do NOT return sources
            answer_lower = answer.lower()
            refusal_phrases = [
                "could not find",
                "not found",
                "not in the textbook",
                "don't have information",
                "no information about"
            ]
            
            is_refusal = any(phrase in answer_lower for phrase in refusal_phrases)
            
            if is_refusal:
                logger.info("AI refused to answer (topic not in textbook)")
                return {
                    "answer": answer,
                    "sources": []  # No sources for refused answers
                }
            
            # Extract sources (only for valid answers)
            sources = self.retriever.get_sources(chunks)
            
            logger.info(f"Generated answer with {len(sources)} sources")
            
            return {
                "answer": answer,
                "sources": sources
            }
            
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            raise
