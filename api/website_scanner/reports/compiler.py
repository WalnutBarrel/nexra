import logging
from typing import Dict, Any

from api.website_scanner.fetchers.http import website_fetcher_service
from api.website_scanner.detectors.tech import tech_detector_service
from api.website_scanner.analyzers.intelligence import seo_analyzer, security_analyzer, performance_analyzer

logger = logging.getLogger(__name__)

class DossierCompiler:
    """Orchestrates the scanner pipeline to compile the full intelligence dossier."""

    async def compile_report(self, domain: str) -> Dict[str, Any]:
        """Run all scanners and compile the dossier."""
        logger.info(f"Initiating full intelligence scan for domain: {domain}")
        
        try:
            # 1. Network / Telemetry Fetch
            fetch_data = await website_fetcher_service.fetch(domain)
            
            # 2. Tech Fingerprinting
            tech_stack = tech_detector_service.detect(fetch_data)
            
            # 3. Intelligence Analysis
            seo_data = seo_analyzer.analyze(fetch_data)
            security_data = security_analyzer.analyze(fetch_data)
            perf_data = performance_analyzer.analyze(fetch_data)
            
            # 4. Generate Final Dossier
            return {
                "domain": domain,
                "timestamp": "Live Data",
                "telemetry": {
                    "latency_ms": fetch_data["latency_ms"],
                    "status": fetch_data["status_code"],
                    "ssl_issuer": fetch_data["ssl_issuer"]
                },
                "technologies": tech_stack,
                "seo_intelligence": seo_data,
                "security_intelligence": security_data,
                "performance_intelligence": perf_data,
                "confidence_score": 98
            }
        except Exception as e:
            logger.error(f"Live scan failed for domain {domain}: {str(e)}. Falling back to degraded state.")
            # Graceful Fallback System
            return {
                "domain": domain,
                "timestamp": "Degraded Fallback (Offline)",
                "telemetry": {
                    "latency_ms": 0,
                    "status": 503,
                    "ssl_issuer": "Unknown (Fetch Failed)"
                },
                "technologies": [{"name": "Unknown", "category": "Stack", "confidence": 0}],
                "seo_intelligence": {"title_present": False, "meta_desc_present": False, "canonical_valid": False, "schema_markup_detected": False, "og_metadata_coverage": "0 nodes", "observations": [f"Live scan blocked or timed out: {str(e)}"], "score": 0},
                "security_intelligence": {"https_enforced": False, "hsts_active": False, "csp_present": False, "x_frame_options": "Unknown", "server_exposure": "Unknown", "observations": ["Could not establish secure perimeter inspection."], "posture": "Critical"},
                "performance_intelligence": {"estimated_dom_complexity": "0 nodes", "script_density": "0 scripts", "render_blocking_assets": 0, "observations": ["Telemetry extraction aborted."], "score": 0},
                "confidence_score": 10
            }

dossier_compiler = DossierCompiler()
