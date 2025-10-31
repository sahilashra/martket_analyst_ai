# Dockerfile for AI Market Analyst Agent (Bonus Feature 3)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies directly with flexible versions
RUN pip install --upgrade pip && \
    pip install fastapi uvicorn[standard] pydantic pydantic-settings python-dotenv \
    google-generativeai chromadb langchain langchain-community langchain-text-splitters \
    numpy tqdm pytest pytest-asyncio pytest-cov httpx streamlit

# Copy application code
COPY . .

# Create data directory if it doesn't exist
RUN mkdir -p data chroma_db

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/v1/health')"

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
