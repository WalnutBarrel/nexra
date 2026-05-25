from typing import Dict, Any
import time
import httpx
import ssl
import socket
from urllib.parse import urlparse

class WebsiteFetcher:
    """Service to handle core network telemetry and HTTP fetching."""

    async def fetch(self, domain: str) -> Dict[str, Any]:
        """Perform real HTTP extraction."""
        start_time = time.time()
        url = f"https://{domain}" if not domain.startswith("http") else domain
        domain_only = urlparse(url).netloc or domain

        headers_dict = {}
        status_code = 500
        html_content = ""
        redirect_chains = []
        
        # 1. SSL Extraction
        ssl_valid = False
        ssl_issuer = "Unknown"
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain_only, 443), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=domain_only) as ssock:
                    cert = ssock.getpeercert()
                    ssl_valid = True
                    for item in cert.get('issuer', []):
                        for k, v in item:
                            if k == 'organizationName':
                                ssl_issuer = v
        except Exception:
            pass # Fallback to False/Unknown

        # 2. HTTP Fetch
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, headers={"User-Agent": "Nexra Intelligence Bot/1.0"}) as client:
                response = await client.get(url)
                status_code = response.status_code
                html_content = response.text
                headers_dict = dict(response.headers)
                redirect_chains = [str(req.url) for req in response.history] + [str(response.url)]
        except Exception as e:
            raise RuntimeError(f"Fetch failed: {str(e)}")

        latency_ms = int((time.time() - start_time) * 1000)

        # 3. Check robots and sitemap existence (fire and forget check)
        robots_found = False
        sitemap_found = False
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                r_res = await client.head(f"https://{domain_only}/robots.txt")
                if r_res.status_code == 200: robots_found = True
                s_res = await client.head(f"https://{domain_only}/sitemap.xml")
                if s_res.status_code == 200: sitemap_found = True
        except Exception:
            pass

        return {
            "status_code": status_code,
            "latency_ms": latency_ms,
            "ssl_valid": ssl_valid,
            "ssl_issuer": ssl_issuer,
            "redirect_chains": redirect_chains,
            "robots_txt_found": robots_found,
            "sitemap_found": sitemap_found,
            "headers": {k.lower(): v for k, v in headers_dict.items()},
            "html_snippet": html_content
        }

website_fetcher_service = WebsiteFetcher()
