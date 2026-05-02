"""
Auditor Agent - Analyzes vendor emissions and prioritizes hydrogen-fueled solutions.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from src.agents.base_agent import BaseAgent, AgentStatus
from src.services.watsonx_service import watsonx_service
from src.utils.logger import get_logger

from .config import auditor_config, AuditorConfig
from .emissions_calculator import emissions_calculator, EmissionsCalculator
from .fleet_prioritizer import fleet_prioritizer, FleetPrioritizer
from .route_optimizer import route_optimizer, RouteOptimizer

logger = get_logger(__name__)


class AuditorAgent(BaseAgent):
    """
    Auditor Agent for emissions analysis and vendor optimization.
    
    Responsibilities:
    - Intercept vendor lists from Monitor Agent
    - Calculate Scope 3 emissions for each vendor's route
    - Heavily prioritize hydrogen-fueled fleets (10x weight)
    - Rank vendors by carbon footprint
    - Use IBM watsonx.ai for advanced analysis
    - Provide optimized vendor recommendations
    """
    
    def __init__(
        self,
        agent_id: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[AuditorConfig] = None,
    ):
        """
        Initialize Auditor Agent.
        
        Args:
            agent_id: Unique agent identifier
            name: Human-readable agent name
            config: Auditor configuration (uses default if not provided)
        """
        self.config = config or auditor_config
        
        super().__init__(
            agent_id=agent_id or self.config.agent_id,
            name=name or self.config.agent_name,
            agent_type="auditor",
        )
        
        # Initialize components
        self.emissions_calculator = emissions_calculator
        self.fleet_prioritizer = fleet_prioritizer
        self.route_optimizer = route_optimizer
        self.watsonx = watsonx_service
        
        # Agent state
        self._last_analysis: Optional[Dict[str, Any]] = None
        self._vendor_cache: Dict[str, Any] = {}
        
        logger.info(f"Auditor Agent initialized: {self.name}")
    
    async def initialize(self) -> None:
        """Initialize agent resources and dependencies."""
        try:
            # Initialize watsonx service if configured
            if self.config.use_watsonx:
                await self.watsonx.initialize()
                logger.info("Watsonx service initialized for Auditor Agent")
            
            # Update metrics
            self.update_metrics({
                "watsonx_enabled": self.config.use_watsonx,
                "hydrogen_preference_multiplier": self.config.optimization_weights.hydrogen_preference,
                "min_eco_rating": self.config.min_eco_rating,
            })
            
            logger.info("Auditor Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Auditor Agent: {e}")
            raise
    
    async def execute(self) -> Dict[str, Any]:
        """
        Execute agent's main task.
        This is a placeholder - actual execution happens via analyze_vendors.
        
        Returns:
            Dictionary with execution results
        """
        logger.info("Auditor Agent execute called - use analyze_vendors for actual analysis")
        return {
            "status": "ready",
            "message": "Auditor Agent ready to analyze vendors",
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    async def cleanup(self) -> None:
        """Cleanup agent resources."""
        try:
            # Close watsonx service if needed
            if self.config.use_watsonx:
                await self.watsonx.close()
            
            # Clear caches
            self._vendor_cache.clear()
            
            logger.info("Auditor Agent cleanup complete")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            raise
    
    async def analyze_vendors(
        self,
        vendors: List[Dict[str, Any]],
        distance_miles: Optional[float] = None,
        load_tons: Optional[float] = None,
        location: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyze vendors and provide optimized recommendations.
        
        Args:
            vendors: List of vendor data from Monitor Agent
            distance_miles: Route distance (uses baseline if not provided)
            load_tons: Cargo load (uses baseline if not provided)
            location: Location for context
            
        Returns:
            Comprehensive analysis with recommendations
        """
        try:
            execution_start = datetime.utcnow()
            
            # Use baseline values if not provided
            if distance_miles is None:
                distance_miles = self.config.baseline_distance
            if load_tons is None:
                load_tons = self.config.baseline_load
            
            logger.info(
                f"Analyzing {len(vendors)} vendors for route: "
                f"{distance_miles} miles, {load_tons} tons"
            )
            
            # Step 1: Calculate emissions for all vendors
            logger.info("Step 1: Calculating Scope 3 emissions")
            emissions_data = self.emissions_calculator.calculate_multiple_routes(
                vendors=vendors,
                distance_miles=distance_miles,
                load_tons=load_tons,
            )
            
            if not emissions_data:
                logger.warning("No emissions data calculated")
                return {
                    "status": "error",
                    "message": "Failed to calculate emissions for vendors",
                    "timestamp": datetime.utcnow().isoformat(),
                }
            
            # Step 2: Score and prioritize vendors (hydrogen gets 10x weight)
            logger.info("Step 2: Scoring and prioritizing vendors (hydrogen-first)")
            scored_vendors = self.fleet_prioritizer.score_vendors(
                vendors=vendors,
                emissions_data=emissions_data,
            )
            
            # Step 3: Optimize routes
            logger.info("Step 3: Optimizing routes")
            optimized_routes = self.route_optimizer.optimize_routes(
                scored_vendors=scored_vendors,
                emissions_data=emissions_data,
                distance_miles=distance_miles,
                load_tons=load_tons,
            )
            
            # Step 4: Get top recommendations
            top_recommendations = self.fleet_prioritizer.get_top_recommendations(
                scored_vendors=scored_vendors,
                limit=self.config.top_recommendations,
            )
            
            # Step 5: Get hydrogen vendors specifically
            hydrogen_vendors = self.fleet_prioritizer.get_hydrogen_vendors(scored_vendors)
            
            # Step 6: Generate summaries
            emissions_summary = self.emissions_calculator.get_emissions_summary(emissions_data)
            scoring_summary = self.fleet_prioritizer.get_scoring_summary(scored_vendors)
            savings_summary = self.route_optimizer.calculate_emissions_savings(optimized_routes)
            
            # Step 7: Get alternative routes for top recommendation
            alternatives = []
            if optimized_routes:
                alternatives = self.route_optimizer.get_alternative_routes(
                    optimized_routes=optimized_routes,
                    primary_route=optimized_routes[0],
                    max_alternatives=3,
                )
            
            # Step 8: Use watsonx.ai for advanced analysis (if enabled)
            watsonx_analysis = None
            if self.config.use_watsonx and emissions_summary:
                logger.info("Step 8: Generating watsonx.ai analysis")
                watsonx_analysis = await self._generate_watsonx_analysis(
                    emissions_summary=emissions_summary,
                    top_recommendations=top_recommendations,
                    location=location,
                )
            
            # Calculate execution time
            execution_time = (datetime.utcnow() - execution_start).total_seconds()
            
            # Update metrics
            self.update_metrics({
                "last_analysis_time": execution_start.isoformat(),
                "vendors_analyzed": len(vendors),
                "emissions_calculated": len(emissions_data),
                "hydrogen_vendors_found": len(hydrogen_vendors),
                "execution_time_seconds": execution_time,
                "total_emissions_savings_kg": savings_summary["total_savings_kg"],
            })
            
            # Prepare comprehensive result
            result = {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "analysis_id": f"audit-{execution_start.strftime('%Y%m%d%H%M%S')}",
                
                # Input parameters
                "parameters": {
                    "distance_miles": distance_miles,
                    "load_tons": load_tons,
                    "location": location,
                    "vendors_analyzed": len(vendors),
                },
                
                # Top recommendations (optimized routes)
                "recommendations": [
                    {
                        "rank": route.rank,
                        "vendor_id": route.vendor_id,
                        "vendor_name": route.vendor_name,
                        "fleet_type": route.fleet_type,
                        "total_emissions_kg": route.total_emissions_kg,
                        "emissions_reduction_percent": route.emissions_reduction_percent,
                        "estimated_cost": route.estimated_cost,
                        "optimization_score": route.optimization_score,
                        "recommendation_reason": route.recommendation_reason,
                        "emissions_savings_kg": route.emissions_savings_kg,
                    }
                    for route in optimized_routes[:self.config.top_recommendations]
                ],
                
                # Hydrogen vendors (highest priority)
                "hydrogen_vendors": [
                    {
                        "vendor_id": v.vendor_id,
                        "vendor_name": v.vendor_name,
                        "total_score": v.total_score,
                        "emissions_kg": v.emissions_kg,
                        "emissions_reduction_percent": v.emissions_reduction_percent,
                        "recommendation_level": v.recommendation_level,
                    }
                    for v in hydrogen_vendors
                ],
                
                # Alternative routes
                "alternatives": [
                    {
                        "vendor_name": alt.route.vendor_name,
                        "fleet_type": alt.route.fleet_type,
                        "reason": alt.reason,
                        "trade_offs": alt.trade_offs,
                        "emissions_kg": alt.route.total_emissions_kg,
                        "estimated_cost": alt.route.estimated_cost,
                    }
                    for alt in alternatives
                ],
                
                # Detailed summaries
                "emissions_summary": emissions_summary,
                "scoring_summary": scoring_summary,
                "savings_summary": savings_summary,
                
                # Watsonx.ai analysis
                "watsonx_analysis": watsonx_analysis,
                
                # Detailed breakdown (if configured)
                "detailed_breakdown": self._generate_detailed_breakdown(
                    emissions_data, scored_vendors, optimized_routes
                ) if self.config.include_detailed_breakdown else None,
                
                # Metrics
                "metrics": self.metrics,
            }
            
            # Cache the analysis
            self._last_analysis = result
            
            logger.info(
                f"Analysis complete: {len(optimized_routes)} routes optimized, "
                f"{len(hydrogen_vendors)} hydrogen vendors found, "
                f"{savings_summary['total_savings_kg']:.2f} kg CO2e savings potential"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error during vendor analysis: {e}")
            raise
    
    async def _generate_watsonx_analysis(
        self,
        emissions_summary: Dict[str, Any],
        top_recommendations: List[Any],
        location: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate advanced analysis using watsonx.ai.
        
        Args:
            emissions_summary: Emissions summary data
            top_recommendations: Top vendor recommendations
            location: Location context
            
        Returns:
            Watsonx analysis results
        """
        try:
            # Prepare context for watsonx
            context = {
                "total_emissions": emissions_summary.get("total_emissions_kg", 0),
                "average_emissions": emissions_summary.get("average_emissions_kg", 0),
                "total_savings": emissions_summary.get("total_savings_kg", 0),
                "best_vendor": emissions_summary.get("best_vendor", {}),
                "fleet_breakdown": emissions_summary.get("fleet_type_breakdown", {}),
                "location": location,
                "top_recommendations": [
                    {
                        "name": rec.vendor_name,
                        "fleet_type": rec.fleet_type,
                        "emissions_reduction": rec.emissions_reduction_percent,
                    }
                    for rec in top_recommendations[:3]
                ],
            }
            
            # Generate analysis prompt
            prompt = f"""
            Analyze the following freight vendor emissions data and provide insights:
            
            Total Emissions: {context['total_emissions']:.2f} kg CO2e
            Average Emissions: {context['average_emissions']:.2f} kg CO2e
            Total Potential Savings: {context['total_savings']:.2f} kg CO2e
            
            Best Vendor: {context['best_vendor'].get('name', 'N/A')} 
            ({context['best_vendor'].get('fleet_type', 'N/A')})
            
            Fleet Type Breakdown:
            {self._format_fleet_breakdown(context['fleet_breakdown'])}
            
            Top Recommendations:
            {self._format_recommendations(context['top_recommendations'])}
            
            Please provide:
            1. Key sustainability insights
            2. Hydrogen fleet advantages
            3. Specific recommendations for maximizing emissions reduction
            4. Long-term sustainability strategy suggestions
            
            Focus on the environmental benefits of hydrogen-fueled transportation.
            """
            
            # Generate analysis
            analysis_text = await self.watsonx.generate_text(
                prompt=prompt,
                max_tokens=self.config.watsonx_max_tokens,
                temperature=self.config.watsonx_temperature,
            )
            
            return {
                "analysis": analysis_text,
                "context": context,
                "generated_at": datetime.utcnow().isoformat(),
            }
            
        except Exception as e:
            logger.error(f"Error generating watsonx analysis: {e}")
            return {
                "error": str(e),
                "analysis": "Watsonx analysis unavailable",
            }
    
    def _format_fleet_breakdown(self, breakdown: Dict[str, Any]) -> str:
        """Format fleet breakdown for prompt."""
        lines = []
        for fleet_type, data in breakdown.items():
            lines.append(
                f"- {fleet_type.capitalize()}: {data['count']} vendors, "
                f"avg {data['average_emissions']:.2f} kg CO2e"
            )
        return "\n".join(lines) if lines else "No data"
    
    def _format_recommendations(self, recommendations: List[Dict[str, Any]]) -> str:
        """Format recommendations for prompt."""
        lines = []
        for i, rec in enumerate(recommendations, 1):
            lines.append(
                f"{i}. {rec['name']} ({rec['fleet_type']}) - "
                f"{rec['emissions_reduction']:.1f}% reduction"
            )
        return "\n".join(lines) if lines else "No recommendations"
    
    def _generate_detailed_breakdown(
        self,
        emissions_data: List[Any],
        scored_vendors: List[Any],
        optimized_routes: List[Any],
    ) -> Dict[str, Any]:
        """Generate detailed breakdown of analysis."""
        return {
            "emissions_details": [
                {
                    "vendor_id": e.vendor_id,
                    "vendor_name": e.vendor_name,
                    "fleet_type": e.fleet_type,
                    "total_emissions_kg": e.total_emissions_kg,
                    "emissions_per_mile": e.emissions_per_mile,
                    "emissions_per_ton_mile": e.emissions_per_ton_mile,
                    "fuel_consumption": e.fuel_consumption,
                    "fuel_unit": e.fuel_unit,
                    "well_to_wheel_emissions": e.well_to_wheel_emissions,
                    "baseline_emissions_kg": e.baseline_emissions_kg,
                    "emissions_reduction_kg": e.emissions_reduction_kg,
                    "emissions_reduction_percent": e.emissions_reduction_percent,
                }
                for e in emissions_data
            ],
            "scoring_details": [
                {
                    "vendor_id": s.vendor_id,
                    "vendor_name": s.vendor_name,
                    "fleet_type": s.fleet_type,
                    "fleet_type_score": s.fleet_type_score,
                    "eco_rating_score": s.eco_rating_score,
                    "reliability_score": s.reliability_score,
                    "capacity_score": s.capacity_score,
                    "emissions_score": s.emissions_score,
                    "total_score": s.total_score,
                    "rank": s.rank,
                    "recommendation_level": s.recommendation_level,
                }
                for s in scored_vendors
            ],
            "optimization_details": [
                {
                    "vendor_id": r.vendor_id,
                    "vendor_name": r.vendor_name,
                    "optimization_score": r.optimization_score,
                    "carbon_score": r.carbon_score,
                    "cost_score": r.cost_score,
                    "reliability_score": r.reliability_score,
                    "estimated_cost": r.estimated_cost,
                    "estimated_delivery_time_hours": r.estimated_delivery_time_hours,
                }
                for r in optimized_routes
            ],
        }
    
    def get_last_analysis(self) -> Optional[Dict[str, Any]]:
        """Get the last analysis results."""
        return self._last_analysis
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get agent statistics.
        
        Returns:
            Dictionary with agent statistics
        """
        return {
            "agent_info": self.get_info(),
            "config": {
                "hydrogen_preference": self.config.optimization_weights.hydrogen_preference,
                "min_eco_rating": self.config.min_eco_rating,
                "watsonx_enabled": self.config.use_watsonx,
            },
            "last_analysis": self._last_analysis is not None,
            "cache_size": len(self._vendor_cache),
        }


# Made with Bob