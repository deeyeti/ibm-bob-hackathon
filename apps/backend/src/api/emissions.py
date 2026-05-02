"""
API routes for emissions tracking and analysis.
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Query, status

from src.models import (
    EmissionData,
    EmissionRequest,
    EmissionSummary,
    EmissionAnalysis,
    OptimizationSuggestion,
)
from src.services import watsonx_service
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

# In-memory storage for demo purposes
# TODO: Replace with actual database
emissions_storage: List[EmissionData] = []


@router.post("/", response_model=EmissionData, status_code=status.HTTP_201_CREATED)
async def log_emission(request: EmissionRequest) -> EmissionData:
    """
    Log a new emission entry.
    
    Args:
        request: Emission data to log
        
    Returns:
        Created emission data
    """
    try:
        emission = EmissionData(
            source=request.source,
            category=request.category,
            amount=request.amount,
            unit=request.unit,
            metadata=request.metadata,
        )
        
        emissions_storage.append(emission)
        logger.info(f"Emission logged: {emission.source} - {emission.amount} {emission.unit}")
        
        return emission
    
    except Exception as e:
        logger.error(f"Failed to log emission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to log emission data",
        )


@router.get("/", response_model=List[EmissionData])
async def get_emissions(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    source: str = Query(None, description="Filter by source"),
    category: str = Query(None, description="Filter by category"),
) -> List[EmissionData]:
    """
    Get emission records with optional filtering.
    
    Args:
        limit: Maximum number of records to return
        source: Filter by emission source
        category: Filter by emission category
        
    Returns:
        List of emission records
    """
    try:
        filtered_emissions = emissions_storage
        
        if source:
            filtered_emissions = [e for e in filtered_emissions if e.source == source]
        
        if category:
            filtered_emissions = [e for e in filtered_emissions if e.category.value == category]
        
        return filtered_emissions[-limit:]
    
    except Exception as e:
        logger.error(f"Failed to get emissions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve emission data",
        )


@router.get("/summary", response_model=EmissionSummary)
async def get_emissions_summary(
    days: int = Query(30, ge=1, le=365, description="Number of days to summarize"),
) -> EmissionSummary:
    """
    Get emissions summary for a time period.
    
    Args:
        days: Number of days to include in summary
        
    Returns:
        Emission summary
    """
    try:
        period_start = datetime.utcnow() - timedelta(days=days)
        period_end = datetime.utcnow()
        
        # Filter emissions within period
        period_emissions = [
            e for e in emissions_storage
            if e.timestamp >= period_start
        ]
        
        # Calculate totals by scope
        scope1_total = sum(e.amount for e in period_emissions if e.category.value == "scope1")
        scope2_total = sum(e.amount for e in period_emissions if e.category.value == "scope2")
        scope3_total = sum(e.amount for e in period_emissions if e.category.value == "scope3")
        
        total_emissions = scope1_total + scope2_total + scope3_total
        
        return EmissionSummary(
            total_emissions=total_emissions,
            scope1=scope1_total,
            scope2=scope2_total,
            scope3=scope3_total,
            period_start=period_start,
            period_end=period_end,
            reduction_target=20.0,  # Placeholder - should come from settings
        )
    
    except Exception as e:
        logger.error(f"Failed to get emissions summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate emissions summary",
        )


@router.post("/analyze", response_model=EmissionAnalysis)
async def analyze_emissions(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
) -> EmissionAnalysis:
    """
    Analyze emissions data using AI.
    
    Args:
        days: Number of days to analyze
        
    Returns:
        AI-powered emission analysis
    """
    try:
        period_start = datetime.utcnow() - timedelta(days=days)
        
        # Get emissions for analysis
        period_emissions = [
            e for e in emissions_storage
            if e.timestamp >= period_start
        ]
        
        if not period_emissions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No emission data found for the specified period",
            )
        
        # Prepare data for analysis
        emission_data = {
            "total_emissions": sum(e.amount for e in period_emissions),
            "num_records": len(period_emissions),
            "period_days": days,
            "sources": list(set(e.source for e in period_emissions)),
        }
        
        # Analyze using watsonx
        analysis_result = await watsonx_service.analyze_emissions(emission_data)
        
        # Parse analysis (placeholder - implement actual parsing)
        return EmissionAnalysis(
            total_emissions=emission_data["total_emissions"],
            trend="stable",  # TODO: Calculate actual trend
            insights=[
                "Total emissions tracked across multiple sources",
                "Consistent emission patterns observed",
                "Opportunities for reduction identified",
            ],
            recommendations=[
                "Consider renewable energy sources",
                "Optimize operational efficiency",
                "Implement carbon offset programs",
            ],
            confidence_score=0.85,
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to analyze emissions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze emission data",
        )


@router.get("/suggestions", response_model=List[OptimizationSuggestion])
async def get_optimization_suggestions(
    limit: int = Query(5, ge=1, le=20, description="Number of suggestions"),
) -> List[OptimizationSuggestion]:
    """
    Get AI-powered optimization suggestions.
    
    Args:
        limit: Maximum number of suggestions to return
        
    Returns:
        List of optimization suggestions
    """
    try:
        # Get recent emissions for context
        recent_emissions = emissions_storage[-100:] if emissions_storage else []
        
        context = {
            "total_emissions": sum(e.amount for e in recent_emissions),
            "num_sources": len(set(e.source for e in recent_emissions)),
        }
        
        # Generate recommendations using watsonx
        recommendations = await watsonx_service.generate_recommendations(
            context,
            num_recommendations=limit,
        )
        
        # Convert to OptimizationSuggestion format
        suggestions = []
        for i, rec in enumerate(recommendations[:limit]):
            suggestions.append(
                OptimizationSuggestion(
                    id=rec.get("id", f"suggestion_{i}"),
                    title=rec.get("title", f"Optimization Suggestion {i+1}"),
                    description=rec.get("description", "Detailed optimization suggestion"),
                    potential_reduction=rec.get("potential_reduction", 100.0),
                    implementation_cost=None,
                    priority=rec.get("priority", "medium"),
                    category="energy_efficiency",
                )
            )
        
        return suggestions
    
    except Exception as e:
        logger.error(f"Failed to get optimization suggestions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate optimization suggestions",
        )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_emissions() -> None:
    """
    Clear all emission data (for testing purposes).
    
    WARNING: This will delete all emission records.
    """
    try:
        emissions_storage.clear()
        logger.warning("All emission data cleared")
    
    except Exception as e:
        logger.error(f"Failed to clear emissions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear emission data",
        )

# Made with Bob
