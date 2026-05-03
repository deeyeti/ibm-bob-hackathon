"""
Orchestrator API endpoints.

Provides endpoints for triggering the BeeAI orchestrator workflow.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

from src.agents.orchestrator.orchestrator_agent import run_beeai_orchestrator_workflow
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


class OrchestrateRequest(BaseModel):
    """Request model for orchestrate endpoint."""
    target_location: str = Field(
        ...,
        description="Target location for weather monitoring (e.g., 'New York,US')"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "target_location": "New York,US"
            }
        }


class OrchestrateResponse(BaseModel):
    """Response model for orchestrate endpoint."""
    workflow_id: str = Field(description="Unique workflow identifier")
    status: str = Field(description="Workflow status (completed/error)")
    reroute_required: bool = Field(description="Whether reroute is required")
    approved_vendor_id: Optional[str] = Field(
        default=None,
        description="ID of the approved vendor"
    )
    emissions_saving: Optional[str] = Field(
        default=None,
        description="Emissions saving information"
    )
    justification: Optional[str] = Field(
        default=None,
        description="AI-generated justification for vendor selection"
    )
    weather_status: Optional[str] = Field(
        default=None,
        description="Weather status"
    )
    timestamp: str = Field(description="Workflow completion timestamp")
    error: Optional[str] = Field(default=None, description="Error message if failed")


@router.post(
    "/orchestrate",
    response_model=OrchestrateResponse,
    status_code=status.HTTP_200_OK,
    summary="Run orchestrator workflow",
    description="Triggers the BeeAI orchestrator workflow to check weather conditions and optimize vendor selection"
)
async def orchestrate(request: OrchestrateRequest) -> OrchestrateResponse:
    """
    Run the complete BeeAI orchestrator workflow.
    
    This endpoint:
    1. Checks weather conditions at the target location
    2. If severe weather is detected, analyzes alternative vendors
    3. Returns the complete Shift Order with approved vendor and AI justification
    
    Args:
        request: OrchestrateRequest containing target_location
        
    Returns:
        OrchestrateResponse with workflow results including status, approved vendor,
        emissions saving, and AI justification
        
    Raises:
        HTTPException: If workflow fails or API keys are missing
    """
    try:
        logger.info(f"Orchestrate endpoint called for location: {request.target_location}")
        
        # Run the BeeAI orchestrator workflow
        result = await run_beeai_orchestrator_workflow(
            target_location=request.target_location
        )
        
        # Extract workflow status
        workflow_status = result.get("status", "unknown")
        
        # Handle error status
        if workflow_status == "error":
            error_message = result.get("error", "Unknown error occurred")
            logger.error(f"Workflow failed: {error_message}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Workflow failed: {error_message}"
            )
        
        # Build response based on workflow result
        response_data = {
            "workflow_id": result.get("workflow_id", "unknown"),
            "status": workflow_status,
            "reroute_required": result.get("reroute_required", False),
            "timestamp": result.get("timestamp", datetime.utcnow().isoformat())
        }
        
        # Add audit results if reroute was required
        if result.get("reroute_required"):
            audit_result = result.get("audit_result", {})
            response_data.update({
                "approved_vendor_id": audit_result.get("approved_vendor_id"),
                "emissions_saving": audit_result.get("emissions_saving"),
                "justification": audit_result.get("justification")
            })
        else:
            # Add weather status if no reroute needed
            response_data["weather_status"] = result.get("weather_status")
        
        logger.info(f"Workflow completed successfully: {response_data['workflow_id']}")
        return OrchestrateResponse(**response_data)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in orchestrate endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


# Made with Bob