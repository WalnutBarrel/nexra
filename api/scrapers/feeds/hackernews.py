import httpx
import time
from typing import List, Dict, Any
import logging
import asyncio

logger = logging.getLogger(__name__)

class HackerNewsFetcher:
    """Fetches top tech stories from the official HackerNews API."""
    
    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0"

    async def fetch_top_stories(self, limit: int = 15) -> List[Dict[str, Any]]:
        articles = []
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # 1. Get top story IDs
                top_resp = await client.get(f"{self.base_url}/topstories.json")
                if top_resp.status_code != 200:
                    return articles
                
                story_ids = top_resp.json()[:limit]
                
                # 2. Fetch story details in parallel
                tasks = [client.get(f"{self.base_url}/item/{sid}.json") for sid in story_ids]
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                
                for resp in responses:
                    if isinstance(resp, Exception):
                        continue
                    if resp.status_code == 200:
                        data = resp.json()
                        if data and data.get("type") == "story" and data.get("url"):
                            articles.append({
                                "id": f"hn_{data['id']}",
                                "title": data["title"],
                                "url": data["url"],
                                "source": "Hacker News",
                                "source_id": "hackernews",
                                "summary": f"Score: {data.get('score', 0)} | By: {data.get('by', 'unknown')}",
                                "timestamp": time.time(),
                                "type": "api"
                            })
        except Exception as e:
            logger.error(f"Failed to fetch HackerNews: {e}")
            
        return articles

hn_fetcher = HackerNewsFetcher()
