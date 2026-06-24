# Phase 2: RAG Infrastructure + AI Tutor - Backend Guide

## 🎯 Overview

Phase 2 adds RAG (Retrieval-Augmented Generation) capabilities and an AI Tutor Chat system to the AI Study Companion.

## 📦 New Dependencies

```bash
pip install -r requirements.txt
```

Added packages:
- `langchain==0.1.0` - RAG framework
- `langchain-google-genai==0.0.6` - Gemini integration  
- `google-generativeai==0.3.2` - Google AI SDK
- `chromadb==0.4.22` - Vector database
- `pypdf==3.17.4` - PDF processing
- `tiktoken==0.5.2` - Text tokenization

## 🏗️ Architecture

### RAG Components

```
PDF Files → Loader → Chunker → Embeddings → ChromaDB
                                                ↓
User Question → Embedding → Similarity Search → Retriever
                                                ↓
Retrieved Chunks → Format Context → LLM → Answer + Sources
```

### Directory Structure

```
app/
├── rag/
│   ├── ingestion/              # PDF processing pipeline
│   │   ├── pdf_loader.py       # Load PDFs
│   │   ├── chunker.py          # Split into chunks
│   │   ├── embedding_service.py # Generate embeddings
│   │   ├── vector_store.py     # ChromaDB interface
│   │   └── ingest_all.py       # Main ingestion script
│   ├── retriever/              # Retrieval system
│   │   └── retriever_service.py
│   └── prompts/                # Prompt templates
│       └── tutor_prompt.py
├── models/
│   └── chat.py                 # Chat models
├── schemas/
│   └── chat.py                 # Chat schemas
├── services/
│   ├── tutor_service.py        # AI tutor logic
│   └── chat_service.py         # Chat management
└── api/v1/endpoints/
    ├── chat.py                 # Chat APIs
    └── tutor.py                # Tutor APIs
```

## 🔧 Configuration

Add to `.env`:

```env
# AI Configuration
GEMINI_API_KEY=your-google-api-key

# RAG Configuration
DATA_DIR=data
CHROMA_DB_PATH=./chroma_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
```

## 📄 PDF Ingestion

### 1. Prepare PDFs

Place PDFs in `backend/data/`:
- `social_history.pdf` → Category: History
- `social_geography.pdf` → Category: Geography
- `social_politics.pdf` → Category: Politics
- `social_economics.pdf` → Category: Economics

**Naming Convention:** `social_<category>.pdf`

### 2. Run Ingestion

```bash
python app/rag/ingestion/ingest_all.py
```

**What it does:**
1. Discovers all PDFs in `data/` directory
2. Extracts text from each page
3. Splits text into chunks (1000 chars, 200 overlap)
4. Generates embeddings using Google AI
5. Stores in ChromaDB with metadata

**Expected Output:**
```
============================================================
AI Study Companion - PDF Ingestion Pipeline
============================================================
[Step 1/5] Loading PDFs...
✓ Loaded 4 documents with 420 pages

[Step 2/5] Chunking documents...
History: 120 chunks
Geography: 140 chunks
Politics: 95 chunks
Economics: 105 chunks
✓ Total chunks created: 460

[Step 3/5] Preparing chunks...
✓ Prepared 460 chunks for embedding

[Step 4/5] Generating embeddings...
✓ Generated 460 embeddings

[Step 5/5] Storing in vector database...
✓ Successfully stored all chunks

Total Chunks: 460
============================================================
```

### 3. Verify Ingestion

Check health endpoint:
```bash
curl http://localhost:8000/api/v1/tutor/health
```

Expected response:
```json
{
  "success": true,
  "message": "AI Tutor is ready",
  "data": {
    "status": "healthy",
    "chunks_loaded": 460,
    "model": "gemini-pro"
  }
}
```

## 🔍 How It Works

### Retrieval Process

1. **User asks question:** "What is democracy?"

2. **Generate query embedding:**
   ```python
   query_embedding = embeddings.embed_query(question)
   ```

3. **Search ChromaDB:**
   ```python
   results = collection.query(
       query_embeddings=[query_embedding],
       n_results=5
   )
   ```

4. **Format context:**
   ```python
   context = format_context_for_llm(chunks)
   ```

5. **Create prompt:**
   ```python
   prompt = create_tutor_prompt(context, question)
   ```

6. **Generate answer:**
   ```python
   response = llm.invoke(prompt)
   ```

7. **Extract sources:**
   ```python
   sources = get_sources(chunks)
   ```

### Metadata Structure

Each chunk stores:
```python
{
    "document_name": "social_politics.pdf",
    "category": "Politics",
    "page_number": 23,
    "chunk_index": 0,
    "total_chunks": 5,
    "source": "/path/to/pdf"
}
```

## 🗄️ Database Schema

### New Tables

**chat_sessions:**
```sql
CREATE TABLE chat_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255) DEFAULT 'New Conversation',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**chat_messages:**
```sql
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES chat_sessions(id),
    role VARCHAR(50) NOT NULL,  -- 'user' or 'assistant'
    message TEXT NOT NULL,
    sources TEXT,  -- JSON string
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Run Migration

```bash
alembic upgrade head
```

## 🌐 API Endpoints

### Chat Management

**Create Session:**
```http
POST /api/v1/chat/session
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "New Conversation"
}
```

**Get All Sessions:**
```http
GET /api/v1/chat/sessions
Authorization: Bearer <token>
```

**Get Session with Messages:**
```http
GET /api/v1/chat/session/{session_id}
Authorization: Bearer <token>
```

**Delete Session:**
```http
DELETE /api/v1/chat/session/{session_id}
Authorization: Bearer <token>
```

### AI Tutor

**Ask Question:**
```http
POST /api/v1/tutor/chat
Authorization: Bearer <token>
Content-Type: application/json

{
  "session_id": 1,
  "question": "What is democracy?"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Answer generated successfully",
  "data": {
    "answer": "Democracy is a form of government...",
    "sources": [
      {
        "document": "social_politics.pdf",
        "page": 23,
        "category": "Politics"
      }
    ],
    "message_id": 42,
    "session_id": 1
  }
}
```

**Check Health:**
```http
GET /api/v1/tutor/health
Authorization: Bearer <token>
```

## 🎨 Tutor Personality

Defined in `app/rag/prompts/tutor_prompt.py`:

**Characteristics:**
- Friendly and approachable
- Patient and understanding
- Encouraging and supportive
- Clear and simple explanations
- Suitable for Class 10 students

**Strict Rules:**
1. Only use textbook context
2. Never hallucinate
3. Say "not found" when unavailable
4. Cite sources
5. Simple explanations

## 🧪 Testing

### Test the Ingestion

```python
# Test PDF loading
from app.rag.ingestion.pdf_loader import PDFLoader
loader = PDFLoader("data")
docs = loader.load_all_pdfs()
print(f"Loaded {len(docs)} documents")

# Test chunking
from app.rag.ingestion.chunker import TextChunker
chunker = TextChunker()
chunks = chunker.chunk_all_documents(docs)
print(f"Created {sum(len(c) for c in chunks.values())} chunks")
```

### Test Retrieval

```python
from app.rag.retriever.retriever_service import RetrieverService

retriever = RetrieverService(
    api_key="your-key",
    persist_directory="./chroma_db"
)

results = retriever.retrieve("What is democracy?")
print(f"Retrieved {len(results)} chunks")
```

### Test Tutor

```python
from app.services.tutor_service import TutorService

tutor = TutorService(api_key="your-key")
result = tutor.answer_question("What is democracy?")

print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
```

### Test via API

```bash
# Create session
curl -X POST http://localhost:8000/api/v1/chat/session \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Session"}'

# Ask question
curl -X POST http://localhost:8000/api/v1/tutor/chat \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 1,
    "question": "What is democracy?"
  }'
```

## 🔧 Troubleshooting

### ChromaDB Connection Error

**Issue:** "Vector store not initialized"

**Solution:**
- Run ingestion: `python app/rag/ingestion/ingest_all.py`
- Verify `chroma_db/` directory exists
- Check file permissions

### Embedding API Error

**Issue:** Rate limit or API error

**Solution:**
- Check Gemini API key is valid
- Wait a minute and retry
- Reduce batch size in ingestion

### No Results Retrieved

**Issue:** Retrieval returns empty

**Solution:**
- Verify ingestion completed
- Check ChromaDB has data: `tutor.retriever.collection.count()`
- Try different questions

### Memory Issues

**Issue:** Out of memory during ingestion

**Solution:**
- Process PDFs in smaller batches
- Reduce chunk size temporarily
- Increase system RAM

## 📊 Performance

**Ingestion:**
- ~500 pages: 3-5 minutes
- Depends on: PDF size, internet speed, API rate limits

**Retrieval:**
- Query time: <1 second
- Embedding generation: ~500ms
- Vector search: <100ms
- Total response: 1-3 seconds

**Storage:**
- ChromaDB size: ~50-100MB for 500 pages
- Embeddings: 768 dimensions per chunk

## 🔐 Security

**Implemented:**
- ✅ Authentication required for all endpoints
- ✅ User can only access own sessions
- ✅ Session ownership verification
- ✅ API key stored securely in environment

**Best Practices:**
- Never commit API keys
- Use environment variables
- Validate all inputs
- Sanitize file paths

## 🚀 Deployment

### Environment Variables

```env
# Required
GEMINI_API_KEY=xxx
DATABASE_URL=postgresql://...

# Optional (with defaults)
DATA_DIR=data
CHROMA_DB_PATH=./chroma_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
```

### Production Checklist

- [ ] Run ingestion before deployment
- [ ] Verify ChromaDB persists to disk
- [ ] Include `chroma_db/` in deployment
- [ ] Set proper file permissions
- [ ] Monitor API usage (Gemini)
- [ ] Set up error logging
- [ ] Configure rate limiting

## 📚 Code Examples

### Add Custom PDF Processor

```python
# app/rag/ingestion/custom_loader.py
from app.rag.ingestion.pdf_loader import PDFLoader

class CustomLoader(PDFLoader):
    def extract_category_from_filename(self, filename: str) -> str:
        # Custom logic
        if "math" in filename:
            return "Mathematics"
        return super().extract_category_from_filename(filename)
```

### Customize Retrieval

```python
# app/rag/retriever/custom_retriever.py
from app.rag.retriever.retriever_service import RetrieverService

class CustomRetriever(RetrieverService):
    def retrieve(self, query: str, category: str = None):
        # Add category filtering
        filters = {"category": category} if category else None
        # Use filters in search...
```

### Modify Tutor Prompt

```python
# app/rag/prompts/tutor_prompt.py

CUSTOM_SYSTEM_PROMPT = """
You are a specialized History tutor...
[Your custom instructions]
"""
```

## 📖 References

- [LangChain Documentation](https://python.langchain.com/)
- [Google Gemini API](https://ai.google.dev/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [PyPDF Documentation](https://pypdf.readthedocs.io/)

---

**Phase 2 Backend Complete!** ✅

For frontend integration, see `frontend/README_PHASE2.md`
