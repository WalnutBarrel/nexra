from typing import Dict

# Deterministic credibility weights for known sources (0.0 to 1.0)
SOURCE_WEIGHTS: Dict[str, float] = {
    # High-tier Developer/Infrastructure (Gold Standard)
    "GitHub Trending": 1.0,
    "HackerNews": 0.95,
    "r/LocalLLaMA": 0.9,
    "r/MachineLearning": 0.9,
    "r/programming": 0.85,
    "r/webdev": 0.85,
    
    # Mid-tier Tech News & General Developer
    "r/opensource": 0.8,
    "r/artificial": 0.75,
    "TechCrunch": 0.6,
    "Bloomberg": 0.6,
    "Arxiv": 0.85,
    
    # Default fallback for unknown RSS feeds or generic scrapers
    "default": 0.3
}

def get_source_weight(source: str) -> float:
    """Returns the deterministic credibility weight for a given source."""
    # Match exact or partial if necessary
    for known_source, weight in SOURCE_WEIGHTS.items():
        if known_source.lower() in source.lower():
            return weight
    return SOURCE_WEIGHTS["default"]
