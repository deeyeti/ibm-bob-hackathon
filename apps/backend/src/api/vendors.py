"""
API routes for vendor recommendations.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Query, status

from src.models import Vendor, VendorRecommendation, VendorSearchRequest, VendorCategory
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

# Mock vendor data for demonstration
# TODO: Replace with actual database
MOCK_VENDORS = [
    {
        "id": "vendor_001",
        "name": "GreenEnergy Solutions",
        "category": VendorCategory.RENEWABLE_ENERGY,
        "description": "Leading provider of solar and wind energy solutions",
        "carbon_reduction_potential": 5000.0,
        "cost_estimate": 50000.0,
        "rating": 4.8,
        "contact_info": {"email": "contact@greenenergy.com", "phone": "+1-555-0100"},
    },
    {
        "id": "vendor_002",
        "name": "CarbonOffset Pro",
        "category": VendorCategory.CARBON_OFFSET,
        "description": "Verified carbon offset programs and credits",
        "carbon_reduction_potential": 3000.0,
        "cost_estimate": 15000.0,
        "rating": 4.5,
        "contact_info": {"email": "info@carbonoffset.com", "phone": "+1-555-0200"},
    },
    {
        "id": "vendor_003",
        "name": "EcoTransport Systems",
        "category": VendorCategory.SUSTAINABLE_TRANSPORT,
        "description": "Electric vehicle fleet and charging infrastructure",
        "carbon_reduction_potential": 4000.0,
        "cost_estimate": 75000.0,
        "rating": 4.6,
        "contact_info": {"email": "sales@ecotransport.com", "phone": "+1-555-0300"},
    },
    {
        "id": "vendor_004",
        "name": "Efficiency First",
        "category": VendorCategory.ENERGY_EFFICIENCY,
        "description": "Energy audit and efficiency optimization services",
        "carbon_reduction_potential": 2500.0,
        "cost_estimate": 20000.0,
        "rating": 4.7,
        "contact_info": {"email": "hello@efficiencyfirst.com", "phone": "+1-555-0400"},
    },
]


@router.get("/", response_model=List[Vendor])
async def get_vendors(
    category: str = Query(None, description="Filter by category"),
    min_reduction: float = Query(None, description="Minimum CO2 reduction"),
    max_cost: float = Query(None, description="Maximum cost"),
) -> List[Vendor]:
    """
    Get list of vendors with optional filtering.
    
    Args:
        category: Filter by vendor category
        min_reduction: Minimum carbon reduction potential
        max_cost: Maximum cost estimate
        
    Returns:
        List of vendors matching criteria
    """
    try:
        vendors = MOCK_VENDORS.copy()
        
        # Apply filters
        if category:
            vendors = [v for v in vendors if v["category"].value == category]
        
        if min_reduction is not None:
            vendors = [v for v in vendors if v["carbon_reduction_potential"] >= min_reduction]
        
        if max_cost is not None:
            vendors = [v for v in vendors if v["cost_estimate"] <= max_cost]
        
        return [Vendor(**v) for v in vendors]
    
    except Exception as e:
        logger.error(f"Failed to get vendors: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve vendors",
        )


@router.get("/{vendor_id}", response_model=Vendor)
async def get_vendor(vendor_id: str) -> Vendor:
    """
    Get details of a specific vendor.
    
    Args:
        vendor_id: Vendor identifier
        
    Returns:
        Vendor details
    """
    try:
        vendor = next((v for v in MOCK_VENDORS if v["id"] == vendor_id), None)
        
        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vendor not found: {vendor_id}",
            )
        
        return Vendor(**vendor)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get vendor {vendor_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve vendor details",
        )


@router.post("/search", response_model=List[Vendor])
async def search_vendors(request: VendorSearchRequest) -> List[Vendor]:
    """
    Search for vendors based on criteria.
    
    Args:
        request: Search criteria
        
    Returns:
        List of matching vendors
    """
    try:
        vendors = MOCK_VENDORS.copy()
        
        # Apply filters from request
        if request.category:
            vendors = [v for v in vendors if v["category"] == request.category]
        
        if request.min_reduction is not None:
            vendors = [
                v for v in vendors
                if v["carbon_reduction_potential"] >= request.min_reduction
            ]
        
        if request.max_cost is not None:
            vendors = [v for v in vendors if v["cost_estimate"] <= request.max_cost]
        
        # TODO: Implement location-based filtering
        
        return [Vendor(**v) for v in vendors]
    
    except Exception as e:
        logger.error(f"Failed to search vendors: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search vendors",
        )


@router.get("/recommendations/", response_model=List[VendorRecommendation])
async def get_vendor_recommendations(
    emission_amount: float = Query(..., description="Current emission amount"),
    category: str = Query(None, description="Preferred category"),
    budget: float = Query(None, description="Available budget"),
) -> List[VendorRecommendation]:
    """
    Get AI-powered vendor recommendations.
    
    Args:
        emission_amount: Current emission levels
        category: Preferred vendor category
        budget: Available budget
        
    Returns:
        List of vendor recommendations with relevance scores
    """
    try:
        vendors = MOCK_VENDORS.copy()
        
        # Filter by category if specified
        if category:
            vendors = [v for v in vendors if v["category"].value == category]
        
        # Filter by budget if specified
        if budget is not None:
            vendors = [v for v in vendors if v["cost_estimate"] <= budget]
        
        # Calculate relevance scores and create recommendations
        recommendations = []
        for vendor in vendors:
            # Simple relevance calculation (TODO: Use AI for better scoring)
            reduction_score = min(vendor["carbon_reduction_potential"] / emission_amount, 1.0)
            cost_score = 1.0 - (vendor["cost_estimate"] / 100000.0) if budget else 0.5
            rating_score = vendor["rating"] / 5.0
            
            relevance_score = (reduction_score * 0.5 + cost_score * 0.3 + rating_score * 0.2)
            
            recommendations.append(
                VendorRecommendation(
                    vendor=Vendor(**vendor),
                    relevance_score=relevance_score,
                    reasoning=f"High carbon reduction potential with good cost-effectiveness",
                    estimated_impact=min(
                        vendor["carbon_reduction_potential"],
                        emission_amount * 0.8,
                    ),
                )
            )
        
        # Sort by relevance score
        recommendations.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return recommendations[:5]  # Return top 5 recommendations
    
    except Exception as e:
        logger.error(f"Failed to get vendor recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate vendor recommendations",
        )


@router.get("/categories/", response_model=List[str])
async def get_vendor_categories() -> List[str]:
    """
    Get list of available vendor categories.
    
    Returns:
        List of vendor category names
    """
    try:
        return [category.value for category in VendorCategory]
    
    except Exception as e:
        logger.error(f"Failed to get vendor categories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve vendor categories",
        )

# Made with Bob
