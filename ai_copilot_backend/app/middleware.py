"""
Custom Middleware

HTTP middleware for logging, error handling, and request processing.
"""

import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    """
    Middleware to log all incoming HTTP requests.
    
    Logs request method, path, processing time, and response status.
    
    Args:
        request: The incoming HTTP request
        call_next: Function to call the next middleware/endpoint
    
    Returns:
        Response from the endpoint
    """
    start_time = time.time()
    
    # Log incoming request
    logger.info(f"→ {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    logger.info(
        f"← {request.method} {request.url.path} "
        f"[{response.status_code}] {process_time:.3f}s"
    )
    
    # Add processing time to response headers
    response.headers["X-Process-Time"] = str(process_time)
    
    return response
