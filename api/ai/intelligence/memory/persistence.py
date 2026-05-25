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
    async def save_snapshots(self, entities: List[Dict[str, Any]]) -> None:
        """Saves current state of entities from the hot cache to PostgreSQL."""
        try:
            async for session in get_db():
                for e in entities:
                    snapshot = EntitySnapshot(
                        entity_name=e["name"],
                        mention_count=e["mentions"],
                        source_diversity=e["sources"],
                        github_stars=e.get("github_stars", 0),
                        reddit_discussion_intensity=e.get("discussion_intensity", 0),
                        velocity_score=e["velocity"]
                    )
                    
                    # Compute sentiment score mapping if needed
                    sentiment_str = e.get("dominant_sentiment")
                    score_map = {"excitement": 1.0, "adoption": 0.8, "neutral": 0.0, "skepticism": -0.5, "frustration": -1.0}
                    snapshot.sentiment_score = score_map.get(sentiment_str, 0.0) if sentiment_str else 0.0
                    
                    # Generate lifecycle state before saving
                    # We need history to calculate lifecycle accurately, but we can do a lightweight version
                    # In a robust system, we would query history first. For now, we save raw metrics.
                    session.add(snapshot)
                
                await session.commit()
                break # Only need one session
        except Exception as e:
            logger.error(f"Failed to persist snapshots: {e}")

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
