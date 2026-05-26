import json
import time
from typing import Dict, Any, List, Optional
from google import genai
from api.core.config import settings

class EntityIntelligenceEngine:
    """Manages empirical entity tracking, mention growth, and correlation."""
    
    def __init__(self):
        self.model_name = "gemini-2.5-flash"
        # In-memory storage: { "Cursor": { "mentions": [ { "timestamp": float, "source": str } ], "category": "AI Tooling" } }
        self.entity_memory: Dict[str, Dict[str, Any]] = {}
        self.relationship_memory: List[Dict[str, Any]] = []
        
    def extract_and_store_entities(self, articles: List[Dict[str, Any]]) -> None:
        """Extracts entities and relationships from a batch of articles and stores them in memory."""
        if not settings.GEMINI_API_KEY or not articles:
            return
            
        now = time.time()
        
        # 1. Native ingestion of GitHub entities (bypassing LLM extraction)
        llm_articles = []
        for article in articles:
            if article.get("source") == "GitHub Trending":
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
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            # Map index to source to maintain attribution
            article_map = {idx: a["source"] for idx, a in enumerate(llm_articles)}
            reddit_metrics_map = {idx: a.get("reddit_metrics", {}) for idx, a in enumerate(llm_articles)}
            headlines = [{"id": idx, "title": a["title"], "source": a["source"]} for idx, a in enumerate(llm_articles)]
            
            from api.ai.intelligence.relationships.extractor import relationship_extractor
            
            prompt = f"""
            You are a senior intelligence analyst. Extract the most prominent technology entities (companies, products, frameworks, tools) from these headlines.
            If a headline comes from Reddit, also infer the dominant developer sentiment (e.g., "excitement", "frustration", "skepticism", "adoption").
            Also, extract any explicit or implicit relationships between these entities (e.g., "Cursor" uses "Claude", "LangGraph" is an "AI Agent Framework").
            
            Input Headlines:
            {json.dumps(headlines)}
            
            Return ONLY a valid JSON array of objects with:
            - id (integer, matching the input headline)
            - entities (list of strings, e.g., ["Cursor", "Anthropic", "React"])
            - category (string, a broad category like "AI Tooling" or "Frameworks" for these entities)
            - sentiment_indicator (string, ONLY if the source is Reddit, e.g., "excitement")
            - relationships (list of objects with 'entity_a', 'relationship', 'entity_b')
            
            No markdown formatting. Return raw JSON array.
            """
            
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            response_text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
            extracted_data = json.loads(response_text)
            
            for item in extracted_data:
                article_id = item.get("id")
                source = article_map.get(article_id, "Unknown Feed")
                category = item.get("category", "Technology")
                entities = item.get("entities", [])
                sentiment = item.get("sentiment_indicator")
                raw_relationships = item.get("relationships", [])
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
                    
                # Parse and track relationships in the hot-cache
                parsed_rels = relationship_extractor.parse_gemini_relationships(raw_relationships, source, now)
                self.relationship_memory.extend(parsed_rels)
                    
        except Exception as e:
            pass # Fail silently for background extraction
            
    async def get_ranked_entities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Calculates empirical velocity and ranks entities."""
        now = time.time()
        results = []
        
        # We need persistence_layer imported inside to avoid circular imports if any, or at top
        from api.ai.intelligence.memory.persistence import persistence_layer
        from api.ai.intelligence.relationships.ecosystems import ecosystem_classifier
        from api.ai.intelligence.relationships.scoring import relationship_scorer
        
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
            
            from api.ai.intelligence.credibility.scoring import credibility_scorer
            
            # Delegate to credibility scorer
            velocity, cred_score, signal_quality = credibility_scorer.calculate_weighted_velocity(
                mentions=recent_mentions,
                github_stars=github_stars,
                reddit_score=reddit_score,
                reddit_comments=reddit_comments
            )
            
            # Noise Suppression: Drop entities with extremely low credibility and low volume
            if cred_score < 40.0 and mention_count < 3:
                continue
                
            # Fetch temporal history from DB
            history = await persistence_layer.get_historical_deltas(name)
            
            from api.ai.intelligence.divergence.scoring import divergence_scorer
            divergence_markers = divergence_scorer.detect_divergence(
                velocity=velocity,
                credibility_score=cred_score,
                mention_count=mention_count,
                unique_sources=unique_sources,
                has_github=has_github,
                github_stars=github_stars,
                dominant_sentiment=dominant_sentiment,
                lifecycle_state=history.get("lifecycle_state"),
                delta_24h=history.get("delta_24h")
            )
            
            # Relationships for this entity
            entity_rels = [r for r in self.relationship_memory if r["entity_a"] == name.lower() or r["entity_b"] == name.lower()]
            
            # Confidence threshold >= 0.5
            high_confidence_rels = []
            for r in entity_rels:
                if r.get("confidence_score", 0) >= 0.5:
                    # Get the other entity
                    other_entity = r["entity_b"] if r["entity_a"] == name.lower() else r["entity_a"]
                    high_confidence_rels.append({
                        "entity": other_entity,
                        "type": r["relationship_type"],
                        "confidence": r["confidence_score"]
                    })
            
            # Classify ecosystem
            ecosystem = ecosystem_classifier.classify(name, [r["entity"] for r in high_confidence_rels])
            
            from api.ai.intelligence.explainability.reasoning import explainability_engine
            evidence_basis = explainability_engine.generate_evidence_basis(
                velocity=velocity,
                credibility_score=cred_score,
                signal_quality=signal_quality,
                unique_sources=unique_sources,
                has_github=has_github,
                github_stars=github_stars,
                has_reddit=has_reddit,
                dominant_sentiment=dominant_sentiment,
                lifecycle_state=history.get("lifecycle_state"),
                delta_24h=history.get("delta_24h"),
                delta_7d=history.get("delta_7d"),
                divergence_markers=divergence_markers
            )
            
            results.append({
                "name": name,
                "category": data["category"],
                "ecosystem": ecosystem,
                "mentions": mention_count,
                "sources": unique_sources,
                "velocity": velocity,
                "credibility_score": cred_score,
                "signal_quality": signal_quality,
                "has_github": has_github,
                "github_stars": github_stars,
                "has_reddit": has_reddit,
                "dominant_sentiment": dominant_sentiment,
                "discussion_intensity": reddit_comments,
                "delta_24h": history.get("delta_24h"),
                "delta_7d": history.get("delta_7d"),
                "lifecycle_state": history.get("lifecycle_state"),
                "divergence_markers": divergence_markers,
                "evidence_basis": evidence_basis,
                "relationships": high_confidence_rels[:3] # Top 3
            })
            
        # Sort by velocity descending
        results.sort(key=lambda x: x["velocity"], reverse=True)
        return results[:limit]

entity_engine = EntityIntelligenceEngine()
