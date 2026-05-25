import feedparser
import time
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class RSSFetcher:
    """Fetches and parses live RSS/Atom feeds."""
    
    def __init__(self):
        self.sources = [
            {"id": "bloomberg_tech", "name": "Bloomberg Technology", "url": "https://feeds.bloomberg.com/technology/news.rss"},
            {"id": "techcrunch", "name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
            {"id": "arxiv_ai", "name": "ArXiv AI", "url": "http://export.arxiv.org/rss/cs.AI"},
        ]

    def fetch_all(self) -> List[Dict[str, Any]]:
        """Fetch all registered RSS feeds synchronously (can be async wrapped later)."""
        articles = []
        for source in self.sources:
            try:
                feed = feedparser.parse(source["url"])
                # Fallback check if the feed failed
                if feed.bozo and getattr(feed.bozo_exception, 'getMessage', lambda: '')() != '':
                    logger.warning(f"Error parsing feed {source['name']}: {feed.bozo_exception}")
                    continue
                    
                for entry in feed.entries[:10]: # Cap at top 10 per feed to prevent flooding
                    articles.append({
                        "id": getattr(entry, "id", entry.link),
                        "title": entry.title,
                        "url": entry.link,
                        "source": source["name"],
                        "source_id": source["id"],
                        "summary": getattr(entry, "summary", ""),
                        "timestamp": time.time(),
                        "type": "rss"
                    })
            except Exception as e:
                logger.error(f"Failed to fetch RSS from {source['name']}: {e}")
        return articles

rss_fetcher = RSSFetcher()
