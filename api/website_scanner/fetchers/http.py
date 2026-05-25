from typing import Dict, Any
import time

class WebsiteFetcher:
    """Service to handle core network telemetry and HTTP fetching."""

    async def fetch(self, domain: str) -> Dict[str, Any]:
        """Mock HTTP extraction simulating a real request."""
        start_time = time.time()
        # Mocking latency
        latency_ms = 145 
        
        return {
            "status_code": 200,
            "latency_ms": latency_ms,
            "ssl_valid": True,
            "ssl_issuer": "Let's Encrypt",
            "redirect_chains": ["http://" + domain, "https://" + domain],
            "robots_txt_found": True,
            "sitemap_found": True,
            "headers": {
                "server": "cloudflare",
                "x-powered-by": "Next.js",
                "content-type": "text/html; charset=utf-8",
                "strict-transport-security": "max-age=31536000; includeSubDomains"
            },
            "html_snippet": "<html><head><title>Mock Data</title><meta name='generator' content='WordPress'></head><body><script src='_next/static/'></script></body></html>"
        }

website_fetcher_service = WebsiteFetcher()
