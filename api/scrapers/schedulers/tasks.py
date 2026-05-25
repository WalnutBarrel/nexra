from apscheduler.schedulers.asyncio import AsyncIOScheduler
from api.scrapers.processors.pipeline import ingestion_pipeline

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('interval', minutes=15)
async def periodic_ingestion_job():
    """Trigger the ingestion pipeline every 15 minutes."""
    await ingestion_pipeline.run_pipeline()

@scheduler.scheduled_job('interval', hours=6)
async def cleanup_stale_data_job():
    """Cleanup old failed scrape logs and stale trending data."""
    # Logic to clean DB
    pass

@scheduler.scheduled_job('interval', hours=1)
async def recalculate_trending_topics_job():
    """Recalculate topic activity scores."""
    # Logic to aggregate search metrics and news frequency
    pass
