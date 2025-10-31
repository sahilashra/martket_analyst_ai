"""
Structured Data Extraction Agent.
"""
import google.generativeai as genai
from typing import Dict, Any
import json
import re


class ExtractorAgent:
    """
    Agent for extracting structured data from documents as JSON.
    
    Design Decision: Prompt Engineering for Reliable JSON Extraction
    
    Rationale:
    1. Clear Schema Definition:
       - Explicitly define expected JSON structure in prompt
       - Provide example format for consistency
       - Specify data types for each field
    
    2. Iterative Refinement Strategy:
       - Use low temperature (0.1) for deterministic output
       - Include "ONLY output valid JSON" instruction
       - Request specific fields relevant to market research
    
    3. Post-processing:
       - Strip markdown code blocks if present
       - Validate JSON structure
       - Provide fallback for parse errors
       - Convert string numbers to proper types
    
    4. Prompt Structure:
       - Start with role definition
       - Show exact schema
       - Give clear extraction instructions
       - End with format reminder
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize the extractor agent.
        
        Args:
            api_key: Google Gemini API key
            model_name: Name of the generation model
        """
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.temperature = 0.1  # Very low for consistent structured output
        self.model = genai.GenerativeModel(model_name)
    
    def extract_structured_data(self, document_text: str) -> Dict[str, Any]:
        """
        Extract structured data from document as JSON.
        
        Args:
            document_text: Full document text
            
        Returns:
            Dictionary containing:
            - data: Extracted structured data
            - success: Whether extraction succeeded
            - raw_response: Original model response (for debugging)
        """
        # Create extraction prompt
        prompt = self._create_extraction_prompt(document_text)
        
        # Generate structured data
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=1024,
                )
            )
            
            raw_response = response.text
            
            # Parse JSON from response
            extracted_data = self._parse_json_response(raw_response)
            
            # Validate and type-cast data
            validated_data = self._validate_and_cast(extracted_data)
            
            return {
                'data': validated_data,
                'success': True,
                'raw_response': raw_response
            }
        
        except Exception as e:
            return {
                'data': {},
                'success': False,
                'error': str(e),
                'raw_response': raw_response if 'raw_response' in locals() else None
            }
    
    def _create_extraction_prompt(self, document: str) -> str:
        """Create the structured extraction prompt."""
        
        prompt = f"""You are a data extraction assistant. Extract structured information from the market research document below.

IMPORTANT: Output ONLY valid JSON. Do not include any explanatory text, markdown formatting, or code blocks.

Extract the following information into this exact JSON structure:
{{
  "company_name": "string - name of the company",
  "product_name": "string - flagship product name",
  "industry_sector": "string - primary industry sector",
  "report_period": "string - report period (e.g., Q3 2025)",
  "market_size_current": "string - current market size with units",
  "market_size_projected": "string - projected market size with units",
  "cagr": "string - compound annual growth rate",
  "market_share": "number - company's market share as percentage (just number)",
  "competitors": [
    {{
      "name": "string - competitor name",
      "market_share": "number - their market share as percentage"
    }}
  ],
  "swot": {{
    "strengths": ["list of strings"],
    "weaknesses": ["list of strings"],
    "opportunities": ["list of strings"],
    "threats": ["list of strings"]
  }},
  "key_metrics": {{
    "total_competitors": "number - count of competitors mentioned",
    "growth_drivers": ["list of key growth drivers"]
  }},
  "strategic_priorities": ["list of strategic priorities or recommendations"]
}}

Document:
{document}

JSON Output:"""
        
        return prompt
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON from model response, handling common formatting issues.
        
        Args:
            response_text: Raw model response
            
        Returns:
            Parsed JSON dictionary
        """
        # Remove markdown code blocks if present
        cleaned = response_text.strip()
        
        # Remove ```json and ``` markers
        cleaned = re.sub(r'^```json\s*', '', cleaned)
        cleaned = re.sub(r'^```\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned)
        cleaned = cleaned.strip()
        
        # Try to find JSON object in the text
        # Look for content between first { and last }
        start_idx = cleaned.find('{')
        end_idx = cleaned.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_str = cleaned[start_idx:end_idx + 1]
            return json.loads(json_str)
        else:
            # Try parsing as-is
            return json.loads(cleaned)
    
    def _validate_and_cast(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and type-cast extracted data.
        
        Args:
            data: Raw extracted data
            
        Returns:
            Validated and type-cast data
        """
        # Ensure numeric fields are properly typed
        if 'market_share' in data and isinstance(data['market_share'], str):
            try:
                # Extract number from string like "12%" or "12"
                numeric_str = re.search(r'(\d+\.?\d*)', data['market_share'])
                if numeric_str:
                    data['market_share'] = float(numeric_str.group(1))
            except:
                pass
        
        # Validate competitors list
        if 'competitors' in data and isinstance(data['competitors'], list):
            for competitor in data['competitors']:
                if isinstance(competitor.get('market_share'), str):
                    try:
                        numeric_str = re.search(r'(\d+\.?\d*)', competitor['market_share'])
                        if numeric_str:
                            competitor['market_share'] = float(numeric_str.group(1))
                    except:
                        pass
        
        # Ensure SWOT categories exist
        if 'swot' not in data:
            data['swot'] = {
                'strengths': [],
                'weaknesses': [],
                'opportunities': [],
                'threats': []
            }
        
        return data
    
    def extract_custom_fields(
        self,
        document_text: str,
        field_schema: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Extract custom fields defined by user schema.
        
        Args:
            document_text: Full document text
            field_schema: Dictionary mapping field names to descriptions
            
        Returns:
            Extracted data matching the schema
        """
        # Build custom schema string
        schema_str = json.dumps(field_schema, indent=2)
        
        prompt = f"""Extract the following fields from the document.
Output ONLY valid JSON matching this schema:

{schema_str}

Document:
{document_text}

JSON Output:"""
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1,
                max_output_tokens=1024,
            )
        )
        
        return self._parse_json_response(response.text)
