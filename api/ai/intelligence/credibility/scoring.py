from typing import List, Dict, Any, Tuple
from .weights import get_source_weight

class CredibilityScorer:
    def calculate_weighted_velocity(self, mentions: List[Dict[str, Any]], github_stars: int, reddit_score: int, reddit_comments: int) -> Tuple[float, float, str]:
        """
        Calculates credibility-weighted velocity, overall credibility score, and signal quality.
        Returns: (velocity, credibility_score, signal_quality)
        """
        if not mentions:
            return 0.0, 0.0, "Low"
            
        total_mentions = len(mentions)
        unique_sources = len(set(m["source"] for m in mentions))
        
        # 1. Base Credibility Calculation
        total_weight = 0.0
        source_weights = {}
        for m in mentions:
            w = get_source_weight(m["source"])
            total_weight += w
            source_weights[m["source"]] = w
            
        avg_credibility = total_weight / total_mentions
        
        # 2. Cross-Source Confirmation Bonus
        # Penalize if all volume comes from a single weak source
        confirmation_density = (sum(source_weights.values()) / len(source_weights)) if source_weights else 0.0
        
        # 3. Weighted Velocity Calculation
        # Instead of (mentions * 2) + (unique_sources * 5)
        # We aggressively scale by the actual credibility weight
        velocity = (total_weight * 2.5) + (sum(source_weights.values()) * 5.0)
        
        # Boosts using actual values
        if github_stars > 0:
            velocity += 20 * get_source_weight("GitHub Trending") + (github_stars // 1000)
            
        if reddit_comments > 0 or reddit_score > 0:
            velocity += 10 * get_source_weight("r/programming") + (reddit_comments // 10) + (reddit_score // 50)
            
        velocity = min(100.0, velocity)
        
        # 4. Final Credibility Score (0.0 to 100.0)
        # Combination of average mention credibility and unique source confirmation density
        cred_score = (avg_credibility * 0.4 + (min(unique_sources, 5) / 5.0) * 0.6) * 100
        cred_score = min(100.0, cred_score)
        
        # 5. Signal Quality Classification
        if cred_score >= 80.0 and unique_sources >= 2:
            signal_quality = "High"
        elif cred_score >= 50.0:
            signal_quality = "Medium"
        else:
            signal_quality = "Low"
            
        return velocity, cred_score, signal_quality

credibility_scorer = CredibilityScorer()
