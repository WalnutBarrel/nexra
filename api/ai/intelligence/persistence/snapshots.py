from typing import List, Dict, Any
from api.models.entity_snapshot import EntitySnapshot
import logging

logger = logging.getLogger(__name__)

class SnapshotPersistence:
    def prepare_snapshots(self, entities: List[Dict[str, Any]]) -> List[EntitySnapshot]:
        """Converts raw entity dictionaries into SQLAlchemy EntitySnapshot objects."""
        logger.info(f"Preparing {len(entities)} entity snapshots for persistence.")
        snapshots = []
        for e in entities:
            try:
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
                
                snapshots.append(snapshot)
            except Exception as exc:
                logger.error(f"Failed to prepare snapshot for entity {e.get('name')}: {exc}")
        return snapshots

snapshot_persistence = SnapshotPersistence()
