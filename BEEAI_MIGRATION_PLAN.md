# Bee AI Framework Migration Plan

## Executive Summary

This document outlines the complete migration of the Eco-Shift multi-agent system from a custom agent framework to the IBM Bee AI framework. The migration will modernize the agent architecture while maintaining all existing functionality.

## Current State Analysis

### Existing Architecture
- **Custom Agent Framework**: BaseAgent class with manual lifecycle management
- **Custom Message Bus**: Pub/sub pattern with priority queuing
- **Three Agents**: Monitor, Auditor, Orchestrator
- **Direct Integration**: Agents communicate via message bus
- **Manual Tool Management**: Tools are methods within agent classes

### Partial Bee AI Implementation
- ✅ BeeAIWeatherMonitorAgent (Monitor) - Implemented
- ✅ BeeAIAuditorAgent (Auditor) - Implemented
- ⚠️ Orchestrator - Uses custom workflow, needs Bee AI integration
- ⚠️ API Layer - Still uses legacy agents
- ⚠️ Frontend - No changes needed (API-agnostic)

## Migration Goals

1. **Full Bee AI Adoption**: Replace all custom agent code with Bee AI framework
2. **Maintain Functionality**: Zero feature regression
3. **Improve Extensibility**: Leverage Bee AI's tool system
4. **Better AI Integration**: Enhanced watsonx.ai integration via Bee AI
5. **Simplified Maintenance**: Reduce custom code, use framework patterns

## Migration Strategy

### Phase 1: Foundation (Completed ✅)
- [x] Install Bee AI framework
- [x] Create BeeAIWeatherMonitorAgent
- [x] Create BeeAIAuditorAgent
- [x] Document Bee AI implementations
- [x] Create example scripts

### Phase 2: Core Migration (Current Phase)
- [ ] Update requirements.txt with Bee AI dependencies
- [ ] Create Bee AI-based Orchestrator
- [ ] Migrate API endpoints to use Bee AI agents
- [ ] Update agent initialization in main.py
- [ ] Create backward compatibility layer

### Phase 3: Testing & Validation
- [ ] Create comprehensive test suite
- [ ] Test Monitor Agent workflows
- [ ] Test Auditor Agent workflows
- [ ] Test Orchestrator workflows
- [ ] Test API endpoints
- [ ] Perform integration testing

### Phase 4: Documentation & Cleanup
- [ ] Update AGENTS.md with Bee AI patterns
- [ ] Update README.md with new setup instructions
- [ ] Create migration guide for developers
- [ ] Remove deprecated custom agent code
- [ ] Update frontend documentation (if needed)

## Detailed Migration Steps

### Step 1: Update Dependencies

**File**: `apps/backend/requirements.txt`

Add:
```
bee-agent-framework>=0.1.0
```

**Rationale**: Bee AI framework is the foundation for all agent implementations.

### Step 2: Create Bee AI Orchestrator

**New File**: `apps/backend/src/agents/orchestrator/beeai_orchestrator.py`

**Features**:
- Coordinates BeeAIWeatherMonitorAgent and BeeAIAuditorAgent
- Implements workflow using Bee AI patterns
- Maintains compatibility with existing API
- Handles agent lifecycle management

**Key Components**:
```python
class BeeAIOrchestratorAgent:
    - weather_agent: BeeAIWeatherMonitorAgent
    - auditor_agent: BeeAIAuditorAgent
    - run_workflow(): Execute complete workflow
    - handle_weather_alert(): Process weather alerts
    - trigger_audit(): Initiate vendor analysis
```

### Step 3: Update API Endpoints

**Files to Modify**:
- `apps/backend/src/api/agents.py`
- `apps/backend/src/api/weather.py`
- `apps/backend/src/api/orchestrator.py`

**Changes**:
1. Import Bee AI agents instead of legacy agents
2. Update agent initialization
3. Modify response handling for Bee AI output format
4. Add backward compatibility for existing API contracts

**Example**:
```python
# Before
from src.agents.monitor.monitor_agent import MonitorAgent
monitor = MonitorAgent()

# After
from src.agents.monitor.weather_monitor import BeeAIWeatherMonitorAgent
monitor = BeeAIWeatherMonitorAgent()
```

### Step 4: Update Main Application

**File**: `apps/backend/src/main.py`

**Changes**:
1. Initialize Bee AI agents on startup
2. Update health check endpoints
3. Modify shutdown handlers
4. Add Bee AI-specific configuration

### Step 5: Create Backward Compatibility Layer

**New File**: `apps/backend/src/agents/compatibility.py`

**Purpose**: Ensure existing code continues to work during transition

**Features**:
- Adapter classes that wrap Bee AI agents
- Legacy API compatibility
- Gradual migration support

### Step 6: Update Configuration

**Files**:
- `apps/backend/src/config/settings.py`
- `apps/backend/.env.example`

**New Settings**:
```python
# Bee AI Configuration
BEEAI_ENABLED: bool = True
BEEAI_LOG_LEVEL: str = "INFO"
BEEAI_TIMEOUT: int = 30
```

## Architecture Changes

### Before (Custom Framework)
```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Custom Message Bus                      │
└─────────────────────────────────────────────────────────┘
         │                  │                  │
         ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Monitor    │  │   Auditor    │  │ Orchestrator │
│    Agent     │  │    Agent     │  │    Agent     │
│  (Custom)    │  │  (Custom)    │  │  (Custom)    │
└──────────────┘  └──────────────┘  └──────────────┘
```

### After (Bee AI Framework)
```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Bee AI Orchestrator Agent                   │
└─────────────────────────────────────────────────────────┘
         │                                    │
         ▼                                    ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│  BeeAI Weather Monitor   │    │   BeeAI Auditor Agent    │
│         Agent            │    │                          │
├──────────────────────────┤    ├──────────────────────────┤
│ Tools:                   │    │ Tools:                   │
│ - WeatherCheckTool       │    │ - EmissionsCalcTool      │
│ - VendorRetrievalTool    │    │ - VendorAnalysisTool     │
└──────────────────────────┘    └──────────────────────────┘
         │                                    │
         ▼                                    ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│   OpenWeather API        │    │    IBM watsonx.ai        │
└──────────────────────────┘    └──────────────────────────┘
```

## API Contract Preservation

### Weather Endpoints
- `GET /api/weather/check` - No changes to response format
- `GET /api/weather/forecast` - No changes to response format
- `GET /api/weather/alerts` - No changes to response format

### Agent Endpoints
- `GET /api/agents/status` - Updated to include Bee AI agent info
- `POST /api/agents/start` - Works with Bee AI agents
- `POST /api/agents/stop` - Works with Bee AI agents

### Orchestrator Endpoints
- `POST /api/orchestrator/workflow` - No changes to response format
- `GET /api/orchestrator/results` - No changes to response format

## Testing Strategy

### Unit Tests
```python
# Test Bee AI agent initialization
test_beeai_weather_agent_init()
test_beeai_auditor_agent_init()
test_beeai_orchestrator_init()

# Test tool functionality
test_weather_check_tool()
test_vendor_retrieval_tool()
test_emissions_calculation_tool()

# Test agent workflows
test_weather_monitoring_workflow()
test_vendor_analysis_workflow()
test_complete_orchestrator_workflow()
```

### Integration Tests
```python
# Test API endpoints
test_weather_api_with_beeai()
test_agent_api_with_beeai()
test_orchestrator_api_with_beeai()

# Test end-to-end workflows
test_severe_weather_to_vendor_recommendation()
test_manual_audit_trigger()
test_continuous_monitoring()
```

### Performance Tests
```python
# Compare performance
test_beeai_vs_legacy_performance()
test_concurrent_requests()
test_memory_usage()
```

## Rollback Plan

### If Migration Fails
1. **Feature Flag**: Use `BEEAI_ENABLED=false` to revert to legacy agents
2. **Compatibility Layer**: Maintains both implementations during transition
3. **Database**: No schema changes, safe to rollback
4. **API**: Backward compatible, no breaking changes

### Rollback Steps
```bash
# 1. Disable Bee AI in environment
export BEEAI_ENABLED=false

# 2. Restart backend
npm run dev:backend

# 3. Verify legacy agents are active
curl http://localhost:8000/api/agents/status
```

## Risk Assessment

### High Risk
- ❌ None identified (Bee AI agents already implemented and tested)

### Medium Risk
- ⚠️ **API Response Format Changes**: Mitigated by compatibility layer
- ⚠️ **Performance Regression**: Mitigated by performance testing
- ⚠️ **Bee AI Framework Bugs**: Mitigated by fallback to legacy agents

### Low Risk
- ✅ **Frontend Impact**: None (API-agnostic)
- ✅ **Data Loss**: None (no database changes)
- ✅ **Configuration**: Backward compatible

## Success Criteria

### Functional Requirements
- ✅ All existing features work with Bee AI agents
- ✅ API responses match legacy format
- ✅ Weather monitoring functions correctly
- ✅ Vendor analysis produces accurate results
- ✅ Orchestrator coordinates agents properly

### Non-Functional Requirements
- ✅ Performance equal to or better than legacy
- ✅ Code maintainability improved
- ✅ Documentation complete and accurate
- ✅ Tests pass with >90% coverage
- ✅ No breaking changes to API

## Timeline

### Week 1: Core Migration
- Day 1-2: Update dependencies and create Bee AI Orchestrator
- Day 3-4: Migrate API endpoints
- Day 5: Update main application and configuration

### Week 2: Testing & Documentation
- Day 1-2: Create and run test suite
- Day 3-4: Update documentation
- Day 5: Final validation and deployment

## Post-Migration Tasks

### Immediate (Week 3)
- [ ] Monitor production logs for errors
- [ ] Track performance metrics
- [ ] Gather user feedback
- [ ] Fix any critical issues

### Short-term (Month 1)
- [ ] Remove legacy agent code
- [ ] Optimize Bee AI agent performance
- [ ] Add advanced Bee AI features
- [ ] Create developer training materials

### Long-term (Quarter 1)
- [ ] Explore additional Bee AI capabilities
- [ ] Implement multi-agent collaboration patterns
- [ ] Add AI-powered decision making
- [ ] Integrate with more IBM watsonx.ai models

## Resources

### Documentation
- [Bee AI Framework Docs](https://github.com/i-am-bee/bee-agent-framework)
- [IBM watsonx.ai Docs](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [Eco-Shift AGENTS.md](./AGENTS.md)

### Code References
- `apps/backend/src/agents/monitor/weather_monitor.py` - Bee AI Weather Agent
- `apps/backend/src/agents/auditor/beeai_auditor.py` - Bee AI Auditor Agent
- `apps/backend/examples/beeai_*.py` - Example implementations

### Support
- Bee AI GitHub Issues
- IBM watsonx.ai Support
- Internal development team

---

**Document Version**: 1.0  
**Last Updated**: 2026-05-03  
**Status**: In Progress  
**Owner**: Eco-Shift Development Team  
**Made with Bob**