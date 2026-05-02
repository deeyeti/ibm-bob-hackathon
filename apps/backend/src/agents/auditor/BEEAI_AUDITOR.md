# BeeAI Auditor Agent

## Overview

The BeeAI Auditor Agent is an intelligent emissions analysis system that uses the BeeAI framework and IBM watsonx.ai to evaluate freight vendors and recommend optimal choices based on carbon footprint analysis.

## Architecture

### Components

1. **BeeAIAuditorAgent**: Main agent class that orchestrates the analysis
2. **EmissionsCalculationTool**: BeeAI tool that interfaces with watsonx.ai
3. **Response Parser**: Robust parsing logic to extract structured recommendations from AI responses

### Workflow

```
Monitor Agent (Severe Weather Detected)
    ↓
Alternative Vendors Payload
    ↓
BeeAI Auditor Agent
    ↓
EmissionsCalculationTool → watsonx.ai (Granite Model)
    ↓
AI Response Parsing
    ↓
Structured JSON Recommendation
```

## Key Features

### 1. Vendor Analysis
- Accepts alternative_vendors payload from Monitor Agent
- Analyzes multiple vendors simultaneously
- Considers fleet type, emissions, reliability, and cost

### 2. AI-Powered Emissions Calculation
- Uses IBM watsonx.ai (Llama 3.3 70B Instruct model)
- Calculates Scope 3 carbon emissions
- Provides detailed environmental impact analysis

### 3. Hydrogen/Electric Fleet Prioritization
- **10x preference** for hydrogen and electric fleets
- Zero direct emissions prioritization
- Aligns with sustainability goals

### 4. Robust Error Handling
- Graceful fallback when AI parsing fails
- Automatic vendor selection based on fleet type priority
- Comprehensive error logging

### 5. Structured Output
Returns JSON with:
- `approved_vendor_id`: Selected vendor identifier
- `emissions_saving`: Quantified emissions reduction
- `justification`: Detailed reasoning for recommendation

## Usage

### Basic Usage

```python
from src.agents.auditor.beeai_auditor import analyze_alternative_vendors

# Payload from Monitor Agent
alternative_vendors = {
    "status": "reroute_required",
    "reason": "severe storm conditions",
    "location": "New York,US",
    "vendors": [
        {
            "id": "vendor_001",
            "name": "GreenFleet Logistics",
            "fleet_type": "hydrogen",
            "eco_rating": 4.9,
            # ... other vendor details
        },
        # ... more vendors
    ]
}

# Analyze vendors
result = await analyze_alternative_vendors(alternative_vendors)

# Result structure:
# {
#     "status": "success",
#     "approved_vendor_id": "vendor_001",
#     "emissions_saving": "100% (zero direct emissions)",
#     "justification": "Selected GreenFleet Logistics with hydrogen fleet...",
#     "timestamp": "2026-05-02T20:00:00.000Z",
#     "vendors_analyzed": 4,
#     "ai_analysis_raw": "..."
# }
```

### Advanced Usage

```python
from src.agents.auditor.beeai_auditor import BeeAIAuditorAgent

# Create agent instance
agent = BeeAIAuditorAgent()

# Analyze vendors
result = await agent.analyze_vendors(alternative_vendors)

# Access detailed analysis
print(f"Approved: {result['approved_vendor_id']}")
print(f"Savings: {result['emissions_saving']}")
print(f"Reason: {result['justification']}")

# Cleanup
await agent.close()
```

## Input Format

### Alternative Vendors Payload

```json
{
  "status": "reroute_required",
  "reason": "severe weather description",
  "location": "City, State/Country",
  "vendors": [
    {
      "id": "unique_vendor_id",
      "name": "Vendor Name",
      "location": "Vendor Location",
      "fleet_type": "hydrogen|electric|hybrid|diesel",
      "fleet_size": 50,
      "capacity_tons": 500,
      "eco_rating": 4.9,
      "reliability_score": 0.95,
      "cost_per_mile": 2.5,
      "carbon_emissions_kg_per_mile": 0.0,
      "service_areas": ["Area 1", "Area 2"],
      "contact_email": "email@vendor.com",
      "contact_phone": "+1-555-0000"
    }
  ]
}
```

## Output Format

### Success Response

```json
{
  "status": "success",
  "approved_vendor_id": "vendor_001",
  "emissions_saving": "100% (zero direct emissions)",
  "justification": "Selected GreenFleet Logistics with hydrogen fleet for optimal environmental performance and emissions reduction. Hydrogen fuel cells produce zero direct emissions.",
  "timestamp": "2026-05-02T20:00:00.000Z",
  "vendors_analyzed": 4,
  "ai_analysis_raw": "Full AI response text..."
}
```

### Error Response

```json
{
  "status": "error",
  "error": "Error description",
  "approved_vendor_id": null,
  "emissions_saving": null,
  "justification": "Error message",
  "timestamp": "2026-05-02T20:00:00.000Z"
}
```

## Response Parsing Logic

The agent implements robust parsing to extract recommendations from AI responses:

### 1. Vendor ID Extraction
- Searches for recommendation keywords: "recommend", "best", "optimal", "choose"
- Validates vendor ID against input data
- Falls back to hydrogen/electric fleet if parsing fails

### 2. Emissions Savings Extraction
- Looks for patterns: "X kg", "X% reduction", "savings of X"
- Estimates based on fleet type if not found:
  - Hydrogen: 100% (zero direct emissions)
  - Electric: 100% (zero direct emissions)
  - Hybrid: 50% (hybrid efficiency)
  - Diesel: baseline

### 3. Justification Extraction
- Identifies sentences with sustainability keywords
- Combines relevant sentences into coherent justification
- Generates fallback justification based on fleet type

## Integration with Monitor Agent

The BeeAI Auditor Agent is designed to work seamlessly with the Monitor Agent:

```python
# In Monitor Agent
weather_result = await monitor_agent.check_weather()

if weather_result["status"] == "reroute_required":
    # Get alternative vendors
    alternative_vendors = weather_result
    
    # Pass to Auditor Agent
    from src.agents.auditor import analyze_alternative_vendors
    recommendation = await analyze_alternative_vendors(alternative_vendors)
    
    # Use recommendation
    approved_vendor = recommendation["approved_vendor_id"]
    savings = recommendation["emissions_saving"]
    reason = recommendation["justification"]
```

## Configuration

### Environment Variables

Required:
- `WATSONX_API_KEY`: IBM watsonx.ai API key
- `WATSONX_PROJECT_ID`: IBM watsonx.ai project ID

Optional:
- `WATSONX_URL`: watsonx.ai endpoint (default: https://us-south.ml.cloud.ibm.com)
- `WATSONX_MODEL_ID`: Model to use (default: meta-llama/llama-3-3-70b-instruct)

### Model Configuration

The agent uses the Llama 3.3 70B Instruct model with:
- `max_new_tokens`: 1000
- `temperature`: 0.5 (for consistent analysis)
- `top_p`: 0.95
- `top_k`: 50

## Error Handling

### Graceful Degradation

1. **AI Service Unavailable**: Falls back to rule-based vendor selection
2. **Parsing Failure**: Uses fleet type priority (hydrogen > electric > hybrid > diesel)
3. **Empty Vendor List**: Returns error with clear message
4. **Invalid Input**: Validates and returns structured error response

### Logging

All operations are logged with appropriate levels:
- `INFO`: Normal operations, analysis results
- `WARNING`: Fallback logic triggered, parsing issues
- `ERROR`: Failures, exceptions with stack traces

## Testing

### Run Example

```bash
cd apps/backend
python -m examples.beeai_auditor_example
```

### Unit Tests

```bash
pytest tests/unit/test_beeai_auditor.py -v
```

### Integration Tests

```bash
pytest tests/integration/test_auditor_monitor_integration.py -v
```

## Performance Considerations

### Caching
- watsonx.ai responses are not cached (each analysis is unique)
- Consider implementing response caching for identical vendor sets

### Rate Limiting
- watsonx.ai has rate limits based on plan
- Implement exponential backoff for retries if needed

### Async Operations
- All operations are async for non-blocking execution
- Uses `asyncio.to_thread()` for synchronous IBM SDK calls

## Best Practices

1. **Always validate input**: Check vendor list is not empty
2. **Handle errors gracefully**: Use try-except blocks
3. **Log comprehensively**: Include context in log messages
4. **Clean up resources**: Call `agent.close()` when done
5. **Monitor AI responses**: Check `ai_analysis_raw` for debugging

## Troubleshooting

### Common Issues

**Issue**: "WATSONX_API_KEY environment variable is required"
- **Solution**: Set the API key in `.env` file

**Issue**: "Failed to calculate emissions"
- **Solution**: Check watsonx.ai service status and API key validity

**Issue**: "No vendors available for analysis"
- **Solution**: Ensure vendor list is not empty in input payload

**Issue**: Type errors about BeeAI imports
- **Solution**: These are expected if BeeAI is not installed; agent uses fallback implementation

## Future Enhancements

1. **Response Caching**: Cache AI responses for identical vendor sets
2. **Batch Processing**: Analyze multiple vendor sets in parallel
3. **Historical Analysis**: Track vendor performance over time
4. **Custom Scoring**: Allow custom weights for different factors
5. **Multi-Model Support**: Support multiple AI models for comparison

## References

- [IBM watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [BeeAI Framework](https://github.com/i-am-bee/bee-agent-framework)
- [Eco-Shift Architecture](../../../docs/ARCHITECTURE.md)
- [Agent Rules](../../../AGENTS.md)

---

**Last Updated**: 2026-05-02  
**Maintained By**: Eco-Shift Development Team  
**Made with Bob**