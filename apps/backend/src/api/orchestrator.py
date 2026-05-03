"""
Orchestrator API endpoints.

Provides endpoints for triggering the BeeAI orchestrator workflow.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime

from src.agents.orchestrator.orchestrator_agent import run_beeai_orchestrator_workflow
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


class OrchestrateRequest(BaseModel):
    """Request model for orchestrate endpoint."""
    origin: Optional[str] = Field(
        None,
        description="Origin port (e.g., 'Shanghai,CN')"
    )
    destination: Optional[str] = Field(
        None,
        description="Destination port (e.g., 'Los Angeles,US')"
    )
    # Keep backward compatibility
    target_location: Optional[str] = Field(
        None,
        description="Target location for weather monitoring (e.g., 'New York,US') - deprecated, use destination"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "origin": "Shanghai,CN",
                "destination": "Los Angeles,US"
            }
        }


class RouteDetails(BaseModel):
    """Route details model."""
    distance: float = Field(description="Distance in kilometers")
    eta: str = Field(description="Estimated time of arrival")
    origin_coords: Optional[List[float]] = Field(default=None, description="Origin coordinates [lat, lon]")
    destination_coords: Optional[List[float]] = Field(default=None, description="Destination coordinates [lat, lon]")


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
    route_details: Optional[RouteDetails] = Field(
        default=None,
        description="Route details including distance and ETA"
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
        # Determine target location (use destination if provided, otherwise target_location for backward compatibility)
        target_location = request.destination or request.target_location
        if not target_location:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either 'destination' or 'target_location' must be provided"
            )
        
        logger.info(f"Orchestrate endpoint called - Origin: {request.origin}, Destination: {target_location}")
        
        # Run the BeeAI orchestrator workflow
        result = await run_beeai_orchestrator_workflow(
            target_location=target_location
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
        
        # Add mock route details (in production, calculate from actual route data)
        # Mock coordinates for common ports
        port_coords = {
            "Shanghai,CN": [31.2304, 121.4737],
            "Los Angeles,US": [34.0522, -118.2437],
            "New York,US": [40.7128, -74.0060],
            "Rotterdam,NL": [51.9225, 4.4792],
            "Singapore,SG": [1.3521, 103.8198],
        }
        
        origin_coords = port_coords.get(request.origin, [0, 0]) if request.origin else None
        dest_coords = port_coords.get(target_location, [0, 0])
        
        # Calculate mock distance (simplified great circle distance)
        if origin_coords and dest_coords:
            import math
            lat1, lon1 = math.radians(origin_coords[0]), math.radians(origin_coords[1])
            lat2, lon2 = math.radians(dest_coords[0]), math.radians(dest_coords[1])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            distance = 6371 * c  # Earth radius in km
            
            # Mock ETA calculation (assuming 40 km/h average speed)
            hours = distance / 40
            days = int(hours / 24)
            remaining_hours = int(hours % 24)
            eta = f"{days} days, {remaining_hours} hours"
            
            response_data["route_details"] = {
                "distance": round(distance, 2),
                "eta": eta,
                "origin_coords": origin_coords,
                "destination_coords": dest_coords
            }
        
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