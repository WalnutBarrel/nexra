from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from api.infrastructure.logger import get_logger

logger = get_logger("exception_handler")

class RateLimitExceeded(Exception):
    pass

class UpstreamServiceUnavailable(Exception):
    pass

async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    logger.warning("Rate limit exceeded", path=request.url.path, ip=request.client.host)
    return JSONResponse(
        status_code=429,
        content={"message": "Too many requests. Please slow down.", "retry_after": 60}
    )

async def upstream_failure_handler(request: Request, exc: UpstreamServiceUnavailable):
    logger.error("Upstream service failed", path=request.url.path, details=str(exc))
    return JSONResponse(
        status_code=502,
        content={"message": "Degraded state: An upstream dependency failed. Retrying in background queues."}
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.fatal("Unhandled exception caught", path=request.url.path, error=str(exc))
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error. Trace ID generated and logged."}
    )
