import httpx
import logging
from typing import List, Dict, Any
from api.scrapers.github.extractors import github_extractor
from api.scrapers.github.normalizers import github_normalizer
from api.scrapers.github.enrichers import github_enricher

logger = logging.getLogger(__name__)

class GithubTrendingFetcher:
    def __init__(self):
        self.url = "https://github.com/trending"
        
    def fetch_all(self) -> List[Dict[str, Any]]:
        try:
            # We use a standard browser user agent to avoid basic blocks
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            response = httpx.get(self.url, headers=headers, timeout=10.0)
            response.raise_for_status()
            
            raw_repos = github_extractor.extract_trending_html(response.text)
            normalized = github_normalizer.normalize(raw_repos)
            enriched = github_enricher.enrich(normalized)
            
            return enriched
        except Exception as e:
            logger.error(f"Failed to fetch GitHub trending: {e}")
            return []

github_fetcher = GithubTrendingFetcher()
