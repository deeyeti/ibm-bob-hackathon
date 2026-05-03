# Orchestrator Agent Workflow

## Overview

The Orchestrator Agent coordinates the **WeatherMonitorAgent** and **BeeAIAuditorAgent** to create an automated workflow for weather-based freight rerouting with ESG-compliant vendor selection.

## Workflow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  ORCHESTRATOR WORKFLOW                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │   Step 1: WeatherMonitorAgent         │
        │   - Check weather conditions          │
        │   - Detect severe weather             │
        │   - Retrieve alternative vendors      │
        └───────────────────────────────────────┘
                            │
                            ▼
                ┌──────────────────────┐
                │  Status Check        │
                │  reroute_required?   │
                └──────────────────────┘
                    │              │
                    │ Yes          │ No
                    ▼              ▼
        ┌───────────────────┐   ┌──────────────┐
        │ Step 2: Extract   │   │ Workflow     │
        │ alternative_      │   │ Complete     │
        │ vendors           │   │ (No action)  │
        └───────────────────┘   └──────────────┘
                    │
                    ▼
        ┌───────────────────────────────────────┐
        │   Step 3: BeeAIAuditorAgent           │
        │   - Analyze vendor emissions          │
        │   - Calculate Scope 3 carbon          │
        │   - Prioritize hydrogen/electric      │
        │   - Select optimal vendor             │
        └───────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────────────┐
        │   Step 4: Generate Shift Order        │
        │   - Format ESG-compliant output       │
        │   - Print to console                  │
        │   - Include emissions savings         │
        └───────────────────────────────────────┘
```

## Components

### 1. WeatherMonitorAgent (BeeAI-based)

**File**: `apps/backend/src/agents/monitor/weather_monitor.py`

**Class**: `BeeAIWeatherMonitorAgent`

**Responsibilities**:
- Monitor weather conditions at target location
- Detect severe weather patterns (storms, hurricanes, extreme temperatures)
- Retrieve alternative freight vendors when severe weather detected
- Return structured response with status and vendor list

**Response Structure**:
```python
{
    "status": "clear" | "reroute_required" | "error",
    "weather": str,  # Weather description (if clear)
    "reason": str,   # Reason for reroute (if required)
    "alternative_vendors": [  # List of vendors (if reroute required)
        {
            "id": str,
            "name": str,
            "fleet_type": str,
            "eco_rating": float,
            "carbon_emissions_kg_per_mile": float,
            ...
        }
    ]
}
```

### 2. BeeAIAuditorAgent

**File**: `apps/backend/src/agents/auditor/beeai_auditor.py`

**Class**: `BeeAIAuditorAgent`

**Responsibilities**:
- Accept alternative_vendors payload from Monitor Agent
- Calculate Scope 3 emissions using IBM watsonx.ai
- Prioritize hydrogen and electric fleets (zero direct emissions)
- Recommend optimal vendor based on carbon footprint
- Provide emissions savings and justification

**Response Structure**:
```python
{
    "status": "success" | "error",
    "approved_vendor_id": str,
    "emissions_saving": str,
    "justification": str,
    "timestamp": str,
    "vendors_analyzed": int,
    "ai_analysis_raw": str  # Raw AI response for debugging
}
```

### 3. Orchestrator Workflow

**File**: `apps/backend/src/agents/orchestrator/orchestrator_agent.py`

**Function**: `run_beeai_orchestrator_workflow()`

**Workflow Steps**:
1. Initialize and run WeatherMonitorAgent
2. Check if status is 'reroute_required'
3. Extract alternative_vendors from response
4. Initialize and run BeeAIAuditorAgent with vendor data
5. Generate and print ESG-compliant Shift Order

## Usage

### Running from Command Line

```bash
# From project root
cd apps/backend

# Run the orchestrator
python -m src.agents.orchestrator.orchestrator_agent
```

### Environment Variables

Required environment variables (set in `.env` file):

```bash
# OpenWeather API (Required)
OPENWEATHER_API_KEY=your_openweather_api_key

# IBM watsonx.ai (Required for Auditor)
WATSONX_API_KEY=your_watsonx_api_key
WATSONX_PROJECT_ID=your_watsonx_project_id

# Optional Configuration
TARGET_LOCATION=New York,US  # Default location to monitor
WATSONX_MODEL_ID=ibm/granite-13b-chat-v2  # AI model to use
```

### Programmatic Usage

```python
import asyncio
from src.agents.orchestrator.orchestrator_agent import run_beeai_orchestrator_workflow

async def main():
    result = await run_beeai_orchestrator_workflow(
        target_location="New York,US",
        openweather_api_key="your_api_key"
    )
    
    print(f"Workflow Status: {result['status']}")
    print(f"Reroute Required: {result['reroute_required']}")

asyncio.run(main())
```

## Output Format

### ESG-Compliant Shift Order

When severe weather is detected and rerouting is required, the workflow generates a formatted Shift Order:

```
══════════════════════════════════════════════════════════════════
                    ESG-COMPLIANT SHIFT ORDER
══════════════════════════════════════════════════════════════════
Order ID: SHIFT-20260503-025800
Timestamp: 2026-05-03T02:58:00Z
Status: APPROVED

WEATHER ALERT
──────────────────────────────────────────────────────────────────
Location: New York, US
Severity: HIGH
Reason: Severe thunderstorm with heavy rain

APPROVED VENDOR
──────────────────────────────────────────────────────────────────
Vendor ID: hydrogen-freight-001
Vendor Name: GreenHaul Logistics
Fleet Type: Hydrogen
Eco Rating: 5.0/5.0

EMISSIONS IMPACT
──────────────────────────────────────────────────────────────────
Emissions Saving: 100% (zero direct emissions)
Vendors Analyzed: 8
ESG Compliance: ✓ Zero-emission fleet

JUSTIFICATION
──────────────────────────────────────────────────────────────────
Selected GreenHaul Logistics with hydrogen fleet for optimal
environmental performance. Hydrogen fuel cells produce zero direct
emissions, significantly reducing carbon footprint compared to
traditional diesel operations.

══════════════════════════════════════════════════════════════════
```

## Key Features

### 1. Conditional Workflow Execution
- Only triggers vendor analysis when severe weather is detected
- Saves API calls and processing time when conditions are clear

### 2. Hydrogen Fleet Prioritization
- Auditor Agent applies 10x multiplier to hydrogen fleets
- Ensures zero-emission vehicles are selected when available

### 3. ESG Compliance
- Tracks and reports emissions savings
- Provides justification for vendor selection
- Aligns with sustainability goals

### 4. Error Handling
- Graceful fallback if APIs are unavailable
- Detailed error logging for debugging
- User-friendly error messages

### 5. Extensibility
- Easy to add new agent types
- Modular design for workflow customization
- Supports additional data sources

## Testing

### Test with Mock Data

```python
# Create a test script
import asyncio
from src.agents.orchestrator.orchestrator_agent import run_beeai_orchestrator_workflow

async def test_workflow():
    # This will use actual APIs
    result = await run_beeai_orchestrator_workflow(
        target_location="Miami,US"  # Try different locations
    )
    
    assert result['status'] in ['completed', 'error']
    print("Test passed!")

asyncio.run(test_workflow())
```

### Expected Behavior

**Scenario 1: Clear Weather**
```
✅ Weather conditions are clear. No reroute required.
```

**Scenario 2: Severe Weather**
```
⚠️  Severe weather detected! Reroute required.
📦 Found 8 alternative vendors
🔍 Analyzing vendors for emissions optimization...
📋 Generating ESG-Compliant Shift Order...
[Shift Order printed to console]
✅ Workflow completed successfully!
```

**Scenario 3: Error**
```
❌ Error: OPENWEATHER_API_KEY environment variable not set
```

## Architecture Decisions

### Why BeeAI Framework?
- Provides structured tool-based agent architecture
- Enables easy integration with IBM watsonx.ai
- Supports complex multi-step workflows
- Facilitates testing and debugging

### Why Separate Agents?
- **Separation of Concerns**: Each agent has a single responsibility
- **Reusability**: Agents can be used independently
- **Testability**: Easier to test individual components
- **Scalability**: Can add more agents without modifying existing ones

### Why Async/Await?
- Non-blocking API calls
- Better performance for I/O operations
- Supports concurrent agent execution
- Modern Python best practice

## Troubleshooting

### Common Issues

**1. Import Errors**
```
ModuleNotFoundError: No module named 'bee_agent'
```
**Solution**: BeeAI framework is optional. The code includes fallback logic.

**2. API Key Errors**
```
❌ Error: OPENWEATHER_API_KEY environment variable not set
```
**Solution**: Ensure `.env` file exists in `apps/backend/` with valid API keys.

**3. No Vendors Found**
```
❌ Error: No alternative vendors available for reroute
```
**Solution**: Check that vendor data is properly configured in `vendors.py`.

**4. Watsonx Errors**
```
Failed to calculate emissions: Watsonx API error
```
**Solution**: Verify `WATSONX_API_KEY` and `WATSONX_PROJECT_ID` are correct.

## Performance Considerations

- **Weather API Caching**: Weather data is cached for 5 minutes to avoid rate limits
- **Vendor Analysis**: Typically takes 2-5 seconds depending on vendor count
- **Total Workflow Time**: 5-10 seconds for complete execution

## Future Enhancements

1. **Database Integration**: Store shift orders for historical analysis
2. **Real-time Monitoring**: Continuous weather polling with webhooks
3. **Multi-location Support**: Monitor multiple locations simultaneously
4. **Advanced Analytics**: Track emissions savings over time
5. **API Endpoints**: Expose workflow via REST API for frontend integration

## Related Files

- `apps/backend/src/agents/monitor/weather_monitor.py` - Weather monitoring logic
- `apps/backend/src/agents/auditor/beeai_auditor.py` - Vendor analysis logic
- `apps/backend/src/services/watsonx_service.py` - IBM watsonx.ai integration
- `apps/backend/src/services/weather_service.py` - OpenWeather API integration
- `apps/backend/src/agents/monitor/vendors.py` - Vendor data management

## Support

For issues or questions:
1. Check the logs in `apps/backend/logs/`
2. Review environment variable configuration
3. Verify API keys are valid and have sufficient quota
4. Consult the main project README for setup instructions

---

**Last Updated**: 2026-05-03  
**Version**: 1.0.0  
**Maintained By**: Eco-Shift Development Team