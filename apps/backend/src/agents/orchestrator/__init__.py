"""
Orchestrator Agent Module

This module provides the orchestrator agent that coordinates the Monitor and Auditor agents.
"""

from .orchestrator_agent import (
    OrchestratorAgent,
    get_orchestrator,
    initialize_orchestrator,
    shutdown_orchestrator
)
from .message_bus import (
    MessageBus,
    Message,
    MessageType,
    MessagePriority,
    get_message_bus,
    initialize_message_bus,
    shutdown_message_bus
)
from .config import (
    OrchestratorConfig,
    get_config,
    update_config
)

__all__ = [
    # Orchestrator
    "OrchestratorAgent",
    "get_orchestrator",
    "initialize_orchestrator",
    "shutdown_orchestrator",
    # Message Bus
    "MessageBus",
    "Message",
    "MessageType",
    "MessagePriority",
    "get_message_bus",
    "initialize_message_bus",
    "shutdown_message_bus",
    # Config
    "OrchestratorConfig",
    "get_config",
    "update_config",
]

# Made with Bob
