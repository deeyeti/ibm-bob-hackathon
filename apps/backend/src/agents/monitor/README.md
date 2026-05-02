# Monitor Agent

The Monitor Agent is responsible for polling the OpenWeather API to detect severe weather conditions at shipping locations and retrieving alternative freight vendor lists when severe weather is detected.

## Overview

**Agent Type:** Monitor  
**Purpose:** Weather monitoring and vendor management  
**Location:** `apps/backend/src/agents/monitor/`

## Features

- ✅ Async weather polling every 5-10 minutes (configurable)
- ✅ Detect severe weather conditions (wind > 50 mph, heavy precipitation, etc.)
- ✅ Automatically pull vendor list when severe weather detected
- ✅ Prioritize hydrogen-fueled and electric fleet vendors
- ✅ Comprehensive logging and error handling
- ✅ API rate limiting and caching to reduce API calls
- ✅ Alert cooldown to prevent spam
- ✅ Support for multiple shipping locations

## Architecture

### Files

- **`monitor_agent.py`**: Main agent implementation extending `BaseAgent`
- **`weather_monitor.py`**: Weather monitoring logic and severe weather detection
- **`vendors.py`**: Freight vendor data management (15 vendors with diverse fleet types)
- **`config.py`**: Agent-specific configuration and thresholds
- **`__init__.py`**: Module exports

## Usage

### Basic Usage

```python
from src.agents.monitor import MonitorAgent

# Create agent instance
agent = MonitorAgent()

# Initialize agent
await agent.initialize()

# Start the agent
await agent.start()

# Execute one-time check
result = await agent.run()

# Stop the agent
await agent.stop()
```

### Continuous Polling

```python
# Start continuous polling (runs every 5 minutes by default)
await agent.start_polling()

# Stop polling
await agent.stop_polling()
```

### Check Specific Location

```python
# Check weather for a specific location
alert = await agent.check_location_weather("New York,US")

if alert:
    print(f"Severe weather detected: {alert['alert']}")
    print(f"Recommended vendors: {alert['vendors']}")
```

### Get Vendor Recommendations

```python
# Get all eco-friendly vendors
eco_vendors = agent.get_eco_friendly_vendors(min_rating=4.5)

# Get vendors for a specific location
vendors = agent.get_vendor_recommendations(location="Los Angeles,US")

# Get all available vendors
all_vendors = agent.get_all_vendors()
```

### Get Statistics

```python
# Get agent statistics
stats = agent.get_statistics()
print(f"Total alerts: {stats['total_alerts']}")
print(f"Locations monitored: {stats['locations_monitored']}")
print(f"Eco-friendly vendors: {stats['eco_friendly_vendors']}")
```

## Configuration

### Default Configuration

```python
from src.agents.monitor import MonitorConfig

config = MonitorConfig(
    polling_interval=300,  # 5 minutes
    severe_wind_speed_threshold=22.35,  # 50 mph in m/s
    severe_precipitation_threshold=50.0,  # mm/hour
    extreme_temperature_low=-10.0,  # Celsius
    extreme_temperature_high=40.0,  # Celsius
    cache_duration=180,  # 3 minutes
    alert_cooldown=1800,  # 30 minutes
    auto_retrieve_vendors=True,
    prioritize_eco_friendly=True,
)

# Create agent with custom config
agent = MonitorAgent(config=config)
```

### Monitored Locations

Default monitored locations (major US shipping hubs):
- Los Angeles, CA
- New York, NY
- Chicago, IL
- Houston, TX
- Miami, FL
- Seattle, WA
- Atlanta, GA
- Dallas, TX
- Boston, MA
- Denver, CO

## Severe Weather Thresholds

The agent detects severe weather based on:

1. **Wind Speed**: > 50 mph (22.35 m/s)
2. **Temperature Extremes**: < -10°C or > 40°C
3. **High Humidity**: > 90%
4. **Weather Keywords**: storm, hurricane, tornado, blizzard, heavy snow, heavy rain, thunderstorm, severe, extreme, cyclone, typhoon

## Vendor Fleet Types

The agent manages 15 freight vendors with the following fleet types:

- **Hydrogen** (6 vendors) - Zero emissions, highest eco-rating
- **Electric** (6 vendors) - Low emissions, renewable energy powered
- **Hybrid** (2 vendors) - Transitioning to full electric
- **Biodiesel** (1 vendor) - Sustainable fuel sources

### Vendor Prioritization

When severe weather is detected, vendors are prioritized by:
1. Fleet type (Hydrogen > Electric > Hybrid > Others)
2. Carbon emissions per mile (lowest first)
3. Eco rating (highest first)
4. Service area coverage

## Integration Points

### With Weather Service

```python
from src.services.weather_service import weather_service

# The agent uses the global weather service instance
# Weather data is cached to reduce API calls
```

### With Orchestrator

The agent emits events/messages to the orchestrator for downstream processing:

```python
# Execution result includes alerts and vendor recommendations
result = await agent.execute()

# Result structure:
{
    "status": "success",
    "timestamp": "2026-05-02T07:00:00Z",
    "alerts": [...],  # List of weather alerts
    "vendor_recommendations": {...},  # Vendors by location
    "metrics": {...}  # Agent metrics
}
```

## API Rate Limiting

The agent implements several strategies to avoid API rate limits:

1. **Caching**: Weather data is cached for 3 minutes (configurable)
2. **Delays**: 0.5 second delay between location checks
3. **Max Calls**: Configurable max API calls per minute (default: 60)
4. **Alert Cooldown**: 30-minute cooldown between alerts for same location

## Error Handling

The agent includes comprehensive error handling:

- HTTP errors from OpenWeather API
- Network timeouts
- Invalid location data
- Rate limit errors
- Graceful degradation on failures

## Logging

The agent logs:

- Initialization and cleanup events
- Weather checks and alerts
- Vendor retrievals
- Errors and warnings
- Performance metrics

## Metrics

The agent tracks:

- `monitored_locations`: Number of locations being monitored
- `polling_interval`: Current polling interval
- `total_vendors`: Total vendors available
- `eco_friendly_vendors`: Number of eco-friendly vendors
- `alerts_detected`: Alerts in current execution
- `total_alerts`: Total alerts since start
- `execution_time_seconds`: Time taken for execution
- `cache_stats`: Cache hit/miss statistics

## Example: Complete Workflow

```python
import asyncio
from src.agents.monitor import MonitorAgent

async def main():
    # Create and initialize agent
    agent = MonitorAgent()
    await agent.initialize()
    await agent.start()
    
    # Start continuous polling
    await agent.start_polling()
    
    # Let it run for a while
    await asyncio.sleep(600)  # 10 minutes
    
    # Get statistics
    stats = agent.get_statistics()
    print(f"Statistics: {stats}")
    
    # Get recent alerts
    alerts = agent.get_recent_alerts(limit=5)
    print(f"Recent alerts: {alerts}")
    
    # Stop and cleanup
    await agent.stop_polling()
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## Testing

```python
# Test weather monitoring
alert = await agent.check_location_weather("Miami,US")

# Test vendor retrieval
vendors = agent.get_eco_friendly_vendors()
assert len(vendors) > 0

# Test statistics
stats = agent.get_statistics()
assert stats['total_vendors_available'] == 15
```

## Future Enhancements

- [ ] Support for international locations
- [ ] Integration with additional weather APIs
- [ ] Machine learning for weather prediction
- [ ] Real-time vendor availability updates
- [ ] SMS/Email alerts for severe weather
- [ ] Historical weather data analysis
- [ ] Vendor performance tracking

## Made with Bob