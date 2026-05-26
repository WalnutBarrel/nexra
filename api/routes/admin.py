from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class AdminMetricsResponse(BaseModel):
    total_users: int
    total_searches: int
    active_scrapers: int
    system_health: str

@router.get("/metrics", response_model=AdminMetricsResponse)
async def get_admin_metrics():
    return AdminMetricsResponse(
        total_users=1204,
        total_searches=45201,
        active_scrapers=8,
        system_health="optimal"
    )

@router.post("/debug/persist-test")
async def manual_persist_test():
    """Manually test the PostgreSQL persistence pipeline."""
    from api.ai.intelligence.persistence.commits import persistence_committer
    import logging
    
    logger = logging.getLogger(__name__)
    logger.info("Executing manual persistence debug test...")
    
    test_entities = [
        {
            "name": "Cursor",
            "category": "ide",
            "mentions": 145,
            "sources": 5,
            "velocity": 88,
            "github_stars": 34000,
            "discussion_intensity": 450,
            "lifecycle_state": "Accelerating",
            "dominant_sentiment": "excitement"
        }
    ]
    
    test_relationships = [
        {
            "entity_a": "cursor",
            "relationship_type": "integrates_with",
            "entity_b": "claude",
            "confidence_score": 0.95
        }
    ]
    
    try:
        success = await persistence_committer.commit_intelligence(test_entities, test_relationships)
        if success:
            return {"status": "success", "message": "Persistence test completed successfully. Check PostgreSQL tables."}
        else:
            return {"status": "failed", "message": "Persistence test returned false."}
    except Exception as e:
        logger.error(f"Manual persistence test failed: {e}")
        return {"status": "error", "message": str(e)}
