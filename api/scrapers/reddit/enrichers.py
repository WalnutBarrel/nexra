from typing import List, Dict, Any

class RedditEnricher:
    def enrich(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        enriched = []
        for post in posts:
            # Basic enrichment
            post["category"] = "Developer Ecosystem"
            post["tags"] = ["Community Sentiment"]
            enriched.append(post)
        return enriched

reddit_enricher = RedditEnricher()
