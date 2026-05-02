"""
Eco-Shift Backend - Main FastAPI Application

AI-powered carbon emissions monitoring and optimization system.
"""

from datetime import datetime
from typing import Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.config import settings
from src.models import HealthResponse, ErrorResponse
from src.utils.logger import get_logger
from src.api import api_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    
    # Initialize services here
    # await initialize_watsonx_service()
    # await initialize_agents()
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    # Cleanup resources here
    # await cleanup_agents()


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered carbon emissions monitoring and optimization system",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"] if settings.cors_allow_methods == "*" else settings.cors_allow_methods.split(","),
    allow_headers=["*"] if settings.cors_allow_headers == "*" else settings.cors_allow_headers.split(","),
)


# Exception Handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle HTTP exceptions."""
    logger.error(f"HTTP error: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="HTTPException",
            message=str(exc.detail),
            timestamp=datetime.utcnow(),
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors."""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error="ValidationError",
            message="Request validation failed",
            detail=str(exc.errors()),
            timestamp=datetime.utcnow(),
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions."""
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred",
            detail=str(exc) if settings.debug else None,
            timestamp=datetime.utcnow(),
        ).model_dump(),
    )


# Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    start_time = datetime.utcnow()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = (datetime.utcnow() - start_time).total_seconds()
    
    # Log response
    logger.info(
        f"Response: {request.method} {request.url.path} - "
        f"Status: {response.status_code} - Duration: {duration:.3f}s"
    )
    
    return response


# Root Endpoints
@app.get("/", tags=["Root"])
async def root() -> Dict[str, Any]:
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "docs": "/docs" if settings.debug else "Documentation disabled in production",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow(),
    )


@app.get("/info", tags=["Info"])
async def info() -> Dict[str, Any]:
    """Get application information and configuration."""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug,
        "features": {
            "weather_integration": settings.enable_weather_integration,
            "vendor_recommendations": settings.enable_vendor_recommendations,
            "emissions_tracking": settings.enable_emissions_tracking,
            "real_time_monitoring": settings.enable_real_time_monitoring,
        },
        "agents": {
            "monitor": settings.agent_monitor_enabled,
            "auditor": settings.agent_auditor_enabled,
            "orchestrator": settings.agent_orchestrator_enabled,
        },
    }


# Include API routers
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )

# Made with Bob
