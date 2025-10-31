# 📊 AI Market Analyst Agent

> **Built for VAIA Agentic AI Residency Program**

A multi-functional AI agent that analyzes market research documents using **Retrieval-Augmented Generation (RAG)**. Ask questions, generate summaries, and extract structured data—all powered by Google Gemini and ChromaDB.

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
<img width="2038" height="1164" alt="image" src="https://github.com/user-attachments/assets/81827e05-b34b-4103-a547-38cbda4cd519" />

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

### Option 1: Docker Setup (Recommended)

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

✅ **All green?** You're ready! See [USER_GUIDE.md](USER_GUIDE.md) for detailed usage.

---

### Full Workflow

```bash
# Morning - Start your day
docker start market-analyst-api
streamlit run app.py

# Evening - Stop services
docker stop market-analyst-api
# (Ctrl+C to stop Streamlit)

# After code changes - Rebuild
docker rm -f market-analyst-api
docker build -t market-analyst .
docker run -d -p 8000:8000 --env-file .env --name market-analyst-api market-analyst
```

**Troubleshooting**: If port 8000 is in use:
```bash
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000

# Then stop the conflicting process or container
docker stop market-analyst-api
```

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

## 📊 API Endpoints

If you prefer API access over the UI:

| Endpoint | Method | Purpose | Example |
|----------|--------|---------|---------|
| `/api/v1/health` | GET | Health check | `curl http://localhost:8000/api/v1/health` |
| `/api/v1/qa` | POST | Question answering | `{"question": "What is the market share?", "top_k": 5}` |
| `/api/v1/summarize` | POST | Summarization | `{"summary_type": "executive", "max_words": 150}` |
| `/api/v1/extract` | POST | Data extraction | `{}` |
| `/api/v1/auto` | POST | Auto routing | `{"query": "What are the competitors?"}` |

**Full API documentation**: http://localhost:8000/docs (Swagger UI)

**Example API Call**:
```bash
curl -X POST "http://localhost:8000/api/v1/qa" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Innovate Inc'\''s market share?", "top_k": 5}'
```

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

**For detailed design decisions, see [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md)**

---

## 📝 License

MIT License - feel free to use this code for your own projects!
