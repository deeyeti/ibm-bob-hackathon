"""
Auditor Agent module.
"""

from .auditor_agent import AuditorAgent
from .config import auditor_config, AuditorConfig
from .emissions_calculator import emissions_calculator, EmissionsCalculator
from .fleet_prioritizer import fleet_prioritizer, FleetPrioritizer
from .route_optimizer import route_optimizer, RouteOptimizer

# BeeAI-based implementation
try:
    from .beeai_auditor import (
        BeeAIAuditorAgent,
        beeai_auditor_agent,
        analyze_alternative_vendors,
    )
    BEEAI_AUDITOR_AVAILABLE = True
except ImportError:
    BeeAIAuditorAgent = None
    beeai_auditor_agent = None
    analyze_alternative_vendors = None
    BEEAI_AUDITOR_AVAILABLE = False

__all__ = [
    "AuditorAgent",
    "auditor_config",
    "AuditorConfig",
    "emissions_calculator",
    "EmissionsCalculator",
    "fleet_prioritizer",
    "FleetPrioritizer",
    "route_optimizer",
    "RouteOptimizer",
    "BeeAIAuditorAgent",
    "beeai_auditor_agent",
    "analyze_alternative_vendors",
    "BEEAI_AUDITOR_AVAILABLE",
]

# Made with Bob
