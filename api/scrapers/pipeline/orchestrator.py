from typing import List, Dict, Any
import asyncio
from api.scrapers.feeds.rss import rss_fetcher
from api.scrapers.feeds.hackernews import hn_fetcher
from api.ai.intelligence.engine import entity_engine

class PipelineOrchestrator:
    """Coordinates data extraction across all feeds and deduplicates it."""
    
    def __init__(self):
        self.seen_ids = set()
        self.intelligence_buffer = []
        
    async def ingest_live_feeds(self) -> List[Dict[str, Any]]:
        """Pulls from all sources and returns new unique articles."""
        new_articles = []
        
        # Run RSS fetch synchronously in a thread, run HN fetch asynchronously
        rss_articles = await asyncio.to_thread(rss_fetcher.fetch_all)
        hn_articles = await hn_fetcher.fetch_top_stories(limit=10)
        
        all_fetched = rss_articles + hn_articles
        
        # Deduplicate
        for article in all_fetched:
            if article["id"] not in self.seen_ids:
                self.seen_ids.add(article["id"])
                new_articles.append(article)
                
        # Send new articles to the Entity Intelligence Engine for background extraction
        if new_articles:
            # We fire this off asynchronously using create_task so it doesn't block ingestion
            asyncio.create_task(asyncio.to_thread(entity_engine.extract_and_store_entities, new_articles))
                
        # Maintain a rolling buffer of the last 100 items for the UI
        self.intelligence_buffer = new_articles + self.intelligence_buffer
        if len(self.intelligence_buffer) > 100:
            self.intelligence_buffer = self.intelligence_buffer[:100]
            
        return new_articles
        
    def get_latest_intelligence(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Returns the current rolling buffer for the API."""
        return self.intelligence_buffer[:limit]

orchestrator = PipelineOrchestrator()
