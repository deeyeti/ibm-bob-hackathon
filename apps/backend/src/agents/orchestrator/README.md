# Orchestrator Agent

The Orchestrator Agent is the central coordinator for the Eco-Shift system, managing the workflow between the Monitor and Auditor agents to provide intelligent logistics optimization.

## Overview

The Orchestrator Agent:
- Coordinates workflow between Monitor and Auditor agents
- Manages agent lifecycle (initialization, start, stop, cleanup)
- Handles inter-agent communication via message bus
- Aggregates results for frontend consumption
- Implements retry logic and error handling
- Provides unified API for the system

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator Agent                        │
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │   Monitor    │◄────────┤  Message Bus │                 │
│  │    Agent     │         │              │                 │
│  └──────────────┘         └──────────────┘                 │
│         │                        ▲                          │
│         │                        │                          │
│         ▼                        │                          │
│  ┌──────────────┐               │                          │
│  │   Auditor    │───────────────┘                          │
│  │    Agent     │                                           │
│  └──────────────┘                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Orchestrator Agent (`orchestrator_agent.py`)

Main coordinator that:
- Initializes and manages child agents
- Executes the main workflow
- Handles weather alerts and triggers audits
- Provides status and results to the API

**Key Methods:**
- `initialize()` - Set up orchestrator and child agents
- `execute()` - Run the main workflow
- `start()` - Start orchestrator and child agents
- `stop()` - Stop all agents
- `get_info()` - Get orchestrator status
- `get_latest_results()` - Get cached results
- `trigger_manual_audit()` - Manually trigger an audit

### 2. Message Bus (`message_bus.py`)

Inter-agent communication system that supports:
- Publish-subscribe pattern
- Message queuing with priorities
- Request-response patterns
- Message expiration (TTL)
- Message history for debugging

**Message Types:**
- `WEATHER_ALERT` - Weather condition alerts
- `VENDOR_LIST` - List of vendors
- `AUDIT_REQUEST` - Request for audit
- `AUDIT_RESULT` - Audit results
- `OPTIMIZATION_REQUEST` - Optimization request
- `OPTIMIZATION_RESULT` - Optimization results
- `AGENT_STATUS` - Agent status updates
- `ERROR` - Error messages
- `COMMAND` - Control commands

**Message Priorities:**
- `CRITICAL` - Highest priority
- `HIGH` - High priority
- `NORMAL` - Normal priority
- `LOW` - Lowest priority

### 3. Configuration (`config.py`)

Configuration settings for the orchestrator:
- Retry settings (max retries, delay)
- Timeout settings
- Message bus configuration
- Agent coordination settings
- Logging configuration

## Workflow

### Standard Workflow

1. **Weather Check**
   - Orchestrator triggers Monitor Agent
   - Monitor checks weather conditions for all vendor locations
   - Returns weather data and alerts

2. **Audit Decision**
   - Orchestrator analyzes weather data
   - Determines if audit is needed based on alerts
   - Identifies affected vendors

3. **Audit Execution** (if needed)
   - Orchestrator triggers Auditor Agent with affected vendors
   - Auditor calculates emissions and optimizes routes
   - Returns optimization recommendations

4. **Result Aggregation**
   - Orchestrator collects and caches results
   - Makes results available to frontend via API

### Event-Driven Workflow

The orchestrator also responds to events:
- Weather alerts trigger automatic audits
- Manual audit requests from frontend
- Agent status changes
- Error conditions

## Usage

### Basic Usage

```python
from src.agents.orchestrator import initialize_orchestrator, get_orchestrator

# Initialize and start
orchestrator = await initialize_orchestrator()

# Run workflow
results = await orchestrator.run()

# Get latest results
latest = await orchestrator.get_latest_results()

# Trigger manual audit
audit_results = await orchestrator.trigger_manual_audit(vendor_ids=["V001", "V002"])

# Get status
info = orchestrator.get_info()

# Shutdown
await orchestrator.cleanup()
```

### With Custom Configuration

```python
from src.agents.orchestrator import OrchestratorConfig, initialize_orchestrator

config = OrchestratorConfig(
    max_retries=5,
    retry_delay=10,
    timeout=60,
    auto_start_agents=True
)

orchestrator = await initialize_orchestrator(config)
```

### Using Message Bus

```python
from src.agents.orchestrator import get_message_bus, Message, MessageType

# Get message bus
bus = get_message_bus()

# Subscribe to messages
async def handle_alert(message: Message):
    print(f"Alert received: {message.payload}")

bus.subscribe(MessageType.WEATHER_ALERT.value, handle_alert)

# Publish a message
message = Message(
    type=MessageType.WEATHER_ALERT,
    sender="monitor",
    payload={"severity": "high", "location": "Mumbai"}
)
await bus.publish(message)

# Request-response pattern
response = await bus.request(message, timeout=30.0)
```

## API Integration

The orchestrator is integrated with the FastAPI backend:

```python
# In src/api/agents.py
from src.agents.orchestrator import get_orchestrator

@router.get("/orchestrator/status")
async def get_orchestrator_status():
    orchestrator = get_orchestrator()
    return orchestrator.get_info()

@router.post("/orchestrator/run")
async def run_orchestrator():
    orchestrator = get_orchestrator()
    results = await orchestrator.run()
    return results

@router.get("/orchestrator/results")
async def get_latest_results():
    orchestrator = get_orchestrator()
    return await orchestrator.get_latest_results()

@router.post("/orchestrator/audit")
async def trigger_audit(vendor_ids: Optional[List[str]] = None):
    orchestrator = get_orchestrator()
    return await orchestrator.trigger_manual_audit(vendor_ids)
```

## Configuration

Environment variables (in `.env`):

```bash
# Orchestrator settings
ORCHESTRATOR_MAX_RETRIES=3
ORCHESTRATOR_RETRY_DELAY=5
ORCHESTRATOR_TIMEOUT=30

# Message bus settings
ORCHESTRATOR_MESSAGE_QUEUE_SIZE=1000
ORCHESTRATOR_MESSAGE_TTL=3600

# Agent coordination
MONITOR_CHECK_INTERVAL=300
AUDITOR_BATCH_SIZE=10
```

## Error Handling

The orchestrator implements comprehensive error handling:

1. **Retry Logic**: Failed operations are retried with exponential backoff
2. **Timeout Protection**: All operations have configurable timeouts
3. **Error Messages**: Errors are published to the message bus
4. **Graceful Degradation**: System continues operating even if one agent fails
5. **Logging**: All errors are logged with full context

## Monitoring

Monitor orchestrator health:

```python
# Get orchestrator info
info = orchestrator.get_info()

# Check message bus stats
stats = orchestrator.message_bus.get_stats()

# View message history
history = orchestrator.message_bus.get_message_history(limit=50)
```

## Testing

```python
import pytest
from src.agents.orchestrator import OrchestratorAgent

@pytest.mark.asyncio
async def test_orchestrator_workflow():
    orchestrator = OrchestratorAgent()
    await orchestrator.initialize()
    
    results = await orchestrator.run()
    
    assert results["status"] == "completed"
    assert "steps" in results
    
    await orchestrator.cleanup()
```

## Best Practices

1. **Always initialize before use**: Call `initialize()` before running workflows
2. **Clean up resources**: Call `cleanup()` when done
3. **Handle errors**: Wrap orchestrator calls in try-except blocks
4. **Monitor status**: Regularly check orchestrator and agent status
5. **Use message bus**: Leverage the message bus for loose coupling
6. **Configure appropriately**: Adjust timeouts and retries for your environment

## Troubleshooting

### Orchestrator won't start
- Check that all dependencies are installed
- Verify environment variables are set
- Check logs for initialization errors

### Agents not responding
- Verify agents are initialized
- Check message bus status
- Review agent logs

### Workflow timeouts
- Increase `ORCHESTRATOR_TIMEOUT`
- Check network connectivity
- Verify external API availability (OpenWeather, watsonx)

### Memory issues
- Reduce `ORCHESTRATOR_MESSAGE_QUEUE_SIZE`
- Decrease message history size
- Check for message bus leaks

## Future Enhancements

- [ ] Add support for more agent types
- [ ] Implement distributed orchestration
- [ ] Add workflow persistence
- [ ] Support for complex workflow DAGs
- [ ] Enhanced monitoring and metrics
- [ ] Workflow visualization
- [ ] A/B testing support
- [ ] Canary deployments

## Contributing

When contributing to the orchestrator:
1. Follow the existing code structure
2. Add comprehensive tests
3. Update documentation
4. Handle errors gracefully
5. Log important events
6. Consider backward compatibility

## License

MIT License - See LICENSE file for details