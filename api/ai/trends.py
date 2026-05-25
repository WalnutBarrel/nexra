import json
from typing import Dict, Any, List
import google.generativeai as genai
from api.core.config import settings

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

class TrendEngine:
    """Analyzes streams of articles to detect accelerating topics."""
    
    def __init__(self):
        self.model_name = "gemini-1.5-flash"
        self.mock_trends = [
            {"topic": "Autonomous Agents", "category": "AI Research", "trend": "up", "score": 95},
            {"topic": "Next.js 15", "category": "Frameworks", "trend": "up", "score": 88},
            {"topic": "Legacy VPNs", "category": "Security", "trend": "down", "score": 32}
        ]

    def compute_trends(self, recent_articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyzes recent headlines to output top 4 trending topics."""
        if not settings.GEMINI_API_KEY or not recent_articles:
            return self.mock_trends
            
        try:
            model = genai.GenerativeModel(self.model_name)
            headlines = [a["title"] for a in recent_articles[:30]]
            
            prompt = f"""
            Analyze these recent technology headlines and identify the 4 most prominent trending topics.
            Calculate a score (0-100) based on perceived velocity and importance.
            
            Headlines:
            {json.dumps(headlines)}
            
            Return ONLY a valid JSON array of 4 objects with:
            - topic (string, e.g. "Quantum Error Correction")
            - category (string, e.g. "Deep Tech")
            - trend (string: "up" or "down")
            - score (integer 0-100)
            """
            
            response = model.generate_content(prompt)
            response_text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
            
            trends = json.loads(response_text)
            return trends[:4]
            
        except Exception as e:
            return self.mock_trends

trend_engine = TrendEngine()
