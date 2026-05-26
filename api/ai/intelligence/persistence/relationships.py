from typing import List, Dict, Any
from api.models.relationship import EntityRelationship
from api.ai.intelligence.relationships.scoring import relationship_scorer
import logging

logger = logging.getLogger(__name__)

class RelationshipPersistence:
    def prepare_relationships(self, relationships: List[Dict[str, Any]]) -> List[EntityRelationship]:
        """Groups and filters relationships, converting them to SQLAlchemy models."""
        if not relationships:
            return []
            
        logger.info(f"Preparing {len(relationships)} raw relationships for persistence.")
        db_rels = []
        try:
            grouped = {}
            for r in relationships:
                pair = tuple(sorted([r["entity_a"], r["entity_b"]]))
                if pair not in grouped:
                    grouped[pair] = []
                grouped[pair].append(r)
                
            for pair, rels in grouped.items():
                conf = relationship_scorer.calculate_confidence(rels)
                if conf >= 0.5:
                    primary_rel = rels[0]
                    db_rel = EntityRelationship(
                        entity_a=primary_rel["entity_a"],
                        relationship_type=primary_rel["relationship_type"],
                        entity_b=primary_rel["entity_b"],
                        confidence_score=conf,
                        source_count=len(rels)
                    )
                    db_rels.append(db_rel)
            logger.info(f"Prepared {len(db_rels)} high-confidence relationships.")
        except Exception as exc:
            logger.error(f"Failed to prepare relationships: {exc}")
            
        return db_rels

relationship_persistence = RelationshipPersistence()
