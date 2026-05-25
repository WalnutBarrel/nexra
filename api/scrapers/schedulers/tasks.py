from apscheduler.schedulers.asyncio import AsyncIOScheduler
from api.scrapers.pipeline.orchestrator import orchestrator
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

@scheduler.scheduled_job('interval', hours=6)
async def cleanup_stale_data_job():
    """Cleanup old failed scrape logs and stale trending data."""
    pass
