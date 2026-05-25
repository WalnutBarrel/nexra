from typing import Dict, Any, List
from datetime import datetime, timedelta
import logging
from sqlalchemy.future import select
from sqlalchemy import desc
from api.database.session import get_db
from api.models.entity_snapshot import EntitySnapshot
from api.ai.intelligence.memory.lifecycle import lifecycle_classifier
from api.ai.intelligence.memory.deltas import delta_calculator

logger = logging.getLogger(__name__)

class PersistenceLayer:
    async def save_snapshots(self, entities: List[Dict[str, Any]], relationships: List[Dict[str, Any]] = None) -> None:
        """Saves current state of entities and relationships from the hot cache to PostgreSQL."""
        from api.models.relationship import EntityRelationship
        try:
            async for session in get_db():
                # Persist Entities
                for e in entities:
                    snapshot = EntitySnapshot(
                        entity_name=e["name"],
                        mention_count=e["mentions"],
                        source_diversity=e["sources"],
                        github_stars=e.get("github_stars", 0),
                        reddit_discussion_intensity=e.get("discussion_intensity", 0),
                        velocity_score=e["velocity"],
                        lifecycle_state=e.get("lifecycle_state")
                    )
                    
                    sentiment_str = e.get("dominant_sentiment")
                    score_map = {"excitement": 1.0, "adoption": 0.8, "neutral": 0.0, "skepticism": -0.5, "frustration": -1.0}
                    snapshot.sentiment_score = score_map.get(sentiment_str, 0.0) if sentiment_str else 0.0
                    
                    session.add(snapshot)
                
                # Persist Relationships
                if relationships:
                    # Group by pairs to get confidence
                    from api.ai.intelligence.relationships.scoring import relationship_scorer
                    
                    grouped = {}
                    for r in relationships:
                        pair = tuple(sorted([r["entity_a"], r["entity_b"]]))
                        if pair not in grouped:
                            grouped[pair] = []
                        grouped[pair].append(r)
                        
                    for pair, rels in grouped.items():
                        conf = relationship_scorer.calculate_confidence(rels)
                        if conf >= 0.5:
                            # Save the highest confidence relationship direction
                            primary_rel = rels[0]
                            db_rel = EntityRelationship(
                                entity_a=primary_rel["entity_a"],
                                relationship_type=primary_rel["relationship_type"],
                                entity_b=primary_rel["entity_b"],
                                confidence_score=conf,
                                source_count=len(rels)
                            )
                            session.add(db_rel)

                await session.commit()
                break # Only need one session
        except Exception as e:
            logger.error(f"Failed to persist snapshots/relationships: {e}")

    async def get_historical_deltas(self, entity_name: str) -> Dict[str, Any]:
        """Calculates 24h and 7d deltas by querying recent snapshots."""
        try:
            async for session in get_db():
                # Get the most recent snapshot
                stmt_current = select(EntitySnapshot).where(EntitySnapshot.entity_name == entity_name).order_by(desc(EntitySnapshot.timestamp)).limit(1)
                res_current = await session.execute(stmt_current)
                current = res_current.scalar_one_or_none()
                
                if not current:
                    return {}
                
                now = current.timestamp
                
                # Get snapshot from roughly 24h ago
                stmt_24h = select(EntitySnapshot).where(
                    EntitySnapshot.entity_name == entity_name,
                    EntitySnapshot.timestamp <= now - timedelta(hours=23)
                ).order_by(desc(EntitySnapshot.timestamp)).limit(1)
                res_24h = await session.execute(stmt_24h)
                snap_24h = res_24h.scalar_one_or_none()
                
                # Get snapshot from roughly 7d ago
                stmt_7d = select(EntitySnapshot).where(
                    EntitySnapshot.entity_name == entity_name,
                    EntitySnapshot.timestamp <= now - timedelta(days=6)
                ).order_by(desc(EntitySnapshot.timestamp)).limit(1)
                res_7d = await session.execute(stmt_7d)
                snap_7d = res_7d.scalar_one_or_none()
                
                deltas = delta_calculator.calculate(current, snap_24h, snap_7d)
                lifecycle = lifecycle_classifier.classify(current, snap_24h, snap_7d)
                
                return {
                    "delta_24h": deltas.get("velocity_24h_pct", 0),
                    "delta_7d": deltas.get("velocity_7d_pct", 0),
                    "lifecycle_state": lifecycle
                }
        except Exception as e:
            logger.error(f"Failed to get deltas for {entity_name}: {e}")
            return {}

persistence_layer = PersistenceLayer()
