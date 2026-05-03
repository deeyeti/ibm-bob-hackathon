"""API routes for Eco-Shift backend."""

from fastapi import APIRouter
from .agents import router as agents_router
from .weather import router as weather_router
from .emissions import router as emissions_router
from .vendors import router as vendors_router
from .orchestrator import router as orchestrator_router
from .chat import router as chat_router

# Create main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(agents_router, prefix="/agents", tags=["Agents"])
api_router.include_router(weather_router, prefix="/weather", tags=["Weather"])
api_router.include_router(emissions_router, prefix="/emissions", tags=["Emissions"])
api_router.include_router(vendors_router, prefix="/vendors", tags=["Vendors"])
api_router.include_router(orchestrator_router, tags=["Orchestrator"])
api_router.include_router(chat_router, prefix="/chat", tags=["Chat"])

__all__ = ["api_router"]

# Made with Bob
