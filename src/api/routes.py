"""
API routes for the AI Market Analyst agent.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import logging

from ..config import settings
from ..data import DocumentLoader
from ..retrieval import GeminiEmbedder, VectorStore
from ..agents import QAAgent, SummarizerAgent, ExtractorAgent, RouterAgent
from .schemas import (
    QARequest, QAResponse,
    SummarizeRequest, SummaryResponse,
    ExtractRequest, ExtractionResponse,
    AutoQueryRequest, AutoQueryResponse,
    HealthResponse, ErrorResponse,
    SourceMetadata, RoutingDecision
)

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/v1", tags=["Market Analyst"])

# Global instances (initialized in startup)
embedder: GeminiEmbedder = None
vector_store: VectorStore = None
qa_agent: QAAgent = None
summarizer_agent: SummarizerAgent = None
extractor_agent: ExtractorAgent = None
router_agent: RouterAgent = None
document_text: str = None


def initialize_components():
    """Initialize all components on startup."""
    global embedder, vector_store, qa_agent, summarizer_agent, extractor_agent, router_agent, document_text
    
    try:
        logger.info("Initializing components...")
        
        # Initialize embedder
        embedder = GeminiEmbedder(
            api_key=settings.gemini_api_key,
            model_name=settings.embedding_model
        )
        
        # Initialize vector store
        vector_store = VectorStore(
            persist_directory=settings.vector_store_path,
            collection_name="market_research"
        )
        
        # Initialize agents
        qa_agent = QAAgent(
            api_key=settings.gemini_api_key,
            model_name=settings.generation_model,
            temperature=settings.temperature
        )
        
        summarizer_agent = SummarizerAgent(
            api_key=settings.gemini_api_key,
            model_name=settings.generation_model,
            temperature=0.3
        )
        
        extractor_agent = ExtractorAgent(
            api_key=settings.gemini_api_key,
            model_name=settings.generation_model
        )
        
        router_agent = RouterAgent(
            api_key=settings.gemini_api_key,
            model_name=settings.generation_model
        )
        
        # Load and index document if vector store is empty
        if vector_store.get_collection_stats()['total_documents'] == 0:
            logger.info("Loading and indexing document...")
            from ..data import DocumentChunker
            
            # Load document
            loader = DocumentLoader()
            document_text = loader.load_document(settings.document_path)
            
            # Chunk document
            chunker = DocumentChunker(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap
            )
            chunks = chunker.chunk_document(document_text)
            
            # Generate embeddings
            chunk_texts = [chunk['text'] for chunk in chunks]
            embeddings = embedder.embed_batch(chunk_texts)
            
            # Add to vector store
            vector_store.add_documents(chunks, embeddings)
            
            logger.info(f"Indexed {len(chunks)} chunks")
        else:
            # Just load document text for summarization/extraction
            loader = DocumentLoader()
            document_text = loader.load_document(settings.document_path)
            logger.info("Vector store already populated, skipping indexing")
        
        logger.info("All components initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing components: {e}")
        raise


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        stats = vector_store.get_collection_stats()
        return HealthResponse(
            status="healthy",
            vector_store=stats,
            embedding_model=settings.embedding_model,
            generation_model=settings.generation_model
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unhealthy: {str(e)}"
        )


@router.post("/qa", response_model=QAResponse)
async def question_answering(request: QARequest):
    """
    Answer questions about the market research document.
    
    This endpoint uses RAG to retrieve relevant chunks and generate answers.
    """
    try:
        # Generate query embedding
        query_embedding = embedder.embed_query(request.question)
        
        # Retrieve relevant chunks
        results = vector_store.query(
            query_embedding=query_embedding,
            top_k=request.top_k
        )
        
        if not results['documents']:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No relevant information found"
            )
        
        # Generate answer
        answer_result = qa_agent.answer_question(
            question=request.question,
            context_chunks=results['documents'],
            metadata=results['metadatas']
        )
        
        # Format metadata
        source_metadata = [
            SourceMetadata(**meta) for meta in results['metadatas']
        ]
        
        return QAResponse(
            answer=answer_result['answer'],
            sources=answer_result['sources'],
            source_metadata=source_metadata,
            confidence=answer_result['confidence'],
            question=request.question
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in Q&A: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )


@router.post("/summarize", response_model=SummaryResponse)
async def summarize_document(request: SummarizeRequest):
    """
    Generate a summary of the market research document.
    
    Different summary types available:
    - comprehensive: Full overview
    - executive: Key metrics and priorities
    - key_findings: Main insights as bullets
    """
    try:
        # Generate summary
        summary_result = summarizer_agent.summarize(
            document_text=document_text,
            summary_type=request.summary_type,
            max_words=request.max_words
        )
        
        return SummaryResponse(**summary_result)
    
    except Exception as e:
        logger.error(f"Error in summarization: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating summary: {str(e)}"
        )


@router.post("/extract", response_model=ExtractionResponse)
async def extract_data(request: ExtractRequest):
    """
    Extract structured data from the document as JSON.
    
    Returns key business metrics, competitors, SWOT analysis, and more
    in a structured format.
    """
    try:
        if request.custom_schema:
            # Use custom schema extraction
            extracted = extractor_agent.extract_custom_fields(
                document_text=document_text,
                field_schema=request.custom_schema
            )
            return ExtractionResponse(
                data=extracted,
                success=True,
                raw_response=None
            )
        else:
            # Use default extraction
            extraction_result = extractor_agent.extract_structured_data(
                document_text=document_text
            )
            return ExtractionResponse(**extraction_result)
    
    except Exception as e:
        logger.error(f"Error in extraction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting data: {str(e)}"
        )


@router.post("/auto", response_model=AutoQueryResponse)
async def auto_query(request: AutoQueryRequest):
    """
    Autonomous query routing (Bonus Feature 1).
    
    The agent automatically determines which tool (Q&A, Summarize, Extract)
    is most appropriate for your query based on the natural language input.
    """
    try:
        # Route the query
        routing_decision = router_agent.route(request.query)
        
        # Execute the selected tool
        tool = routing_decision['tool']
        
        if tool == 'qa':
            # Execute Q&A
            query_embedding = embedder.embed_query(request.query)
            results = vector_store.query(
                query_embedding=query_embedding,
                top_k=request.top_k
            )
            
            if not results['documents']:
                result = {
                    'answer': "No relevant information found",
                    'sources': [],
                    'confidence': 0.0
                }
            else:
                result = qa_agent.answer_question(
                    question=request.query,
                    context_chunks=results['documents'],
                    metadata=results['metadatas']
                )
        
        elif tool == 'summarize':
            # Execute summarization
            result = summarizer_agent.summarize(
                document_text=document_text,
                summary_type="comprehensive",
                max_words=200
            )
        
        elif tool == 'extract':
            # Execute extraction
            result = extractor_agent.extract_structured_data(
                document_text=document_text
            )
        
        else:
            raise ValueError(f"Unknown tool: {tool}")
        
        return AutoQueryResponse(
            routing=RoutingDecision(**routing_decision),
            result=result,
            query=request.query
        )
    
    except Exception as e:
        logger.error(f"Error in auto query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing auto query: {str(e)}"
        )
