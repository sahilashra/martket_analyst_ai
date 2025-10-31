"""
Vector store using ChromaDB.
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import uuid


class VectorStore:
    """
    Vector database for document storage and retrieval.
    
    Design Decision: Using ChromaDB
    
    Rationale:
    1. Why ChromaDB:
       - Lightweight and embeddable (no separate server needed)
       - Persistent storage with minimal setup
       - Excellent Python integration
       - Fast similarity search
       - Free and open-source
       - Perfect for prototypes and production
    
    2. Alternatives Considered:
       - Pinecone: Requires cloud, paid tier for production
       - Weaviate: Heavy, requires Docker
       - FAISS: No persistence without extra work
       - Qdrant: More complex setup
       - Milvus: Overkill for this scale
    
    3. ChromaDB Advantages:
       - Single pip install
       - Automatic persistence
       - Built-in metadata filtering
       - Good performance up to millions of vectors
       - Active development and community
    """
    
    def __init__(self, persist_directory: str = "./chroma_db", collection_name: str = "market_research"):
        """
        Initialize the vector store.
        
        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection to use
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine distance
        )
    
    def add_documents(self, chunks: List[Dict[str, any]], embeddings: List[List[float]]) -> None:
        """
        Add document chunks with embeddings to the vector store.
        
        Args:
            chunks: List of chunk dictionaries with text and metadata
            embeddings: List of embedding vectors
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must match number of embeddings")
        
        # Prepare data for ChromaDB
        ids = [chunk.get('chunk_id', str(uuid.uuid4())) for chunk in chunks]
        documents = [chunk['text'] for chunk in chunks]
        metadatas = [
            {
                'chunk_index': chunk.get('chunk_index', i),
                'start_char': chunk.get('start_char', 0),
                'end_char': chunk.get('end_char', 0),
                'length': chunk.get('length', len(chunk['text']))
            }
            for i, chunk in enumerate(chunks)
        ]
        
        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
    
    def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[Dict] = None
    ) -> Dict[str, any]:
        """
        Query the vector store for similar documents.
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            where: Optional metadata filter
            
        Returns:
            Dictionary containing:
            - documents: List of document texts
            - metadatas: List of metadata dicts
            - distances: List of similarity distances
            - ids: List of document IDs
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where
        )
        
        return {
            'documents': results['documents'][0] if results['documents'] else [],
            'metadatas': results['metadatas'][0] if results['metadatas'] else [],
            'distances': results['distances'][0] if results['distances'] else [],
            'ids': results['ids'][0] if results['ids'] else []
        }
    
    def get_collection_stats(self) -> Dict[str, any]:
        """
        Get statistics about the collection.
        
        Returns:
            Dictionary with collection statistics
        """
        count = self.collection.count()
        
        return {
            'name': self.collection_name,
            'total_documents': count,
            'persist_directory': self.persist_directory
        }
    
    def clear_collection(self) -> None:
        """Delete all documents from the collection."""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def delete_collection(self) -> None:
        """Permanently delete the collection."""
        self.client.delete_collection(name=self.collection_name)
