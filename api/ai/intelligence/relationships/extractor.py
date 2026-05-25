from typing import List, Dict, Any

class RelationshipExtractor:
    def parse_gemini_relationships(self, raw_relationships: List[Dict[str, Any]], source: str, timestamp: float) -> List[Dict[str, Any]]:
        """Parses and normalizes relationships returned by Gemini."""
        parsed = []
        for rel in raw_relationships:
            parsed.append({
                "entity_a": rel.get("entity_a", "").strip().lower(),
                "relationship_type": rel.get("relationship", "associated_with").strip().lower(),
                "entity_b": rel.get("entity_b", "").strip().lower(),
                "source": source,
                "timestamp": timestamp,
                "confidence": 0.5 # Base confidence, will be adjusted by scoring
            })
        return parsed

relationship_extractor = RelationshipExtractor()
