from typing import List

class ExplainabilityEngine:
    def generate_evidence_basis(
        self,
        velocity: float,
        credibility_score: float,
        signal_quality: str,
        unique_sources: int,
        has_github: bool,
        github_stars: int,
        has_reddit: bool,
        dominant_sentiment: str,
        lifecycle_state: str,
        delta_24h: float,
        delta_7d: float,
        divergence_markers: List[str]
    ) -> List[str]:
        """
        Generates deterministic, operational evidence strings based on entity telemetry.
        """
        evidence = []

        # 1. Temporal & Growth Evidence
        if delta_7d is not None and delta_7d >= 20:
            evidence.append(f"Momentum acceleration increased {int(delta_7d)}% over the last 7 days.")
        elif delta_24h is not None and delta_24h >= 10:
            evidence.append(f"Momentum acceleration increased {int(delta_24h)}% over the last 24 hours.")
        elif lifecycle_state == "Stabilizing":
            evidence.append("Momentum is stabilizing after a period of rapid growth.")

        # 2. Source Confirmation Evidence
        if unique_sources >= 3 and signal_quality == "High":
            evidence.append(f"Strong cross-source confirmation detected across {unique_sources} distinct sources.")
        elif signal_quality == "Low":
            evidence.append("Momentum remains low-confidence due to weak cross-source confirmation.")

        # 3. Developer Traction Evidence
        if has_github and github_stars > 0:
            evidence.append(f"Repository traction confirmed with {github_stars}+ recent GitHub stars.")
            
        # 4. Ecosystem Sentiment Evidence
        if has_reddit and dominant_sentiment:
            sentiment_clean = dominant_sentiment.lower()
            if sentiment_clean in ["skepticism", "frustration", "caution"]:
                evidence.append(f"Ecosystem discussion is currently dominated by community {sentiment_clean}.")
            elif sentiment_clean in ["excitement", "praise", "adoption"]:
                evidence.append("Strong community excitement and adoption signals detected.")

        # 5. Divergence Evidence
        if divergence_markers:
            evidence.append(f"Signal conflict detected: {divergence_markers[0].lower()}.")

        # Keep to max 4 statements for density
        return evidence[:4]

explainability_engine = ExplainabilityEngine()
