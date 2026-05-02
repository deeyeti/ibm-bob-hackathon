"""
Configuration for the Auditor Agent.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field


class EmissionFactors(BaseModel):
    """Emission factors for different fleet types (kg CO2e per mile)."""
    
    # Hydrogen fuel cell (green hydrogen)
    hydrogen: float = Field(default=0.05, description="Hydrogen fuel cell emissions")
    
    # Electric vehicles (varies by grid mix)
    electric_renewable: float = Field(default=0.08, description="Electric with renewable energy")
    electric_grid: float = Field(default=0.50, description="Electric with grid mix")
    
    # Biodiesel
    biodiesel: float = Field(default=0.45, description="Biodiesel emissions")
    
    # Hybrid (40-60% of diesel)
    hybrid: float = Field(default=1.34, description="Hybrid vehicle emissions")
    
    # Compressed Natural Gas
    cng: float = Field(default=1.80, description="CNG vehicle emissions")
    
    # Diesel (baseline)
    diesel: float = Field(default=2.68, description="Diesel vehicle emissions")
    
    # Fuel consumption rates (gallons/kWh/kg per mile)
    diesel_consumption: float = Field(default=0.15, description="Diesel gallons per mile")
    electric_consumption: float = Field(default=2.0, description="kWh per mile")
    hydrogen_consumption: float = Field(default=0.08, description="kg H2 per mile")


class FleetPriorities(BaseModel):
    """Priority scores for different fleet types."""
    
    hydrogen: int = Field(default=100, description="Hydrogen fleet priority")
    electric_renewable: int = Field(default=90, description="Electric (renewable) priority")
    electric_grid: int = Field(default=70, description="Electric (grid) priority")
    biodiesel: int = Field(default=50, description="Biodiesel priority")
    hybrid: int = Field(default=40, description="Hybrid priority")
    cng: int = Field(default=30, description="CNG priority")
    diesel: int = Field(default=10, description="Diesel priority")
    
    # Multipliers for additional factors
    eco_rating_multiplier: float = Field(default=10.0, description="Eco rating multiplier")
    reliability_multiplier: float = Field(default=0.5, description="Reliability multiplier")
    capacity_multiplier: float = Field(default=0.1, description="Capacity multiplier")


class OptimizationWeights(BaseModel):
    """Weights for route optimization factors."""
    
    carbon_footprint: float = Field(default=0.70, description="Carbon footprint weight")
    cost: float = Field(default=0.15, description="Cost weight")
    reliability: float = Field(default=0.10, description="Reliability weight")
    delivery_time: float = Field(default=0.05, description="Delivery time weight")
    
    # Hydrogen preference multiplier
    hydrogen_preference: float = Field(default=10.0, description="Hydrogen fleet preference multiplier")


class AuditorConfig(BaseModel):
    """Configuration for the Auditor Agent."""
    
    # Agent identification
    agent_id: str = Field(default="auditor-agent-001", description="Agent identifier")
    agent_name: str = Field(default="Emissions Auditor Agent", description="Agent name")
    
    # Emission factors
    emission_factors: EmissionFactors = Field(default_factory=EmissionFactors)
    
    # Fleet priorities
    fleet_priorities: FleetPriorities = Field(default_factory=FleetPriorities)
    
    # Optimization weights
    optimization_weights: OptimizationWeights = Field(default_factory=OptimizationWeights)
    
    # Analysis settings
    min_eco_rating: float = Field(default=4.0, description="Minimum eco rating for recommendations")
    max_vendors_to_analyze: int = Field(default=20, description="Maximum vendors to analyze")
    top_recommendations: int = Field(default=5, description="Number of top recommendations to return")
    
    # Watsonx.ai settings
    use_watsonx: bool = Field(default=True, description="Use watsonx.ai for analysis")
    watsonx_temperature: float = Field(default=0.5, description="Watsonx temperature for analysis")
    watsonx_max_tokens: int = Field(default=1000, description="Max tokens for watsonx responses")
    
    # Route optimization
    consider_distance: bool = Field(default=True, description="Consider distance in optimization")
    consider_load: bool = Field(default=True, description="Consider load capacity in optimization")
    baseline_distance: float = Field(default=100.0, description="Baseline distance for calculations (miles)")
    baseline_load: float = Field(default=20.0, description="Baseline load for calculations (tons)")
    
    # Reporting
    include_detailed_breakdown: bool = Field(default=True, description="Include detailed emissions breakdown")
    calculate_savings: bool = Field(default=True, description="Calculate emissions savings vs baseline")
    
    class Config:
        """Pydantic config."""
        use_enum_values = True


# Default configuration instance
auditor_config = AuditorConfig()


# Emission calculation constants
EMISSION_CONSTANTS = {
    "diesel_gallon_to_co2": 10.21,  # kg CO2 per gallon of diesel
    "electricity_kwh_to_co2_grid": 0.92,  # kg CO2 per kWh (US average grid mix)
    "electricity_kwh_to_co2_renewable": 0.04,  # kg CO2 per kWh (renewable)
    "hydrogen_kg_to_co2_green": 0.1,  # kg CO2 per kg H2 (green hydrogen)
    "hydrogen_kg_to_co2_grey": 9.3,  # kg CO2 per kg H2 (grey hydrogen)
    "biodiesel_gallon_to_co2": 2.5,  # kg CO2 per gallon of biodiesel
    "cng_gallon_to_co2": 6.06,  # kg CO2 per gallon equivalent of CNG
}


# Vehicle efficiency factors
EFFICIENCY_FACTORS = {
    "hydrogen": 1.0,  # Baseline efficiency
    "electric": 0.95,  # 95% efficient
    "biodiesel": 0.85,  # 85% efficient
    "hybrid": 0.80,  # 80% efficient
    "cng": 0.75,  # 75% efficient
    "diesel": 0.70,  # 70% efficient
}


# Load factor adjustments (emissions increase with load)
LOAD_FACTORS = {
    "empty": 0.7,  # 70% of base emissions when empty
    "half": 1.0,  # 100% of base emissions at half load
    "full": 1.3,  # 130% of base emissions at full load
}


def get_emission_factor(fleet_type: str, energy_source: str = "standard") -> float:
    """
    Get emission factor for a fleet type.
    
    Args:
        fleet_type: Type of fleet (hydrogen, electric, diesel, etc.)
        energy_source: Energy source (renewable, grid, green, grey)
        
    Returns:
        Emission factor in kg CO2e per mile
    """
    config = auditor_config.emission_factors
    
    fleet_type = fleet_type.lower()
    energy_source = energy_source.lower()
    
    if fleet_type == "hydrogen":
        return config.hydrogen
    elif fleet_type == "electric":
        if energy_source in ["renewable", "solar", "wind"]:
            return config.electric_renewable
        else:
            return config.electric_grid
    elif fleet_type == "biodiesel":
        return config.biodiesel
    elif fleet_type == "hybrid":
        return config.hybrid
    elif fleet_type == "cng":
        return config.cng
    elif fleet_type == "diesel":
        return config.diesel
    else:
        # Default to diesel as worst case
        return config.diesel


def get_fleet_priority(fleet_type: str) -> int:
    """
    Get priority score for a fleet type.
    
    Args:
        fleet_type: Type of fleet
        
    Returns:
        Priority score (higher is better)
    """
    priorities = auditor_config.fleet_priorities
    
    fleet_type = fleet_type.lower()
    
    priority_map = {
        "hydrogen": priorities.hydrogen,
        "electric": priorities.electric_renewable,  # Assume renewable by default
        "biodiesel": priorities.biodiesel,
        "hybrid": priorities.hybrid,
        "cng": priorities.cng,
        "diesel": priorities.diesel,
    }
    
    return priority_map.get(fleet_type, priorities.diesel)


# Made with Bob