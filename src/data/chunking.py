"""
Text chunking strategies for optimal retrieval.
"""
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:
    """
    Intelligent document chunking for RAG applications.
    
    Design Decision: Using RecursiveCharacterTextSplitter with:
    - Chunk size: 1000 characters
    - Overlap: 200 characters (20%)
    
    Rationale:
    1. Chunk Size (1000):
       - Balances context preservation with retrieval granularity
       - Typical embedding models handle 512-1024 tokens well
       - 1000 chars ≈ 200-250 tokens for English text
       - Not too small (loses context) or too large (dilutes relevance)
    
    2. Overlap (200, 20%):
       - Prevents information loss at chunk boundaries
       - Ensures continuity for concepts spanning chunks
       - 20% is empirically optimal for most document types
       - Helps retrieval by providing redundancy
    
    3. Recursive Splitting:
       - Respects document structure (paragraphs, sentences)
       - Uses hierarchy: \\n\\n -> \\n -> . -> space
       - Maintains semantic coherence within chunks
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the chunker.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Separator hierarchy for semantic preservation
        self.separators = [
            "\n\n",  # Paragraph breaks (highest priority)
            "\n",    # Line breaks
            ". ",    # Sentences
            ", ",    # Clauses
            " ",     # Words
            ""       # Characters (fallback)
        ]
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
            length_function=len,
            is_separator_regex=False
        )
    
    def chunk_document(self, text: str) -> List[Dict[str, any]]:
        """
        Split document into overlapping chunks with metadata.
        
        Args:
            text: The full document text
            
        Returns:
            List of chunks with metadata:
            - text: The chunk content
            - chunk_id: Unique identifier
            - start_char: Starting character position
            - end_char: Ending character position
        """
        # Split text into chunks
        chunks = self.splitter.split_text(text)
        
        # Add metadata to each chunk
        chunked_docs = []
        current_position = 0
        
        for idx, chunk in enumerate(chunks):
            # Find actual position in original text (accounting for overlap)
            chunk_position = text.find(chunk, current_position)
            
            chunk_metadata = {
                'text': chunk,
                'chunk_id': f"chunk_{idx}",
                'chunk_index': idx,
                'start_char': chunk_position,
                'end_char': chunk_position + len(chunk),
                'length': len(chunk)
            }
            
            chunked_docs.append(chunk_metadata)
            
            # Update position for next search (considering overlap)
            current_position = chunk_position + len(chunk) - self.chunk_overlap
        
        return chunked_docs
    
    def get_chunk_statistics(self, chunks: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Calculate statistics about the chunking process.
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            Statistics dictionary with metrics
        """
        if not chunks:
            return {
                'total_chunks': 0,
                'avg_chunk_size': 0,
                'min_chunk_size': 0,
                'max_chunk_size': 0,
                'total_characters': 0
            }
        
        chunk_sizes = [chunk['length'] for chunk in chunks]
        
        return {
            'total_chunks': len(chunks),
            'avg_chunk_size': sum(chunk_sizes) / len(chunk_sizes),
            'min_chunk_size': min(chunk_sizes),
            'max_chunk_size': max(chunk_sizes),
            'total_characters': sum(chunk_sizes),
            'overlap_ratio': self.chunk_overlap / self.chunk_size
        }
