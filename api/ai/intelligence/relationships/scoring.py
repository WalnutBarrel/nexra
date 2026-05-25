from typing import Dict, Any, List

class RelationshipScorer:
    def calculate_confidence(self, rel_occurrences: List[Dict[str, Any]]) -> float:
        """Calculates confidence score based on recurrence and source diversity."""
        if not rel_occurrences:
            return 0.0
            
        sources = set(r["source"] for r in rel_occurrences)
        count = len(rel_occurrences)
        
        # Base confidence
        score = 0.5
        
        # Boost by count
        if count > 2:
            score += 0.2
        elif count > 5:
            score += 0.3
            
        # Boost by source diversity
        if len(sources) > 1:
            score += 0.2
            
        return min(1.0, score)

relationship_scorer = RelationshipScorer()
