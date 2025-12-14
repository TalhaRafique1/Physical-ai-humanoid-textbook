"""
Main FastAPI application for the textbook generation system.

This module initializes the FastAPI application and includes all API routes.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from typing import Dict, Any

from .routes import textbook_generation, export, preview
from .routes.rag import chatbot
from .routes.auth import auth
from .routes.translation import translation
from .routes.learning_tools import learning_tools
from ..config.database import settings


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Textbook Generation API",
        description="API for generating, customizing, and exporting textbooks",
        version="1.0.0",
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # Expose headers for client-side access
        expose_headers=["Access-Control-Allow-Origin"]
    )

    # Include API routes
    app.include_router(
        textbook_generation.router,
        prefix="/api/textbook-generation",
        tags=["textbook-generation"]
    )

    app.include_router(
        export.router,
        prefix="/api/export",
        tags=["export"]
    )

    app.include_router(
        preview.router,
        prefix="/api/preview",
        tags=["preview"]
    )

    app.include_router(
        chatbot.router,
        prefix="/api/rag",
        tags=["rag-chatbot"]
    )

    app.include_router(
        auth.router,
        prefix="/api/auth",
        tags=["authentication"]
    )

    app.include_router(
        translation.router,
        prefix="/api/translation",
        tags=["translation"]
    )

    app.include_router(
        learning_tools.router,
        prefix="/api/learning-tools",
        tags=["learning-tools"]
    )

    # Add middleware for request logging
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s")
        return response

    # Add health check endpoint
    @app.get("/health")
    async def health_check() -> Dict[str, Any]:
        return {
            "status": "healthy",
            "version": "1.0.0",
            "database_connected": not settings.debug  # Simplified check
        }

    # Add root endpoint
    @app.get("/")
    async def root() -> Dict[str, str]:
        return {
            "message": "Textbook Generation API",
            "version": "1.0.0",
            "docs": "/api/docs"
        }

    return app


# Create the main application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )