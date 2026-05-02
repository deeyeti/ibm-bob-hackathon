"""
Configuration for the Monitor Agent.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field


class MonitorConfig(BaseModel):
    """Configuration for the Monitor Agent."""

    # Polling Configuration
    polling_interval: int = Field(
        default=300,
        description="Weather polling interval in seconds (default: 5 minutes)",
    )
    
    # Severe Weather Thresholds
    severe_wind_speed_threshold: float = Field(
        default=22.35,  # 50 mph in m/s
        description="Wind speed threshold for severe weather in m/s",
    )
    severe_precipitation_threshold: float = Field(
        default=50.0,
        description="Precipitation threshold for severe weather in mm/hour",
    )
    extreme_temperature_low: float = Field(
        default=-10.0,
        description="Extreme low temperature threshold in Celsius",
    )
    extreme_temperature_high: float = Field(
        default=40.0,
        description="Extreme high temperature threshold in Celsius",
    )
    severe_humidity_threshold: float = Field(
        default=90.0,
        description="High humidity threshold percentage",
    )
    
    # Weather Condition Keywords for Severe Weather
    severe_weather_keywords: List[str] = Field(
        default=[
            "storm",
            "hurricane",
            "tornado",
            "blizzard",
            "heavy snow",
            "heavy rain",
            "thunderstorm",
            "severe",
            "extreme",
            "cyclone",
            "typhoon",
        ],
        description="Keywords indicating severe weather conditions",
    )
    
    # Monitored Locations (shipping hubs)
    monitored_locations: List[str] = Field(
        default=[
            "Los Angeles,US",
            "New York,US",
            "Chicago,US",
            "Houston,US",
            "Miami,US",
            "Seattle,US",
            "Atlanta,US",
            "Dallas,US",
            "Boston,US",
            "Denver,US",
        ],
        description="List of locations to monitor for weather conditions",
    )
    
    # Cache Configuration
    cache_duration: int = Field(
        default=180,
        description="Weather data cache duration in seconds (3 minutes)",
    )
    
    # API Rate Limiting
    max_api_calls_per_minute: int = Field(
        default=60,
        description="Maximum API calls per minute to avoid rate limits",
    )
    
    # Alert Configuration
    alert_cooldown: int = Field(
        default=1800,
        description="Cooldown period between alerts for same location in seconds (30 minutes)",
    )
    
    # Vendor Retrieval
    auto_retrieve_vendors: bool = Field(
        default=True,
        description="Automatically retrieve vendor list when severe weather detected",
    )
    prioritize_eco_friendly: bool = Field(
        default=True,
        description="Prioritize hydrogen and electric fleet vendors",
    )


# Default configuration instance
monitor_config = MonitorConfig()

# Made with Bob