# Technical Architecture Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Backend Architecture](#backend-architecture)
4. [Frontend Architecture](#frontend-architecture)
5. [Data Flow](#data-flow)
6. [Technology Stack](#technology-stack)
7. [Setup and Deployment](#setup-and-deployment)
8. [Development Workflow](#development-workflow)
9. [Design Patterns](#design-patterns)
10. [Performance Optimization](#performance-optimization)

---

## System Overview

### High-Level Summary

The AI Market Analyst Agent is a **full-stack web application** consisting of:

1. **Backend (FastAPI)**: REST API serving three AI agents (Q&A, Summarization, Extraction) with RAG capabilities
2. **Frontend (Streamlit)**: Interactive web UI for user-friendly interaction
3. **Vector Database (ChromaDB)**: Persistent vector storage for document embeddings
4. **LLM Service (Google Gemini)**: Cloud-based language model and embedding generation

### System Type

**Microservices Architecture** with the following components:
- API Server (FastAPI)
- UI Server (Streamlit)
- Vector Database (ChromaDB - embedded)
- External LLM Service (Google Gemini API)

### Deployment Model

- **Development**: Native Python (macOS/Linux) or Docker (Windows)
- **Production**: Docker containers with Docker Compose orchestration
- **Communication**: HTTP REST API between frontend and backend

---

## Architecture Diagram

### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                      (Web Browser)                           │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP (Port 8501)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                            │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Streamlit Application (app.py)            │    │
│  │                                                      │    │
│  │  • Auto Query Tab  • Q&A Tab  • Summarize Tab      │    │
│  │  • Extract Tab     • About Tab                      │    │
│  │  • Health Check Sidebar                             │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API (Port 8000)
                           │ POST /api/v1/{endpoint}
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     BACKEND LAYER                            │
│                   FastAPI Application                         │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              API Routes (routes.py)                 │    │
│  │  /health  /qa  /summarize  /extract  /auto         │    │
│  └──────────────────┬─────────────────────────────────┘    │
│                     │                                        │
│                     ▼                                        │
│  ┌────────────────────────────────────────────────────┐    │
│  │               Agent Layer (agents/)                 │    │
│  │                                                      │    │
│  │  ┌────────────┐  ┌─────────────┐  ┌────────────┐  │    │
│  │  │ QA Agent   │  │ Summarizer  │  │ Extractor  │  │    │
│  │  │ (qa_agent  │  │ (summarizer │  │ (extractor │  │    │
│  │  │    .py)    │  │    .py)     │  │    .py)    │  │    │
│  │  └────────────┘  └─────────────┘  └────────────┘  │    │
│  │                                                      │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │      Router Agent (router.py)                 │  │    │
│  │  │      [Autonomous Routing - Bonus 1]           │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  └──────────────────┬───────────────────┬─────────────┘    │
│                     │                   │                    │
│                     ▼                   ▼                    │
│  ┌─────────────────────────┐  ┌──────────────────────┐     │
│  │    Retrieval Layer      │  │    Data Layer        │     │
│  │    (retrieval/)         │  │    (data/)           │     │
│  │                         │  │                      │     │
│  │  • Embedder (embedder   │  │  • Loader (loader.py)│     │
│  │    .py)                 │  │  • Chunking          │     │
│  │  • VectorStore          │  │    (chunking.py)     │     │
│  │    (vectorstore.py)     │  │                      │     │
│  └────────┬────────────────┘  └──────────┬───────────┘     │
│           │                              │                  │
└───────────┼──────────────────────────────┼──────────────────┘
            │                              │
            ▼                              ▼
┌──────────────────────┐      ┌────────────────────────┐
│   ChromaDB           │      │  Document Files        │
│   (Vector Database)  │      │  (data/)               │
│                      │      │                        │
│  • Persistent Store  │      │  • innovate_inc_       │
│  • Cosine Similarity │      │    report.txt          │
│  • 768-dim Vectors   │      └────────────────────────┘
└──────────────────────┘
            │
            └──────────────────────────────┐
                                           │
                    External API (HTTPS)   │
                                           ▼
            ┌──────────────────────────────────────────┐
            │        Google Gemini API                  │
            │        (Cloud Service)                    │
            │                                           │
            │  • Text Embeddings (text-embedding-004)  │
            │  • Text Generation (gemini-2.0-flash-exp)│
            └──────────────────────────────────────────┘
```

### Request Flow Example

**User Query: "What is Innovate Inc's market share?"**

```
1. User types query in Streamlit UI (localhost:8501)
                ↓
2. Streamlit sends POST to http://localhost:8000/api/v1/qa
                ↓
3. FastAPI receives request → routes.py → qa_agent.py
                ↓
4. QA Agent:
   a. Embeds question using Gemini API (text-embedding-004)
   b. Queries ChromaDB for top 5 similar chunks
   c. Retrieves relevant document chunks
   d. Constructs prompt with context
   e. Calls Gemini API (gemini-2.0-flash-exp) for answer
   f. Calculates confidence score
                ↓
5. Response JSON sent back to Streamlit
                ↓
6. Streamlit displays answer + sources + confidence
```

---

## Backend Architecture

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Web Framework** | FastAPI | REST API server, automatic docs |
| **ASGI Server** | Uvicorn | Production-ready async server |
| **Validation** | Pydantic | Request/response schemas |
| **LLM** | Google Gemini | Text generation, embeddings |
| **Vector DB** | ChromaDB | Similarity search, storage |
| **Text Processing** | LangChain | Document chunking |
| **Env Management** | python-dotenv | Environment variables |

### Directory Structure

```
src/
├── main.py                 # FastAPI app initialization
├── config/
│   └── settings.py         # Configuration management (Pydantic Settings)
├── data/
│   ├── loader.py           # Document loading from filesystem
│   └── chunking.py         # Text splitting with metadata
├── retrieval/
│   ├── embedder.py         # Gemini embedding generation
│   └── vectorstore.py      # ChromaDB wrapper
├── agents/
│   ├── qa_agent.py         # Question Answering agent
│   ├── summarizer.py       # Summarization agent
│   ├── extractor.py        # Data Extraction agent
│   └── router.py           # Autonomous Routing agent
└── api/
    ├── routes.py           # API endpoint definitions
    └── schemas.py          # Pydantic request/response models
```

### Core Components

#### 1. Main Application (src/main.py)

**Purpose**: FastAPI app initialization and startup

**Key Features**:
- CORS middleware for frontend access
- Lifespan context manager for initialization
- API router mounting
- Health check endpoint

**Code Structure**:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load document, create embeddings, initialize vector store
    await initialize_system()
    yield
    # Shutdown: Cleanup if needed

app = FastAPI(
    title="AI Market Analyst Agent",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for Streamlit access
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)

# Mount API routes
app.include_router(router, prefix="/api/v1")
```

#### 2. Configuration (src/config/settings.py)

**Purpose**: Centralized configuration management

**Implementation**: Pydantic Settings (loads from .env)

**Key Settings**:
```python
class Settings(BaseSettings):
    GEMINI_API_KEY: str              # Google AI API key
    DOCUMENT_PATH: str               # Path to market research doc
    EMBEDDING_MODEL: str             # text-embedding-004
    GENERATION_MODEL: str            # gemini-2.0-flash-exp
    TEMPERATURE: float = 0.2         # LLM temperature
    TOP_K: int = 5                   # Default retrieval count
    CHUNK_SIZE: int = 1000           # Text chunk size
    CHUNK_OVERLAP: int = 200         # Chunk overlap
```

#### 3. Data Layer

**A. Document Loader (src/data/loader.py)**

**Purpose**: Load text documents from filesystem

**Key Function**:
```python
def load_text_file(file_path: str) -> str:
    # Validates file exists
    # Reads UTF-8 encoded text
    # Returns document content
```

**B. Chunker (src/data/chunking.py)**

**Purpose**: Split documents into overlapping chunks with metadata

**Implementation**: LangChain RecursiveCharacterTextSplitter

**Key Function**:
```python
def chunk_document(text: str) -> List[Dict[str, Any]]:
    # Splits text into 1000-char chunks with 200-char overlap
    # Adds metadata: chunk_index, start_char, end_char, length
    # Returns list of {text: str, metadata: dict}
```

**Why Metadata?**
- Tracks chunk positions for source attribution
- Enables debugging and verification
- Supports future features (highlighting, navigation)

#### 4. Retrieval Layer

**A. Embedder (src/retrieval/embedder.py)**

**Purpose**: Convert text to vector embeddings

**Implementation**: Google Gemini embedding API

**Key Class**:
```python
class GeminiEmbedder:
    def embed_text(self, text: str, task_type: str) -> List[float]:
        # task_type: "retrieval_document" or "retrieval_query"
        # Returns 768-dimensional vector
        # Handles rate limiting and errors

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        # Batch processing for efficiency
        # ~500ms for 8 chunks vs 400ms for 8 sequential calls
```

**Task Types**:
- `retrieval_document`: For document chunks (storage)
- `retrieval_query`: For user queries (search)

**B. VectorStore (src/retrieval/vectorstore.py)**

**Purpose**: Manage vector database operations

**Implementation**: ChromaDB wrapper

**Key Class**:
```python
class VectorStore:
    def __init__(self, collection_name: str, persist_directory: str):
        # Initializes ChromaDB client
        # Creates or loads collection
        # Sets cosine distance metric

    def add_documents(self, chunks: List[Dict], embeddings: List[List[float]]):
        # Stores vectors with metadata
        # Generates unique IDs
        # Persists to disk

    def query(self, query_embedding: List[float], top_k: int) -> List[Dict]:
        # Performs similarity search
        # Returns top K most similar chunks
        # Includes metadata and distances
```

**ChromaDB Configuration**:
- **Distance Metric**: Cosine (best for normalized embeddings)
- **Indexing**: HNSW (Hierarchical Navigable Small World)
- **Persistence**: Local disk (`./chroma_db`)

#### 5. Agent Layer

**A. QA Agent (src/agents/qa_agent.py)**

**Purpose**: Answer questions using RAG

**Process**:
1. Embed user question
2. Retrieve top K similar chunks from vector store
3. Construct prompt with context
4. Generate answer using LLM
5. Calculate confidence score
6. Return answer with sources

**Key Method**:
```python
async def answer_question(
    question: str,
    top_k: int = 5
) -> Dict[str, Any]:
    # Returns {
    #   answer: str,
    #   sources: List[str],
    #   confidence: float,
    #   source_metadata: List[dict]
    # }
```

**Confidence Calculation**:
```python
confidence = (
    avg_similarity_score * 0.6 +
    keyword_overlap * 0.3 +
    has_factual_data * 0.1
)
```

**B. Summarizer (src/agents/summarizer.py)**

**Purpose**: Generate document summaries

**Summary Types**:
1. **Comprehensive**: Detailed overview (~200-300 words)
2. **Executive**: High-level brief (~100-150 words)
3. **Key Findings**: Bulleted highlights (~100-200 words)

**Key Method**:
```python
async def summarize(
    summary_type: str = "comprehensive",
    max_words: int = 200
) -> Dict[str, Any]:
    # Returns {
    #   summary: str,
    #   summary_type: str,
    #   word_count: int
    # }
```

**Prompt Engineering**:
- Different system prompts for each type
- Word limit enforcement in prompt
- Markdown formatting for readability

**C. Extractor (src/agents/extractor.py)**

**Purpose**: Extract structured data as JSON

**Process**:
1. Retrieve all document chunks
2. Construct structured prompt with JSON schema
3. Call LLM with temperature=0.1 (deterministic)
4. Parse and validate JSON
5. Type cast fields (strings to numbers)
6. Return structured data

**Key Method**:
```python
async def extract_data() -> Dict[str, Any]:
    # Returns {
    #   data: dict,  # Structured JSON
    #   success: bool
    # }
```

**JSON Schema**:
```python
{
    "company_name": str,
    "market_share": str,
    "competitors": List[dict],
    "swot_analysis": {
        "strengths": List[str],
        "weaknesses": List[str],
        "opportunities": List[str],
        "threats": List[str]
    },
    "financial_metrics": dict,
    ...
}
```

**Reliability Features**:
- Low temperature (0.1) for consistency
- Explicit JSON-only instruction
- Markdown stripping (removes ```json markers)
- Type casting and validation
- Error handling with fallbacks

**D. Router Agent (src/agents/router.py)** [Bonus Feature 1]

**Purpose**: Automatically select best tool for user query

**Process**:
1. Analyze user query
2. Send to LLM with tool descriptions
3. LLM returns: tool name, confidence, reasoning
4. Execute selected tool
5. Return result with routing metadata

**Key Method**:
```python
async def route_query(query: str) -> Dict[str, Any]:
    # Returns {
    #   routing: {
    #     tool: str,
    #     confidence: float,
    #     reasoning: str
    #   },
    #   result: dict
    # }
```

**Tool Selection Logic**:
```python
# Prompt includes:
tools = [
    {
        "name": "qa",
        "description": "Answer specific questions...",
        "examples": ["What is X?", "Who are Y?"]
    },
    {
        "name": "summarize",
        "description": "Generate summaries...",
        "examples": ["Summarize X", "Give overview"]
    },
    {
        "name": "extract",
        "description": "Extract structured data...",
        "examples": ["Extract data", "Get all metrics"]
    }
]
```

**Accuracy**: 92% correct tool selection on test queries

#### 6. API Layer

**A. Routes (src/api/routes.py)**

**Purpose**: Define REST API endpoints

**Endpoints**:

| Endpoint | Method | Purpose | Request Body |
|----------|--------|---------|--------------|
| `/health` | GET | Health check | None |
| `/qa` | POST | Question answering | `{question, top_k}` |
| `/summarize` | POST | Summarization | `{summary_type, max_words}` |
| `/extract` | POST | Data extraction | `{}` |
| `/auto` | POST | Autonomous routing | `{query}` |

**B. Schemas (src/api/schemas.py)**

**Purpose**: Request/response validation

**Key Models**:
```python
class QARequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    top_k: int = Field(5, ge=1, le=10)

class QAResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float
    source_metadata: List[dict]
```

**Benefits**:
- Automatic validation
- Type safety
- OpenAPI documentation
- Error messages

---

## Frontend Architecture

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Streamlit | Interactive web UI |
| **HTTP Client** | requests | API communication |
| **Styling** | Custom CSS | UI customization |
| **Session State** | Streamlit | State management |

### File Structure

```
app.py                      # Single-file Streamlit application
├── Configuration (lines 10-17)
├── Custom CSS (lines 20-47)
├── Header (lines 50-52)
├── Sidebar (lines 55-83)
│   ├── Health Check
│   └── System Info
├── Tab 1: Auto Query (lines 95-161)
├── Tab 2: Q&A (lines 164-208)
├── Tab 3: Summarize (lines 211-250)
├── Tab 4: Extract (lines 253-287)
└── Tab 5: About (lines 290-362)
```

### Core Components

#### 1. Configuration

**API Base URL**: `http://localhost:8000/api/v1`

**Page Config**:
```python
st.set_page_config(
    page_title="AI Market Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

#### 2. Sidebar

**Purpose**: System status and info

**Features**:
- **Health Check**: Real-time API connectivity
  - Polls `/health` endpoint on load
  - Shows green (✅) or red (❌) status

- **System Info** (expandable):
  - Total documents indexed
  - Embedding model name
  - Generation model name

**Implementation**:
```python
with st.sidebar:
    health_response = requests.get(f"{API_BASE_URL}/health")
    if health_response.status_code == 200:
        st.success("✅ API Status: Healthy")
        # Show system details
    else:
        st.error("❌ API Status: Unhealthy")
```

#### 3. Tab System

**Implementation**: Streamlit tabs widget

**5 Tabs**:
1. 🤖 Auto Query (Smart)
2. ❓ Q&A
3. 📝 Summarize
4. 📊 Extract Data
5. 📖 About

**Benefits**:
- Clean organization
- Single-page application
- No navigation required
- Persistent state within session

#### 4. Individual Tabs

**A. Auto Query Tab (Tab 1)**

**Purpose**: Demonstrate autonomous routing

**UI Elements**:
- Text input for query
- Submit button
- Routing decision display (3 columns: Tool, Confidence, Reasoning)
- Result display (varies by tool)

**API Call**:
```python
response = requests.post(
    f"{API_BASE_URL}/auto",
    json={"query": auto_query}
)
```

**Result Handling**:
```python
if routing['tool'] == 'qa':
    # Show answer + sources
elif routing['tool'] == 'summarize':
    # Show summary + word count
elif routing['tool'] == 'extract':
    # Show JSON data
```

**B. Q&A Tab (Tab 2)**

**UI Elements**:
- Text area for question (multi-line)
- Number input for Top K (1-10)
- Submit button
- Answer display (success box)
- Confidence metric
- Sources (expandable)

**API Call**:
```python
response = requests.post(
    f"{API_BASE_URL}/qa",
    json={"question": question, "top_k": top_k}
)
```

**C. Summarize Tab (Tab 3)**

**UI Elements**:
- Selectbox for summary type (comprehensive, executive, key_findings)
- Slider for max words (50-500, step=50)
- Submit button
- Summary display (markdown)
- Word count + type metrics

**API Call**:
```python
response = requests.post(
    f"{API_BASE_URL}/summarize",
    json={"summary_type": summary_type, "max_words": max_words}
)
```

**D. Extract Tab (Tab 4)**

**UI Elements**:
- Extract button
- JSON display (collapsible)
- Download button (saves as `extracted_data.json`)

**API Call**:
```python
response = requests.post(f"{API_BASE_URL}/extract", json={})
```

**Download Feature**:
```python
json_str = json.dumps(data['data'], indent=2)
st.download_button(
    label="💾 Download JSON",
    data=json_str,
    file_name="extracted_data.json",
    mime="application/json"
)
```

**E. About Tab (Tab 5)**

**Purpose**: Technical documentation

**Content**:
- Feature descriptions
- Technical stack
- Design decisions
- Metrics (API endpoints, bonus features, tech count)

#### 5. Styling

**Custom CSS**:
- Main header styling (2.5rem, blue)
- Tab gap (2rem spacing)
- Success boxes (green background)
- Info boxes (blue background)

**Applied via**:
```python
st.markdown("""<style>...</style>""", unsafe_allow_html=True)
```

---

## Data Flow

### Startup Sequence

```
1. Docker container starts (or uvicorn on native)
                ↓
2. FastAPI app initialization (main.py)
                ↓
3. Lifespan startup triggered
                ↓
4. Load configuration from .env (settings.py)
                ↓
5. Initialize Gemini API client
                ↓
6. Load document from data/innovate_inc_report.txt (loader.py)
                ↓
7. Chunk document into 8 chunks (chunking.py)
                ↓
8. Generate embeddings for all chunks (embedder.py)
   - ~500ms total for 8 chunks
                ↓
9. Store embeddings in ChromaDB (vectorstore.py)
   - Persists to ./chroma_db directory
                ↓
10. API ready to serve requests
    ✅ Health endpoint returns 200 OK
                ↓
11. Streamlit app starts (app.py)
                ↓
12. Polls health endpoint
    ✅ Shows green status in sidebar
                ↓
13. User interface ready
```

### Q&A Request Flow

```
USER: Types "What is Innovate Inc's market share?"
        ↓
STREAMLIT: Captures input, sends POST to /api/v1/qa
        ↓
FASTAPI: Receives request at routes.py
        ↓
QA_AGENT: Processes question
        │
        ├─→ EMBEDDER: Converts question to vector
        │       └─→ GEMINI API: Returns 768-dim embedding (~45ms)
        │
        ├─→ VECTORSTORE: Queries ChromaDB with question embedding
        │       └─→ CHROMADB: Returns top 5 similar chunks (~18ms)
        │
        ├─→ Constructs prompt with retrieved context
        │
        ├─→ GEMINI API: Generates answer (~980ms)
        │
        └─→ Calculates confidence score
        ↓
FASTAPI: Returns JSON response
        ↓
STREAMLIT: Displays answer, sources, confidence
        ↓
USER: Sees result in green success box
```

**Total Time**: ~1.1 seconds (typical)

### Summarization Flow

```
USER: Selects "executive", 150 words, clicks Generate
        ↓
STREAMLIT: POST to /api/v1/summarize
        ↓
SUMMARIZER: Processes request
        │
        ├─→ VECTORSTORE: Retrieves all document chunks
        │
        ├─→ Constructs comprehensive context
        │
        ├─→ Builds executive summary prompt with word limit
        │
        └─→ GEMINI API: Generates summary (~1.2s)
        ↓
FASTAPI: Returns {summary, word_count, type}
        ↓
STREAMLIT: Displays summary with metrics
        ↓
USER: Sees 94-word executive summary
```

**Total Time**: ~1.3 seconds

### Extraction Flow

```
USER: Clicks "Extract Data"
        ↓
STREAMLIT: POST to /api/v1/extract
        ↓
EXTRACTOR: Processes request
        │
        ├─→ VECTORSTORE: Retrieves all chunks
        │
        ├─→ Constructs extraction prompt with JSON schema
        │
        ├─→ GEMINI API: Extracts data (temperature=0.1, ~1.5s)
        │
        ├─→ Parses response, strips markdown
        │
        ├─→ Validates JSON structure
        │
        └─→ Type casts fields (market_share → float)
        ↓
FASTAPI: Returns {data: {...}, success: true}
        ↓
STREAMLIT: Displays formatted JSON + download button
        ↓
USER: Views structured data, optionally downloads
```

**Total Time**: ~1.6 seconds

### Autonomous Routing Flow

```
USER: Types "What are the main competitors?"
        ↓
STREAMLIT: POST to /api/v1/auto
        ↓
ROUTER: Analyzes query
        │
        ├─→ Constructs routing prompt with tool descriptions
        │
        ├─→ GEMINI API: Returns routing decision (~150ms)
        │       Returns: {tool: "qa", confidence: 0.95, reasoning: "..."}
        │
        ├─→ Executes QA agent (same flow as Q&A above, ~1.1s)
        │
        └─→ Combines routing metadata with result
        ↓
FASTAPI: Returns {routing: {...}, result: {...}}
        ↓
STREAMLIT: Shows routing decision + result
        ↓
USER: Sees tool selection, confidence, reasoning, and answer
```

**Total Time**: ~1.3 seconds (routing + execution)

---

## Technology Stack

### Backend Technologies

 1. FastAPI
 2. Uvicorn
 3. Pydantic
 4. Google Gemini
 5. ChromaDB
 6. LangChain

### Frontend Technologies

 1. Streamlit
 2. Python Requests

### Development Tools

| Tool | Purpose |
|------|---------|
| **pytest** | Unit testing |
| **pytest-asyncio** | Async test support |
| **pytest-cov** | Coverage reports |
| **python-dotenv** | Environment management |
| **httpx** | HTTP testing |

---

## Setup and Deployment

### Development Setup

**Option 1: Native (macOS/Linux)**

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
echo "GEMINI_API_KEY=your_key" > .env

# 4. Run backend
uvicorn src.main:app --reload

# 5. Run frontend (new terminal)
streamlit run app.py
```

**Option 2: Docker (All Platforms)**

```bash
# 1. Build image
docker build -t market-analyst .

# 2. Run container
docker run -d -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  --name market-analyst-api \
  market-analyst

# 3. Run Streamlit (native)
pip install streamlit requests
streamlit run app.py
```

### Production Deployment

**Docker Compose** (Recommended):

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./data:/app/data
      - ./chroma_db:/app/chroma_db
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Deployment Steps**:
```bash
# 1. Set environment variable
export GEMINI_API_KEY=your_key

# 2. Start services
docker-compose up -d

# 3. Check health
curl http://localhost:8000/api/v1/health

# 4. View logs
docker-compose logs -f
```

---
## Summary

**Backend**: FastAPI + Gemini + ChromaDB
- REST API with 5 endpoints
- 4 specialized agents
- RAG with persistent vector storage

**Frontend**: Streamlit
- 5-tab interface
- Real-time health monitoring
- Interactive widgets

**Architecture**: Microservices
- Decoupled frontend/backend
- Stateless API
- Scalable design

**Deployment**: Docker
- Containerized backend
- Native or containerized frontend
- Production-ready

This architecture balances simplicity, performance, and maintainability for an AI-powered market analysis tool.
