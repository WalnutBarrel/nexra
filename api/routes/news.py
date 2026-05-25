from fastapi import APIRouter
from api.scrapers.pipeline.orchestrator import orchestrator
from api.ai.synthesizer import synthesizer
from api.ai.trends import trend_engine

router = APIRouter()

@router.get("/live")
async def list_live_news():
    """Returns the latest ingested intelligence enriched by AI."""
    raw_articles = orchestrator.get_latest_intelligence(limit=10)
    
    # If buffer is empty, we force an ingest to kickstart
    if not raw_articles:
        raw_articles = await orchestrator.ingest_live_feeds()
        
    enriched = synthesizer.synthesize_batch(raw_articles)
    return {"data": enriched}

@router.get("/trending")
async def get_trending_topics():
    """Returns the accelerating topics computed by the AI engine."""
    recent_articles = orchestrator.get_latest_intelligence(limit=30)
    
    if not recent_articles:
        recent_articles = await orchestrator.ingest_live_feeds()
        
    trends = trend_engine.compute_trends(recent_articles)
    return {"data": trends}
