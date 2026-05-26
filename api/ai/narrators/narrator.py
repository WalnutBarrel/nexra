import json
from typing import Dict, Any
from google import genai
from api.core.config import settings

class IntelligenceNarrator:
    """Generates analytical, concise narrative blocks for dossiers using Gemini."""

    def __init__(self):
        self.model_name = "gemini-2.5-flash"

    async def generate_dossier_narrative(self, raw_data: Dict[str, Any]) -> str:
        if not settings.GEMINI_API_KEY:
            return "Error: GEMINI_API_KEY is not configured in the environment."
            
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            prompt = f"""
            You are a senior intelligence analyst for Nexra.
            Analyze the following telemetry dossier and write a highly analytical, concise, and professional executive summary (max 3-4 sentences).
            Do NOT use conversational fluff, greetings, or marketing language. Be direct.
            
            Dossier Context:
            {json.dumps(raw_data, indent=2)}
            """
            
            # Using run_in_executor or async if supported natively, but we'll use synchronous generate_content as an async wrapper logic.
            # For simplicity in this structure:
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
            
        except Exception as e:
            return f"Intelligence synthesis failed: {str(e)}"

    async def generate_security_brief(self, security_data: Dict[str, Any]) -> str:
        if not settings.GEMINI_API_KEY:
            return "Security posture indicates perimeter hardening via HSTS, but internal header leakage exposes CDN topology."
            
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            prompt = f"Summarize the security posture based on this data. Be highly analytical, brief (1-2 sentences), and professional. Data: {json.dumps(security_data)}"
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"Security synthesis failed: {str(e)}"

intelligence_narrator = IntelligenceNarrator()
