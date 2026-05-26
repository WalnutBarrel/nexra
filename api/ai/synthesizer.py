import json
from typing import Dict, Any, List
from google import genai
from api.core.config import settings

class IntelligenceSynthesizer:
    """Uses AI to enrich raw news items with sentiment and executive summaries."""
    
    def __init__(self):
        self.model_name = "gemini-2.5-flash"
        
    def synthesize_batch(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processes a batch of articles and adds AI metadata."""
        if not settings.GEMINI_API_KEY or not articles:
            # Degraded fallback if no API key
            for a in articles:
                a["sentiment"] = "neutral"
                a["credibilityScore"] = 85
                a["tags"] = ["Tech", "News"]
            return articles
            
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            # Pack headlines into a prompt to minimize API calls
            headlines = [{"id": a["id"], "title": a["title"]} for a in articles]
            
            prompt = f"""
            You are a senior intelligence analyst. Analyze the following tech news headlines.
            For each, return a JSON object with:
            - id (string, matching the input)
            - sentiment (string: 'positive', 'negative', or 'neutral')
            - credibilityScore (integer 1-100 based on standard tech journalism norms)
            - tags (list of 2-3 precise technical tags, e.g., 'Agentic AI', 'Supply Chain')
            
            Input Headlines:
            {json.dumps(headlines)}
            
            Return ONLY a valid JSON array of objects. No markdown formatting.
            """
            
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            # Clean up potential markdown formatting in response
            response_text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
            
            ai_data = json.loads(response_text)
            ai_dict = {item["id"]: item for item in ai_data if "id" in item}
            
            for article in articles:
                meta = ai_dict.get(article["id"], {})
                article["sentiment"] = meta.get("sentiment", "neutral")
                article["credibilityScore"] = meta.get("credibilityScore", 85)
                article["tags"] = meta.get("tags", ["Intelligence"])
                
        except Exception as e:
            # Fallback on failure
            for a in articles:
                a["sentiment"] = "neutral"
                a["credibilityScore"] = 80
                a["tags"] = ["Unverified"]
                
        return articles

synthesizer = IntelligenceSynthesizer()
