from typing import List, Dict, Any

class TechnologyDetector:
    """Service to fingerprint tech stacks based on HTML, headers, and scripts."""

    def detect(self, fetch_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Mock detection logic returning frameworks and confidences."""
        detected = []
        headers = fetch_data.get("headers", {})
        html = fetch_data.get("html_snippet", "").lower()

        # Mocking heuristics
        if "cloudflare" in headers.get("server", "").lower():
            detected.append({"name": "Cloudflare", "category": "CDN", "confidence": 0.99})
        
        if "_next/static/" in html or "next.js" in headers.get("x-powered-by", "").lower():
            detected.append({"name": "Next.js", "category": "Framework", "confidence": 0.95})
            detected.append({"name": "React", "category": "UI Library", "confidence": 0.98})
            
        if "wordpress" in html:
            detected.append({"name": "WordPress", "category": "CMS", "confidence": 0.85})

        if not detected:
            detected.append({"name": "Custom/Unknown", "category": "Stack", "confidence": 0.5})

        return detected

tech_detector_service = TechnologyDetector()
