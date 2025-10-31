"""
Main FastAPI application for AI Market Analyst Agent.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

from .api import router, initialize_components
from .config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Market Analyst Agent",
    description="Multi-functional AI agent for market research analysis using RAG",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    logger.info("Starting AI Market Analyst Agent...")
    try:
        initialize_components()
        logger.info("Startup completed successfully")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "AI Market Analyst Agent",
        "version": "1.0.0",
        "description": "Multi-functional AI agent for market research analysis",
        "endpoints": {
            "health": "/api/v1/health",
            "qa": "/api/v1/qa",
            "summarize": "/api/v1/summarize",
            "extract": "/api/v1/extract",
            "auto": "/api/v1/auto (Bonus: Autonomous Routing)"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
