"""
Quick verification script to check if vector store has data
"""
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.rag.retriever.retriever_service import RetrieverService
from app.core.config import settings

def main():
    print("=" * 60)
    print("Vector Store Verification")
    print("=" * 60)
    
    try:
        # Initialize retriever
        print("\n[1/3] Connecting to ChromaDB...")
        retriever = RetrieverService(
            api_key="",  # Not needed for local embeddings
            persist_directory=settings.CHROMA_DB_PATH,
            use_local=True
        )
        
        # Check chunk count
        print("[2/3] Counting chunks...")
        chunk_count = retriever.get_chunk_count()
        
        if chunk_count == 0:
            print("\n❌ ERROR: Vector store is EMPTY!")
            print("\nYou need to run the ingestion script first:")
            print("  cd backend")
            print("  python app/rag/ingestion/ingest_all_local.py")
            print("\nThis will load your PDF textbooks into the database.")
            return False
        
        print(f"✅ Vector store has {chunk_count} chunks")
        
        # Test retrieval for each category
        print("\n[3/3] Testing retrieval for each category...")
        categories = ["History", "Geography", "Politics", "Economics"]
        
        for category in categories:
            try:
                query = f"Important topics in {category}"
                chunks = retriever.retrieve(query, top_k=2)
                
                # Filter by category
                cat_chunks = [c for c in chunks if c['metadata'].get('category') == category]
                
                if cat_chunks:
                    print(f"  ✅ {category}: {len(cat_chunks)} chunks retrieved")
                else:
                    print(f"  ⚠️  {category}: No chunks found (may need ingestion)")
            except Exception as e:
                print(f"  ❌ {category}: Error - {str(e)}")
        
        print("\n" + "=" * 60)
        print("✅ Vector store verification complete!")
        print("=" * 60)
        return True
        
    except ValueError as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nThe vector store has not been initialized.")
        print("\nTo fix this:")
        print("  1. Make sure you have PDF files in backend/data/")
        print("  2. Run: cd backend")
        print("  3. Run: python app/rag/ingestion/ingest_all_local.py")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
