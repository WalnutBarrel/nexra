from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class SearchResponse(BaseModel):
    query: str
    status: str
    results_count: int
    news_results: List[dict]
    website_results: List[dict]

@router.get("/", response_model=SearchResponse)
async def perform_search(q: str):
    # Mocking response until DB is hooked up to service layer
    return SearchResponse(
        query=q,
        status="completed",
        results_count=2,
        news_results=[],
        website_results=[]
    )
