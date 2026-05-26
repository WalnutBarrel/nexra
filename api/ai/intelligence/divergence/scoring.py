from typing import List, Dict, Any

class DivergenceScorer:
    def detect_divergence(
        self,
        velocity: float,
        credibility_score: float,
        mention_count: int,
        unique_sources: int,
        has_github: bool,
        github_stars: int,
        dominant_sentiment: str,
        lifecycle_state: str,
        delta_24h: float
    ) -> List[str]:
        """
        Calculates deterministic divergence markers based on telemetry conflict.
        Returns a list of string markers (empty if no contradictions).
        """
        markers = []

        # 1. Traction vs. Sentiment Contradiction
        if has_github and github_stars > 10:
            if dominant_sentiment and dominant_sentiment.lower() in ["skepticism", "frustration", "negative", "caution"]:
                markers.append("Developer Adoption vs Community Skepticism")

        # 2. Hype vs. Credibility Contradiction
        if velocity > 70 and credibility_score < 50:
            markers.append("High Momentum but Low Credibility")

        # 3. Fragmented Confirmation (Spam / Astroturfing indicator)
        if mention_count > 8 and unique_sources <= 2:
            markers.append("Weak Cross-Source Confirmation")

        # 4. Temporal Instability
        if lifecycle_state == "Decaying" and delta_24h is not None and delta_24h > 50:
            markers.append("Unstable Momentum Spike")

        return markers

divergence_scorer = DivergenceScorer()
