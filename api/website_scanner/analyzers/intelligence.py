from typing import Dict, Any, List
from bs4 import BeautifulSoup
import re

class SEOAnalyzer:
    """Intelligence analyzer for SEO metadata."""

    def analyze(self, fetch_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate professional intelligence-style observations for SEO."""
        html = fetch_data.get("html_snippet", "")
        soup = BeautifulSoup(html, "html.parser")
        
        title_tag = soup.find("title")
        title_present = title_tag is not None and bool(title_tag.text.strip())
        
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_desc_present = meta_desc is not None and bool(meta_desc.get("content", "").strip())
        
        canonical = soup.find("link", attrs={"rel": "canonical"})
        canonical_valid = canonical is not None and bool(canonical.get("href", "").strip())
        
        # OpenGraph
        og_tags = soup.find_all("meta", attrs={"property": re.compile(r"^og:")})
        og_metadata_coverage = f"{len(og_tags)} nodes"
        
        # Schema markup
        schema_tags = soup.find_all("script", attrs={"type": "application/ld+json"})
        schema_markup_detected = len(schema_tags) > 0
        
        # Headings
        h1_tags = soup.find_all("h1")

        observations = []
        if not title_present:
            observations.append("Critical intelligence gap: Missing primary <title> node.")
        if not meta_desc_present:
            observations.append("Surface visibility degraded: <meta name='description'> is absent.")
        if len(h1_tags) == 0:
            observations.append("Structural anomaly: Missing root <h1> node in document hierarchy.")
        elif len(h1_tags) > 1:
            observations.append("Structural fragmentation: Multiple <h1> nodes detected.")
            
        if not schema_markup_detected:
            observations.append("Schema.org markup is unconfigured, limiting rich entity extraction.")
        else:
            observations.append("Structured entity markup (application/ld+json) actively detected.")

        if not observations:
            observations.append("SEO structural integrity is nominal and adheres to standard specs.")

        return {
            "title_present": title_present,
            "meta_desc_present": meta_desc_present,
            "canonical_valid": canonical_valid,
            "schema_markup_detected": schema_markup_detected,
            "og_metadata_coverage": og_metadata_coverage,
            "observations": observations[:3], # Keep it dense
            "score": 100 - (len(observations) * 5)
        }

class SecurityAnalyzer:
    """Intelligence analyzer for Security posture."""

    def analyze(self, fetch_data: Dict[str, Any]) -> Dict[str, Any]:
        headers = fetch_data.get("headers", {})
        
        hsts_present = "strict-transport-security" in headers
        csp_present = "content-security-policy" in headers
        x_frame = headers.get("x-frame-options", "Not Set")
        server_exposure = headers.get("server", "Hidden")
        
        observations = []
        if hsts_present:
            observations.append("Strict-Transport-Security (HSTS) actively enforcing TLS.")
        else:
            observations.append("HSTS enforcement missing, exposing downgrade vectors.")
            
        if csp_present:
            observations.append("Content-Security-Policy (CSP) active and mitigating XSS.")
        else:
            observations.append("CSP unconfigured, leaving DOM susceptible to injection.")
            
        if server_exposure != "Hidden":
            observations.append(f"Server header leaking infrastructure fingerprint: {server_exposure}.")

        return {
            "https_enforced": fetch_data.get("ssl_valid", False),
            "hsts_active": hsts_present,
            "csp_present": csp_present,
            "x_frame_options": x_frame,
            "server_exposure": server_exposure,
            "observations": observations[:3],
            "posture": "Secure" if hsts_present and csp_present else "Warning"
        }

class PerformanceAnalyzer:
    """Intelligence analyzer for DOM and Asset performance."""

    def analyze(self, fetch_data: Dict[str, Any]) -> Dict[str, Any]:
        html = fetch_data.get("html_snippet", "")
        soup = BeautifulSoup(html, "html.parser")
        
        # Real estimation
        dom_nodes = len(soup.find_all())
        scripts = soup.find_all("script")
        stylesheets = soup.find_all("link", attrs={"rel": "stylesheet"})
        images = soup.find_all("img")
        
        observations = []
        if dom_nodes > 1500:
            observations.append(f"Excessive DOM complexity detected ({dom_nodes} nodes), risk of layout thrashing.")
        else:
            observations.append(f"DOM complexity within optimal thresholds ({dom_nodes} nodes).")
            
        if len(scripts) > 15:
            observations.append(f"Heavy script density ({len(scripts)} execution nodes) indicating potential JS bloat.")
            
        if len(stylesheets) > 3:
            observations.append(f"Multiple render-blocking stylesheet requests ({len(stylesheets)}).")
            
        return {
            "estimated_dom_complexity": f"{dom_nodes} nodes",
            "script_density": f"{len(scripts)} scripts",
            "render_blocking_assets": len(stylesheets),
            "observations": observations[:3],
            "score": max(0, 100 - (dom_nodes // 100) - len(scripts))
        }

seo_analyzer = SEOAnalyzer()
security_analyzer = SecurityAnalyzer()
performance_analyzer = PerformanceAnalyzer()
