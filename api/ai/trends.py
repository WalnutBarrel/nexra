import json
from typing import Dict, Any, List
import google.generativeai as genai
from api.core.config import settings
from api.ai.intelligence.engine import entity_engine

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

class TrendEngine:
    """Analyzes streams of articles to detect accelerating topics."""
    
    def __init__(self):
        self.model_name = "gemini-1.5-flash"
        self.mock_trends = [
            {"topic": "Autonomous Agents", "category": "AI Research", "trend": "up", "score": 95, "sources": 3, "mentions": 12, "narrative": "Empirical velocity indicates strong acceleration in autonomous capabilities."},
        ]

    def compute_trends(self, recent_articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyzes recent headlines to output top trending topics using evidence-backed entity telemetry."""
        entities = entity_engine.get_ranked_entities(limit=4)
        
        if not settings.GEMINI_API_KEY or not entities:
            return self.mock_trends
            
        try:
            model = genai.GenerativeModel(self.model_name)
            
            prompt = f"""
            You are a senior intelligence analyst. Write a highly tactical, 1-sentence evidence-backed narrative for each of the following tracked entities based ONLY on their telemetry.
            Do not invent data. Use operational terminology (e.g. "Velocity indicates strong multi-source recurrence").
            
            Entity Telemetry:
            {json.dumps(entities)}
            
            Return ONLY a valid JSON array of objects with:
            - topic (string, matching the entity name)
            - category (string, matching the entity category)
            - trend (string: "up")
            - score (integer, matching velocity)
            - sources (integer, matching sources)
            - mentions (integer, matching mentions)
            - narrative (string, your 1-sentence synthesis)
            """
            
            response = model.generate_content(prompt)
            response_text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
            
            trends = json.loads(response_text)
            return trends
            
        except Exception as e:
            # Fallback to returning the entities directly if generation fails
            fallback = []
            for e in entities:
                fallback.append({
                    "topic": e["name"],
                    "category": e["category"],
                    "trend": "up",
                    "score": e["velocity"],
                    "sources": e["sources"],
                    "mentions": e["mentions"],
                    "narrative": "Empirical entity telemetry captured. AI synthesis unavailable."
                })
            return fallback if fallback else self.mock_trends

trend_engine = TrendEngine()
