"""External service integrations for Eco-Shift backend."""

from .watsonx_service import watsonx_service, WatsonxService
from .weather_service import weather_service, WeatherService

__all__ = [
    "watsonx_service",
    "WatsonxService",
    "weather_service",
    "WeatherService",
]

# Made with Bob
