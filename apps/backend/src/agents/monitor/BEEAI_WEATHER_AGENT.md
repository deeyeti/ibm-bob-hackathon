# BeeAI Weather Monitor Agent

## Overview

The BeeAI Weather Monitor Agent is an AI-powered agent that monitors weather conditions and recommends freight rerouting when severe weather is detected. It uses the BeeAI framework to coordinate between weather checking and vendor retrieval tools.

## Features

- **Real-time Weather Monitoring**: Checks current weather conditions using OpenWeather API
- **Severe Weather Detection**: Identifies dangerous weather patterns (storms, hurricanes, extreme conditions)
- **Automatic Vendor Retrieval**: Gets eco-friendly alternative vendors when rerouting is needed
- **Structured Responses**: Returns JSON responses with clear status and recommendations

## Installation

### 1. Install BeeAI Framework

```bash
# From the backend directory
cd apps/backend

# Install BeeAI framework
pip install bee-agent-framework

# Or add to pyproject.toml dependencies
```

### 2. Set Environment Variables

Create or update your `.env` file:

```bash
# Required
OPENWEATHER_API_KEY=your_openweather_api_key_here
TARGET_LOCATION=New York,US

# Optional (has defaults)
LOG_LEVEL=INFO
```

### 3. Verify Installation

```python
from src.agents.monitor.weather_monitor import BEEAI_AVAILABLE

if BEEAI_AVAILABLE:
    print("BeeAI framework is installed and ready!")
else:
    print("BeeAI framework not found. Please install it.")
```

## Architecture

### Components

1. **BeeAIWeatherMonitorAgent**: Main agent class that coordinates weather monitoring
2. **WeatherCheckTool**: Tool for checking current weather conditions
3. **VendorRetrievalTool**: Tool for retrieving alternative freight vendors
4. **WeatherCheckResponse**: Pydantic model for structured responses

### Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                  BeeAI Weather Monitor Agent                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Check Weather   │
                    │ (WeatherCheckTool)│
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Is Severe?      │
                    └─────────────────┘
                         │         │
                    Yes  │         │  No
                         ▼         ▼
              ┌──────────────┐  ┌──────────┐
              │ Get Vendors  │  │ Return   │
              │ (VendorTool) │  │ Clear    │
              └──────────────┘  └──────────┘
                         │
                         ▼
              ┌──────────────────┐
              │ Return Reroute   │
              │ Recommendation   │
              └──────────────────┘
```

## Usage Examples

### Basic Usage

```python
import asyncio
from src.agents.monitor.weather_monitor import BeeAIWeatherMonitorAgent

async def main():
    # Create agent
    agent = BeeAIWeatherMonitorAgent(
        target_location="New York,US",
        api_key="your_api_key"
    )
    
    # Check weather
    result = await agent.run()
    
    print(f"Status: {result['status']}")
    if result['status'] == 'reroute_required':
        print(f"Reason: {result['reason']}")
        print(f"Alternative vendors: {len(result['alternative_vendors'])}")
    else:
        print(f"Weather: {result['weather']}")
    
    # Cleanup
    await agent.close()

# Run
asyncio.run(main())
```

### Using Environment Variables

```python
import asyncio
import os
from src.agents.monitor.weather_monitor import BeeAIWeatherMonitorAgent

async def main():
    # Agent reads from environment variables
    # TARGET_LOCATION and OPENWEATHER_API_KEY
    agent = BeeAIWeatherMonitorAgent()
    
    result = await agent.run()
    print(result)
    
    await agent.close()

asyncio.run(main())
```

### With Helper Function

```python
import asyncio
from src.agents.monitor.weather_monitor import create_beeai_weather_agent

async def main():
    # Create agent using helper
    agent = await create_beeai_weather_agent(
        target_location="Los Angeles,US"
    )
    
    if agent:
        result = await agent.run()
        print(result)
        await agent.close()
    else:
        print("Failed to create agent")

asyncio.run(main())
```

### Integration with FastAPI

```python
from fastapi import APIRouter, HTTPException
from src.agents.monitor.weather_monitor import BeeAIWeatherMonitorAgent

router = APIRouter()

@router.get("/weather/check")
async def check_weather(location: str = "New York,US"):
    """Check weather and get reroute recommendations."""
    try:
        agent = BeeAIWeatherMonitorAgent(target_location=location)
        result = await agent.run()
        await agent.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Continuous Monitoring

```python
import asyncio
from src.agents.monitor.weather_monitor import BeeAIWeatherMonitorAgent

async def monitor_weather(interval_seconds: int = 300):
    """Monitor weather continuously."""
    agent = BeeAIWeatherMonitorAgent()
    
    try:
        while True:
            result = await agent.run()
            
            if result['status'] == 'reroute_required':
                print(f"⚠️  ALERT: {result['reason']}")
                print(f"📦 {len(result['alternative_vendors'])} vendors available")
            else:
                print(f"✅ Clear: {result['weather']}")
            
            await asyncio.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("Stopping monitor...")
    finally:
        await agent.close()

# Run continuous monitoring
asyncio.run(monitor_weather(interval_seconds=300))
```

## Response Format

### Clear Weather Response

```json
{
  "status": "clear",
  "weather": "clear sky",
  "reason": null,
  "alternative_vendors": null
}
```

### Reroute Required Response

```json
{
  "status": "reroute_required",
  "weather": null,
  "reason": "heavy thunderstorm",
  "alternative_vendors": [
    {
      "id": "VND-001",
      "name": "GreenHaul Logistics",
      "location": "Los Angeles, CA",
      "fleet_type": "hydrogen",
      "fleet_size": 150,
      "capacity_tons": 3000,
      "eco_rating": 5.0,
      "reliability_score": 95.0,
      "cost_per_mile": 2.85,
      "carbon_emissions_kg_per_mile": 0.05,
      "service_areas": ["California", "Nevada", "Arizona", "Oregon"],
      "contact_email": "dispatch@greenhaul.com",
      "contact_phone": "+1-310-555-0101"
    }
  ]
}
```

### Error Response

```json
{
  "status": "error",
  "weather": null,
  "reason": "Failed to check weather: API key invalid",
  "alternative_vendors": null
}
```

## Severe Weather Keywords

The agent detects the following severe weather conditions:

- `storm`
- `hurricane`
- `tornado`
- `blizzard`
- `extreme`
- `severe`
- `heavy`
- `cyclone`
- `typhoon`
- `thunderstorm`

## Configuration

### Agent Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `target_location` | str | `$TARGET_LOCATION` | Location to monitor |
| `api_key` | str | `$OPENWEATHER_API_KEY` | OpenWeather API key |

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TARGET_LOCATION` | No | `New York,US` | Default location to monitor |
| `OPENWEATHER_API_KEY` | Yes | - | OpenWeather API key |
| `LOG_LEVEL` | No | `INFO` | Logging level |

## Tools

### WeatherCheckTool

**Purpose**: Check current weather conditions for a location

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "location": {
      "type": "string",
      "description": "Location to check (e.g., 'New York,US')"
    }
  },
  "required": ["location"]
}
```

**Output**:
```json
{
  "success": true,
  "data": {
    "condition": "clear sky",
    "temperature": 22.5,
    "wind_speed": 3.2,
    "humidity": 65.0
  }
}
```

### VendorRetrievalTool

**Purpose**: Get list of eco-friendly alternative freight vendors

**Input Schema**:
```json
{
  "type": "object",
  "properties": {},
  "required": []
}
```

**Output**:
```json
{
  "success": true,
  "data": {
    "vendors": [...]
  }
}
```

## Error Handling

The agent handles errors gracefully:

1. **Missing API Key**: Raises `ValueError` on initialization
2. **Weather API Failure**: Returns error status with message
3. **Vendor Retrieval Failure**: Returns reroute status with empty vendor list
4. **BeeAI Not Installed**: Raises `ImportError` with installation instructions

## Testing

### Unit Tests

```python
import pytest
from src.agents.monitor.weather_monitor import (
    BeeAIWeatherMonitorAgent,
    get_vendors,
    BEEAI_AVAILABLE
)

@pytest.mark.skipif(not BEEAI_AVAILABLE, reason="BeeAI not installed")
@pytest.mark.asyncio
async def test_agent_initialization():
    """Test agent initialization."""
    agent = BeeAIWeatherMonitorAgent(
        target_location="Test,US",
        api_key="test_key"
    )
    assert agent.target_location == "Test,US"
    assert agent.api_key == "test_key"

def test_get_vendors():
    """Test vendor retrieval."""
    vendors = get_vendors()
    assert isinstance(vendors, list)
    assert len(vendors) > 0
    assert all('id' in v for v in vendors)
```

### Integration Tests

```python
import pytest
from src.agents.monitor.weather_monitor import BeeAIWeatherMonitorAgent

@pytest.mark.skipif(not BEEAI_AVAILABLE, reason="BeeAI not installed")
@pytest.mark.asyncio
async def test_weather_check_integration():
    """Test full weather check workflow."""
    agent = BeeAIWeatherMonitorAgent(
        target_location="New York,US"
    )
    
    result = await agent.run()
    
    assert 'status' in result
    assert result['status'] in ['clear', 'reroute_required', 'error']
    
    await agent.close()
```

## Troubleshooting

### BeeAI Not Found

**Error**: `ImportError: BeeAI framework is not installed`

**Solution**:
```bash
pip install bee-agent-framework
```

### Invalid API Key

**Error**: `ValueError: OPENWEATHER_API_KEY environment variable is required`

**Solution**: Set the environment variable:
```bash
export OPENWEATHER_API_KEY=your_key_here
```

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'src.agents.monitor.vendors'`

**Solution**: Ensure you're running from the correct directory:
```bash
cd apps/backend
python -m src.agents.monitor.weather_monitor
```

## Performance Considerations

- **API Rate Limits**: OpenWeather free tier allows 60 calls/minute
- **Caching**: Weather data is cached for 5 minutes in the underlying WeatherService
- **Async Operations**: All I/O operations are async for better performance
- **Vendor Retrieval**: Vendors are filtered to eco-friendly options (4.5+ rating)

## Best Practices

1. **Use Environment Variables**: Store API keys in `.env` files, not in code
2. **Handle Errors**: Always wrap agent calls in try-except blocks
3. **Close Resources**: Call `agent.close()` when done to cleanup
4. **Monitor Logs**: Set `LOG_LEVEL=DEBUG` for detailed logging
5. **Rate Limiting**: Don't poll more frequently than every 5 minutes

## Comparison with Traditional WeatherMonitor

| Feature | BeeAI Agent | Traditional Monitor |
|---------|-------------|---------------------|
| Framework | BeeAI | Custom |
| Tools | Modular tools | Integrated methods |
| Extensibility | Easy to add tools | Requires code changes |
| AI Integration | Built-in | Manual |
| Response Format | Structured JSON | Custom objects |
| Learning Curve | Higher | Lower |

## Future Enhancements

- [ ] Add forecast prediction tool
- [ ] Integrate with IBM watsonx.ai for intelligent recommendations
- [ ] Add multi-location monitoring
- [ ] Implement alert notifications (email, SMS)
- [ ] Add historical weather analysis
- [ ] Create dashboard for monitoring

## Support

For issues or questions:
- Check the main project README
- Review AGENTS.md for architecture details
- Check logs with `LOG_LEVEL=DEBUG`

## License

MIT License - See project root LICENSE file

---

**Last Updated**: 2026-05-02  
**Version**: 1.0.0  
**Maintained By**: Eco-Shift Development Team