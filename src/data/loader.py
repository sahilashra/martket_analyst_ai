"""
Document loading utilities.
"""
from pathlib import Path


class DocumentLoader:
    """Load and preprocess documents from various formats."""

    @staticmethod
    def load_text_file(file_path: str) -> str:
        """
        Load content from a text file.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            The text content of the file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            UnicodeDecodeError: If the file encoding is not supported
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except UnicodeDecodeError:
            # Try with a different encoding if UTF-8 fails
            with open(path, 'r', encoding='latin-1') as f:
                content = f.read()
            return content
    
    @staticmethod
    def load_document(file_path: str) -> str:
        """
        Load a document based on file extension.
        
        Args:
            file_path: Path to the document
            
        Returns:
            The text content of the document
        """
        path = Path(file_path)
        extension = path.suffix.lower()
        
        if extension in ['.txt', '.md', '.text']:
            return DocumentLoader.load_text_file(file_path)
        elif extension == '.pdf':
            # For future PDF support
            raise NotImplementedError("PDF support coming soon")
        else:
            raise ValueError(f"Unsupported file format: {extension}")
