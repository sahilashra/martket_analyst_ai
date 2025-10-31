"""
Question Answering Agent using RAG.
"""
import google.generativeai as genai
from typing import Dict, List, Any


class QAAgent:
    """
    Question-answering agent using retrieval-augmented generation.
    
    This agent retrieves relevant document chunks and generates
    contextual answers using Gemini's generation capabilities.
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp", temperature: float = 0.2):
        """
        Initialize the QA agent.
        
        Args:
            api_key: Google Gemini API key
            model_name: Name of the generation model
            temperature: Sampling temperature (0.0 to 1.0)
        """
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.model = genai.GenerativeModel(model_name)
    
    def answer_question(
        self,
        question: str,
        context_chunks: List[str],
        metadata: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Answer a question based on retrieved context.
        
        Args:
            question: The user's question
            context_chunks: List of relevant text chunks
            metadata: Optional metadata for each chunk
            
        Returns:
            Dictionary containing:
            - answer: The generated answer
            - sources: List of source chunks used
            - confidence: Estimated confidence score
        """
        # Build context from chunks
        context = self._build_context(context_chunks, metadata)
        
        # Create prompt
        prompt = self._create_qa_prompt(question, context)
        
        # Generate answer
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=512,
            )
        )
        
        answer_text = response.text
        
        # Estimate confidence
        confidence = self._estimate_confidence(answer_text, context_chunks)
        
        return {
            'answer': answer_text,
            'sources': context_chunks,
            'source_metadata': metadata if metadata else [],
            'confidence': confidence
        }
    
    def _build_context(self, chunks: List[str], metadata: List[Dict] = None) -> str:
        """Build formatted context from chunks."""
        context_parts = []
        
        for i, chunk in enumerate(chunks):
            source_num = i + 1
            context_parts.append(f"[Source {source_num}]\n{chunk}\n")
        
        return "\n".join(context_parts)
    
    def _create_qa_prompt(self, question: str, context: str) -> str:
        """Create the QA prompt template."""
        prompt = f"""You are a helpful AI assistant answering questions about a market research document.

Answer the question based ONLY on the provided context below.
If the information is not in the context, say "I don't have sufficient information to answer this question."
Cite sources in your answer using [Source N] notation.
Be concise but comprehensive.

Context:
{context}

Question: {question}

Answer:"""
        
        return prompt
    
    def _estimate_confidence(self, answer: str, context_chunks: List[str]) -> float:
        """
        Estimate confidence in the answer.
        
        This is a heuristic based on answer characteristics.
        """
        answer_lower = answer.lower()
        
        # Check for uncertainty indicators
        uncertainty_phrases = [
            "i don't have",
            "insufficient information",
            "not mentioned",
            "unclear",
            "cannot determine",
            "not specified"
        ]
        
        for phrase in uncertainty_phrases:
            if phrase in answer_lower:
                return 0.0
        
        # Check for citation presence
        has_citations = "[source" in answer_lower
        
        # Base confidence on presence of citations and answer length
        if has_citations and len(answer) > 50:
            return 0.85
        elif len(answer) > 30:
            return 0.70
        else:
            return 0.50
