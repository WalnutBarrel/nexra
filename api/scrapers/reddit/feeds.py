import httpx
import logging
import asyncio
from typing import List, Dict, Any
from api.scrapers.reddit.extractors import reddit_extractor
from api.scrapers.reddit.normalizers import reddit_normalizer
from api.scrapers.reddit.enrichers import reddit_enricher

logger = logging.getLogger(__name__)

class RedditFetcher:
    def __init__(self):
        self.subreddits = [
            "LocalLLaMA",
            "MachineLearning",
            "artificial",
            "programming",
            "webdev",
            "opensource"
        ]
        
    async def fetch_subreddit(self, subreddit: str) -> List[Dict[str, Any]]:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=5"
        try:
            # Reddit requires a highly specific User-Agent format for unauthenticated scripts
            # format: <platform>:<app ID>:<version string> (by /u/<reddit username>)
            headers = {
                "User-Agent": "web:nexra.intelligence.engine:v1.0 (by /u/nexradev)"
            }
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=10.0)
                response.raise_for_status()
                json_data = response.json()
                
            raw_posts = reddit_extractor.extract_posts(json_data, subreddit)
            return raw_posts
        except Exception as e:
            logger.error(f"Failed to fetch Reddit r/{subreddit}: {e}")
            return []
            
    async def fetch_all(self) -> List[Dict[str, Any]]:
        tasks = [self.fetch_subreddit(sub) for sub in self.subreddits]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_raw_posts = []
        for res in results:
            if isinstance(res, list):
                all_raw_posts.extend(res)
                
        normalized = reddit_normalizer.normalize(all_raw_posts)
        enriched = reddit_enricher.enrich(normalized)
        
        return enriched

reddit_fetcher = RedditFetcher()
