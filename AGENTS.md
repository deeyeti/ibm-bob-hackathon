# AGENTS.md

This file provides guidance to AI agents when working with the Eco-Shift codebase. It focuses on non-obvious architectural decisions, project-specific patterns, and critical gotchas.

## Project Overview

**Eco-Shift** is a multi-agent logistics optimization platform that uses IBM watsonx.ai and real-time weather data to reduce carbon emissions in supply chains. The system employs three coordinating agents (Monitor, Auditor, Orchestrator) powered by the **IBM Bee AI framework**.

**Key Technologies:**
- Frontend: Next.js 14.2.3 (App Router), React 18.3.1, TypeScript 5.4.5, Tailwind CSS 3.4.3, GSAP 3.12.5
- Backend: Python 3.10+, FastAPI 0.109.0+, Pydantic 2.5.3+, IBM watsonx.ai 0.2.6+
- **Agent Framework: IBM Bee AI framework (with legacy fallback support)**
- APIs: OpenWeather API, IBM watsonx.ai (Granite/Llama models)

**🆕 BeeAI Framework Integration:**
The system now uses the IBM Bee AI framework for agent implementation, providing:
- Modern tool-based architecture
- Enhanced AI integration with watsonx.ai
- Better error handling and lifecycle management
- Backward compatibility with legacy agents

## Build, Test, and Lint Commands

### Root-Level Commands (from workspace root)
```bash
# Development
npm run dev                    # Start both frontend and backend concurrently
npm run dev:frontend           # Frontend only (port 3000)
npm run dev:backend            # Backend only (port 8000)

# Building
npm run build                  # Build both apps
npm run build:frontend         # Next.js production build
npm run build:backend          # Install Python dependencies

# Testing
npm run test                   # Run all tests (frontend + backend)
npm run test:frontend          # Jest tests for frontend
npm run test:backend           # pytest for backend
npm run test:watch             # Frontend tests in watch mode

# Code Quality
npm run lint                   # Lint both apps
npm run lint:frontend          # ESLint for frontend
npm run lint:backend           # flake8 for backend (src/ and tests/)
npm run format                 # Format both apps
npm run format:frontend        # Prettier for frontend
npm run format:backend         # Black for backend
npm run type-check             # TypeScript type checking

# Docker
npm run docker:build           # Build Docker images
npm run docker:up              # Start containers
npm run docker:down            # Stop containers
npm run docker:logs            # View logs
npm run docker:clean           # Remove containers and volumes

# Agent Management
npm run agents:status          # Check agent statuses
npm run agents:start           # Start all agents
npm run agents:stop            # Stop all agents

# Utilities
npm run health                 # Check health of both services
npm run logs                   # Tail backend logs
```

### Frontend Commands (from `apps/frontend/`)
```bash
npm run dev                    # Development server (port 3000)
npm run build                  # Production build
npm run start                  # Start production server
npm run lint                   # ESLint
npm run type-check             # TypeScript checking
npm run format                 # Prettier formatting
```

### Backend Commands (from `apps/backend/`)
```bash
# Development
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Testing
pytest                         # Run all tests
pytest --cov=src              # With coverage
pytest -v                      # Verbose output
pytest tests/unit/            # Unit tests only
pytest tests/integration/     # Integration tests only

# Code Quality
flake8 src/ tests/            # Linting
black src/ tests/             # Formatting
isort src/ tests/             # Import sorting
mypy src/                     # Type checking
```

## Code Style Guidelines

### TypeScript/React (Frontend)
- **Line length:** 100 characters (Prettier default)
- **Import order:** React imports → Third-party → Local components → Utils → Types
- **Component structure:** Functional components with TypeScript interfaces
- **File naming:** `kebab-case.tsx` for components, `camelCase.ts` for utilities
- **Type definitions:** Use interfaces for props, types for unions/intersections
- **Async operations:** Use React hooks (useState, useEffect) with proper cleanup

### Python (Backend)
- **Line length:** 100 characters (Black configuration)
- **Import order:** Standard library → Third-party → Local imports (enforced by isort with Black profile)
- **Type hints:** Required for all function signatures (mypy strict mode)
- **Docstrings:** Google-style docstrings for all public functions/classes
- **Async/await:** Use async/await for all I/O operations
- **Error handling:** Use custom exceptions, log with structured logging

### Naming Conventions
- **Python:** `snake_case` for functions/variables, `PascalCase` for classes
- **TypeScript:** `camelCase` for functions/variables, `PascalCase` for components/types
- **Constants:** `UPPER_SNAKE_CASE` in both languages
- **Private methods:** Prefix with `_` in Python

## Architecture-Specific Rules (NON-OBVIOUS)

### Agent Communication via Message Bus
**Critical:** Agents communicate through `apps/backend/src/agents/orchestrator/message_bus.py`, NOT direct function calls.

**Message Bus Patterns:**
- **Publish-Subscribe:** Use `publish()` for broadcasting to all subscribers of a message type
- **Direct Send:** Use `send()` for targeted messages to specific agents (requires `recipient` field)
- **Request-Response:** Use `request()` with `correlation_id` for synchronous-style communication
- **Priority Queuing:** Messages use negative priority values internally (-4 to -1) for correct ordering

**Message TTL:** Default 3600 seconds. Messages expire and are cleaned up every 60 seconds. Set custom TTL for time-sensitive operations.

**Queue Size:** Max 1000 messages per agent queue. Exceeding this drops messages with error log.

### Monitor and Auditor Agent Interaction
**Workflow Pattern:**
1. Monitor Agent polls weather every 300 seconds (configurable via `agent_polling_interval`)
2. Severe weather triggers `MessageType.WEATHER_ALERT` with `MessagePriority.HIGH`
3. Orchestrator receives alert and publishes `MessageType.AUDIT_REQUEST` to Auditor
4. Auditor processes request and publishes `MessageType.AUDIT_RESULT`
5. Orchestrator aggregates results for frontend API

**Weather Cache:** Monitor Agent caches weather data for 300 seconds (5 minutes) to avoid API rate limits. Cache is location-specific and checked before each API call.

**Alert Cooldown:** Weather alerts have 1800-second (30-minute) cooldown per location to prevent spam. Tracked in `_alert_history` dict.

### Orchestrator Workflow Patterns
**Lifecycle Management:**
- Agents are NOT automatically started on backend startup
- Must explicitly call `orchestrator.start_agents()` or use CLI commands
- Each agent runs in its own asyncio task
- Graceful shutdown requires `orchestrator.stop_agents()` to cancel tasks

**Error Handling:**
- Failed agent tasks are logged but don't crash the orchestrator
- Use `MessageType.ERROR` for agent-level errors
- Orchestrator maintains agent status in memory (not persisted)

### API Integration Between Frontend and Backend
**Proxy Pattern:** Frontend uses Next.js API routes (`apps/frontend/src/app/api/`) as proxies to backend. This hides backend URL and enables server-side auth.

**Base URL Configuration:**
- Frontend: `NEXT_PUBLIC_API_URL` (default: `http://localhost:8000`)
- Backend: `cors_origins` setting (default: `http://localhost:3000,http://localhost:3001`)

**API Client:** `apps/frontend/src/lib/api.ts` uses axios with 30-second timeout. All requests include error handling with structured error objects.

### Environment Variable Requirements
**Critical Dependencies:**
- `WATSONX_API_KEY` and `WATSONX_PROJECT_ID` - Required for Auditor Agent AI recommendations
- `OPENWEATHER_API_KEY` - Required for Monitor Agent weather data
- Backend fails gracefully if keys missing, but agents won't function

**Optional but Recommended:**
- `WATSONX_MODEL_ID` - Defaults to `ibm/granite-13b-chat-v2` if not set
- `LOG_LEVEL` - Defaults to `INFO`, use `DEBUG` for development

**CORS Configuration:** `cors_origins` must include frontend URL or requests will fail. Comma-separated string, not array.

### Configuration Dependencies
**Settings Cascade:**
1. Environment variables (`.env` files)
2. `apps/backend/src/config/settings.py` defaults
3. Agent-specific configs in `apps/backend/src/agents/*/config.py`

**Agent Configs:** Each agent has its own config class (e.g., `MonitorConfig`, `AuditorConfig`) that can override global settings. These are NOT loaded from environment variables directly.

## Agent System Details (NON-OBVIOUS)

### Agent Lifecycle Management
**Initialization Order:**
1. Message bus must be initialized first: `await initialize_message_bus()`
2. Create agent instances (they auto-subscribe to message bus)
3. Start agents: `await agent.start()`
4. Agents run in background asyncio tasks until stopped

**Shutdown Order:**
1. Stop agents: `await agent.stop()`
2. Shutdown message bus: `await shutdown_message_bus()`
3. Close external service connections (weather service, watsonx client)

### Message Bus Usage Patterns
**Subscription Pattern:**
```python
# Subscribe to message type
message_bus.subscribe("weather_alert", callback_function)

# Callback receives Message object
async def callback_function(message: Message):
    payload = message.payload
    # Process message
```

**Publishing Pattern:**
```python
# Create message
message = Message(
    type=MessageType.WEATHER_ALERT,
    sender="monitor_agent",
    payload={"location": "New York", "severity": "high"},
    priority=MessagePriority.HIGH,
    ttl=1800  # 30 minutes
)

# Publish to all subscribers
await message_bus.publish(message)
```

**Request-Response Pattern:**
```python
# Send request and wait for response
request = Message(
    type=MessageType.AUDIT_REQUEST,
    sender="orchestrator",
    recipient="auditor_agent",
    payload={"vendors": vendor_list}
)

response = await message_bus.request(request, timeout=30.0)
result = response.payload
```

### How to Add New Agents
1. Create directory in `apps/backend/src/agents/new_agent/`
2. Extend `BaseAgent` class from `apps/backend/src/agents/base_agent.py`
3. Implement `start()`, `stop()`, and main logic methods
4. Create agent-specific config in `config.py`
5. Register with orchestrator in `apps/backend/src/agents/orchestrator/orchestrator_agent.py`
6. Add message type to `MessageType` enum if needed
7. Subscribe to relevant message types in agent's `start()` method

### Agent Configuration Patterns
**Config Classes:** Use Pydantic BaseModel for type safety and validation
```python
class NewAgentConfig(BaseModel):
    enabled: bool = True
    polling_interval: int = 300
    custom_setting: str = "default"
```

**Loading Configs:** Configs are instantiated at agent creation, not loaded from env vars. Override defaults by passing config instance to agent constructor.

### Error Handling in Agent Workflows
**Agent-Level Errors:**
- Catch exceptions in agent methods
- Log with structured logging: `logger.error(f"Error: {e}", exc_info=True)`
- Publish `MessageType.ERROR` message to notify orchestrator
- Don't let exceptions crash the agent task

**Message Bus Errors:**
- Subscriber callback exceptions are caught and logged by message bus
- Failed message delivery logs error but doesn't raise exception
- Expired messages are silently dropped with debug log

## Development Workflow

### Starting the Full Stack
```bash
# Option 1: Using npm scripts (recommended)
npm run dev

# Option 2: Manual start
# Terminal 1 - Backend
cd apps/backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd apps/frontend
npm run dev

# Option 3: Docker
npm run docker:up
```

### Testing Individual Agents
```bash
# From apps/backend/
python -m pytest tests/unit/test_agents.py -v

# Test specific agent
python -m pytest tests/unit/test_agents.py::TestMonitorAgent -v

# Run agent directly (for debugging)
python -m src.agents.monitor.monitor_agent
```

### Debugging Agent Communication
**View Message History:**
```python
from src.agents.orchestrator.message_bus import get_message_bus

message_bus = get_message_bus()
history = message_bus.get_message_history(limit=50)
print(history)
```

**Check Message Bus Stats:**
```python
stats = message_bus.get_stats()
# Returns: subscribers, queue sizes, pending responses, history size
```

**Enable Debug Logging:**
Set `LOG_LEVEL=DEBUG` in `.env` to see detailed message bus activity.

### Common Development Tasks
**Add New API Endpoint:**
1. Create route in `apps/backend/src/api/` (e.g., `new_feature.py`)
2. Import and include router in `apps/backend/src/main.py`
3. Add Pydantic schemas in `apps/backend/src/models/schemas.py`
4. Update frontend API client in `apps/frontend/src/lib/api.ts`

**Add New Frontend Component:**
1. Create component in `apps/frontend/src/components/`
2. Use TypeScript interfaces for props
3. Import types from `apps/frontend/src/types/index.ts`
4. Use Tailwind CSS for styling
5. Add GSAP animations via `apps/frontend/src/lib/animations.ts`

## Critical Gotchas (NON-OBVIOUS)

### Hydrogen Fleet Prioritization (10x Multiplier)
**CRITICAL:** In `apps/backend/src/agents/auditor/fleet_prioritizer.py`, hydrogen fleets receive a **10x score multiplier** (line 124-126). This is intentional and central to the business logic.

```python
if fleet_type == "hydrogen":
    fleet_type_score *= 10.0  # 10x multiplier for hydrogen
```

This means hydrogen fleets will almost always rank first unless they have catastrophically bad other metrics. Don't "fix" this - it's by design.

### Emissions Calculation Specifics
**Baseline Calculation:** Emissions reduction percentage is calculated against a diesel baseline (2.68 kg CO2e per liter). Found in `apps/backend/src/agents/auditor/emissions_calculator.py`.

**Fuel Type Factors:**
- Diesel: 2.68 kg CO2e/L
- Petrol: 2.31 kg CO2e/L
- Electric: 0.0 kg CO2e (direct emissions only)
- Hybrid: 1.34 kg CO2e/L (50% reduction)
- Hydrogen: 0.0 kg CO2e (direct emissions only)

**Scope 3 Emissions:** System calculates transportation emissions only. Does not include manufacturing, maintenance, or end-of-life emissions.

### Weather Polling Intervals and Caching
**Polling Interval:** Default 300 seconds (5 minutes) set in `settings.py` as `agent_polling_interval`.

**Cache Duration:** Weather data cached for 300 seconds (5 minutes) in `WeatherMonitor._cache`. This is SEPARATE from polling interval.

**Race Condition:** If multiple requests hit the same location within cache window, only the first fetches from API. Others use cached data. This is intentional to avoid rate limits.

**Cache Invalidation:** No automatic invalidation. Cache entries expire based on timestamp. Use `weather_monitor.clear_cache()` to force refresh.

### API Rate Limiting Considerations
**OpenWeather Free Tier:** 60 calls/minute, 1,000,000 calls/month. Monitor Agent adds 0.5-second delay between location checks to stay under limit.

**watsonx.ai Rate Limits:** Varies by plan. No built-in rate limiting in code. Implement retry logic with exponential backoff if needed.

**Message Bus Queue Full:** If agent queue exceeds 1000 messages, new messages are dropped with error log. This can happen if agent is slow or stopped. Monitor queue sizes via `get_stats()`.

### watsonx.ai Integration Requirements
**Model ID:** Default is `ibm/granite-13b-chat-v2` but can be overridden via `WATSONX_MODEL_ID` env var.

**Project ID Required:** `WATSONX_PROJECT_ID` is mandatory. Requests fail without it. No fallback.

**URL Configuration:** Default is `https://us-south.ml.cloud.ibm.com`. Change via `WATSONX_URL` for different regions.

**Async Operations:** watsonx service in `apps/backend/src/services/watsonx_service.py` uses synchronous IBM SDK. Wrap calls in `asyncio.to_thread()` for async compatibility.

**Token Limits:** Granite models have token limits. Long prompts may be truncated. Monitor response for truncation warnings.

### TypeScript Path Aliases
Frontend uses path aliases configured in `tsconfig.json`:
- `@/components/*` → `src/components/*`
- `@/lib/*` → `src/lib/*`
- `@/types/*` → `src/types/*`

These work in Next.js but may not work in test files without additional Jest configuration.

### Pydantic V2 Breaking Changes
Backend uses Pydantic V2 (2.5.3+). Key differences from V1:
- `.dict()` is now `.model_dump()`
- `.parse_obj()` is now `.model_validate()`
- Config is now `model_config` dict, not nested `Config` class
- Validators use `@field_validator` decorator, not `@validator`

### Message Bus Priority Queue Gotcha
Priority queue uses NEGATIVE priority values internally (line 301 in `message_bus.py`):
```python
priority = -message.priority.value  # Negative for correct ordering
```

This means `MessagePriority.CRITICAL` (value 4) becomes -4 in queue, ensuring it's processed first. Don't change this without understanding asyncio.PriorityQueue behavior.

### CORS Configuration Format
`cors_origins` in settings is a COMMA-SEPARATED STRING, not a list. The `@validator` converts it to a list at runtime (line 119 in `settings.py`). Don't pass a list directly to the Settings constructor.

### Agent Status Not Persisted
Agent status (running/stopped) is stored in memory only. Restarting the backend resets all agent states. Implement database persistence if needed for production.

---

**Last Updated:** 2026-05-02  
**Maintained By:** Eco-Shift Development Team
# ============================================================================
# BeeAI Framework Integration
# ============================================================================

## BeeAI Agent Architecture

The Eco-Shift system now uses the **IBM Bee AI framework** for agent implementation. This provides a modern, tool-based architecture with enhanced AI capabilities.

### BeeAI vs Legacy Agents

| Feature | BeeAI Agents | Legacy Agents |
|---------|--------------|---------------|
| Framework | IBM Bee AI | Custom |
| Tools | Modular tool system | Integrated methods |
| AI Integration | Built-in watsonx.ai | Manual integration |
| Extensibility | Easy to add tools | Requires code changes |
| Error Handling | Framework-managed | Manual |
| Lifecycle | Framework-managed | Manual |

### BeeAI Agent Components

#### 1. BeeAIWeatherMonitorAgent
**Location**: `apps/backend/src/agents/monitor/weather_monitor.py`

**Tools**:
- `WeatherCheckTool` - Checks current weather conditions
- `VendorRetrievalTool` - Retrieves eco-friendly vendors

**Usage**:
```python
from src.agents.monitor.weather_monitor import BeeAIWeatherMonitorAgent

agent = BeeAIWeatherMonitorAgent(
    target_location="New York,US",
    api_key=os.getenv("OPENWEATHER_API_KEY")
)

result = await agent.check_weather()
# Returns: {status, weather/reason, alternative_vendors}
```

**Response Format**:
```json
{
  "status": "reroute_required",
  "reason": "heavy thunderstorm",
  "alternative_vendors": [...]
}
```

#### 2. BeeAIAuditorAgent
**Location**: `apps/backend/src/agents/auditor/beeai_auditor.py`

**Tools**:
- `EmissionsCalculationTool` - Calculates emissions using watsonx.ai

**Usage**:
```python
from src.agents.auditor.beeai_auditor import BeeAIAuditorAgent

agent = BeeAIAuditorAgent()

result = await agent.analyze_vendors({
    "vendors": vendor_list,
    "location": "New York,US"
})
# Returns: {approved_vendor_id, emissions_saving, justification}
```

**Response Format**:
```json
{
  "status": "success",
  "approved_vendor_id": "vendor_001",
  "emissions_saving": "100% (zero direct emissions)",
  "justification": "Selected hydrogen fleet...",
  "vendors_analyzed": 4
}
```

#### 3. Enhanced Orchestrator
**Location**: `apps/backend/src/agents/orchestrator/orchestrator_agent.py`

**Features**:
- Coordinates BeeAI agents
- Backward compatible with legacy agents
- Automatic response format detection
- Feature flag controlled

**Configuration**:
```python
# Enable BeeAI agents (default)
config = OrchestratorConfig(use_beeai=True)

# Or via environment variable
USE_BEEAI=true
```

### BeeAI Configuration

#### Environment Variables
```bash
# BeeAI Framework
USE_BEEAI=true                    # Enable BeeAI agents
BEEAI_LOG_LEVEL=INFO              # BeeAI logging level
BEEAI_TIMEOUT=30                  # Agent timeout (seconds)

# Required API Keys
OPENWEATHER_API_KEY=your_key      # Weather data
WATSONX_API_KEY=your_key          # IBM watsonx.ai
WATSONX_PROJECT_ID=your_project   # watsonx.ai project
```

#### Settings Configuration
```python
# apps/backend/src/config/settings.py
use_beeai: bool = True            # Use BeeAI framework
beeai_log_level: str = "INFO"     # Logging level
beeai_timeout: int = 30           # Timeout in seconds
```

### BeeAI Workflow Patterns

#### Pattern 1: Weather Monitoring → Vendor Analysis
```python
# 1. Check weather
weather_agent = BeeAIWeatherMonitorAgent()
weather_result = await weather_agent.check_weather()

# 2. If reroute required, analyze vendors
if weather_result["status"] == "reroute_required":
    auditor_agent = BeeAIAuditorAgent()
    audit_result = await auditor_agent.analyze_vendors({
        "vendors": weather_result["alternative_vendors"]
    })
    
    # 3. Use approved vendor
    approved_vendor = audit_result["approved_vendor_id"]
```

#### Pattern 2: Orchestrated Workflow
```python
# Orchestrator handles the complete workflow
orchestrator = OrchestratorAgent(config=OrchestratorConfig(use_beeai=True))
await orchestrator.initialize()

# Run workflow
result = await orchestrator.execute()
# Returns: {weather_data, audit_results, recommendations}
```

### BeeAI Tool Development

#### Creating a New Tool
```python
from bee_agent.tools.base import Tool

class MyCustomTool(Tool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="Tool description",
            input_schema={
                "type": "object",
                "properties": {
                    "param": {"type": "string"}
                },
                "required": ["param"]
            }
        )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Tool logic here
        return {
            "success": True,
            "data": {...}
        }
```

#### Adding Tool to Agent
```python
agent = BeeAgent(
    name="MyAgent",
    description="Agent description",
    tools=[MyCustomTool(), OtherTool()],
    system_prompt="Agent instructions..."
)
```

### BeeAI Best Practices

1. **Use Environment Variables**: Store API keys in `.env` files
2. **Handle Errors Gracefully**: BeeAI provides built-in error handling
3. **Close Resources**: Always call `agent.close()` when done
4. **Monitor Logs**: Set `BEEAI_LOG_LEVEL=DEBUG` for detailed logging
5. **Test Tools Independently**: Test each tool before integrating

### BeeAI Troubleshooting

#### Issue: "BeeAI framework not available"
**Solution**: Install the framework
```bash
pip install bee-agent-framework
```

#### Issue: Type errors about BeeAI imports
**Solution**: These are cosmetic if BeeAI is not installed. The code has fallback implementations.

#### Issue: Agent timeout
**Solution**: Increase timeout in configuration
```python
config = OrchestratorConfig(beeai_timeout=60)
```

### BeeAI Migration Status

✅ **Complete** - All agents migrated to BeeAI framework
- Monitor Agent: BeeAIWeatherMonitorAgent
- Auditor Agent: BeeAIAuditorAgent  
- Orchestrator: Enhanced with BeeAI support
- Configuration: Feature flags added
- Documentation: Comprehensive guides created

**Migration Documents**:
- `BEEAI_MIGRATION_PLAN.md` - Migration strategy
- `BEEAI_MIGRATION_COMPLETE.md` - Implementation summary
- `apps/backend/src/agents/monitor/BEEAI_WEATHER_AGENT.md` - Weather agent docs
- `apps/backend/src/agents/auditor/BEEAI_AUDITOR.md` - Auditor agent docs

### BeeAI Resources

- [Bee AI Framework](https://github.com/i-am-bee/bee-agent-framework)
- [IBM watsonx.ai](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [Example Scripts](apps/backend/examples/)

---
