"""
Orchestrator Agent Configuration

This module contains configuration settings for the Orchestrator Agent,
which coordinates the Monitor and Auditor agents.
"""

import os
from typing import Dict, Any
from pydantic import BaseModel, Field


class OrchestratorConfig(BaseModel):
    """Configuration for the Orchestrator Agent"""
    
    # Agent settings
    enabled: bool = Field(
        default=True,
        description="Whether the orchestrator is enabled"
    )
    
    max_retries: int = Field(
        default=int(os.getenv("ORCHESTRATOR_MAX_RETRIES", "3")),
        description="Maximum number of retries for failed operations"
    )
    
    retry_delay: int = Field(
        default=int(os.getenv("ORCHESTRATOR_RETRY_DELAY", "5")),
        description="Delay in seconds between retries"
    )
    
    timeout: int = Field(
        default=int(os.getenv("ORCHESTRATOR_TIMEOUT", "30")),
        description="Timeout in seconds for agent operations"
    )
    
    # Message bus settings
    message_queue_size: int = Field(
        default=1000,
        description="Maximum size of the message queue"
    )
    
    message_ttl: int = Field(
        default=3600,
        description="Time-to-live for messages in seconds"
    )
    
    # Agent coordination settings
    monitor_check_interval: int = Field(
        default=int(os.getenv("MONITOR_CHECK_INTERVAL", "300")),
        description="Interval in seconds for monitor agent checks"
    )
    
    auditor_batch_size: int = Field(
        default=10,
        description="Number of vendors to process in a single batch"
    )
    
    # Workflow settings
    auto_start_agents: bool = Field(
        default=True,
        description="Automatically start child agents on orchestrator start"
    )
    
    parallel_execution: bool = Field(
        default=True,
        description="Enable parallel execution of agent tasks"
    )
    
    # Logging settings
    log_level: str = Field(
        default=os.getenv("LOG_LEVEL", "INFO"),
        description="Logging level for the orchestrator"
    )
    
    log_agent_messages: bool = Field(
        default=True,
        description="Log all inter-agent messages"
    )
    
    class Config:
        env_prefix = "ORCHESTRATOR_"


# Default configuration instance
config = OrchestratorConfig()


def get_config() -> OrchestratorConfig:
    """Get the orchestrator configuration"""
    return config


def update_config(updates: Dict[str, Any]) -> OrchestratorConfig:
    """Update configuration with new values"""
    global config
    for key, value in updates.items():
        if hasattr(config, key):
            setattr(config, key, value)
    return config

# Made with Bob
