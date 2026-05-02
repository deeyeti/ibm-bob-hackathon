"""
Route optimizer for emissions-based vendor selection and route planning.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from .config import auditor_config
from .emissions_calculator import RouteEmissions
from .fleet_prioritizer import VendorScore
from src.utils.logger import get_logger

logger = get_logger(__name__)


class OptimizedRoute(BaseModel):
    """Model for optimized route recommendation."""
    
    vendor_id: str = Field(description="Recommended vendor ID")
    vendor_name: str = Field(description="Vendor name")
    fleet_type: str = Field(description="Fleet type")
    
    # Route details
    distance_miles: float = Field(description="Route distance")
    estimated_delivery_time_hours: float = Field(description="Estimated delivery time")
    
    # Emissions
    total_emissions_kg: float = Field(description="Total emissions")
    emissions_per_mile: float = Field(description="Emissions per mile")
    emissions_reduction_percent: float = Field(description="Reduction vs baseline")
    
    # Costs
    estimated_cost: float = Field(description="Estimated cost in USD")
    cost_per_mile: float = Field(description="Cost per mile")
    
    # Scores
    optimization_score: float = Field(description="Overall optimization score")
    carbon_score: float = Field(description="Carbon footprint score")
    cost_score: float = Field(description="Cost efficiency score")
    reliability_score: float = Field(description="Reliability score")
    
    # Recommendation
    rank: Optional[int] = Field(default=None, description="Recommendation rank")
    recommendation_reason: str = Field(description="Reason for recommendation")
    
    # Savings
    emissions_savings_kg: float = Field(description="Emissions saved vs baseline")
    cost_comparison: str = Field(description="Cost comparison description")


class AlternativeRoute(BaseModel):
    """Model for alternative route suggestion."""
    
    route: OptimizedRoute = Field(description="Alternative route details")
    reason: str = Field(description="Reason for suggesting this alternative")
    trade_offs: List[str] = Field(description="Trade-offs compared to primary recommendation")


class RouteOptimizer:
    """Optimize routes based on emissions, cost, and other factors."""
    
    def __init__(self):
        """Initialize route optimizer."""
        self.config = auditor_config
        logger.info("Route optimizer initialized")
    
    def optimize_routes(
        self,
        scored_vendors: List[VendorScore],
        emissions_data: List[RouteEmissions],
        distance_miles: float,
        load_tons: float,
    ) -> List[OptimizedRoute]:
        """
        Optimize and rank routes based on multiple factors.
        
        Args:
            scored_vendors: List of scored vendors
            emissions_data: List of emissions calculations
            distance_miles: Route distance
            load_tons: Cargo load
            
        Returns:
            List of optimized routes, ranked by optimization score
        """
        try:
            # Create emissions lookup
            emissions_map = {e.vendor_id: e for e in emissions_data}
            
            optimized_routes = []
            for vendor_score in scored_vendors:
                emissions = emissions_map.get(vendor_score.vendor_id)
                if not emissions:
                    continue
                
                route = self._create_optimized_route(
                    vendor_score, emissions, distance_miles, load_tons
                )
                optimized_routes.append(route)
            
            # Sort by optimization score
            optimized_routes.sort(key=lambda r: r.optimization_score, reverse=True)
            
            # Assign ranks
            for i, route in enumerate(optimized_routes, 1):
                route.rank = i
            
            logger.info(f"Optimized {len(optimized_routes)} routes")
            return optimized_routes
            
        except Exception as e:
            logger.error(f"Error optimizing routes: {e}")
            raise
    
    def _create_optimized_route(
        self,
        vendor_score: VendorScore,
        emissions: RouteEmissions,
        distance_miles: float,
        load_tons: float,
    ) -> OptimizedRoute:
        """
        Create optimized route for a vendor.
        
        Args:
            vendor_score: Vendor scoring data
            emissions: Emissions calculation
            distance_miles: Route distance
            load_tons: Cargo load
            
        Returns:
            OptimizedRoute object
        """
        # Calculate estimated delivery time (assume average speed of 55 mph)
        avg_speed = 55.0
        delivery_time = distance_miles / avg_speed
        
        # Calculate estimated cost
        cost_per_mile = self._get_cost_per_mile(vendor_score.fleet_type)
        estimated_cost = distance_miles * cost_per_mile
        
        # Calculate optimization scores
        weights = self.config.optimization_weights
        
        # Carbon score (0-100, higher is better)
        carbon_score = self._calculate_carbon_score(emissions)
        
        # Cost score (0-100, higher is better - lower cost)
        cost_score = self._calculate_cost_score(estimated_cost, distance_miles)
        
        # Reliability score (already 0-100)
        reliability_score = vendor_score.reliability
        
        # Time score (assume faster is better, but not heavily weighted)
        time_score = 100 - (delivery_time / 10 * 10)  # Normalize to 0-100
        
        # Calculate weighted optimization score
        optimization_score = (
            carbon_score * weights.carbon_footprint +
            cost_score * weights.cost +
            reliability_score * weights.reliability +
            time_score * weights.delivery_time
        )
        
        # Apply hydrogen preference multiplier
        if vendor_score.fleet_type == "hydrogen":
            optimization_score *= weights.hydrogen_preference
            logger.debug(f"Applied hydrogen preference multiplier to {vendor_score.vendor_name}")
        
        # Generate recommendation reason
        recommendation_reason = self._generate_recommendation_reason(
            vendor_score, emissions, carbon_score
        )
        
        # Calculate savings
        baseline_cost = distance_miles * 2.50  # Assume baseline diesel cost
        emissions_savings = emissions.emissions_reduction_kg or 0
        
        # Cost comparison
        cost_diff = estimated_cost - baseline_cost
        if cost_diff < 0:
            cost_comparison = f"${abs(cost_diff):.2f} cheaper than baseline"
        elif cost_diff > 0:
            cost_comparison = f"${cost_diff:.2f} more than baseline"
        else:
            cost_comparison = "Same as baseline"
        
        return OptimizedRoute(
            vendor_id=vendor_score.vendor_id,
            vendor_name=vendor_score.vendor_name,
            fleet_type=vendor_score.fleet_type,
            distance_miles=distance_miles,
            estimated_delivery_time_hours=round(delivery_time, 2),
            total_emissions_kg=emissions.total_emissions_kg,
            emissions_per_mile=emissions.emissions_per_mile,
            emissions_reduction_percent=emissions.emissions_reduction_percent or 0,
            estimated_cost=round(estimated_cost, 2),
            cost_per_mile=round(cost_per_mile, 2),
            optimization_score=round(optimization_score, 2),
            carbon_score=round(carbon_score, 2),
            cost_score=round(cost_score, 2),
            reliability_score=round(reliability_score, 2),
            recommendation_reason=recommendation_reason,
            emissions_savings_kg=round(emissions_savings, 2),
            cost_comparison=cost_comparison,
        )
    
    def _calculate_carbon_score(self, emissions: RouteEmissions) -> float:
        """
        Calculate carbon footprint score (0-100, higher is better).
        
        Args:
            emissions: Emissions data
            
        Returns:
            Carbon score
        """
        # Base score on emissions reduction percentage
        reduction_percent = emissions.emissions_reduction_percent or 0
        
        # Convert to 0-100 scale
        carbon_score = reduction_percent
        
        # Bonus for very low emissions
        if emissions.total_emissions_kg < 10:
            carbon_score = min(100, carbon_score + 10)
        elif emissions.total_emissions_kg < 50:
            carbon_score = min(100, carbon_score + 5)
        
        return max(0, min(100, carbon_score))
    
    def _calculate_cost_score(self, estimated_cost: float, distance_miles: float) -> float:
        """
        Calculate cost efficiency score (0-100, higher is better).
        
        Args:
            estimated_cost: Estimated route cost
            distance_miles: Route distance
            
        Returns:
            Cost score
        """
        # Calculate cost per mile
        cost_per_mile = estimated_cost / distance_miles if distance_miles > 0 else 0
        
        # Baseline cost per mile (diesel)
        baseline_cost_per_mile = 2.50
        
        # Calculate score (lower cost = higher score)
        if cost_per_mile <= baseline_cost_per_mile:
            # Better than or equal to baseline
            score = 100 - ((cost_per_mile / baseline_cost_per_mile) * 20)
        else:
            # More expensive than baseline
            excess_ratio = (cost_per_mile - baseline_cost_per_mile) / baseline_cost_per_mile
            score = max(0, 80 - (excess_ratio * 50))
        
        return max(0, min(100, score))
    
    def _get_cost_per_mile(self, fleet_type: str) -> float:
        """
        Get estimated cost per mile for fleet type.
        
        Args:
            fleet_type: Type of fleet
            
        Returns:
            Cost per mile in USD
        """
        # Cost estimates based on fleet type
        cost_map = {
            "hydrogen": 2.90,
            "electric": 2.70,
            "biodiesel": 2.45,
            "hybrid": 2.55,
            "cng": 2.40,
            "diesel": 2.50,
        }
        
        return cost_map.get(fleet_type.lower(), 2.50)
    
    def _generate_recommendation_reason(
        self,
        vendor_score: VendorScore,
        emissions: RouteEmissions,
        carbon_score: float,
    ) -> str:
        """
        Generate human-readable recommendation reason.
        
        Args:
            vendor_score: Vendor scoring data
            emissions: Emissions data
            carbon_score: Carbon score
            
        Returns:
            Recommendation reason string
        """
        fleet_type = vendor_score.fleet_type
        reduction = emissions.emissions_reduction_percent or 0
        
        reasons = []
        
        # Fleet type reason
        if fleet_type == "hydrogen":
            reasons.append("Zero-emission hydrogen fuel cell technology")
        elif fleet_type == "electric":
            reasons.append("Clean electric fleet with minimal emissions")
        elif reduction > 70:
            reasons.append(f"Significantly lower emissions ({reduction:.1f}% reduction)")
        
        # Eco rating reason
        if vendor_score.eco_rating >= 4.8:
            reasons.append("Excellent environmental rating")
        elif vendor_score.eco_rating >= 4.5:
            reasons.append("High environmental rating")
        
        # Reliability reason
        if vendor_score.reliability >= 90:
            reasons.append("Highly reliable service")
        
        # Carbon score reason
        if carbon_score >= 90:
            reasons.append("Outstanding carbon footprint")
        
        if not reasons:
            reasons.append("Meets environmental standards")
        
        return "; ".join(reasons)
    
    def get_alternative_routes(
        self,
        optimized_routes: List[OptimizedRoute],
        primary_route: OptimizedRoute,
        max_alternatives: int = 3,
    ) -> List[AlternativeRoute]:
        """
        Get alternative route suggestions.
        
        Args:
            optimized_routes: List of all optimized routes
            primary_route: Primary recommended route
            max_alternatives: Maximum number of alternatives
            
        Returns:
            List of alternative routes
        """
        alternatives = []
        
        for route in optimized_routes:
            if route.vendor_id == primary_route.vendor_id:
                continue
            
            if len(alternatives) >= max_alternatives:
                break
            
            # Determine reason and trade-offs
            reason, trade_offs = self._analyze_alternative(route, primary_route)
            
            alternative = AlternativeRoute(
                route=route,
                reason=reason,
                trade_offs=trade_offs,
            )
            alternatives.append(alternative)
        
        return alternatives
    
    def _analyze_alternative(
        self,
        alternative: OptimizedRoute,
        primary: OptimizedRoute,
    ) -> tuple[str, List[str]]:
        """
        Analyze alternative route compared to primary.
        
        Args:
            alternative: Alternative route
            primary: Primary route
            
        Returns:
            Tuple of (reason, trade_offs list)
        """
        trade_offs = []
        
        # Compare emissions
        if alternative.total_emissions_kg > primary.total_emissions_kg:
            diff = alternative.total_emissions_kg - primary.total_emissions_kg
            trade_offs.append(f"Higher emissions (+{diff:.1f} kg CO2e)")
        
        # Compare cost
        if alternative.estimated_cost < primary.estimated_cost:
            diff = primary.estimated_cost - alternative.estimated_cost
            reason = f"Lower cost option (saves ${diff:.2f})"
        elif alternative.estimated_cost > primary.estimated_cost:
            diff = alternative.estimated_cost - primary.estimated_cost
            trade_offs.append(f"Higher cost (+${diff:.2f})")
            reason = "Alternative fleet type option"
        else:
            reason = "Comparable alternative"
        
        # Compare reliability
        if alternative.reliability_score < primary.reliability_score:
            diff = primary.reliability_score - alternative.reliability_score
            trade_offs.append(f"Lower reliability (-{diff:.1f} points)")
        
        # Compare delivery time
        if alternative.estimated_delivery_time_hours > primary.estimated_delivery_time_hours:
            diff = alternative.estimated_delivery_time_hours - primary.estimated_delivery_time_hours
            trade_offs.append(f"Longer delivery time (+{diff:.1f} hours)")
        
        if not trade_offs:
            trade_offs.append("Comparable performance to primary recommendation")
        
        return reason, trade_offs
    
    def calculate_emissions_savings(
        self,
        optimized_routes: List[OptimizedRoute],
    ) -> Dict[str, Any]:
        """
        Calculate total emissions savings across all routes.
        
        Args:
            optimized_routes: List of optimized routes
            
        Returns:
            Savings summary dictionary
        """
        if not optimized_routes:
            return {
                "total_savings_kg": 0,
                "average_reduction_percent": 0,
                "best_savings": None,
            }
        
        total_savings = sum(r.emissions_savings_kg for r in optimized_routes)
        avg_reduction = sum(r.emissions_reduction_percent for r in optimized_routes) / len(optimized_routes)
        
        best_route = max(optimized_routes, key=lambda r: r.emissions_savings_kg)
        
        return {
            "total_savings_kg": round(total_savings, 2),
            "average_reduction_percent": round(avg_reduction, 2),
            "best_savings": {
                "vendor": best_route.vendor_name,
                "savings_kg": best_route.emissions_savings_kg,
                "reduction_percent": best_route.emissions_reduction_percent,
            },
            "total_routes_analyzed": len(optimized_routes),
        }


# Global optimizer instance
route_optimizer = RouteOptimizer()


# Made with Bob