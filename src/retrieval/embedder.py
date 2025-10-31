"""
Embedding generation using Google Gemini.
"""
import google.generativeai as genai
from typing import List
import numpy as np


class GeminiEmbedder:
    """
    Generate embeddings using Google's Gemini embedding model.
    
    Design Decision: Using models/text-embedding-004
    
    Rationale:
    1. Model Choice (text-embedding-004):
       - Latest Gemini embedding model (as of 2024)
       - 768-dimensional embeddings (good balance)
       - Optimized for semantic search and RAG
       - Free tier available
       - Better multilingual support than alternatives
    
    2. Why Gemini over alternatives:
       - OpenAI ada-002: Costs money, 1536 dims (more compute)
       - Sentence-BERT: Requires local GPU, larger models
       - Cohere: Also paid, though good quality
       - Gemini: Free, cloud-based, excellent quality
    
    3. Batch Processing:
       - Process multiple texts at once for efficiency
       - Reduces API calls and latency
       - Built-in rate limiting handling
    """
    
    def __init__(self, api_key: str, model_name: str = "models/text-embedding-004"):
        """
        Initialize the embedder.
        
        Args:
            api_key: Google Gemini API key
            model_name: Name of the embedding model to use
        """
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.embedding_dim = 768  # text-embedding-004 dimension
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        result = genai.embed_content(
            model=self.model_name,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    
    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a query.
        
        Uses task_type="retrieval_query" for optimal query embedding.
        
        Args:
            query: Query text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        result = genai.embed_content(
            model=self.model_name,
            content=query,
            task_type="retrieval_query"
        )
        return result['embedding']
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        embeddings = []
        
        # Process in batches to avoid rate limits
        batch_size = 100  # Gemini API batch limit
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            for text in batch:
                embedding = self.embed_text(text)
                embeddings.append(embedding)
        
        return embeddings
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score (0 to 1)
        """
        vec1_np = np.array(vec1)
        vec2_np = np.array(vec2)
        
        dot_product = np.dot(vec1_np, vec2_np)
        norm1 = np.linalg.norm(vec1_np)
        norm2 = np.linalg.norm(vec2_np)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
