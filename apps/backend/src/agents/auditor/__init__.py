"""
Auditor Agent module for emissions analysis and vendor optimization.
"""

from .auditor_agent import AuditorAgent
from .config import auditor_config, AuditorConfig
from .emissions_calculator import emissions_calculator, EmissionsCalculator, RouteEmissions
from .fleet_prioritizer import fleet_prioritizer, FleetPrioritizer, VendorScore
from .route_optimizer import route_optimizer, RouteOptimizer, OptimizedRoute, AlternativeRoute

__all__ = [
    # Main agent
    "AuditorAgent",
    
    # Configuration
    "auditor_config",
    "AuditorConfig",
    
    # Emissions calculator
    "emissions_calculator",
    "EmissionsCalculator",
    "RouteEmissions",
    
    # Fleet prioritizer
    "fleet_prioritizer",
    "FleetPrioritizer",
    "VendorScore",
    
    # Route optimizer
    "route_optimizer",
    "RouteOptimizer",
    "OptimizedRoute",
    "AlternativeRoute",
]

# Made with Bob
