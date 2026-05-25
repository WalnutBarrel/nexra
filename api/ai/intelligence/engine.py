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
                
        # 2. Standard LLM extraction for regular news
        if not llm_articles:
            return
            
        try:
            model = genai.GenerativeModel(self.model_name)
            
            # Map index to source to maintain attribution
            article_map = {idx: a["source"] for idx, a in enumerate(llm_articles)}
            headlines = [{"id": idx, "title": a["title"]} for idx, a in enumerate(llm_articles)]
            
            prompt = f"""
            You are a senior intelligence analyst. Extract the most prominent technology entities (companies, products, frameworks, tools) from these headlines.
            
            Input Headlines:
            {json.dumps(headlines)}
            
            Return ONLY a valid JSON array of objects with:
            - id (integer, matching the input headline)
            - entities (list of strings, e.g., ["Cursor", "Anthropic", "React"])
            - category (string, a broad category like "AI Tooling" or "Frameworks" for these entities)
            
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
                
                for entity in entities:
                    # Normalize entity name
                    e_name = str(entity).strip().title()
                    if e_name not in self.entity_memory:
                        self.entity_memory[e_name] = {
                            "category": category,
                            "mentions": []
                        }
                    
                    self.entity_memory[e_name]["mentions"].append({
                        "timestamp": now,
                        "source": source
                    })
                    
        except Exception as e:
            pass # Fail silently for background extraction
            
    def get_ranked_entities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Calculates empirical velocity and ranks entities."""
        now = time.time()
        results = []
        
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
            for m in recent_mentions:
                if m["source"] == "GitHub Trending":
                    has_github = True
                    github_stars = max(github_stars, m.get("github_stars", 0))
            
            # Velocity Calculation: (Mention Count * 2) + (Unique Sources * 5)
            velocity = (mention_count * 2) + (unique_sources * 5)
            
            # Heavy boost for GitHub trending presence
            if has_github:
                velocity += 20 + (github_stars // 1000)
                
            velocity = min(100, velocity)
            
            results.append({
                "name": name,
                "category": data["category"],
                "mentions": mention_count,
                "sources": unique_sources,
                "velocity": velocity,
                "has_github": has_github,
                "github_stars": github_stars
            })
            
        # Sort by velocity descending
        results.sort(key=lambda x: x["velocity"], reverse=True)
        return results[:limit]

entity_engine = EntityIntelligenceEngine()
