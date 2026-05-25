from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import re
from api.ai.trends import trend_engine
from api.scrapers.pipeline.orchestrator import orchestrator
from api.ai.synthesizer import synthesizer
from api.website_scanner.reports.compiler import dossier_compiler

router = APIRouter()

class SearchResponse(BaseModel):
    query: str
    status: str
    results_count: int
    news_results: List[dict]
    website_results: List[dict]
    intent: str

def classify_intent(query: str) -> str:
    """Classifies the user query intent to route to the correct intelligence pipeline."""
    q_lower = query.lower()
    
    # Domain Intent (detect common TLDs or protocols)
    domain_pattern = r'([a-zA-Z0-9-]+\.(com|io|ai|dev|org|net|co|app))|^(https?://)'
    if re.search(domain_pattern, q_lower):
        return "DOMAIN_SCAN"
        
    # Trend Intent
    if "trend" in q_lower or "accelerat" in q_lower or "emerg" in q_lower:
        return "TREND_ANALYSIS"
        
    return "NEWS_INTELLIGENCE"

@router.get("/", response_model=SearchResponse)
async def perform_search(q: str):
    intent = classify_intent(q)
    news = []
    websites = []
    
    # 1. DOMAIN SCAN INTENT
    if intent == "DOMAIN_SCAN":
        # Extract just the domain if they passed a URL
        domain_match = re.search(r'([a-zA-Z0-9-]+\.[a-zA-Z0-9-]+)', q.lower())
        domain = domain_match.group(1) if domain_match else q.lower()
        
        # Trigger the Website Scanner Pipeline
        dossier = await dossier_compiler.compile_report(domain)
        websites.append(dossier)
        
        # Append highly contextual news specifically about the domain
        raw_news = orchestrator.get_latest_intelligence(limit=10)
        enriched = synthesizer.synthesize_batch(raw_news)
        
        # Simple fuzzy match for domain keywords (e.g. 'github' in 'github.com')
        base_name = domain.split('.')[0]
        for item in enriched:
            if base_name in item.get("title", "").lower() or base_name in item.get("summary", "").lower():
                news.append(item)
            
    # 2. TREND ANALYSIS INTENT
    elif intent == "TREND_ANALYSIS":
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
            
    # 3. STANDARD NEWS INTELLIGENCE INTENT
    else:
        raw_news = orchestrator.get_latest_intelligence(limit=10)
        if not raw_news:
            raw_news = await orchestrator.ingest_live_feeds()
        enriched = synthesizer.synthesize_batch(raw_news)
        
        q_lower = q.lower()
        for item in enriched:
            if q_lower in item.get("title", "").lower() or q_lower in item.get("summary", "").lower():
                news.append(item)
                
        if not news:
            news = enriched[:4]
            
    return SearchResponse(
        query=q,
        status="completed",
        results_count=len(news) + len(websites),
        news_results=news,
        website_results=websites,
        intent=intent
    )
