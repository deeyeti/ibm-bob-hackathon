"""
Base agent class for Eco-Shift agents.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

from src.utils.logger import get_logger

logger = get_logger(__name__)


class AgentStatus(str, Enum):
    """Agent status enumeration."""
    IDLE = "idle"
    RUNNING = "running"
    ERROR = "error"
    STOPPED = "stopped"


class BaseAgent(ABC):
    """Base class for all Eco-Shift agents."""

    def __init__(self, agent_id: str, name: str, agent_type: str):
        """
        Initialize base agent.

        Args:
            agent_id: Unique agent identifier
            name: Human-readable agent name
            agent_type: Type of agent (monitor/auditor/orchestrator)
        """
        self.agent_id = agent_id
        self.name = name
        self.agent_type = agent_type
        self.status = AgentStatus.IDLE
        self.last_run: Optional[datetime] = None
        self.next_run: Optional[datetime] = None
        self.metrics: Dict[str, Any] = {}
        self._initialized = False

        logger.info(f"Agent initialized: {self.name} ({self.agent_id})")

    @abstractmethod
    async def initialize(self) -> None:
        """
        Initialize agent resources and dependencies.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    async def execute(self) -> Dict[str, Any]:
        """
        Execute agent's main task.
        Must be implemented by subclasses.

        Returns:
            Dictionary with execution results
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """
        Cleanup agent resources.
        Must be implemented by subclasses.
        """
        pass

    async def start(self) -> None:
        """Start the agent."""
        if not self._initialized:
            await self.initialize()
            self._initialized = True

        self.status = AgentStatus.RUNNING
        logger.info(f"Agent started: {self.name}")

    async def stop(self) -> None:
        """Stop the agent."""
        self.status = AgentStatus.STOPPED
        await self.cleanup()
        logger.info(f"Agent stopped: {self.name}")

    async def run(self) -> Dict[str, Any]:
        """
        Run the agent's execution cycle.

        Returns:
            Execution results
        """
        try:
            self.status = AgentStatus.RUNNING
            self.last_run = datetime.utcnow()

            logger.info(f"Running agent: {self.name}")
            result = await self.execute()

            self.status = AgentStatus.IDLE
            self.metrics["last_execution_time"] = (
                datetime.utcnow() - self.last_run
            ).total_seconds()

            return result

        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"Agent execution failed: {self.name} - {e}")
            raise

    def get_info(self) -> Dict[str, Any]:
        """
        Get agent information.

        Returns:
            Dictionary with agent details
        """
        return {
            "id": self.agent_id,
            "name": self.name,
            "type": self.agent_type,
            "status": self.status.value,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "metrics": self.metrics,
        }

    def update_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Update agent metrics.

        Args:
            metrics: Dictionary of metrics to update
        """
        self.metrics.update(metrics)
        logger.debug(f"Metrics updated for {self.name}: {metrics}")

# Made with Bob
