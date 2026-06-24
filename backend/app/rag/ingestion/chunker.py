"""
Text Chunking Service
Splits text into manageable chunks for embedding
"""
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)


class TextChunker:
    """Service for splitting text into chunks"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize text chunker
        
        Args:
            chunk_size: Maximum size of each chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        logger.info(f"Initialized chunker with size={chunk_size}, overlap={chunk_overlap}")
    
    def chunk_page(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Chunk a single page
        
        Args:
            page_data: Dictionary containing page text and metadata
            
        Returns:
            List of chunks with metadata
        """
        text = page_data["text"]
        metadata = page_data["metadata"]
        
        # Split text into chunks
        chunks = self.splitter.split_text(text)
        
        # Create chunk dictionaries with metadata
        chunk_dicts = []
        for i, chunk_text in enumerate(chunks):
            chunk_dict = {
                "text": chunk_text,
                "metadata": {
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            }
            chunk_dicts.append(chunk_dict)
        
        return chunk_dicts
    
    def chunk_document(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Chunk all pages in a document
        
        Args:
            pages: List of page data dictionaries
            
        Returns:
            List of all chunks from the document
        """
        all_chunks = []
        
        for page_data in pages:
            chunks = self.chunk_page(page_data)
            all_chunks.extend(chunks)
        
        return all_chunks
    
    def chunk_all_documents(
        self, 
        documents: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Chunk all documents
        
        Args:
            documents: Dictionary mapping document names to their pages
            
        Returns:
            Dictionary mapping document names to their chunks
        """
        chunked_documents = {}
        total_chunks = 0
        
        for doc_name, pages in documents.items():
            chunks = self.chunk_document(pages)
            chunked_documents[doc_name] = chunks
            total_chunks += len(chunks)
            
            category = chunks[0]["metadata"]["category"] if chunks else "Unknown"
            logger.info(f"{category}: {len(chunks)} chunks from {doc_name}")
        
        logger.info(f"Total chunks created: {total_chunks}")
        
        return chunked_documents
