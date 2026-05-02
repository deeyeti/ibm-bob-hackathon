"""
Weather monitoring module for the Monitor Agent.

This module provides both traditional and BeeAI-based weather monitoring agents.
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
import asyncio
import os
import json

from src.services.weather_service import WeatherService
from src.models.schemas import WeatherData
from src.utils.logger import get_logger
from .config import MonitorConfig
from .vendors import vendor_manager, FreightVendor
from pydantic import BaseModel, Field

logger = get_logger(__name__)

# Import BeeAI framework
try:
    from bee_agent.agents.bee_agent import BeeAgent
    from bee_agent.tools.base import Tool, ToolResult
    BEEAI_AVAILABLE = True
except ImportError:
    # Fallback if BeeAI not installed
    BeeAgent = None
    Tool = None
    ToolResult = None
    BEEAI_AVAILABLE = False
    logger.warning("BeeAI framework not available. BeeAI features will be disabled.")


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

# ============================================================================
# BeeAI-Based Weather Monitor Agent
# ============================================================================


class WeatherCheckResponse(BaseModel):
    """Response model for weather check results."""
    status: str = Field(description="Status: 'clear' or 'reroute_required'")
    weather: Optional[str] = Field(default=None, description="Weather condition description")
    reason: Optional[str] = Field(default=None, description="Reason for reroute if required")
    alternative_vendors: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="List of alternative vendors if reroute required"
    )


def get_vendors() -> List[Dict[str, Any]]:
    """
    Get list of alternative freight vendors.
    
    Returns:
        List of vendor dictionaries with details
    """
    try:
        vendors = vendor_manager.get_eco_friendly_vendors(min_rating=4.5)
        return [
            {
                "id": v.id,
                "name": v.name,
                "location": v.location,
                "fleet_type": v.fleet_type.value,
                "fleet_size": v.fleet_size,
                "capacity_tons": v.capacity_tons,
                "eco_rating": v.eco_rating,
                "reliability_score": v.reliability_score,
                "cost_per_mile": v.cost_per_mile,
                "carbon_emissions_kg_per_mile": v.carbon_emissions_kg_per_mile,
                "service_areas": v.service_areas,
                "contact_email": v.contact_email,
                "contact_phone": v.contact_phone,
            }
            for v in vendors
        ]
    except Exception as e:
        logger.error(f"Error retrieving vendors: {e}")
        return []


class WeatherCheckTool(Tool if BEEAI_AVAILABLE else object):
    """Tool for checking current weather conditions."""
    
    def __init__(self, api_key: str):
        """
        Initialize weather check tool.
        
        Args:
            api_key: OpenWeather API key
        """
        self.api_key = api_key
        self.weather_service = WeatherService()
        if BEEAI_AVAILABLE:
            super().__init__(
                name="check_weather",
                description="Check current weather conditions for a location",
                input_schema={
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Location to check weather for (e.g., 'New York,US')"
                        }
                    },
                    "required": ["location"]
                }
            )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute weather check.
        
        Args:
            input_data: Tool input containing location
            
        Returns:
            Tool output with weather condition description
        """
        try:
            location = input_data.get("location", "")
            if not location:
                return {
                    "success": False,
                    "error": "Location parameter is required"
                }
            
            # Initialize weather service if needed
            if not hasattr(self.weather_service, 'client') or self.weather_service.client is None:
                await self.weather_service.initialize()
            
            # Get weather data
            weather_data = await self.weather_service.get_weather(location)
            
            return {
                "success": True,
                "data": {
                    "condition": weather_data.description,
                    "temperature": weather_data.temperature,
                    "wind_speed": weather_data.wind_speed,
                    "humidity": weather_data.humidity,
                }
            }
        except Exception as e:
            logger.error(f"Error checking weather: {e}")
            return {
                "success": False,
                "error": f"Failed to check weather: {str(e)}"
            }


class VendorRetrievalTool(Tool if BEEAI_AVAILABLE else object):
    """Tool for retrieving alternative freight vendors."""
    
    def __init__(self):
        """Initialize vendor retrieval tool."""
        if BEEAI_AVAILABLE:
            super().__init__(
                name="get_alternative_vendors",
                description="Get list of alternative freight vendors with eco-friendly fleets",
                input_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute vendor retrieval.
        
        Args:
            input_data: Tool input (no parameters required)
            
        Returns:
            Tool output with list of vendors
        """
        try:
            vendors = get_vendors()
            return {
                "success": True,
                "data": {"vendors": vendors}
            }
        except Exception as e:
            logger.error(f"Error retrieving vendors: {e}")
            return {
                "success": False,
                "error": f"Failed to retrieve vendors: {str(e)}"
            }


class BeeAIWeatherMonitorAgent:
    """
    BeeAI-based Weather Monitor Agent for detecting severe weather and recommending reroutes.
    
    This agent uses the BeeAI framework to:
    1. Check weather conditions for a target location
    2. Detect severe weather patterns
    3. Retrieve alternative vendors when rerouting is needed
    
    Environment Variables Required:
        - TARGET_LOCATION: Location to monitor (e.g., 'New York,US')
        - OPENWEATHER_API_KEY: OpenWeather API key
    """
    
    # Severe weather keywords
    SEVERE_KEYWORDS = [
        'storm', 'hurricane', 'tornado', 'blizzard', 'extreme',
        'severe', 'heavy', 'cyclone', 'typhoon', 'thunderstorm'
    ]
    
    def __init__(
        self,
        target_location: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Initialize BeeAI Weather Monitor Agent.
        
        Args:
            target_location: Location to monitor (defaults to TARGET_LOCATION env var)
            api_key: OpenWeather API key (defaults to OPENWEATHER_API_KEY env var)
        """
        self.target_location = target_location or os.getenv('TARGET_LOCATION', 'New York,US')
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY', '')
        
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY environment variable is required")
        
        # Initialize tools
        self.weather_tool = WeatherCheckTool(self.api_key)
        self.vendor_tool = VendorRetrievalTool()
        
        # Initialize BeeAI agent (only if available)
        if BEEAI_AVAILABLE:
            self.agent = BeeAgent(
                name="WeatherMonitorAgent",
                description="Monitor weather conditions and recommend reroutes for severe weather",
                tools=[self.weather_tool, self.vendor_tool],
                system_prompt=self._get_system_prompt(),
            )
        else:
            self.agent = None
        
        logger.info(f"BeeAI Weather Monitor Agent initialized for location: {self.target_location}")
    
    def _get_system_prompt(self) -> str:
        """
        Get system prompt for the agent.
        
        Returns:
            System prompt string
        """
        return f"""You are a weather monitoring agent for freight logistics.

Your task is to:
1. Check weather conditions for the target location: {self.target_location}
2. Determine if weather is severe (contains keywords: {', '.join(self.SEVERE_KEYWORDS)})
3. If severe weather detected:
   - Get alternative vendors
   - Return status 'reroute_required' with reason and vendor list
4. If weather is clear:
   - Return status 'clear' with weather description

Always use the available tools to gather information before making decisions.
Return responses in JSON format matching the WeatherCheckResponse schema."""
    
    def _is_severe_weather(self, weather_condition: str) -> bool:
        """
        Check if weather condition indicates severe weather.
        
        Args:
            weather_condition: Weather condition description
            
        Returns:
            True if severe weather detected
        """
        condition_lower = weather_condition.lower()
        return any(keyword in condition_lower for keyword in self.SEVERE_KEYWORDS)
    
    async def check_weather(self) -> WeatherCheckResponse:
        """
        Check weather and determine if rerouting is needed.
        
        Returns:
            WeatherCheckResponse with status and recommendations
        """
        try:
            # Check weather using tool
            weather_result = await self.weather_tool.execute(
                {"location": self.target_location}
            )
            
            if not weather_result.get("success"):
                error_msg = weather_result.get("error", "Unknown error")
                logger.error(f"Weather check failed: {error_msg}")
                return WeatherCheckResponse(
                    status="error",
                    reason=f"Failed to check weather: {error_msg}"
                )
            
            weather_data = weather_result.get("data", {})
            weather_condition = weather_data.get("condition", "")
            
            # Check if severe weather
            if self._is_severe_weather(weather_condition):
                logger.warning(f"Severe weather detected: {weather_condition}")
                
                # Get alternative vendors
                vendor_result = await self.vendor_tool.execute({})
                
                if vendor_result.get("success"):
                    vendor_data = vendor_result.get("data", {})
                    vendors = vendor_data.get("vendors", [])
                    return WeatherCheckResponse(
                        status="reroute_required",
                        reason=weather_condition,
                        alternative_vendors=vendors
                    )
                else:
                    error_msg = vendor_result.get("error", "Unknown error")
                    logger.error(f"Failed to retrieve vendors: {error_msg}")
                    return WeatherCheckResponse(
                        status="reroute_required",
                        reason=weather_condition,
                        alternative_vendors=[]
                    )
            else:
                logger.info(f"Clear weather conditions: {weather_condition}")
                return WeatherCheckResponse(
                    status="clear",
                    weather=weather_condition
                )
                
        except Exception as e:
            logger.error(f"Error in weather check: {e}", exc_info=True)
            return WeatherCheckResponse(
                status="error",
                reason=f"Error checking weather: {str(e)}"
            )
    
    async def run(self) -> Dict[str, Any]:
        """
        Run the agent to check weather and provide recommendations.
        
        Returns:
            Dictionary with agent response
        """
        try:
            response = await self.check_weather()
            return response.model_dump()
        except Exception as e:
            logger.error(f"Error running agent: {e}", exc_info=True)
            return {
                "status": "error",
                "reason": f"Agent execution failed: {str(e)}"
            }
    
    async def close(self) -> None:
        """Close agent and cleanup resources."""
        if hasattr(self.weather_tool.weather_service, 'close'):
            await self.weather_tool.weather_service.close()
        logger.info("BeeAI Weather Monitor Agent closed")


# ============================================================================
# Helper Functions
# ============================================================================


async def create_beeai_weather_agent(
    target_location: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Optional[BeeAIWeatherMonitorAgent]:
    """
    Create and initialize a BeeAI Weather Monitor Agent.
    
    Args:
        target_location: Location to monitor
        api_key: OpenWeather API key
        
    Returns:
        Initialized agent or None if BeeAI not available
    """
    try:
        agent = BeeAIWeatherMonitorAgent(
            target_location=target_location,
            api_key=api_key
        )
        return agent
    except Exception as e:
        logger.error(f"Failed to create BeeAI agent: {e}")
        return None


# Made with Bob