# 📊 AI Market Analyst Agent

> **Built for VAIA Agentic AI Residency Program**

A multi-functional AI agent that analyzes market research documents using **Retrieval-Augmented Generation (RAG)**. Ask questions, generate summaries, and extract structured data, all powered by Google Gemini and ChromaDB.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 🎯 Features

- **📝 Question Answering**: Ask questions and get contextual answers with source citations
- **📄 Summarization**: Generate comprehensive, executive, or key findings summaries
- **📊 Data Extraction**: Extract structured data as JSON (company metrics, SWOT, competitors)
- **🤖 Autonomous Routing**: AI automatically selects the best tool for your query
- **🎨 Interactive UI**: Beautiful Streamlit web interface
- **🐳 Docker Ready**: Containerized deployment (recommended for Windows)

---

## Screenshots
### QA
<img width="2038" height="1164" alt="image" src="https://github.com/user-attachments/assets/81827e05-b34b-4103-a547-38cbda4cd519" />

### Autonomous Routing
<img width="2047" height="1160" alt="image" src="https://github.com/user-attachments/assets/1342d036-a46a-42c8-9a13-dd9c5f7afb62" />

---

## 📚 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete guide to using the UI, all features explained

- **[TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md)** - System design, architecture, technology stack

---

## 🚀 Quick Start

### Prerequisites

- **Docker** (Recommended for Windows) - [Install Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **OR** Python 3.11+ (for macOS/Linux)
- **Google Gemini API key** - [Get one free here](https://makersuite.google.com/app/apikey)

> **⚠️ Windows Users**: Docker is strongly recommended due to native library compatibility issues.

---

### Option 1: Docker Setup

**Perfect for**: Windows users, quick setup, production deployment

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/MarketAnalystAgent.git
cd MarketAnalystAgent

# 2. Create .env file with your API key
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env

# 3. Build and run Docker container
docker build -t market-analyst .
docker run -d -p 8000:8000 --env-file .env --name market-analyst-api market-analyst

# 4. Install Streamlit (lightweight, only 2 packages)
pip install streamlit requests

# 5. Start the UI
python -m streamlit run app.py --server.headless true
```

**Access the application**: http://localhost:8501

**API Docs**: http://localhost:8000/docs

**Health Check**: http://localhost:8000/api/v1/health

---

### Option 2: Native Python (macOS/Linux)

**Use if**: You prefer native installation and are not on Windows

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/MarketAnalystAgent.git
cd MarketAnalystAgent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env

# 5. Run backend (Terminal 1)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 6. Run frontend (Terminal 2)
streamlit run app.py
```

**Access the application**: http://localhost:8501

---

## ✅ Verify Installation

After starting, check these three things:

1. **API Health**: Visit http://localhost:8000/api/v1/health
   - Should show: `{"status": "healthy", "vector_store": {"total_documents": 2}}`

2. **Streamlit UI**: Visit http://localhost:8501
   - Sidebar should show: "✅ API Status: Healthy"

3. **Test Query**:
   - Go to "🤖 Auto Query" tab
   - Type: "What is Innovate Inc's market share?"
   - Click "🚀 Submit"
   - Should return: "12%" with sources

---

## 🎨 Using the Application

### Interface Overview

The Streamlit UI has **5 tabs**:

1. **🤖 Auto Query** - Type any question, AI picks the right tool
2. **❓ Q&A** - Ask specific questions with source citations
3. **📝 Summarize** - Generate executive summaries or key findings
4. **📊 Extract Data** - Get structured JSON data (download ready)
5. **📖 About** - Technical details and architecture

**Example Queries**:

| What to Ask | Which Tab | Expected Result |
|-------------|-----------|-----------------|
| "What is the market share?" | Auto Query or Q&A | "12%" with sources |
| "Who are the competitors?" | Auto Query or Q&A | List with market shares |
| "Give me an executive summary" | Auto Query or Summarize | 100-word brief |
| "Extract all financial data" | Auto Query or Extract | JSON with metrics |

**See [USER_GUIDE.md](USER_GUIDE.md) for detailed instructions on each feature.**

---

## 📊 API Usage Examples

If you prefer API access over the UI, here are complete examples for all three core tasks:

**Full API documentation**: http://localhost:8000/docs (Swagger UI)

### 1. Question Answering (`/api/v1/qa`)

Ask specific questions and get answers with source citations:

```bash
curl -X POST "http://localhost:8000/api/v1/qa" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Innovate Inc'\''s market share?",
    "top_k": 5
  }'
```

**Response**:
```json
{
  "answer": "Innovate Inc currently holds 12% of the market share.",
  "sources": ["chunk_0", "chunk_3"],
  "source_metadata": [
    {"chunk_index": 0, "start_char": 0, "end_char": 1000, "length": 1000}
  ],
  "confidence": 0.92,
  "question": "What is Innovate Inc's market share?"
}
```

### 2. Summarization (`/api/v1/summarize`)

Generate different types of summaries:

```bash
# Executive summary (100-150 words)
curl -X POST "http://localhost:8000/api/v1/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "summary_type": "executive",
    "max_words": 150
  }'

# Key findings (bullet points)
curl -X POST "http://localhost:8000/api/v1/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "summary_type": "key_findings",
    "max_words": 200
  }'
```

**Response**:
```json
{
  "summary": "Innovate Inc holds 12% market share in the AI-powered CRM sector...",
  "summary_type": "executive",
  "word_count": 145,
  "requested_max_words": 150
}
```

### 3. Data Extraction (`/api/v1/extract`)

Extract structured data as JSON:

```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response**:
```json
{
  "data": {
    "company_name": "Innovate Inc",
    "product_name": "SmartCRM AI",
    "industry_sector": "AI-Powered CRM",
    "market_share": 12.0,
    "competitors": [
      {"name": "MarketLeader Corp", "market_share": 25.0},
      {"name": "TechGiant Solutions", "market_share": 18.0}
    ],
    "swot": {
      "strengths": ["Advanced AI capabilities", "Strong customer base"],
      "weaknesses": ["Limited market share", "High operational costs"],
      "opportunities": ["Emerging markets", "Product diversification"],
      "threats": ["Intense competition", "Regulatory challenges"]
    },
    "strategic_priorities": ["Expand market share", "Enhance AI features"]
  },
  "success": true
}
```

### All Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/qa` | POST | Question answering with RAG |
| `/api/v1/summarize` | POST | Document summarization |
| `/api/v1/extract` | POST | Structured data extraction |
| `/api/v1/auto` | POST | Autonomous query routing |

---

## 🎯 Design Decisions

This section explains the key technical choices made in building this AI Market Analyst Agent and the rationale behind each decision.

### 1. Chunking Strategy

**Choice**: RecursiveCharacterTextSplitter with 1000-character chunks and 200-character overlap (20%)

**Why**:
- **Chunk Size (1000 chars)**: Balances context preservation with retrieval granularity
  - 1000 characters ≈ 200-250 tokens for English text
  - Fits well within embedding model's optimal input range (512-1024 tokens)
  - Not too small (which loses context) or too large (which dilutes relevance)
  - Typical market research paragraphs fit well within this size

- **Overlap (200 chars, 20%)**: Prevents information loss at chunk boundaries
  - Ensures continuity for concepts spanning multiple chunks
  - 20% is empirically optimal for most document types
  - Provides redundancy that improves retrieval recall
  - Critical for queries that might match content near chunk edges

- **Recursive Splitting**: Respects document structure
  - Splits by hierarchy: `\n\n` → `\n` → `. ` → `, ` → ` ` → characters
  - Maintains semantic coherence within chunks (keeps paragraphs/sentences intact)
  - Results in more meaningful retrievals than arbitrary character splits

**Implementation**: src/data/chunking.py:35-62

---

### 2. Embedding Model

**Choice**: Google Gemini `text-embedding-004` (768 dimensions)

**Why**:
- **Cost Efficiency**: Free tier with generous quota (perfect for prototypes and production)
- **Quality**: Latest Gemini embedding model (2024), optimized for semantic search and RAG
- **Dimensionality (768)**: Good balance between quality and computational efficiency
  - Lower than OpenAI ada-002 (1536 dims) → faster similarity search
  - Higher than many open-source models (384-512 dims) → better semantic capture
- **Cloud-based**: No need for local GPU or model management
- **Multilingual Support**: Better than many alternatives for non-English text

**Alternatives Considered**:

| Model | Pros | Cons | Verdict |
|-------|------|------|---------|
| OpenAI ada-002 | High quality | Costs money, 1536 dims (more compute) | ❌ Cost prohibitive |
| Sentence-BERT | Open source | Requires local GPU, larger models | ❌ Infrastructure overhead |
| Cohere Embed | Good quality | Paid tier | ❌ Cost |
| **Gemini text-embedding-004** | **Free, cloud-based, excellent quality** | **None for this use case** | ✅ **Selected** |

**Implementation**: src/retrieval/embedder.py:35-45

---

### 3. Vector Database

**Choice**: ChromaDB with cosine similarity

**Why**:
- **Lightweight & Embeddable**: No separate server needed, single pip install
- **Persistent Storage**: Automatic persistence with minimal setup (just specify directory)
- **Excellent Python Integration**: Native Python API, no REST overhead for local use
- **Fast Similarity Search**: HNSW algorithm for efficient nearest-neighbor search
- **Metadata Filtering**: Built-in support for filtering by chunk metadata
- **Free & Open-Source**: No licensing costs or cloud dependencies
- **Performance**: Handles millions of vectors efficiently (sufficient for this scale)
- **Developer Experience**: Active development, good documentation

**Alternatives Considered**:

| Database | Pros | Cons | Verdict |
|----------|------|------|---------|
| Pinecone | Managed, scalable | Requires cloud, paid for production | ❌ Unnecessary cloud dependency |
| Weaviate | Feature-rich | Heavy, requires Docker setup | ❌ Over-engineered for this use case |
| **ChromaDB** | **Perfect balance of simplicity & power** | **None** | ✅ **Selected** |

**Implementation**: src/retrieval/vectorstore.py:40-61

---

### 4. Data Extraction Prompt Design

**Challenge**: Get reliable, structured JSON output from an LLM (which tends to be verbose and unstructured)

**Solution**: Multi-layered prompt engineering strategy

**Design Principles**:

1. **Explicit Schema Definition**:
   - Show exact JSON structure with type annotations in the prompt
   - Provide field descriptions inline with schema
   - Example: `"market_share": "number - company's market share as percentage"`

2. **Strict Output Instructions**:
   - Clear directive: "IMPORTANT: Output ONLY valid JSON"
   - Explicit prohibition of markdown, explanations, or extra text
   - Prevents common LLM behavior of adding commentary

3. **Low Temperature (0.1)**:
   - Near-deterministic output for consistency
   - Reduces creativity/variation in favor of structured compliance
   - Critical for production-grade reliability

4. **Robust Post-Processing** (src/agents/extractor.py:144-173):
   - Strips markdown code blocks (``json ... ``)
   - Extracts JSON between first `{` and last `}`
   - Handles LLMs that ignore "no markdown" instruction

5. **Type Validation & Casting** (src/agents/extractor.py:175-215):
   - Converts string numbers ("12%") to proper types (12.0)
   - Validates SWOT structure exists
   - Provides graceful fallbacks for missing fields

**Example Prompt Structure**:
```
You are a data extraction assistant. Extract structured information...

IMPORTANT: Output ONLY valid JSON. No explanatory text, markdown, or code blocks.

Extract into this exact structure:
{
  "company_name": "string - name of the company",
  "market_share": "number - percentage as number",
  ...
}

Document:
[full document text]

JSON Output:
```

**Implementation**: src/agents/extractor.py:101-142

---

## 🏗️ Project Structure

```
MarketAnalystAgent/
├── README.md                      # This file (quick start)
├── USER_GUIDE.md                  # Complete user guide
├── TECHNICAL_ARCHITECTURE.md      # System design docs
├── NON_TECHNICAL_DEMO.md          # Demo script
├── requirements.txt               # Python dependencies
├── .env                           # API keys (create this)
├── Dockerfile                     # Container definition
├── app.py                         # Streamlit UI
│
├── data/
│   └── innovate_inc_report.txt    # Sample market research document
│
├── src/
│   ├── main.py                    # FastAPI application
│   ├── config/settings.py         # Configuration
│   ├── data/                      # Document loading & chunking
│   ├── retrieval/                 # Embeddings & vector store
│   ├── agents/                    # QA, Summarizer, Extractor, Router
│   └── api/                       # REST endpoints
│
└── tests/                         # Unit tests
```

---

## 💡 Key Technical Highlights

- **RAG Architecture**: ChromaDB + Google Gemini embeddings (768-dim)
- **Smart Chunking**: 1000 chars with 200 char overlap for context preservation
- **Autonomous Routing**: AI automatically picks Q&A, Summarize, or Extract
- **Source Citations**: Every answer shows where information came from
- **Production Ready**: Docker containerized, health checks, error handling

---

## 📝 License

MIT License - feel free to use this code for your own projects!
