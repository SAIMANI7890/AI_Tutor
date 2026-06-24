"""
Complete PDF Ingestion Pipeline
Discovers, loads, chunks, embeds, and stores all PDFs
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging
from pypdf import PdfReader
# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from app.rag.ingestion.pdf_loader import PDFLoader
from app.rag.ingestion.chunker import TextChunker
from app.rag.ingestion.embedding_service import EmbeddingService
from app.rag.ingestion.vector_store import VectorStore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run complete ingestion pipeline"""
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is required")
    
    DATA_DIR = os.getenv("DATA_DIR", "data")
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    logger.info("=" * 60)
    logger.info("AI Study Companion - PDF Ingestion Pipeline")
    logger.info("=" * 60)
    logger.info(f"Data Directory: {DATA_DIR}")
    logger.info(f"ChromaDB Path: {CHROMA_DB_PATH}")
    logger.info(f"Chunk Size: {CHUNK_SIZE}")
    logger.info(f"Chunk Overlap: {CHUNK_OVERLAP}")
    logger.info("=" * 60)
    
    try:
        # Step 1: Load PDFs
        logger.info("\n[Step 1/5] Loading PDFs...")
        pdf_loader = PDFLoader(data_dir=DATA_DIR)
        documents = pdf_loader.load_all_pdfs()
        
        if not documents:
            logger.error("No PDFs found! Please add PDF files to the data directory.")
            return
        
        total_pages = sum(len(pages) for pages in documents.values())
        logger.info(f"✓ Loaded {len(documents)} documents with {total_pages} pages")
        
        # Step 2: Chunk documents
        logger.info("\n[Step 2/5] Chunking documents...")
        chunker = TextChunker(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        chunked_documents = chunker.chunk_all_documents(documents)
        
        # Step 3: Prepare all chunks
        logger.info("\n[Step 3/5] Preparing chunks...")
        all_chunks = []
        for doc_name, chunks in chunked_documents.items():
            all_chunks.extend(chunks)
        
        logger.info(f"✓ Prepared {len(all_chunks)} chunks for embedding")
        
        # Step 4: Generate embeddings
        logger.info("\n[Step 4/5] Generating embeddings...")
        embedding_service = EmbeddingService(api_key=GEMINI_API_KEY)
        
        # Extract texts
        texts = [chunk["text"] for chunk in all_chunks]
        
        # Generate embeddings in batches to avoid rate limits
        batch_size = 50  # Reduced from 100 to stay under rate limit
        all_embeddings = []
        
        import time
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_num = i//batch_size + 1
            total_batches = (len(texts)-1)//batch_size + 1
            logger.info(f"  Generating embeddings for batch {batch_num}/{total_batches} (texts {i+1}-{min(i+batch_size, len(texts))}/{len(texts)})")
            
            try:
                batch_embeddings = embedding_service.generate_embeddings(batch_texts)
                all_embeddings.extend(batch_embeddings)
                
                # Rate limiting: Wait if we're not on the last batch
                if i + batch_size < len(texts):
                    wait_time = 35  # Wait 35 seconds between batches (free tier: 100 req/min)
                    logger.info(f"  Waiting {wait_time}s to respect rate limits...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                if "429" in str(e) or "quota" in str(e).lower():
                    logger.warning(f"  Rate limit hit! Waiting 60 seconds before retry...")
                    time.sleep(60)
                    # Retry this batch
                    batch_embeddings = embedding_service.generate_embeddings(batch_texts)
                    all_embeddings.extend(batch_embeddings)
                    if i + batch_size < len(texts):
                        logger.info(f"  Waiting {wait_time}s to respect rate limits...")
                        time.sleep(wait_time)
                else:
                    raise
        
        logger.info(f"✓ Generated {len(all_embeddings)} embeddings")
        
        # Step 5: Store in vector database
        logger.info("\n[Step 5/5] Storing in vector database...")
        vector_store = VectorStore(persist_directory=CHROMA_DB_PATH)
        
        # Clear existing data
        logger.info("  Clearing existing data...")
        vector_store.clear_collection()
        
        # Add chunks with embeddings
        logger.info("  Adding chunks to vector store...")
        vector_store.add_chunks(all_chunks, all_embeddings)
        
        logger.info("✓ Successfully stored all chunks")
        
        # Display statistics
        logger.info("\n" + "=" * 60)
        logger.info("INGESTION COMPLETE")
        logger.info("=" * 60)
        
        stats = vector_store.get_stats()
        logger.info(f"\nTotal Chunks: {stats['total_chunks']}")
        logger.info("\nChunks by Category:")
        for category, count in sorted(stats['category_counts'].items()):
            logger.info(f"  {category}: {count} chunks")
        
        logger.info("\n" + "=" * 60)
        logger.info("✓ PDF ingestion pipeline completed successfully!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"\n✗ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
