"""
Complete PDF Ingestion Pipeline (LOCAL EMBEDDINGS - No API limits!)
Uses local sentence-transformers instead of Google Gemini
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from app.rag.ingestion.pdf_loader import PDFLoader
from app.rag.ingestion.chunker import TextChunker
from app.rag.ingestion.local_embedding_service import LocalEmbeddingService
from app.rag.ingestion.vector_store import VectorStore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run complete ingestion pipeline with LOCAL embeddings"""
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    DATA_DIR = os.getenv("DATA_DIR", "data")
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    logger.info("=" * 60)
    logger.info("AI Study Companion - PDF Ingestion Pipeline (LOCAL)")
    logger.info("=" * 60)
    logger.info(f"Data Directory: {DATA_DIR}")
    logger.info(f"ChromaDB Path: {CHROMA_DB_PATH}")
    logger.info(f"Chunk Size: {CHUNK_SIZE}")
    logger.info(f"Chunk Overlap: {CHUNK_OVERLAP}")
    logger.info(f"Embedding: LOCAL (no API limits!)")
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
        
        # Step 4: Generate embeddings (LOCAL - NO API LIMITS!)
        logger.info("\n[Step 4/5] Generating embeddings with LOCAL model...")
        logger.info("  This will take a few minutes but has NO API limits!")
        
        # Initialize local embedding service
        logger.info("  Loading local embedding model (first time may download ~90MB)...")
        embedding_service = LocalEmbeddingService()
        
        # Extract texts
        texts = [chunk["text"] for chunk in all_chunks]
        
        # Generate ALL embeddings at once (no rate limits!)
        logger.info(f"  Processing {len(texts)} texts locally...")
        all_embeddings = embedding_service.generate_embeddings(texts)
        
        logger.info(f"✓ Generated {len(all_embeddings)} embeddings (NO API calls!)")
        
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
        logger.info("\n⚠️  NOTE: You're using LOCAL embeddings.")
        logger.info("The AI Tutor will also need to use the same embedding model.")
        logger.info("Update tutor_service.py to use LocalEmbeddingService.")
        
    except Exception as e:
        logger.error(f"\n✗ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
