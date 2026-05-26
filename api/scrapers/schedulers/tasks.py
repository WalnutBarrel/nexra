from apscheduler.schedulers.asyncio import AsyncIOScheduler
from api.scrapers.pipeline.orchestrator import orchestrator
from api.ai.intelligence.engine import entity_engine
from api.ai.intelligence.memory.persistence import persistence_layer
import logging

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('interval', minutes=5)
async def periodic_ingestion_job():
    """Trigger the live ingestion pipeline every 5 minutes."""
    try:
        new_items = await orchestrator.ingest_live_feeds()
        logger.info(f"Ingestion job complete: pulled {len(new_items)} new unique items.")
    except Exception as e:
        logger.error(f"Ingestion job failed: {e}")

@scheduler.scheduled_job('interval', hours=1)
async def snapshot_persistence_job():
    """Persist the current entity hot-cache to PostgreSQL every hour."""
    logger.info("Executing snapshot persistence job...")
    try:
        # get_ranked_entities without limit to get all active entities
        entities = await entity_engine.get_ranked_entities(limit=100)
        logger.info(f"Retrieved {len(entities)} entities from hot-cache for persistence.")
        relationships = entity_engine.relationship_memory
        logger.info(f"Retrieved {len(relationships)} raw relationships from hot-cache for persistence.")
        
        from api.ai.intelligence.persistence.commits import persistence_committer
        success = await persistence_committer.commit_intelligence(entities, relationships)
        if success:
            logger.info(f"Snapshot persistence job complete: saved {len(entities)} entities.")
        else:
            logger.warning("Snapshot persistence job returned false (no entities or error).")
    except Exception as e:
        logger.error(f"Snapshot persistence job failed: {e}")

@scheduler.scheduled_job('interval', hours=6)
async def cleanup_stale_data_job():
    """Cleanup old failed scrape logs and stale trending data."""
    pass
