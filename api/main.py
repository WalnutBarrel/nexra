from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.core.config import settings

from contextlib import asynccontextmanager

from api.routes import health, search, admin, news, websites, analytics, ai, auth
from api.scrapers.schedulers.tasks import scheduler

from api.core.exceptions import (
    RateLimitExceeded, UpstreamServiceUnavailable,
    rate_limit_handler, upstream_failure_handler, global_exception_handler
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Initialize the database tables on boot
    from api.database.session import engine
    from api.database.base import Base
    # Import all models so Base knows about them before create_all
    from api.models.intelligence import NewsArticle, WebsiteReport, TrendingTopic
    from api.models.entity_snapshot import EntitySnapshot
    from api.models.relationship import EntityRelationship
    
    import logging
    logger = logging.getLogger(__name__)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables verified.")
        
    logger.info("Scheduler initialized.")
    scheduler.start()
    logger.info("Snapshot persistence job registered.")
    
    # 7. Force Snapshot Execution On Startup
    from api.scrapers.schedulers.tasks import snapshot_persistence_job
    import asyncio
    logger.info("Executing snapshot persistence job on startup...")
    asyncio.create_task(snapshot_persistence_job())
    
    yield
    # Shutdown
    scheduler.shutdown()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
app.add_exception_handler(UpstreamServiceUnavailable, upstream_failure_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(search.router, prefix=f"{settings.API_V1_STR}/search", tags=["Search"])
app.include_router(news.router, prefix=f"{settings.API_V1_STR}/news", tags=["Intelligence"])
app.include_router(websites.router, prefix=f"{settings.API_V1_STR}/websites", tags=["Intelligence"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["Analytics"])
app.include_router(ai.router, prefix=f"{settings.API_V1_STR}/ai", tags=["AI"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "Nexra Intelligence API is running"}
