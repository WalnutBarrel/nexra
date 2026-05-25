from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from api.ai.trends import trend_engine
from api.scrapers.pipeline.orchestrator import orchestrator
from api.ai.synthesizer import synthesizer

router = APIRouter()

class SearchResponse(BaseModel):
    query: str
    status: str
    results_count: int
    news_results: List[dict]
    website_results: List[dict]

@router.get("/", response_model=SearchResponse)
async def perform_search(q: str):
    q_lower = q.lower()
    news = []
    
    # 1. AI Query Enhancements (Trend Queries)
    if "trend" in q_lower or "accelerat" in q_lower or "emerg" in q_lower:
        recent = orchestrator.get_latest_intelligence(limit=30)
        if not recent:
            recent = await orchestrator.ingest_live_feeds()
            
        trends = trend_engine.compute_trends(recent)
        
        # Format trends as news cards for the UI
        for t in trends:
            news.append({
                "title": f"Trend Alert: {t['topic']}",
                "source": "Nexra AI Trend Synthesis",
                "timestamp": "Live",
                "summary": f"Our intelligence engine detects rapid acceleration in {t['topic']}. Cross-source velocity score is {t['score']}/100. Mention trajectory is trending {t['trend']}.",
                "sentiment": "neutral",
                "credibilityScore": 99,
                "tags": [t["category"], "Emerging Trend"]
            })
            
    # 2. Standard Intelligence Query
    else:
        raw_news = orchestrator.get_latest_intelligence(limit=10)
        if not raw_news:
            raw_news = await orchestrator.ingest_live_feeds()
        enriched = synthesizer.synthesize_batch(raw_news)
        
        # Basic filter for now
        for item in enriched:
            if q_lower in item.get("title", "").lower() or q_lower in item.get("summary", "").lower():
                news.append(item)
                
        # Fallback if no specific matches
        if not news:
            news = enriched[:3]
            
    return SearchResponse(
        query=q,
        status="completed",
        results_count=len(news),
        news_results=news,
        website_results=[]
    )
