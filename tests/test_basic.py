"""
Basic tests for the Market Analyst Agent.
Run with: pytest tests/test_basic.py -v
"""
import pytest
from pathlib import Path


def test_project_structure():
    """Test that all required files and directories exist."""
    base_path = Path(__file__).parent.parent
    
    required_paths = [
        base_path / "README.md",
        base_path / "requirements.txt",
        base_path / ".env.example",
        base_path / "data" / "innovate_inc_report.txt",
        base_path / "src" / "main.py",
        base_path / "src" / "config",
        base_path / "src" / "data",
        base_path / "src" / "retrieval",
        base_path / "src" / "agents",
        base_path / "src" / "api",
    ]
    
    for path in required_paths:
        assert path.exists(), f"Missing required path: {path}"


def test_document_exists():
    """Test that the market research document exists and has content."""
    doc_path = Path(__file__).parent.parent / "data" / "innovate_inc_report.txt"
    
    assert doc_path.exists(), "Document file not found"
    
    content = doc_path.read_text()
    assert len(content) > 0, "Document is empty"
    assert "Innovate Inc" in content, "Document doesn't contain expected content"
    assert "Q3 2025" in content, "Document doesn't contain expected report period"


def test_imports():
    """Test that all main modules can be imported."""
    try:
        from src.config import settings
        from src.data import DocumentLoader, DocumentChunker
        from src.retrieval import GeminiEmbedder, VectorStore
        from src.agents import QAAgent, SummarizerAgent, ExtractorAgent, RouterAgent
        from src.api import router
    except ImportError as e:
        pytest.fail(f"Failed to import modules: {e}")


def test_document_loading():
    """Test document loading functionality."""
    from src.data import DocumentLoader
    
    doc_path = Path(__file__).parent.parent / "data" / "innovate_inc_report.txt"
    loader = DocumentLoader()
    
    content = loader.load_document(str(doc_path))
    
    assert isinstance(content, str)
    assert len(content) > 100
    assert "Innovate Inc" in content


def test_document_chunking():
    """Test document chunking functionality."""
    from src.data import DocumentLoader, DocumentChunker
    
    doc_path = Path(__file__).parent.parent / "data" / "innovate_inc_report.txt"
    loader = DocumentLoader()
    content = loader.load_document(str(doc_path))
    
    chunker = DocumentChunker(chunk_size=1000, chunk_overlap=200)
    chunks = chunker.chunk_document(content)
    
    assert len(chunks) > 0, "No chunks created"
    assert all('text' in chunk for chunk in chunks), "Chunks missing text field"
    assert all('chunk_id' in chunk for chunk in chunks), "Chunks missing chunk_id"
    
    # Check overlap
    if len(chunks) > 1:
        # Last part of first chunk should appear in second chunk (overlap)
        first_end = chunks[0]['text'][-100:]
        second_start = chunks[1]['text'][:100]
        # At least some overlap should exist
        assert len(set(first_end.split()) & set(second_start.split())) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
