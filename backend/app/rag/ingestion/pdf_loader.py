"""
PDF Loading Service
Loads and extracts text from PDF files
"""
import os
from typing import List, Dict, Any
from pathlib import Path
from pypdf import PdfReader
import logging

logger = logging.getLogger(__name__)


class PDFLoader:
    """Service for loading PDF files and extracting text with metadata"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize PDF loader
        
        Args:
            data_dir: Directory containing PDF files
        """
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise ValueError(f"Data directory does not exist: {data_dir}")
    
    def discover_pdfs(self) -> List[Path]:
        """
        Discover all PDF files in the data directory
        
        Returns:
            List of PDF file paths
        """
        pdf_files = list(self.data_dir.glob("*.pdf"))
        logger.info(f"Discovered {len(pdf_files)} PDF files")
        return pdf_files
    
    def extract_category_from_filename(self, filename: str) -> str:
        """
        Extract category from filename
        
        Args:
            filename: PDF filename (e.g., 'social_history.pdf')
            
        Returns:
            Category name (e.g., 'History')
        """
        # Remove extension and prefix
        name = filename.replace('.pdf', '').replace('social_', '')
        
        # Capitalize first letter
        category = name.capitalize()
        
        return category
    
    def load_pdf(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """
        Load a PDF file and extract text with metadata
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of dictionaries containing page text and metadata
        """
        try:
            reader = PdfReader(str(pdf_path))
            document_name = pdf_path.name
            category = self.extract_category_from_filename(document_name)
            
            pages = []
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                
                if text.strip():  # Only include pages with text
                    pages.append({
                        "text": text,
                        "metadata": {
                            "document_name": document_name,
                            "category": category,
                            "page_number": page_num,
                            "source": str(pdf_path)
                        }
                    })
            
            logger.info(f"Loaded {len(pages)} pages from {document_name}")
            return pages
            
        except Exception as e:
            logger.error(f"Error loading PDF {pdf_path}: {e}")
            raise
    
    def load_all_pdfs(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load all PDFs in the data directory
        
        Returns:
            Dictionary mapping document names to their pages
        """
        pdf_files = self.discover_pdfs()
        
        if not pdf_files:
            logger.warning("No PDF files found in data directory")
            return {}
        
        all_documents = {}
        
        for pdf_path in pdf_files:
            try:
                pages = self.load_pdf(pdf_path)
                all_documents[pdf_path.name] = pages
            except Exception as e:
                logger.error(f"Failed to load {pdf_path}: {e}")
                continue
        
        return all_documents
