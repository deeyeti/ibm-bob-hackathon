"""
Weather monitoring module for the Monitor Agent.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio

from src.services.weather_service import WeatherService
from src.models.schemas import WeatherData
from src.utils.logger import get_logger
from .config import MonitorConfig

logger = get_logger(__name__)


class WeatherAlert(Dict[str, Any]):
    """Weather alert data structure."""
    
    def __init__(
        self,
        location: str,
        severity: str,
        alert_type: str,
        message: str,
        weather_data: WeatherData,
        timestamp: Optional[datetime] = None,
    ):
        """Initialize weather alert."""
        super().__init__(
            location=location,
            severity=severity,
            alert_type=alert_type,
            message=message,
            weather_data=weather_data.dict(),
            timestamp=timestamp or datetime.utcnow(),
        )


class WeatherMonitor:
    """Weather monitoring service for detecting severe weather conditions."""

    def __init__(self, config: Optional[MonitorConfig] = None):
        """
        Initialize weather monitor.
        
        Args:
            config: Monitor configuration (uses default if not provided)
        """
        self.config = config or MonitorConfig()
        self.weather_service = WeatherService()
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._alert_history: Dict[str, datetime] = {}
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize weather service."""
        if not self._initialized:
            await self.weather_service.initialize()
            self._initialized = True
            logger.info("Weather monitor initialized")

    async def close(self) -> None:
        """Close weather service and cleanup."""
        await self.weather_service.close()
        self._initialized = False
        logger.info("Weather monitor closed")

    def _is_cached(self, location: str) -> bool:
        """
        Check if weather data is cached and still valid.
        
        Args:
            location: Location to check
            
        Returns:
            True if cached data is valid
        """
        if location not in self._cache:
            return False
        
        cache_entry = self._cache[location]
        cache_time = cache_entry.get("timestamp")
        
        if not cache_time:
            return False
        
        age = (datetime.utcnow() - cache_time).total_seconds()
        return age < self.config.cache_duration

    def _get_cached_data(self, location: str) -> Optional[WeatherData]:
        """
        Get cached weather data.
        
        Args:
            location: Location to get data for
            
        Returns:
            Cached weather data or None
        """
        if self._is_cached(location):
            return self._cache[location]["data"]
        return None

    def _cache_data(self, location: str, data: WeatherData) -> None:
        """
        Cache weather data.
        
        Args:
            location: Location to cache data for
            data: Weather data to cache
        """
        self._cache[location] = {
            "data": data,
            "timestamp": datetime.utcnow(),
        }

    def _is_severe_weather(self, weather_data: WeatherData) -> tuple[bool, List[str]]:
        """
        Check if weather conditions are severe.
        
        Args:
            weather_data: Weather data to check
            
        Returns:
            Tuple of (is_severe, list of reasons)
        """
        reasons = []
        
        # Check wind speed
        if weather_data.wind_speed >= self.config.severe_wind_speed_threshold:
            reasons.append(
                f"High wind speed: {weather_data.wind_speed:.1f} m/s "
                f"(threshold: {self.config.severe_wind_speed_threshold} m/s)"
            )
        
        # Check temperature extremes
        if weather_data.temperature <= self.config.extreme_temperature_low:
            reasons.append(
                f"Extreme low temperature: {weather_data.temperature:.1f}°C "
                f"(threshold: {self.config.extreme_temperature_low}°C)"
            )
        elif weather_data.temperature >= self.config.extreme_temperature_high:
            reasons.append(
                f"Extreme high temperature: {weather_data.temperature:.1f}°C "
                f"(threshold: {self.config.extreme_temperature_high}°C)"
            )
        
        # Check humidity
        if weather_data.humidity >= self.config.severe_humidity_threshold:
            reasons.append(
                f"High humidity: {weather_data.humidity:.1f}% "
                f"(threshold: {self.config.severe_humidity_threshold}%)"
            )
        
        # Check weather description for severe keywords
        description_lower = weather_data.description.lower()
        for keyword in self.config.severe_weather_keywords:
            if keyword in description_lower:
                reasons.append(f"Severe weather condition detected: {weather_data.description}")
                break
        
        return len(reasons) > 0, reasons

    def _can_send_alert(self, location: str) -> bool:
        """
        Check if an alert can be sent for a location (respects cooldown).
        
        Args:
            location: Location to check
            
        Returns:
            True if alert can be sent
        """
        if location not in self._alert_history:
            return True
        
        last_alert = self._alert_history[location]
        time_since_alert = (datetime.utcnow() - last_alert).total_seconds()
        
        return time_since_alert >= self.config.alert_cooldown

    def _record_alert(self, location: str) -> None:
        """
        Record that an alert was sent for a location.
        
        Args:
            location: Location to record alert for
        """
        self._alert_history[location] = datetime.utcnow()

    async def check_location(self, location: str) -> Optional[WeatherAlert]:
        """
        Check weather conditions for a single location.
        
        Args:
            location: Location to check
            
        Returns:
            WeatherAlert if severe weather detected, None otherwise
        """
        try:
            # Check cache first
            cached_data = self._get_cached_data(location)
            if cached_data:
                weather_data = cached_data
                logger.debug(f"Using cached weather data for {location}")
            else:
                # Fetch fresh data
                weather_data = await self.weather_service.get_weather(location)
                self._cache_data(location, weather_data)
                logger.info(f"Fetched weather data for {location}")
            
            # Check for severe weather
            is_severe, reasons = self._is_severe_weather(weather_data)
            
            if is_severe:
                # Check if we can send an alert (cooldown)
                if not self._can_send_alert(location):
                    logger.debug(
                        f"Severe weather detected at {location} but alert is in cooldown"
                    )
                    return None
                
                # Create alert
                alert = WeatherAlert(
                    location=location,
                    severity="high" if len(reasons) > 2 else "medium",
                    alert_type="severe_weather",
                    message=f"Severe weather detected at {location}: {'; '.join(reasons)}",
                    weather_data=weather_data,
                )
                
                self._record_alert(location)
                logger.warning(f"Severe weather alert for {location}: {reasons}")
                
                return alert
            
            logger.debug(f"Normal weather conditions at {location}")
            return None
            
        except Exception as e:
            logger.error(f"Error checking weather for {location}: {e}")
            return None

    async def check_all_locations(
        self,
        locations: Optional[List[str]] = None,
    ) -> List[WeatherAlert]:
        """
        Check weather conditions for multiple locations.
        
        Args:
            locations: List of locations to check (uses config default if not provided)
            
        Returns:
            List of weather alerts for locations with severe weather
        """
        if not self._initialized:
            await self.initialize()
        
        locations = locations or self.config.monitored_locations
        alerts = []
        
        # Check locations with rate limiting
        for location in locations:
            alert = await self.check_location(location)
            if alert:
                alerts.append(alert)
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(0.5)
        
        if alerts:
            logger.info(f"Found {len(alerts)} severe weather alerts")
        else:
            logger.info("No severe weather detected at monitored locations")
        
        return alerts

    async def get_location_forecast(
        self,
        location: str,
        days: int = 3,
    ) -> Dict[str, Any]:
        """
        Get weather forecast for a location.
        
        Args:
            location: Location to get forecast for
            days: Number of days for forecast
            
        Returns:
            Forecast data
        """
        try:
            if not self._initialized:
                await self.initialize()
            
            forecast = await self.weather_service.get_forecast(location, days=days)
            logger.info(f"Retrieved {days}-day forecast for {location}")
            return forecast
            
        except Exception as e:
            logger.error(f"Error getting forecast for {location}: {e}")
            raise

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        valid_entries = sum(1 for loc in self._cache if self._is_cached(loc))
        
        return {
            "total_entries": len(self._cache),
            "valid_entries": valid_entries,
            "expired_entries": len(self._cache) - valid_entries,
            "cache_duration_seconds": self.config.cache_duration,
        }

    def clear_cache(self) -> None:
        """Clear the weather data cache."""
        self._cache.clear()
        logger.info("Weather data cache cleared")

    def clear_alert_history(self) -> None:
        """Clear the alert history."""
        self._alert_history.clear()
        logger.info("Alert history cleared")

    def get_alert_history(self) -> Dict[str, str]:
        """
        Get alert history.
        
        Returns:
            Dictionary mapping locations to last alert timestamps
        """
        return {
            location: timestamp.isoformat()
            for location, timestamp in self._alert_history.items()
        }


# Made with Bob