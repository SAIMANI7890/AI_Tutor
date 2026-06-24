# 🔧 Fix: "Could only generate 0 valid questions" Error

## Problem
When you try to generate an exam, you get:
```
Exam generation failed: Could only generate 0 valid questions out of 1 requested
```

## Root Cause
**Your ChromaDB vector store is empty!** The AI can't generate questions because there's no textbook content loaded.

## Solution: Load Your Textbooks

### Step 1: Verify the Problem
```bash
cd backend
python verify_vector_store.py
```

If you see "Vector store is EMPTY", continue to Step 2.

### Step 2: Add Your PDF Textbooks
1. Create the data directory if it doesn't exist:
   ```bash
   mkdir data
   ```

2. Add your Social Studies PDF textbooks to `backend/data/`:
   ```
   backend/data/
   ├── history.pdf
   ├── geography.pdf
   ├── politics.pdf
   └── economics.pdf
   ```

3. **Important**: Rename your PDFs to match these categories:
   - `history.pdf` → History questions
   - `geography.pdf` → Geography questions
   - `politics.pdf` → Politics questions
   - `economics.pdf` → Economics questions

### Step 3: Run Ingestion (Local Embeddings - NO API LIMITS!)
```bash
cd backend
python app/rag/ingestion/ingest_all_local.py
```

**Time estimate**: 5-15 minutes depending on PDF size

You'll see output like:
```
[Step 1/5] Loading PDFs...
✓ Loaded 4 documents with 256 pages

[Step 2/5] Chunking documents...
✓ Prepared 1,234 chunks for embedding

[Step 3/5] Generating embeddings...
✓ Generated 1,234 embeddings

[Step 4/5] Storing in vector database...
✓ Successfully stored all chunks

INGESTION COMPLETE
Total Chunks: 1,234
Chunks by Category:
  History: 312 chunks
  Geography: 298 chunks  
  Politics: 315 chunks
  Economics: 309 chunks
```

### Step 4: Verify It Worked
```bash
python verify_vector_store.py
```

You should see:
```
✅ Vector store has 1,234 chunks
  ✅ History: 2 chunks retrieved
  ✅ Geography: 2 chunks retrieved
  ✅ Politics: 2 chunks retrieved
  ✅ Economics: 2 chunks retrieved
✅ Vector store verification complete!
```

### Step 5: Try Exam Generation Again
1. Go to http://localhost:3000/dashboard/social/examination
2. Select a category (e.g., History)
3. Choose MCQ
4. Set 5 questions
5. Click "Generate Test"

It should work now! ✅

---

## Alternative: Use Gemini Embeddings (If Local Fails)

If local embeddings fail, use Gemini embeddings:

```bash
cd backend
python app/rag/ingestion/ingest_all.py
```

**Note**: This uses Gemini API (free tier has limits).

---

## Troubleshooting

### Error: "No PDFs found"
- Make sure PDFs are in `backend/data/` directory
- Check file extensions are `.pdf` (not `.PDF`)

### Error: "Failed to extract text from PDF"
- Your PDF might be image-based (scanned)
- Try converting to text-based PDF using Adobe Acrobat or online tools

### Error: "GEMINI_API_KEY environment variable is required"
- Check `backend/.env` file has `GEMINI_API_KEY=your_key_here`
- If using local embeddings, ignore this (Gemini API not needed)

### Ingestion takes too long (>30 minutes)
- PDFs are too large
- Try splitting PDFs into smaller files
- Or reduce CHUNK_SIZE in .env: `CHUNK_SIZE=500`

### Still getting "0 valid questions" after ingestion
1. Check backend logs for errors
2. Verify categories match exactly: "History", "Geography", "Politics", "Economics"
3. Try selecting multiple categories
4. Try MCQ type first (easier to generate)

---

## Quick Test Command

After ingestion, test question generation directly:

```bash
cd backend
python -c "
from app.services.question_generation.generator import QuestionGeneratorService
from app.models.enums import QuestionType
from app.db.session import get_db

generator = QuestionGeneratorService(
    api_key='your_gemini_key',
    use_local_embeddings=True
)

# Test retrieval
context = generator.retrieve_context_by_category(['History'], top_k_per_category=5)
print(f'Retrieved {len(context)} characters of context')
print('First 200 chars:', context[:200])
"
```

---

## Prevention: Add to CI/CD

Add verification to your startup script:

```bash
# In your startup script (e.g., start.sh)
echo "Verifying vector store..."
python verify_vector_store.py || {
    echo "ERROR: Vector store not initialized!"
    echo "Run: python app/rag/ingestion/ingest_all_local.py"
    exit 1
}
```

---

## Summary

The exam generation works, but needs textbook content loaded first!

**Fix in 3 steps**:
1. Add PDFs to `backend/data/`
2. Run `python app/rag/ingestion/ingest_all_local.py`
3. Verify with `python verify_vector_store.py`

**Time**: 10-20 minutes total

Then exam generation will work perfectly! 🎉
