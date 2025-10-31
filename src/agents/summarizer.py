"""
Document Summarization Agent.
"""
import google.generativeai as genai
from typing import Dict, Any


class SummarizerAgent:
    """
    Agent for generating concise summaries of market research documents.
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp", temperature: float = 0.3):
        """
        Initialize the summarizer agent.
        
        Args:
            api_key: Google Gemini API key
            model_name: Name of the generation model
            temperature: Sampling temperature (slightly higher for creative summarization)
        """
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.model = genai.GenerativeModel(model_name)
    
    def summarize(
        self,
        document_text: str,
        summary_type: str = "comprehensive",
        max_words: int = 200
    ) -> Dict[str, Any]:
        """
        Generate a summary of the document.
        
        Args:
            document_text: Full document text or concatenated chunks
            summary_type: Type of summary ("comprehensive", "executive", "key_findings")
            max_words: Maximum length of summary in words
            
        Returns:
            Dictionary containing:
            - summary: The generated summary
            - summary_type: Type of summary generated
            - word_count: Approximate word count
        """
        # Create prompt based on summary type
        prompt = self._create_summary_prompt(document_text, summary_type, max_words)
        
        # Generate summary
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=max_words * 2,  # Rough token estimate
            )
        )
        
        summary_text = response.text
        word_count = len(summary_text.split())
        
        return {
            'summary': summary_text,
            'summary_type': summary_type,
            'word_count': word_count,
            'requested_max_words': max_words
        }
    
    def _create_summary_prompt(self, document: str, summary_type: str, max_words: int) -> str:
        """Create the appropriate summary prompt based on type."""
        
        base_instruction = f"Summarize the following market research document in approximately {max_words} words or less."
        
        if summary_type == "comprehensive":
            specific_instruction = """
Include:
- Company overview and main product
- Market size and growth projections
- Competitive position and key competitors
- Main strengths, weaknesses, opportunities, and threats
- Strategic recommendations"""
        
        elif summary_type == "executive":
            specific_instruction = """
Focus on:
- Key business metrics (market share, market size)
- Critical insights for decision-makers
- Top 3 strategic priorities
Keep it concise and action-oriented."""
        
        elif summary_type == "key_findings":
            specific_instruction = """
Extract only:
- Most important market insights
- Critical competitive intelligence
- Key strategic recommendations
Present as bullet points."""
        
        else:
            specific_instruction = "Provide a balanced overview of the document's main points."
        
        prompt = f"""{base_instruction}

{specific_instruction}

Document:
{document}

Summary:"""
        
        return prompt
    
    def generate_insights(self, document_text: str) -> Dict[str, Any]:
        """
        Generate strategic insights from the document.
        
        Args:
            document_text: Full document text
            
        Returns:
            Dictionary with categorized insights
        """
        prompt = f"""Analyze this market research document and provide strategic insights in the following categories:

1. Market Opportunity (1-2 sentences)
2. Competitive Threats (1-2 sentences)
3. Strategic Recommendations (2-3 key actions)

Document:
{document_text}

Insights:"""
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=400,
            )
        )
        
        return {
            'insights': response.text,
            'insight_type': 'strategic_analysis'
        }
