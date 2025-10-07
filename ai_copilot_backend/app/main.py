"""
Main FastAPI Application Entry Point

This module initializes the FastAPI application with all necessary
middleware, CORS configuration, and route handlers.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.middleware import log_requests
from app.api.routes import router as api_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    """
    logger.info("Starting AI Copilot Backend...")
    logger.info(f"Model: {settings.MODEL_NAME}")
    logger.info(f"Allowed Origins: {settings.ALLOWED_ORIGINS}")
    yield
    logger.info("Shutting down AI Copilot Backend...")


# Initialize FastAPI application
app = FastAPI(
    title="AI Copilot Backend",
    description="Backend API for AI Copilot chat application powered by Google Gemini",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check endpoints"
        },
        {
            "name": "sessions",
            "description": "Session management operations"
        },
        {
            "name": "chat",
            "description": "Chat and conversation endpoints"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.middleware("http")(log_requests)

# Include API routes
app.include_router(api_router)


# PUBLIC_INTERFACE
@app.get("/healthz", tags=["health"], summary="Health Check")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    
    Returns:
        dict: Status information including service name and version
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "ai-copilot-backend",
            "version": "1.0.0"
        }
    )


# PUBLIC_INTERFACE
@app.get("/", tags=["health"], summary="Root Endpoint")
async def root():
    """
    Root endpoint providing basic service information.
    
    Returns:
        dict: Welcome message and API documentation link
    """
    return {
        "message": "AI Copilot Backend API",
        "docs": "/docs",
        "health": "/healthz"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )
