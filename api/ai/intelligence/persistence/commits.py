from typing import List, Dict, Any
from api.database.session import AsyncSessionLocal
from api.ai.intelligence.persistence.snapshots import snapshot_persistence
from api.ai.intelligence.persistence.relationships import relationship_persistence
import logging

logger = logging.getLogger(__name__)

class PersistenceCommitter:
    async def commit_intelligence(self, entities: List[Dict[str, Any]], relationships: List[Dict[str, Any]] = None) -> bool:
        """Explicitly handles the async session and commit lifecycle for the APScheduler background job."""
        
        # 1. Prepare ORM objects synchronously
        snapshots = snapshot_persistence.prepare_snapshots(entities)
        db_rels = relationship_persistence.prepare_relationships(relationships)
        
        if not snapshots:
            logger.warning("No snapshots to persist.")
            return False

        logger.info("Initiating PostgreSQL commit transaction...")
        
        # 2. Use manual AsyncSessionLocal instead of FastAPI Depends() injection
        async with AsyncSessionLocal() as session:
            try:
                for snap in snapshots:
                    session.add(snap)
                    
                for rel in db_rels:
                    session.add(rel)
                    
                await session.commit()
                logger.info(f"Successfully persisted {len(snapshots)} entity snapshots and {len(db_rels)} relationships.")
                return True
            except Exception as e:
                await session.rollback()
                logger.error(f"Snapshot persistence failed. Transaction rolled back. Reason: {e}")
                return False

persistence_committer = PersistenceCommitter()
