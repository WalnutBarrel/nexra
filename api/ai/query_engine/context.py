import json
from typing import Dict, Any
import google.generativeai as genai
from api.core.config import settings

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

class DossierQueryEngine:
    """Contextual query interface for interacting with intelligence dossiers using Gemini."""

    def __init__(self):
        self.model_name = "gemini-1.5-flash"

    async def execute_query(self, query: str, context: Dict[str, Any]) -> Dict[str, str]:
        """Process a natural language query against a dossier context."""
        
        if not settings.GEMINI_API_KEY:
            return {
                "query": query,
                "response": "Error: GEMINI_API_KEY is not configured.",
                "tone": "error",
                "tokens_used": 0
            }

        try:
            model = genai.GenerativeModel(self.model_name)
            
            prompt = f"""
            You are a senior intelligence analyst for Nexra.
            A user is asking a question about a specific intelligence dossier.
            Answer their query based ONLY on the provided dossier context.
            Keep your answer analytical, concise, and professional. 
            Do NOT use chatbot phrases like "I can help with that". Just deliver the intelligence.
            
            User Query: {query}
            
            Dossier Context:
            {json.dumps(context, indent=2)}
            """
            
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Note: Token counting is approximated or handled via metadata if available
            tokens = model.count_tokens(prompt).total_tokens if hasattr(model, 'count_tokens') else 0
            
            return {
                "query": query,
                "response": response_text,
                "tone": "analytical",
                "tokens_used": tokens
            }
        except Exception as e:
             return {
                "query": query,
                "response": f"Query execution failed: {str(e)}",
                "tone": "error",
                "tokens_used": 0
            }

dossier_query_engine = DossierQueryEngine()
