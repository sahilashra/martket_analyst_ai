"""
Configuration management using Pydantic Settings.
"""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Google Gemini API
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    
    # Document Configuration
    document_path: str = Field("data/innovate_inc_report.txt", env="DOCUMENT_PATH")
    
    # Model Configuration
    embedding_model: str = Field("models/text-embedding-004", env="EMBEDDING_MODEL")
    generation_model: str = Field("gemini-2.0-flash-exp", env="GENERATION_MODEL")
    temperature: float = Field(0.2, env="TEMPERATURE")
    
    # RAG Parameters
    chunk_size: int = Field(1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(200, env="CHUNK_OVERLAP")
    top_k_retrieval: int = Field(5, env="TOP_K_RETRIEVAL")
    
    # Vector Store
    vector_store_path: str = Field("./chroma_db", env="VECTOR_STORE_PATH")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
