"""
Retriever Service
Retrieves relevant chunks from vector store based on queries
"""
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
import logging
import os

logger = logging.getLogger(__name__)


class RetrieverService:
    """Service for retrieving relevant context from vector store"""
    
    def __init__(
        self, 
        api_key: str = "",
        persist_directory: str = "./chroma_db",
        top_k: int = 5,
        use_local: bool = True
    ):
        """
        Initialize retriever service
        
        Args:
            api_key: Google API key for embeddings (not needed if use_local=True)
            persist_directory: ChromaDB persist directory
            top_k: Number of top results to retrieve
            use_local: Use local embeddings (default: True, no API limits!)
        """
        self.top_k = top_k
        self.use_local = use_local
        
        # Initialize embedding service
        if use_local:
            logger.info("Using LOCAL embeddings (no API limits!)")
            from app.rag.ingestion.local_embedding_service import LocalEmbeddingService
            self.embeddings = LocalEmbeddingService()
        else:
            logger.info("Using Gemini embeddings (requires API key)")
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            if not api_key:
                raise ValueError("API key required when use_local=False")
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                google_api_key=api_key
            )
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get collection
        try:
            self.collection = self.client.get_collection(name="social_studies")
            logger.info(f"Connected to vector store with {self.collection.count()} chunks")
        except Exception as e:
            logger.error(f"Failed to connect to vector store: {e}")
            raise ValueError(
                "Vector store not initialized. Please run ingestion first: "
                "python app/rag/ingestion/ingest_all_local.py"
            )
    
    def get_chunk_count(self) -> int:
        """Get total number of chunks in vector store"""
        try:
            return self.collection.count()
        except Exception:
            return 0
    
    def retrieve(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks for a query
        
        Args:
            query: User question
            top_k: Number of results to retrieve (overrides default)
            
        Returns:
            List of relevant chunks with metadata and scores
        """
        k = top_k if top_k is not None else self.top_k
        
        try:
            # Generate query embedding
            if self.use_local:
                query_embedding = self.embeddings.generate_embedding(query)
            else:
                query_embedding = self.embeddings.embed_query(query)
            
            # Search in vector store
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            retrieved_chunks = []
            
            if results and results["documents"] and len(results["documents"]) > 0:
                documents = results["documents"][0]
                metadatas = results["metadatas"][0]
                distances = results["distances"][0]
                
                for doc, metadata, distance in zip(documents, metadatas, distances):
                    # Convert distance to similarity score (lower distance = higher similarity)
                    similarity_score = 1 / (1 + distance)
                    
                    retrieved_chunks.append({
                        "text": doc,
                        "metadata": metadata,
                        "similarity_score": similarity_score
                    })
            
            logger.info(f"Retrieved {len(retrieved_chunks)} chunks for query")
            return retrieved_chunks
            
        except Exception as e:
            logger.error(f"Error retrieving chunks: {e}")
            raise
    
    def format_context_for_llm(self, chunks: List[Dict[str, Any]]) -> str:
        """
        Format retrieved chunks into context string for LLM
        
        Args:
            chunks: List of retrieved chunks
            
        Returns:
            Formatted context string
        """
        if not chunks:
            return ""
        
        context_parts = []
        
        for i, chunk in enumerate(chunks, start=1):
            metadata = chunk["metadata"]
            text = chunk["text"]
            
            context_part = f"""
[Source {i}]
Document: {metadata['document_name']}
Category: {metadata['category']}
Page: {metadata['page_number']}

Content:
{text}
"""
            context_parts.append(context_part)
        
        return "\n".join(context_parts)
    
    def get_sources(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract source information from chunks
        
        Args:
            chunks: List of retrieved chunks
            
        Returns:
            List of source dictionaries
        """
        sources = []
        seen = set()
        
        for chunk in chunks:
            metadata = chunk["metadata"]
            
            # Create unique key for deduplication
            source_key = (
                metadata["document_name"],
                metadata["page_number"],
                metadata["category"]
            )
            
            if source_key not in seen:
                seen.add(source_key)
                sources.append({
                    "document": metadata["document_name"],
                    "page": metadata["page_number"],
                    "category": metadata["category"]
                })
        
        return sources
