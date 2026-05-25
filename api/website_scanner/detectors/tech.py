from typing import List, Dict, Any
import re

class TechnologyDetector:
    """Service to fingerprint tech stacks based on HTML, headers, and scripts."""

    def detect(self, fetch_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Real detection logic returning frameworks and confidences."""
        detected = []
        headers = fetch_data.get("headers", {})
        html = fetch_data.get("html_snippet", "").lower()
        
        server_header = headers.get("server", "").lower()
        powered_by = headers.get("x-powered-by", "").lower()
        via = headers.get("via", "").lower()

        # CDN & Infrastructure
        if "cloudflare" in server_header or "cloudflare" in via:
            detected.append({"name": "Cloudflare", "category": "CDN", "confidence": 0.99})
        if "vercel" in server_header or "vercel" in headers.get("x-vercel-id", "").lower():
            detected.append({"name": "Vercel", "category": "PaaS", "confidence": 0.99})

        # Frameworks & UI
        if "_next/static/" in html or "next.js" in powered_by:
            detected.append({"name": "Next.js", "category": "Framework", "confidence": 0.95})
            detected.append({"name": "React", "category": "UI Library", "confidence": 0.98})
        elif "react" in html or "data-reactroot" in html:
            detected.append({"name": "React", "category": "UI Library", "confidence": 0.80})

        if "data-v-" in html and "vue" in html:
            detected.append({"name": "Vue.js", "category": "UI Library", "confidence": 0.85})
            
        if "ng-version" in html:
            detected.append({"name": "Angular", "category": "Framework", "confidence": 0.90})

        # CMS
        if "wp-content" in html or "wordpress" in html:
            detected.append({"name": "WordPress", "category": "CMS", "confidence": 0.95})
        
        # CSS Frameworks
        if "text-center" in html and "flex" in html and "p-4" in html:
            detected.append({"name": "Tailwind CSS", "category": "Styling", "confidence": 0.70})
            
        # Analytics
        if "google-analytics.com" in html or "googletagmanager.com" in html:
            detected.append({"name": "Google Analytics", "category": "Analytics", "confidence": 0.90})
        if "connect.facebook.net/en_us/fbevents.js" in html:
            detected.append({"name": "Meta Pixel", "category": "Analytics", "confidence": 0.95})

        if not detected:
            detected.append({"name": "Custom/Unknown", "category": "Stack", "confidence": 0.5})

        # Deduplicate and sort by confidence
        seen = set()
        final_detected = []
        for d in sorted(detected, key=lambda x: x['confidence'], reverse=True):
            if d['name'] not in seen:
                seen.add(d['name'])
                final_detected.append(d)

        return final_detected

tech_detector_service = TechnologyDetector()
