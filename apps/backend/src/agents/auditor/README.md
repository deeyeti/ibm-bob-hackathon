# Auditor Agent - The Emissions Auditor

## Overview

The Auditor Agent is a critical component of the Eco-Shift project that intercepts vendor lists from the Monitor Agent, calculates projected Scope 3 emissions for transportation routes, and heavily prioritizes alternative energy fleets—especially hydrogen-fueled solutions—to find the lowest carbon footprint options.

## Purpose

- **Intercept vendor data** from Agent A (The Monitor)
- **Calculate Scope 3 emissions** for each vendor's route using accurate emission factors
- **Heavily prioritize hydrogen-fueled fleets** (10x weight multiplier)
- **Rank vendors** by carbon footprint and sustainability metrics
- **Use IBM watsonx.ai** for advanced analysis and recommendations
- **Provide optimized recommendations** with detailed emissions breakdowns

## Architecture

### Components

1. **AuditorAgent** (`auditor_agent.py`)
   - Main agent class extending `BaseAgent`
   - Orchestrates emissions analysis workflow
   - Integrates with IBM watsonx.ai for advanced insights
   - Provides comprehensive vendor recommendations

2. **EmissionsCalculator** (`emissions_calculator.py`)
   - Calculates Scope 3 emissions for freight transportation
   - Supports multiple fleet types (hydrogen, electric, diesel, hybrid, biodiesel, CNG)
   - Includes well-to-wheel analysis
   - Provides detailed emissions breakdowns

3. **FleetPrioritizer** (`fleet_prioritizer.py`)
   - Scores and ranks vendors based on multiple factors
   - Applies 10x multiplier to hydrogen fleets (highest priority)
   - Considers eco-rating, reliability, capacity, and emissions
   - Generates recommendation levels (highly_recommended/recommended/acceptable)

4. **RouteOptimizer** (`route_optimizer.py`)
   - Optimizes routes based on emissions, cost, reliability, and delivery time
   - Heavily weights carbon footprint (70% by default)
   - Provides alternative route suggestions
   - Calculates emissions savings compared to baseline

5. **Configuration** (`config.py`)
   - Emission factors for each fleet type
   - Fleet prioritization weights
   - Optimization parameters
   - watsonx.ai integration settings

## Fleet Type Prioritization

The Auditor Agent uses a sophisticated scoring system that heavily favors low-emission fleets:

### Priority Scores (Base)

- **Hydrogen**: 100 points × 10 = **1000 points** (highest priority)
- **Electric (Renewable)**: 90 points
- **Electric (Grid)**: 70 points
- **Biodiesel**: 50 points
- **Hybrid**: 40 points
- **CNG**: 30 points
- **Diesel**: 10 points (lowest priority)

### Emission Factors (kg CO2e per mile)

- **Hydrogen**: 0.05 kg (green hydrogen)
- **Electric (Renewable)**: 0.08 kg
- **Electric (Grid)**: 0.50 kg
- **Biodiesel**: 0.45 kg
- **Hybrid**: 1.34 kg
- **CNG**: 1.80 kg
- **Diesel**: 2.68 kg (baseline)

## Usage

### Basic Usage

```python
from src.agents.auditor import AuditorAgent

# Initialize agent
auditor = AuditorAgent()
await auditor.initialize()

# Analyze vendors from Monitor Agent
vendors = [...]  # Vendor list from Monitor Agent
result = await auditor.analyze_vendors(
    vendors=vendors,
    distance_miles=150.0,
    load_tons=25.0,
    location="Los Angeles, CA"
)

# Access recommendations
recommendations = result["recommendations"]
hydrogen_vendors = result["hydrogen_vendors"]
emissions_summary = result["emissions_summary"]
watsonx_analysis = result["watsonx_analysis"]
```

### Advanced Usage

```python
# Custom configuration
from src.agents.auditor import AuditorAgent, AuditorConfig

config = AuditorConfig(
    min_eco_rating=4.5,
    top_recommendations=10,
    use_watsonx=True,
    hydrogen_preference=15.0,  # Even higher hydrogen preference
)

auditor = AuditorAgent(config=config)
await auditor.initialize()

# Analyze with custom parameters
result = await auditor.analyze_vendors(
    vendors=vendors,
    distance_miles=200.0,
    load_tons=30.0,
)

# Get detailed breakdown
if result["detailed_breakdown"]:
    emissions_details = result["detailed_breakdown"]["emissions_details"]
    scoring_details = result["detailed_breakdown"]["scoring_details"]
```

## Analysis Workflow

1. **Receive Vendor Data**: Accept vendor list from Monitor Agent
2. **Calculate Emissions**: Compute Scope 3 emissions for each vendor's route
3. **Score Vendors**: Apply hydrogen-first scoring with 10x multiplier
4. **Optimize Routes**: Rank by optimization score (carbon footprint heavily weighted)
5. **Generate Insights**: Use watsonx.ai for advanced analysis
6. **Return Recommendations**: Provide ranked vendor list with detailed metrics

## Output Format

### Recommendations

```json
{
  "status": "success",
  "timestamp": "2024-01-01T12:00:00Z",
  "recommendations": [
    {
      "rank": 1,
      "vendor_id": "VND-001",
      "vendor_name": "GreenHaul Logistics",
      "fleet_type": "hydrogen",
      "total_emissions_kg": 7.5,
      "emissions_reduction_percent": 98.2,
      "estimated_cost": 427.50,
      "optimization_score": 9850.0,
      "recommendation_reason": "Zero-emission hydrogen fuel cell technology; Excellent environmental rating; Highly reliable service",
      "emissions_savings_kg": 392.5
    }
  ],
  "hydrogen_vendors": [...],
  "alternatives": [...],
  "emissions_summary": {...},
  "watsonx_analysis": {...}
}
```

## Emissions Calculation

### Formula

```
Total Emissions = (Distance × Emission Factor × Load Factor) / Efficiency Factor × WTW Multiplier
```

Where:
- **Distance**: Route distance in miles
- **Emission Factor**: kg CO2e per mile for fleet type
- **Load Factor**: Adjustment based on capacity utilization (0.7-1.3)
- **Efficiency Factor**: Vehicle efficiency rating (0.7-1.0)
- **WTW Multiplier**: Well-to-wheel lifecycle multiplier (1.1-1.4)

### Well-to-Wheel Analysis

Includes:
- Fuel/energy production
- Processing and refining
- Distribution and delivery
- Vehicle operation

## Integration with watsonx.ai

The Auditor Agent uses IBM watsonx.ai Granite-3.0-8b for:

1. **Advanced Emissions Analysis**: Deep insights into emission patterns
2. **Sustainability Recommendations**: Specific actions for emissions reduction
3. **Hydrogen Fleet Advantages**: Analysis of hydrogen technology benefits
4. **Long-term Strategy**: Suggestions for sustainable transportation planning

### Example watsonx.ai Analysis

```python
watsonx_analysis = result["watsonx_analysis"]
print(watsonx_analysis["analysis"])
# Output: Detailed sustainability insights and recommendations
```

## Configuration Options

### Emission Factors

```python
emission_factors = EmissionFactors(
    hydrogen=0.05,
    electric_renewable=0.08,
    electric_grid=0.50,
    biodiesel=0.45,
    hybrid=1.34,
    diesel=2.68,
)
```

### Fleet Priorities

```python
fleet_priorities = FleetPriorities(
    hydrogen=100,  # Will be multiplied by 10
    electric_renewable=90,
    electric_grid=70,
    biodiesel=50,
    hybrid=40,
    diesel=10,
)
```

### Optimization Weights

```python
optimization_weights = OptimizationWeights(
    carbon_footprint=0.70,  # 70% weight on emissions
    cost=0.15,
    reliability=0.10,
    delivery_time=0.05,
    hydrogen_preference=10.0,  # 10x multiplier for hydrogen
)
```

## Key Features

### 1. Hydrogen-First Strategy

- **10x Priority Multiplier**: Hydrogen fleets receive 10 times the base score
- **Near-Zero Emissions**: Green hydrogen produces only 0.05 kg CO2e per mile
- **Highly Recommended**: Hydrogen vendors always marked as "highly_recommended"

### 2. Comprehensive Emissions Analysis

- **Scope 3 Calculations**: Accurate freight transportation emissions
- **Multiple Fleet Types**: Support for 6+ fleet types
- **Well-to-Wheel**: Lifecycle emissions including fuel production
- **Load Adjustments**: Emissions vary based on capacity utilization

### 3. Multi-Factor Optimization

- **Carbon Footprint**: Primary optimization factor (70% weight)
- **Cost Efficiency**: Balanced with environmental impact
- **Reliability**: Vendor track record considered
- **Delivery Time**: Logistics efficiency included

### 4. AI-Powered Insights

- **watsonx.ai Integration**: Advanced analysis using IBM's AI
- **Sustainability Recommendations**: Actionable insights
- **Trend Analysis**: Pattern recognition in emissions data

### 5. Detailed Reporting

- **Emissions Breakdown**: Per-mile, per-ton-mile metrics
- **Savings Calculations**: Comparison to diesel baseline
- **Alternative Routes**: Multiple options with trade-off analysis
- **Fleet Comparisons**: Side-by-side vendor analysis

## API Integration

The Auditor Agent integrates with the orchestrator and can be accessed via API endpoints:

```python
# Via orchestrator
from src.agents.orchestrator import orchestrator

result = await orchestrator.run_auditor_analysis(
    vendors=vendors,
    distance_miles=150.0,
    load_tons=25.0,
)
```

## Performance Metrics

The agent tracks:
- Vendors analyzed
- Emissions calculated
- Hydrogen vendors found
- Total emissions savings potential
- Execution time
- watsonx.ai analysis generation time

## Error Handling

The agent includes comprehensive error handling:
- Validation of vendor data
- Fallback for missing emission factors
- Graceful degradation if watsonx.ai unavailable
- Detailed logging for debugging

## Testing

```python
# Example test
async def test_auditor_agent():
    auditor = AuditorAgent()
    await auditor.initialize()
    
    vendors = [
        {
            "id": "VND-001",
            "name": "GreenHaul Logistics",
            "fleet_type": "hydrogen",
            "eco_rating": 5.0,
            "reliability_score": 95.0,
            "capacity_tons": 3000,
        }
    ]
    
    result = await auditor.analyze_vendors(
        vendors=vendors,
        distance_miles=100.0,
        load_tons=20.0,
    )
    
    assert result["status"] == "success"
    assert len(result["recommendations"]) > 0
    assert result["hydrogen_vendors"][0]["vendor_id"] == "VND-001"
```

## Future Enhancements

- Real-time emissions monitoring
- Machine learning for emission predictions
- Integration with carbon offset markets
- Multi-modal transportation analysis
- Dynamic route optimization based on traffic/weather

## Dependencies

- `pydantic`: Data validation and settings
- `ibm-watsonx-ai`: IBM watsonx.ai integration
- `src.agents.base_agent`: Base agent class
- `src.services.watsonx_service`: watsonx service
- `src.utils.logger`: Logging utilities

## Contributing

When contributing to the Auditor Agent:
1. Maintain hydrogen-first prioritization
2. Ensure accurate emission calculations
3. Add tests for new fleet types
4. Update documentation
5. Follow existing code patterns

## License

Part of the Eco-Shift project for IBM Bob Hackathon.

---

**Made with Bob** 🤖

For questions or issues, please refer to the main project documentation.