import json
import time
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from api.core.config import settings

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

class EntityIntelligenceEngine:
    """Manages empirical entity tracking, mention growth, and correlation."""
    
    def __init__(self):
        self.model_name = "gemini-1.5-flash"
        # In-memory storage: { "Cursor": { "mentions": [ { "timestamp": float, "source": str } ], "category": "AI Tooling" } }
        self.entity_memory: Dict[str, Dict[str, Any]] = {}
        
    def extract_and_store_entities(self, articles: List[Dict[str, Any]]) -> None:
        """Extracts entities from a batch of articles and stores them in memory."""
        if not settings.GEMINI_API_KEY or not articles:
            return
            
        now = time.time()
        
        # 1. Native ingestion of GitHub entities (bypassing LLM extraction)
        llm_articles = []
        for article in articles:
            if article.get("source") == "GitHub Trending":
                # The entity is the repo itself
                metrics = article.get("github_metrics", {})
                e_name = article["title"].replace("GitHub Trending: ", "").strip().title()
                
                if e_name not in self.entity_memory:
                    self.entity_memory[e_name] = {
                        "category": article.get("category", "AI/Dev Infrastructure"),
                        "mentions": []
                    }
                
                self.entity_memory[e_name]["mentions"].append({
                    "timestamp": now,
                    "source": "GitHub Trending",
                    "github_stars": metrics.get("stars", 0),
                    "github_rank": metrics.get("rank", 999)
                })
            else:
                llm_articles.append(article)
                
        # 2. Standard LLM extraction for regular news and Reddit
        if not llm_articles:
            return
            
        try:
            model = genai.GenerativeModel(self.model_name)
            
            # Map index to source to maintain attribution
            article_map = {idx: a["source"] for idx, a in enumerate(llm_articles)}
            reddit_metrics_map = {idx: a.get("reddit_metrics", {}) for idx, a in enumerate(llm_articles)}
            headlines = [{"id": idx, "title": a["title"], "source": a["source"]} for idx, a in enumerate(llm_articles)]
            
            prompt = f"""
            You are a senior intelligence analyst. Extract the most prominent technology entities (companies, products, frameworks, tools) from these headlines.
            If a headline comes from Reddit, also infer the dominant developer sentiment (e.g., "excitement", "frustration", "skepticism", "adoption").
            
            Input Headlines:
            {json.dumps(headlines)}
            
            Return ONLY a valid JSON array of objects with:
            - id (integer, matching the input headline)
            - entities (list of strings, e.g., ["Cursor", "Anthropic", "React"])
            - category (string, a broad category like "AI Tooling" or "Frameworks" for these entities)
            - sentiment_indicator (string, ONLY if the source is Reddit, e.g., "excitement")
            
            No markdown formatting. Return raw JSON array.
            """
            
            response = model.generate_content(prompt)
            response_text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
            extracted_data = json.loads(response_text)
            
            for item in extracted_data:
                article_id = item.get("id")
                source = article_map.get(article_id, "Unknown Feed")
                category = item.get("category", "Technology")
                entities = item.get("entities", [])
                sentiment = item.get("sentiment_indicator")
                r_metrics = reddit_metrics_map.get(article_id, {})
                
                for entity in entities:
                    # Normalize entity name
                    e_name = str(entity).strip().title()
                    if e_name not in self.entity_memory:
                        self.entity_memory[e_name] = {
                            "category": category,
                            "mentions": []
                        }
                    
                    mention_data = {
                        "timestamp": now,
                        "source": source
                    }
                    if "Reddit" in source:
                        mention_data["sentiment"] = sentiment or "neutral"
                        mention_data["reddit_score"] = r_metrics.get("score", 0)
                        mention_data["reddit_comments"] = r_metrics.get("comments", 0)
                    
                    self.entity_memory[e_name]["mentions"].append(mention_data)
                    
        except Exception as e:
            pass # Fail silently for background extraction
            
    async def get_ranked_entities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Calculates empirical velocity and ranks entities."""
        now = time.time()
        results = []
        
        # We need persistence_layer imported inside to avoid circular imports if any, or at top
        from api.ai.intelligence.memory.persistence import persistence_layer
        
        for name, data in self.entity_memory.items():
            mentions = data["mentions"]
            
            # Filter mentions to last 24h (86400 seconds)
            recent_mentions = [m for m in mentions if now - m["timestamp"] <= 86400]
            if not recent_mentions:
                continue
                
            unique_sources = len(set(m["source"] for m in recent_mentions))
            mention_count = len(recent_mentions)
            
            # Check for GitHub presence to boost velocity
            has_github = False
            github_stars = 0
            has_reddit = False
            reddit_score = 0
            reddit_comments = 0
            sentiments = []
            
            for m in recent_mentions:
                if m["source"] == "GitHub Trending":
                    has_github = True
                    github_stars = max(github_stars, m.get("github_stars", 0))
                if "Reddit" in m["source"]:
                    has_reddit = True
                    reddit_score += m.get("reddit_score", 0)
                    reddit_comments += m.get("reddit_comments", 0)
                    if m.get("sentiment") and m.get("sentiment") != "neutral":
                        sentiments.append(m.get("sentiment"))
            
            dominant_sentiment = max(set(sentiments), key=sentiments.count) if sentiments else None
            
            # Velocity Calculation: (Mention Count * 2) + (Unique Sources * 5)
            velocity = (mention_count * 2) + (unique_sources * 5)
            
            # Heavy boost for GitHub trending presence
            if has_github:
                velocity += 20 + (github_stars // 1000)
                
            # Boost for Reddit engagement
            if has_reddit:
                velocity += 10 + (reddit_comments // 10) + (reddit_score // 50)
                
            velocity = min(100, velocity)
            
            # Fetch temporal history from DB
            history = await persistence_layer.get_historical_deltas(name)
            
            results.append({
                "name": name,
                "category": data["category"],
                "mentions": mention_count,
                "sources": unique_sources,
                "velocity": velocity,
                "has_github": has_github,
                "github_stars": github_stars,
                "has_reddit": has_reddit,
                "dominant_sentiment": dominant_sentiment,
                "discussion_intensity": reddit_comments,
                "delta_24h": history.get("delta_24h"),
                "delta_7d": history.get("delta_7d"),
                "lifecycle_state": history.get("lifecycle_state")
            })
            
        # Sort by velocity descending
        results.sort(key=lambda x: x["velocity"], reverse=True)
        return results[:limit]

entity_engine = EntityIntelligenceEngine()
