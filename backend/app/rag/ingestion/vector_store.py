"""
Vector Store Service
Manages ChromaDB vector storage
"""
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    """Service for managing ChromaDB vector store"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize vector store
        
        Args:
            persist_directory: Directory to persist ChromaDB data
        """
        self.persist_directory = persist_directory
        
        # Initialize ChromaDB client with persistent storage
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="social_studies",
            metadata={"description": "Social Studies textbook content"}
        )
        
        logger.info(f"Initialized vector store at {persist_directory}")
    
    def add_chunks(
        self, 
        chunks: List[Dict[str, Any]], 
        embeddings: List[List[float]]
    ) -> None:
        """
        Add chunks with embeddings to vector store
        
        Args:
            chunks: List of chunk dictionaries with text and metadata
            embeddings: List of embedding vectors
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must match number of embeddings")
        
        # Prepare data for ChromaDB
        ids = []
        documents = []
        metadatas = []
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # Create unique ID
            doc_name = chunk["metadata"]["document_name"]
            page_num = chunk["metadata"]["page_number"]
            chunk_idx = chunk["metadata"]["chunk_index"]
            chunk_id = f"{doc_name}_{page_num}_{chunk_idx}_{i}"
            
            ids.append(chunk_id)
            documents.append(chunk["text"])
            metadatas.append(chunk["metadata"])
        
        # Add to collection
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        logger.info(f"Added {len(chunks)} chunks to vector store")
    
    def clear_collection(self) -> None:
        """Clear all data from the collection"""
        # Delete and recreate collection
        try:
            self.client.delete_collection(name="social_studies")
            logger.info("Deleted existing collection")
        except:
            pass
        
        self.collection = self.client.get_or_create_collection(
            name="social_studies",
            metadata={"description": "Social Studies textbook content"}
        )
        logger.info("Created new collection")
    
    def get_collection_count(self) -> int:
        """Get number of items in collection"""
        return self.collection.count()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store
        
        Returns:
            Dictionary containing stats
        """
        count = self.get_collection_count()
        
        # Get all metadata to count by category
        if count > 0:
            results = self.collection.get(limit=count)
            metadatas = results["metadatas"]
            
            # Count by category
            category_counts = {}
            for metadata in metadatas:
                category = metadata.get("category", "Unknown")
                category_counts[category] = category_counts.get(category, 0) + 1
            
            return {
                "total_chunks": count,
                "category_counts": category_counts
            }
        
        return {
            "total_chunks": 0,
            "category_counts": {}
        }
