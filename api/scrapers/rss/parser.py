from typing import List, Dict, Any
from datetime import datetime

class RSSParser:
    """Service to handle RSS feed parsing and deduplication."""
    
    def __init__(self):
        # Mock realistic sources for seeding
        self.registered_sources = [
            {"id": "bloomberg", "url": "https://feeds.bloomberg.com/technology/news.rss"},
            {"id": "techcrunch", "url": "https://techcrunch.com/feed/"},
            {"id": "arxiv_ai", "url": "http://export.arxiv.org/rss/cs.AI"},
        ]
        # In-memory deduplication set for prototype
        self.seen_guids = set()

    async def fetch_feed(self, source_url: str) -> List[Dict[str, Any]]:
        """Mock implementation of feedparser logic."""
        # Realistic mock response
        return [
            {
                "guid": f"mock_guid_{datetime.utcnow().timestamp()}_1",
                "title": "Quantum Computing Startups See $2B Inflow in Q3",
                "link": "https://example.com/quantum-q3",
                "published_parsed": datetime.utcnow(),
                "summary": "Deep tech venture capital accelerates despite macroeconomic headwinds..."
            },
            {
                "guid": f"mock_guid_{datetime.utcnow().timestamp()}_2",
                "title": "European Union Finalizes Next Phase of AI Act",
                "link": "https://example.com/eu-ai-act",
                "published_parsed": datetime.utcnow(),
                "summary": "The European parliament passes stringent regulations focusing on general purpose AI models..."
            }
        ]

    async def process_feed(self, source_id: str, url: str) -> List[Dict[str, Any]]:
        """Fetch and filter out duplicate articles."""
        raw_items = await self.fetch_feed(url)
        new_items = []
        
        for item in raw_items:
            if item["guid"] not in self.seen_guids:
                self.seen_guids.add(item["guid"])
                new_items.append(item)
                
        return new_items

rss_parser_service = RSSParser()
