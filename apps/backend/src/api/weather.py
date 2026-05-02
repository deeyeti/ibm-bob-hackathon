"""
API routes for weather data.
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Query, status

from src.services import weather_service
from src.models import WeatherData, WeatherRequest
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/current", response_model=WeatherData)
async def get_current_weather(
    location: str = Query(..., description="City name or coordinates (lat,lon)"),
    units: str = Query("metric", description="Units (metric/imperial)"),
) -> WeatherData:
    """
    Get current weather data for a location.
    
    Args:
        location: City name or coordinates
        units: Units of measurement
        
    Returns:
        Current weather data
    """
    try:
        weather_data = await weather_service.get_weather(location, units)
        return weather_data
    
    except Exception as e:
        logger.error(f"Failed to get weather data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve weather data",
        )


@router.post("/current", response_model=WeatherData)
async def get_current_weather_post(request: WeatherRequest) -> WeatherData:
    """
    Get current weather data for a location (POST method).
    
    Args:
        request: Weather request with location and units
        
    Returns:
        Current weather data
    """
    try:
        weather_data = await weather_service.get_weather(
            request.location,
            request.units,
        )
        return weather_data
    
    except Exception as e:
        logger.error(f"Failed to get weather data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve weather data",
        )


@router.get("/forecast", response_model=Dict[str, Any])
async def get_weather_forecast(
    location: str = Query(..., description="City name or coordinates"),
    days: int = Query(5, ge=1, le=5, description="Number of days (1-5)"),
    units: str = Query("metric", description="Units (metric/imperial)"),
) -> Dict[str, Any]:
    """
    Get weather forecast for a location.
    
    Args:
        location: City name or coordinates
        days: Number of days for forecast
        units: Units of measurement
        
    Returns:
        Weather forecast data
    """
    try:
        forecast = await weather_service.get_forecast(location, days, units)
        return forecast
    
    except Exception as e:
        logger.error(f"Failed to get weather forecast: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve weather forecast",
        )


@router.get("/air-quality", response_model=Dict[str, Any])
async def get_air_quality(
    location: str = Query(..., description="Coordinates as 'lat,lon'"),
) -> Dict[str, Any]:
    """
    Get air quality data for a location.
    
    Args:
        location: Coordinates in format 'lat,lon'
        
    Returns:
        Air quality data
    """
    try:
        air_quality = await weather_service.get_air_quality(location)
        return air_quality
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Failed to get air quality data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve air quality data",
        )

# Made with Bob
