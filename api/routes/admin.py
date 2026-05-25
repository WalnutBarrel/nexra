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
