"""
API routes for agent management.
"""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, status

from src.agents import orchestrator_agent
from src.models import AgentInfo, AgentAction, AgentResponse
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[AgentInfo])
async def get_all_agents() -> List[AgentInfo]:
    """
    Get information about all agents.
    
    Returns:
        List of agent information
    """
    try:
        agent_status = await orchestrator_agent.get_agent_status()
        
        agents = []
        for agent_type, info in agent_status.items():
            agents.append(AgentInfo(**info))
        
        return agents
    
    except Exception as e:
        logger.error(f"Failed to get agent information: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve agent information",
        )


@router.get("/{agent_id}", response_model=AgentInfo)
async def get_agent(agent_id: str) -> AgentInfo:
    """
    Get information about a specific agent.
    
    Args:
        agent_id: Agent identifier
        
    Returns:
        Agent information
    """
    try:
        agent_status = await orchestrator_agent.get_agent_status()
        
        # Map agent_id to agent type
        agent_map = {
            "agent_orchestrator": "orchestrator",
            "agent_monitor": "monitor",
            "agent_auditor": "auditor",
        }
        
        agent_type = agent_map.get(agent_id)
        if not agent_type or agent_type not in agent_status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent not found: {agent_id}",
            )
        
        return AgentInfo(**agent_status[agent_type])
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get agent {agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve agent information",
        )


@router.post("/action", response_model=AgentResponse)
async def perform_agent_action(action: AgentAction) -> AgentResponse:
    """
    Perform an action on an agent (start/stop/restart).
    
    Args:
        action: Agent action details
        
    Returns:
        Action result
    """
    try:
        agent_name = action.agent_id.replace("agent_", "")
        
        if action.action == "start":
            result = await orchestrator_agent.start_agent(agent_name)
        elif action.action == "stop":
            result = await orchestrator_agent.stop_agent(agent_name)
        elif action.action == "restart":
            await orchestrator_agent.stop_agent(agent_name)
            result = await orchestrator_agent.start_agent(agent_name)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid action: {action.action}",
            )
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Action failed"),
            )
        
        # Get updated agent status
        agent_status = await orchestrator_agent.get_agent_status()
        agent_info = agent_status.get(agent_name, {})
        
        return AgentResponse(
            agent_id=action.agent_id,
            status=agent_info.get("status", "unknown"),
            message=f"Action '{action.action}' completed successfully",
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to perform action on agent {action.agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to perform agent action",
        )


@router.post("/orchestrate", response_model=Dict[str, Any])
async def trigger_orchestration() -> Dict[str, Any]:
    """
    Trigger a manual orchestration cycle.
    
    Returns:
        Orchestration results
    """
    try:
        logger.info("Manual orchestration triggered")
        result = await orchestrator_agent.run()
        return result
    
    except Exception as e:
        logger.error(f"Orchestration failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Orchestration failed",
        )


@router.get("/workflows/history", response_model=List[Dict[str, Any]])
async def get_workflow_history(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get recent workflow execution history.
    
    Args:
        limit: Maximum number of workflows to return
        
    Returns:
        List of workflow results
    """
    try:
        history = orchestrator_agent.get_workflow_history(limit)
        return history
    
    except Exception as e:
        logger.error(f"Failed to get workflow history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve workflow history",
        )

# Made with Bob
