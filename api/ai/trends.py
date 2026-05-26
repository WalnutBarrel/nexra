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
        self.model_name = "gemini-1.5-flash-latest"
        self.mock_trends = [
            {"topic": "Autonomous Agents", "category": "AI Research", "trend": "up", "score": 95, "sources": 3, "mentions": 12, "narrative": "Empirical velocity indicates strong acceleration in autonomous capabilities."},
        ]

    async def compute_trends(self, recent_articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyzes recent headlines to output top trending topics using evidence-backed entity telemetry."""
        entities = await entity_engine.get_ranked_entities(limit=4)
        
        if not settings.GEMINI_API_KEY or not entities:
            return self.mock_trends
            
        try:
            model = genai.GenerativeModel(self.model_name)
            
            prompt = f"""
            You are a senior intelligence analyst. Write a highly tactical, 1-sentence evidence-backed narrative for each of the following tracked entities based ONLY on their telemetry.
            Do not invent data. Use operational terminology (e.g. "Velocity indicates strong multi-source recurrence").
            If an entity has 'has_github' set to true, you MUST cite its GitHub trending presence and star count as evidence of developer traction.
            If an entity has 'has_reddit' set to true, you MUST cite its 'dominant_sentiment' (e.g., excitement, skepticism) and 'discussion_intensity' to describe ecosystem realism.
            If an entity has 'lifecycle_state' and deltas, you MUST incorporate this temporal intelligence into the narrative (e.g. "Momentum accelerated 340% over the past 24 hours", "Stabilizing after rapid growth").
            If an entity has 'ecosystem' or 'relationships', explicitly contextualize it within its ecosystem (e.g. "Acceleration observed across the AI IDE ecosystem surrounding Cursor, Claude integration...").
            If an entity has 'signal_quality', use it to frame the narrative: if High, describe verified momentum; if Low, note weak cross-source confirmation.
            If an entity has 'divergence_markers', the narrative MUST reflect the conflict analytically (e.g. "Developer adoption signals remain strong despite rising ecosystem skepticism"). Do not use dramatic or alarmist language.
            If an entity has an 'evidence_basis' array, you MUST ground your 1-sentence narrative directly in the provided evidence.
            
            Entity Telemetry:
            {json.dumps(entities)}
            
            Return ONLY a valid JSON array of objects with:
            - topic (string, matching the entity name)
            - category (string, matching the entity category)
            - ecosystem (string, matching the ecosystem)
            - trend (string: "up")
            - score (integer, matching velocity)
            - credibility_score (float, matching credibility_score)
            - signal_quality (string, matching signal_quality)
            - sources (integer, matching sources)
            - mentions (integer, matching mentions)
            - narrative (string, your 1-sentence synthesis)
            - has_github (boolean, matching has_github)
            - github_stars (integer, matching github_stars)
            - has_reddit (boolean, matching has_reddit)
            - dominant_sentiment (string, matching dominant_sentiment)
            - discussion_intensity (integer, matching discussion_intensity)
            - delta_24h (float, matching delta_24h)
            - delta_7d (float, matching delta_7d)
            - lifecycle_state (string, matching lifecycle_state)
            - divergence_markers (list of strings, matching divergence_markers)
            - evidence_basis (list of strings, matching evidence_basis)
            - relationships (list of objects, matching relationships)
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
                    "ecosystem": e.get("ecosystem"),
                    "trend": "up",
                    "score": e["velocity"],
                    "credibility_score": e.get("credibility_score", 0),
                    "signal_quality": e.get("signal_quality", "Low"),
                    "sources": e["sources"],
                    "mentions": e["mentions"],
                    "narrative": "Empirical entity telemetry captured. AI synthesis unavailable.",
                    "has_github": e.get("has_github", False),
                    "github_stars": e.get("github_stars", 0),
                    "has_reddit": e.get("has_reddit", False),
                    "dominant_sentiment": e.get("dominant_sentiment", None),
                    "discussion_intensity": e.get("discussion_intensity", 0),
                    "delta_24h": e.get("delta_24h", None),
                    "delta_7d": e.get("delta_7d", None),
                    "lifecycle_state": e.get("lifecycle_state", None),
                    "divergence_markers": e.get("divergence_markers", []),
                    "evidence_basis": e.get("evidence_basis", []),
                    "relationships": e.get("relationships", [])
                })
            return fallback if fallback else self.mock_trends

trend_engine = TrendEngine()
