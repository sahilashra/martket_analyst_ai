"""
API request and response schemas using Pydantic.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal


# ==================== Request Schemas ====================

class QARequest(BaseModel):
    """Request schema for Q&A endpoint."""
    question: str = Field(..., description="Question to answer", min_length=1, max_length=500)
    top_k: Optional[int] = Field(5, description="Number of chunks to retrieve", ge=1, le=10)


class SummarizeRequest(BaseModel):
    """Request schema for summarization endpoint."""
    summary_type: Optional[Literal["comprehensive", "executive", "key_findings"]] = Field(
        "comprehensive",
        description="Type of summary to generate"
    )
    max_words: Optional[int] = Field(200, description="Maximum words in summary", ge=50, le=500)


class ExtractRequest(BaseModel):
    """Request schema for data extraction endpoint."""
    custom_schema: Optional[Dict[str, str]] = Field(
        None,
        description="Optional custom field schema for extraction"
    )


class AutoQueryRequest(BaseModel):
    """Request schema for autonomous routing endpoint (Bonus Feature 1)."""
    query: str = Field(..., description="Natural language query", min_length=1, max_length=500)
    top_k: Optional[int] = Field(5, description="Number of chunks to retrieve for Q&A", ge=1, le=10)


# ==================== Response Schemas ====================

class SourceMetadata(BaseModel):
    """Metadata for a source chunk."""
    chunk_index: int
    start_char: int
    end_char: int
    length: int


class QAResponse(BaseModel):
    """Response schema for Q&A endpoint."""
    answer: str
    sources: List[str]
    source_metadata: List[SourceMetadata]
    confidence: float
    question: str


class SummaryResponse(BaseModel):
    """Response schema for summarization endpoint."""
    summary: str
    summary_type: str
    word_count: int
    requested_max_words: int


class ExtractedData(BaseModel):
    """Schema for extracted structured data."""
    company_name: Optional[str] = None
    product_name: Optional[str] = None
    industry_sector: Optional[str] = None
    report_period: Optional[str] = None
    market_size_current: Optional[str] = None
    market_size_projected: Optional[str] = None
    cagr: Optional[str] = None
    market_share: Optional[float] = None
    competitors: Optional[List[Dict[str, Any]]] = None
    swot: Optional[Dict[str, List[str]]] = None
    key_metrics: Optional[Dict[str, Any]] = None
    strategic_priorities: Optional[List[str]] = None


class ExtractionResponse(BaseModel):
    """Response schema for extraction endpoint."""
    data: Dict[str, Any]
    success: bool
    raw_response: Optional[str] = None
    error: Optional[str] = None


class RoutingDecision(BaseModel):
    """Schema for routing decision."""
    tool: Literal["qa", "summarize", "extract"]
    confidence: float
    reasoning: str


class AutoQueryResponse(BaseModel):
    """Response schema for autonomous query endpoint."""
    routing: RoutingDecision
    result: Dict[str, Any]
    query: str


class HealthResponse(BaseModel):
    """Response schema for health check endpoint."""
    status: str
    vector_store: Dict[str, Any]
    embedding_model: str
    generation_model: str


class ErrorResponse(BaseModel):
    """Response schema for errors."""
    error: str
    detail: Optional[str] = None
    status_code: int
