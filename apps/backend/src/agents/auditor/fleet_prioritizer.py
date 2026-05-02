"""
Fleet prioritization system with heavy emphasis on hydrogen-fueled solutions.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from .config import auditor_config, get_fleet_priority
from .emissions_calculator import RouteEmissions
from src.utils.logger import get_logger

logger = get_logger(__name__)


class VendorScore(BaseModel):
    """Model for vendor scoring results."""
    
    vendor_id: str = Field(description="Vendor identifier")
    vendor_name: str = Field(description="Vendor name")
    fleet_type: str = Field(description="Fleet type")
    
    # Score components
    fleet_type_score: float = Field(description="Base fleet type score")
    eco_rating_score: float = Field(description="Eco rating score")
    reliability_score: float = Field(description="Reliability score")
    capacity_score: float = Field(description="Capacity score")
    emissions_score: float = Field(description="Emissions score")
    
    # Total score
    total_score: float = Field(description="Total weighted score")
    
    # Rankings
    rank: Optional[int] = Field(default=None, description="Overall rank")
    
    # Additional data
    emissions_kg: float = Field(description="Total emissions in kg CO2e")
    emissions_reduction_percent: float = Field(description="Emissions reduction vs baseline")
    eco_rating: float = Field(description="Vendor eco rating")
    reliability: float = Field(description="Vendor reliability score")
    
    # Recommendation strength
    recommendation_level: str = Field(description="Recommendation level (highly_recommended/recommended/acceptable)")


class FleetPrioritizer:
    """Prioritize vendors with heavy emphasis on hydrogen fleets."""
    
    def __init__(self):
        """Initialize fleet prioritizer."""
        self.config = auditor_config
        logger.info("Fleet prioritizer initialized with hydrogen-first strategy")
    
    def score_vendors(
        self,
        vendors: List[Dict[str, Any]],
        emissions_data: List[RouteEmissions],
    ) -> List[VendorScore]:
        """
        Score and rank vendors with hydrogen fleets receiving highest priority.
        
        Args:
            vendors: List of vendor data dictionaries
            emissions_data: List of calculated emissions for each vendor
            
        Returns:
            List of VendorScore objects, sorted by total score (highest first)
        """
        try:
            # Create emissions lookup
            emissions_map = {e.vendor_id: e for e in emissions_data}
            
            scores = []
            for vendor in vendors:
                vendor_id = vendor.get("id", "unknown")
                emissions = emissions_map.get(vendor_id)
                
                if not emissions:
                    logger.warning(f"No emissions data for vendor {vendor_id}, skipping")
                    continue
                
                score = self._calculate_vendor_score(vendor, emissions)
                scores.append(score)
            
            # Sort by total score (highest first)
            scores.sort(key=lambda s: s.total_score, reverse=True)
            
            # Assign ranks
            for i, score in enumerate(scores, 1):
                score.rank = i
            
            logger.info(f"Scored and ranked {len(scores)} vendors")
            return scores
            
        except Exception as e:
            logger.error(f"Error scoring vendors: {e}")
            raise
    
    def _calculate_vendor_score(
        self,
        vendor: Dict[str, Any],
        emissions: RouteEmissions,
    ) -> VendorScore:
        """
        Calculate comprehensive score for a vendor.
        
        Args:
            vendor: Vendor data
            emissions: Emissions calculation results
            
        Returns:
            VendorScore object
        """
        vendor_id = vendor.get("id", "unknown")
        vendor_name = vendor.get("name", "Unknown")
        fleet_type = vendor.get("fleet_type", "diesel").lower()
        eco_rating = vendor.get("eco_rating", 0)
        reliability = vendor.get("reliability_score", 0)
        capacity = vendor.get("capacity_tons", 0)
        
        # 1. Fleet Type Score (Base Priority)
        fleet_type_score = get_fleet_priority(fleet_type)
        
        # Apply 10x multiplier for hydrogen fleets (as specified)
        if fleet_type == "hydrogen":
            fleet_type_score *= 10.0
            logger.debug(f"Applied 10x hydrogen multiplier to {vendor_name}")
        
        # 2. Eco Rating Score
        eco_rating_score = eco_rating * self.config.fleet_priorities.eco_rating_multiplier
        
        # 3. Reliability Score
        reliability_score = reliability * self.config.fleet_priorities.reliability_multiplier
        
        # 4. Capacity Score
        capacity_score = capacity * self.config.fleet_priorities.capacity_multiplier
        
        # 5. Emissions Score (inverse - lower emissions = higher score)
        # Normalize emissions to 0-100 scale
        max_emissions = 500.0  # Assume max emissions for normalization
        emissions_score = max(0, 100 - (emissions.total_emissions_kg / max_emissions * 100))
        
        # Boost emissions score for low-emission fleets
        emissions_reduction = emissions.emissions_reduction_percent or 0
        if emissions_reduction > 90:
            emissions_score *= 1.5
        elif emissions_reduction > 80:
            emissions_score *= 1.3
        elif emissions_reduction > 70:
            emissions_score *= 1.2
        
        # Calculate total score
        total_score = (
            fleet_type_score +
            eco_rating_score +
            reliability_score +
            capacity_score +
            emissions_score
        )
        
        # Determine recommendation level
        recommendation_level = self._determine_recommendation_level(
            fleet_type, total_score, emissions_reduction
        )
        
        return VendorScore(
            vendor_id=vendor_id,
            vendor_name=vendor_name,
            fleet_type=fleet_type,
            fleet_type_score=round(fleet_type_score, 2),
            eco_rating_score=round(eco_rating_score, 2),
            reliability_score=round(reliability_score, 2),
            capacity_score=round(capacity_score, 2),
            emissions_score=round(emissions_score, 2),
            total_score=round(total_score, 2),
            emissions_kg=emissions.total_emissions_kg,
            emissions_reduction_percent=emissions.emissions_reduction_percent or 0,
            eco_rating=eco_rating,
            reliability=reliability,
            recommendation_level=recommendation_level,
        )
    
    def _determine_recommendation_level(
        self,
        fleet_type: str,
        total_score: float,
        emissions_reduction: float,
    ) -> str:
        """
        Determine recommendation level for a vendor.
        
        Args:
            fleet_type: Type of fleet
            total_score: Total vendor score
            emissions_reduction: Emissions reduction percentage
            
        Returns:
            Recommendation level string
        """
        # Hydrogen fleets are always highly recommended
        if fleet_type == "hydrogen":
            return "highly_recommended"
        
        # Electric with high emissions reduction
        if fleet_type == "electric" and emissions_reduction > 85:
            return "highly_recommended"
        
        # High score and good emissions reduction
        if total_score > 200 and emissions_reduction > 70:
            return "recommended"
        
        # Acceptable alternatives
        if total_score > 100 and emissions_reduction > 50:
            return "acceptable"
        
        # Default
        return "acceptable"
    
    def get_top_recommendations(
        self,
        scored_vendors: List[VendorScore],
        limit: Optional[int] = None,
    ) -> List[VendorScore]:
        """
        Get top vendor recommendations.
        
        Args:
            scored_vendors: List of scored vendors
            limit: Maximum number of recommendations (uses config default if not provided)
            
        Returns:
            List of top recommended vendors
        """
        if limit is None:
            limit = self.config.top_recommendations
        
        return scored_vendors[:limit]
    
    def get_hydrogen_vendors(self, scored_vendors: List[VendorScore]) -> List[VendorScore]:
        """
        Get all hydrogen-fueled vendors.
        
        Args:
            scored_vendors: List of scored vendors
            
        Returns:
            List of hydrogen vendors
        """
        return [v for v in scored_vendors if v.fleet_type == "hydrogen"]
    
    def get_eco_friendly_vendors(
        self,
        scored_vendors: List[VendorScore],
        min_eco_rating: Optional[float] = None,
    ) -> List[VendorScore]:
        """
        Get eco-friendly vendors (hydrogen and electric with high ratings).
        
        Args:
            scored_vendors: List of scored vendors
            min_eco_rating: Minimum eco rating (uses config default if not provided)
            
        Returns:
            List of eco-friendly vendors
        """
        if min_eco_rating is None:
            min_eco_rating = self.config.min_eco_rating
        
        return [
            v for v in scored_vendors
            if v.fleet_type in ["hydrogen", "electric"] and v.eco_rating >= min_eco_rating
        ]
    
    def get_scoring_summary(self, scored_vendors: List[VendorScore]) -> Dict[str, Any]:
        """
        Generate summary of scoring results.
        
        Args:
            scored_vendors: List of scored vendors
            
        Returns:
            Summary dictionary
        """
        if not scored_vendors:
            return {
                "total_vendors": 0,
                "hydrogen_vendors": 0,
                "electric_vendors": 0,
                "highly_recommended": 0,
            }
        
        # Count by fleet type
        fleet_counts = {}
        for vendor in scored_vendors:
            fleet_type = vendor.fleet_type
            fleet_counts[fleet_type] = fleet_counts.get(fleet_type, 0) + 1
        
        # Count by recommendation level
        recommendation_counts = {
            "highly_recommended": 0,
            "recommended": 0,
            "acceptable": 0,
        }
        for vendor in scored_vendors:
            level = vendor.recommendation_level
            recommendation_counts[level] = recommendation_counts.get(level, 0) + 1
        
        # Get top vendor
        top_vendor = scored_vendors[0] if scored_vendors else None
        
        # Calculate average scores
        avg_total_score = sum(v.total_score for v in scored_vendors) / len(scored_vendors)
        avg_emissions_reduction = sum(v.emissions_reduction_percent for v in scored_vendors) / len(scored_vendors)
        
        return {
            "total_vendors": len(scored_vendors),
            "fleet_type_counts": fleet_counts,
            "recommendation_counts": recommendation_counts,
            "top_vendor": {
                "id": top_vendor.vendor_id,
                "name": top_vendor.vendor_name,
                "fleet_type": top_vendor.fleet_type,
                "score": top_vendor.total_score,
                "emissions_reduction": top_vendor.emissions_reduction_percent,
            } if top_vendor else None,
            "average_total_score": round(avg_total_score, 2),
            "average_emissions_reduction": round(avg_emissions_reduction, 2),
            "hydrogen_vendors": fleet_counts.get("hydrogen", 0),
            "electric_vendors": fleet_counts.get("electric", 0),
            "highly_recommended_count": recommendation_counts["highly_recommended"],
        }
    
    def filter_by_criteria(
        self,
        scored_vendors: List[VendorScore],
        min_score: Optional[float] = None,
        min_emissions_reduction: Optional[float] = None,
        fleet_types: Optional[List[str]] = None,
        recommendation_levels: Optional[List[str]] = None,
    ) -> List[VendorScore]:
        """
        Filter vendors by various criteria.
        
        Args:
            scored_vendors: List of scored vendors
            min_score: Minimum total score
            min_emissions_reduction: Minimum emissions reduction percentage
            fleet_types: List of acceptable fleet types
            recommendation_levels: List of acceptable recommendation levels
            
        Returns:
            Filtered list of vendors
        """
        filtered = scored_vendors
        
        if min_score is not None:
            filtered = [v for v in filtered if v.total_score >= min_score]
        
        if min_emissions_reduction is not None:
            filtered = [v for v in filtered if v.emissions_reduction_percent >= min_emissions_reduction]
        
        if fleet_types:
            filtered = [v for v in filtered if v.fleet_type in fleet_types]
        
        if recommendation_levels:
            filtered = [v for v in filtered if v.recommendation_level in recommendation_levels]
        
        return filtered


# Global prioritizer instance
fleet_prioritizer = FleetPrioritizer()


# Made with Bob