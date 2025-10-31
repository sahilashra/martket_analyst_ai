"""
Router Agent for Autonomous Tool Selection (Bonus Feature 1).
"""
import google.generativeai as genai
from typing import Dict, Any, Literal
import json
import re


ToolType = Literal["qa", "summarize", "extract"]


class RouterAgent:
    """
    Autonomous agent that routes user queries to the appropriate tool.
    
    This implements Bonus Feature 1: Instead of the user specifying which
    tool to use, the agent analyzes the natural language query and decides
    which tool (Q&A, Summarize, or Extract) is most appropriate.
    
    Design Decision: LLM-based Intent Classification
    
    Rationale:
    1. Why LLM-based routing:
       - Handles nuanced natural language queries
       - Better than keyword matching for ambiguous cases
       - Understands context and intent
       - Can explain reasoning (for debugging)
    
    2. Alternative Approaches Considered:
       - Keyword matching: Too brittle, fails on variations
       - Classification model: Requires training data
       - Rule-based: Hard to maintain and expand
       - LLM: Flexible, accurate, easy to improve
    
    3. Implementation Strategy:
       - Use low temperature for consistent routing
       - Provide clear tool descriptions
       - Request JSON output for easy parsing
       - Include confidence score for ambiguous cases
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize the router agent.
        
        Args:
            api_key: Google Gemini API key
            model_name: Name of the generation model
        """
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.temperature = 0.1  # Low temperature for consistent routing
        self.model = genai.GenerativeModel(model_name)
        
        # Tool descriptions for the router
        self.tool_descriptions = {
            "qa": "Answer specific questions about the document. Use when user asks 'what', 'who', 'when', 'where', 'why', or 'how' questions.",
            "summarize": "Generate summaries or overviews. Use when user wants a summary, overview, main points, or key takeaways.",
            "extract": "Extract structured data as JSON. Use when user wants specific data points, metrics, lists, or structured information."
        }
    
    def route(self, user_query: str) -> Dict[str, Any]:
        """
        Route the user query to the appropriate tool.
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Dictionary containing:
            - tool: Selected tool name ("qa", "summarize", "extract")
            - confidence: Confidence score (0.0 to 1.0)
            - reasoning: Explanation for the choice
        """
        # Create routing prompt
        prompt = self._create_routing_prompt(user_query)
        
        try:
            # Get routing decision
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=256,
                )
            )
            
            # Parse response
            routing_decision = self._parse_routing_response(response.text)
            
            return routing_decision
        
        except Exception as e:
            # Fallback to Q&A on error
            return {
                'tool': 'qa',
                'confidence': 0.5,
                'reasoning': f'Defaulting to Q&A due to routing error: {str(e)}',
                'error': str(e)
            }
    
    def _create_routing_prompt(self, query: str) -> str:
        """Create the routing decision prompt."""
        
        prompt = f"""You are a routing assistant that decides which tool should handle a user's query.

Available Tools:
1. "qa" - Question Answering: {self.tool_descriptions['qa']}
2. "summarize" - Summarization: {self.tool_descriptions['summarize']}
3. "extract" - Data Extraction: {self.tool_descriptions['extract']}

Analyze the user's query and select the most appropriate tool.

User Query: "{query}"

Respond with ONLY a JSON object in this format:
{{
  "tool": "qa" | "summarize" | "extract",
  "confidence": 0.0 to 1.0,
  "reasoning": "brief explanation of why this tool was chosen"
}}

JSON Response:"""
        
        return prompt
    
    def _parse_routing_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the routing decision from model response."""
        
        # Clean response
        cleaned = response_text.strip()
        
        # Remove markdown code blocks
        cleaned = re.sub(r'^```json\s*', '', cleaned)
        cleaned = re.sub(r'^```\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned)
        cleaned = cleaned.strip()
        
        # Extract JSON
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_str = cleaned[start_idx:end_idx + 1]
            routing_data = json.loads(json_str)
        else:
            routing_data = json.loads(cleaned)
        
        # Validate tool choice
        if routing_data.get('tool') not in ['qa', 'summarize', 'extract']:
            # Default to qa if invalid
            routing_data['tool'] = 'qa'
            routing_data['confidence'] = 0.5
            routing_data['reasoning'] = 'Invalid tool in response, defaulting to Q&A'
        
        return routing_data
    
    def explain_routing(self, query: str, routing_decision: Dict[str, Any]) -> str:
        """
        Generate a human-readable explanation of the routing decision.
        
        Args:
            query: Original user query
            routing_decision: Routing decision dictionary
            
        Returns:
            Formatted explanation string
        """
        tool_name_map = {
            'qa': 'Question Answering',
            'summarize': 'Summarization',
            'extract': 'Data Extraction'
        }
        
        tool = routing_decision.get('tool', 'qa')
        confidence = routing_decision.get('confidence', 0.0)
        reasoning = routing_decision.get('reasoning', 'No reasoning provided')
        
        explanation = f"""
Routing Decision:
- Selected Tool: {tool_name_map.get(tool, tool)}
- Confidence: {confidence:.0%}
- Reasoning: {reasoning}
"""
        
        return explanation.strip()
    
    def batch_route(self, queries: list[str]) -> list[Dict[str, Any]]:
        """
        Route multiple queries at once.
        
        Args:
            queries: List of user queries
            
        Returns:
            List of routing decisions
        """
        return [self.route(query) for query in queries]
