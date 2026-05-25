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
    try:
        # get_ranked_entities without limit to get all active entities
        entities = entity_engine.get_ranked_entities(limit=100)
        await persistence_layer.save_snapshots(entities)
        logger.info(f"Snapshot persistence job complete: saved {len(entities)} entities.")
    except Exception as e:
        logger.error(f"Snapshot persistence job failed: {e}")

@scheduler.scheduled_job('interval', hours=6)
async def cleanup_stale_data_job():
    """Cleanup old failed scrape logs and stale trending data."""
    pass
