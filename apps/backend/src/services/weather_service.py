"""
OpenWeather API service integration.
"""

from typing import Optional, Dict, Any
import httpx

from src.config import settings
from src.models import WeatherData
from src.utils.logger import get_logger

logger = get_logger(__name__)


class WeatherService:
    """Service for interacting with OpenWeather API."""

    def __init__(self):
        """Initialize weather service."""
        self.base_url = settings.openweather_base_url
        self.api_key = settings.openweather_api_key
        self.client: Optional[httpx.AsyncClient] = None

    async def initialize(self) -> None:
        """Initialize HTTP client."""
        if self.client is None:
            self.client = httpx.AsyncClient(timeout=30.0)
            logger.info("Weather service HTTP client initialized")

    async def get_weather(
        self,
        location: str,
        units: str = "metric",
    ) -> WeatherData:
        """
        Get current weather data for a location.

        Args:
            location: City name or coordinates (lat,lon)
            units: Units of measurement (metric/imperial)

        Returns:
            WeatherData object with current weather information
        """
        if self.client is None:
            await self.initialize()

        try:
            # Determine if location is coordinates or city name
            if "," in location and all(part.replace(".", "").replace("-", "").isdigit() 
                                      for part in location.split(",")):
                lat, lon = location.split(",")
                params = {
                    "lat": lat.strip(),
                    "lon": lon.strip(),
                    "appid": self.api_key,
                    "units": units,
                }
            else:
                params = {
                    "q": location,
                    "appid": self.api_key,
                    "units": units,
                }

            response = await self.client.get(f"{self.base_url}/weather", params=params)
            response.raise_for_status()
            data = response.json()

            # Parse response into WeatherData model
            weather_data = WeatherData(
                location=data.get("name", location),
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
                description=data["weather"][0]["description"],
            )

            logger.info(f"Weather data retrieved for {location}")
            return weather_data

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error getting weather data: {e.response.status_code}")
            raise
        except Exception as e:
            logger.error(f"Failed to get weather data: {e}")
            raise

    async def get_forecast(
        self,
        location: str,
        days: int = 5,
        units: str = "metric",
    ) -> Dict[str, Any]:
        """
        Get weather forecast for a location.

        Args:
            location: City name or coordinates
            days: Number of days for forecast (1-5)
            units: Units of measurement

        Returns:
            Dictionary with forecast data
        """
        if self.client is None:
            await self.initialize()

        try:
            # Determine if location is coordinates or city name
            if "," in location and all(part.replace(".", "").replace("-", "").isdigit() 
                                      for part in location.split(",")):
                lat, lon = location.split(",")
                params = {
                    "lat": lat.strip(),
                    "lon": lon.strip(),
                    "appid": self.api_key,
                    "units": units,
                    "cnt": days * 8,  # 8 forecasts per day (3-hour intervals)
                }
            else:
                params = {
                    "q": location,
                    "appid": self.api_key,
                    "units": units,
                    "cnt": days * 8,
                }

            response = await self.client.get(f"{self.base_url}/forecast", params=params)
            response.raise_for_status()
            data = response.json()

            logger.info(f"Weather forecast retrieved for {location}")
            return {
                "location": data["city"]["name"],
                "forecast": data["list"],
                "days": days,
            }

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error getting forecast: {e.response.status_code}")
            raise
        except Exception as e:
            logger.error(f"Failed to get forecast: {e}")
            raise

    async def get_air_quality(self, location: str) -> Dict[str, Any]:
        """
        Get air quality data for a location.

        Args:
            location: Coordinates as "lat,lon"

        Returns:
            Dictionary with air quality information
        """
        if self.client is None:
            await self.initialize()

        try:
            if "," not in location:
                raise ValueError("Air quality requires coordinates in format 'lat,lon'")

            lat, lon = location.split(",")
            params = {
                "lat": lat.strip(),
                "lon": lon.strip(),
                "appid": self.api_key,
            }

            response = await self.client.get(
                f"{self.base_url.replace('/data/2.5', '/data/2.5')}/air_pollution",
                params=params,
            )
            response.raise_for_status()
            data = response.json()

            logger.info(f"Air quality data retrieved for {location}")
            return {
                "location": location,
                "aqi": data["list"][0]["main"]["aqi"],
                "components": data["list"][0]["components"],
            }

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error getting air quality: {e.response.status_code}")
            raise
        except Exception as e:
            logger.error(f"Failed to get air quality: {e}")
            raise

    async def close(self) -> None:
        """Close HTTP client and cleanup resources."""
        if self.client:
            await self.client.aclose()
            logger.info("Weather service HTTP client closed")
            self.client = None


# Global service instance
weather_service = WeatherService()

# Made with Bob
