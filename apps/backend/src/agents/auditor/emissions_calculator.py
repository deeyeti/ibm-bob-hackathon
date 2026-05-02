"""
Emissions calculator for Scope 3 emissions from freight transportation.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import math

from .config import (
    auditor_config,
    get_emission_factor,
    EMISSION_CONSTANTS,
    EFFICIENCY_FACTORS,
    LOAD_FACTORS,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RouteEmissions(BaseModel):
    """Model for route emissions calculation results."""
    
    vendor_id: str = Field(description="Vendor identifier")
    vendor_name: str = Field(description="Vendor name")
    fleet_type: str = Field(description="Fleet type")
    distance_miles: float = Field(description="Route distance in miles")
    load_tons: float = Field(description="Cargo load in tons")
    
    # Emissions breakdown
    total_emissions_kg: float = Field(description="Total emissions in kg CO2e")
    emissions_per_mile: float = Field(description="Emissions per mile")
    emissions_per_ton_mile: float = Field(description="Emissions per ton-mile")
    
    # Calculation details
    fuel_consumption: float = Field(description="Fuel/energy consumption")
    fuel_unit: str = Field(description="Fuel unit (gallons/kWh/kg)")
    emission_factor: float = Field(description="Emission factor used")
    efficiency_factor: float = Field(description="Vehicle efficiency factor")
    load_factor: float = Field(description="Load adjustment factor")
    
    # Comparison
    baseline_emissions_kg: Optional[float] = Field(default=None, description="Baseline diesel emissions")
    emissions_reduction_kg: Optional[float] = Field(default=None, description="Emissions reduction vs baseline")
    emissions_reduction_percent: Optional[float] = Field(default=None, description="Reduction percentage")
    
    # Additional metrics
    well_to_wheel_emissions: float = Field(description="Well-to-wheel emissions")
    carbon_intensity: float = Field(description="Carbon intensity (kg CO2e per ton-mile)")


class EmissionsCalculator:
    """Calculator for Scope 3 freight transportation emissions."""
    
    def __init__(self):
        """Initialize emissions calculator."""
        self.config = auditor_config
        logger.info("Emissions calculator initialized")
    
    def calculate_route_emissions(
        self,
        vendor_data: Dict[str, Any],
        distance_miles: float,
        load_tons: Optional[float] = None,
        energy_source: str = "standard",
    ) -> RouteEmissions:
        """
        Calculate Scope 3 emissions for a specific route.
        
        Args:
            vendor_data: Vendor information including fleet type
            distance_miles: Route distance in miles
            load_tons: Cargo load in tons (uses baseline if not provided)
            energy_source: Energy source type (renewable, grid, green, grey)
            
        Returns:
            RouteEmissions object with detailed calculations
        """
        try:
            # Extract vendor information
            vendor_id = vendor_data.get("id", "unknown")
            vendor_name = vendor_data.get("name", "Unknown Vendor")
            fleet_type = vendor_data.get("fleet_type", "diesel").lower()
            
            # Use baseline load if not provided
            if load_tons is None:
                load_tons = self.config.baseline_load
            
            # Get emission factor for fleet type
            emission_factor = get_emission_factor(fleet_type, energy_source)
            
            # Get efficiency factor
            efficiency_factor = EFFICIENCY_FACTORS.get(fleet_type, 0.70)
            
            # Calculate load factor
            load_factor = self._calculate_load_factor(load_tons, vendor_data.get("capacity_tons", 20.0))
            
            # Calculate fuel consumption based on fleet type
            fuel_consumption, fuel_unit = self._calculate_fuel_consumption(
                fleet_type, distance_miles, load_factor
            )
            
            # Calculate total emissions
            # Formula: Distance × Emission Factor × Load Factor / Efficiency Factor
            base_emissions = distance_miles * emission_factor * load_factor / efficiency_factor
            
            # Calculate well-to-wheel emissions (includes production and distribution)
            wtw_multiplier = self._get_wtw_multiplier(fleet_type, energy_source)
            well_to_wheel_emissions = base_emissions * wtw_multiplier
            
            # Use well-to-wheel for total emissions
            total_emissions = well_to_wheel_emissions
            
            # Calculate per-unit metrics
            emissions_per_mile = total_emissions / distance_miles if distance_miles > 0 else 0
            emissions_per_ton_mile = total_emissions / (distance_miles * load_tons) if (distance_miles > 0 and load_tons > 0) else 0
            carbon_intensity = emissions_per_ton_mile
            
            # Calculate baseline (diesel) for comparison
            baseline_emissions = self._calculate_baseline_emissions(distance_miles, load_tons)
            emissions_reduction = baseline_emissions - total_emissions
            emissions_reduction_percent = (emissions_reduction / baseline_emissions * 100) if baseline_emissions > 0 else 0
            
            result = RouteEmissions(
                vendor_id=vendor_id,
                vendor_name=vendor_name,
                fleet_type=fleet_type,
                distance_miles=distance_miles,
                load_tons=load_tons,
                total_emissions_kg=round(total_emissions, 2),
                emissions_per_mile=round(emissions_per_mile, 4),
                emissions_per_ton_mile=round(emissions_per_ton_mile, 4),
                fuel_consumption=round(fuel_consumption, 2),
                fuel_unit=fuel_unit,
                emission_factor=emission_factor,
                efficiency_factor=efficiency_factor,
                load_factor=load_factor,
                baseline_emissions_kg=round(baseline_emissions, 2),
                emissions_reduction_kg=round(emissions_reduction, 2),
                emissions_reduction_percent=round(emissions_reduction_percent, 2),
                well_to_wheel_emissions=round(well_to_wheel_emissions, 2),
                carbon_intensity=round(carbon_intensity, 4),
            )
            
            logger.debug(
                f"Calculated emissions for {vendor_name}: {total_emissions:.2f} kg CO2e "
                f"({emissions_reduction_percent:.1f}% reduction vs diesel)"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating route emissions: {e}")
            raise
    
    def calculate_multiple_routes(
        self,
        vendors: List[Dict[str, Any]],
        distance_miles: float,
        load_tons: Optional[float] = None,
    ) -> List[RouteEmissions]:
        """
        Calculate emissions for multiple vendors/routes.
        
        Args:
            vendors: List of vendor data dictionaries
            distance_miles: Route distance in miles
            load_tons: Cargo load in tons
            
        Returns:
            List of RouteEmissions objects
        """
        results = []
        
        for vendor in vendors:
            try:
                # Determine energy source based on vendor data
                energy_source = self._determine_energy_source(vendor)
                
                emissions = self.calculate_route_emissions(
                    vendor_data=vendor,
                    distance_miles=distance_miles,
                    load_tons=load_tons,
                    energy_source=energy_source,
                )
                results.append(emissions)
                
            except Exception as e:
                logger.error(f"Error calculating emissions for vendor {vendor.get('id')}: {e}")
                continue
        
        logger.info(f"Calculated emissions for {len(results)} vendors")
        return results
    
    def _calculate_fuel_consumption(
        self,
        fleet_type: str,
        distance_miles: float,
        load_factor: float,
    ) -> tuple[float, str]:
        """
        Calculate fuel/energy consumption for a route.
        
        Args:
            fleet_type: Type of fleet
            distance_miles: Distance in miles
            load_factor: Load adjustment factor
            
        Returns:
            Tuple of (consumption amount, unit)
        """
        factors = self.config.emission_factors
        
        if fleet_type == "hydrogen":
            consumption = distance_miles * factors.hydrogen_consumption * load_factor
            return consumption, "kg H2"
        elif fleet_type == "electric":
            consumption = distance_miles * factors.electric_consumption * load_factor
            return consumption, "kWh"
        elif fleet_type in ["diesel", "biodiesel", "hybrid"]:
            consumption = distance_miles * factors.diesel_consumption * load_factor
            if fleet_type == "hybrid":
                consumption *= 0.5  # Hybrids use ~50% less fuel
            return consumption, "gallons"
        elif fleet_type == "cng":
            consumption = distance_miles * factors.diesel_consumption * 0.8 * load_factor
            return consumption, "GGE"  # Gasoline Gallon Equivalent
        else:
            consumption = distance_miles * factors.diesel_consumption * load_factor
            return consumption, "gallons"
    
    def _calculate_load_factor(self, load_tons: float, capacity_tons: float) -> float:
        """
        Calculate load adjustment factor based on capacity utilization.
        
        Args:
            load_tons: Actual load in tons
            capacity_tons: Vehicle capacity in tons
            
        Returns:
            Load factor multiplier
        """
        if capacity_tons <= 0:
            return 1.0
        
        utilization = load_tons / capacity_tons
        
        if utilization <= 0.3:
            return LOAD_FACTORS["empty"]
        elif utilization <= 0.7:
            return LOAD_FACTORS["half"]
        else:
            return LOAD_FACTORS["full"]
    
    def _get_wtw_multiplier(self, fleet_type: str, energy_source: str) -> float:
        """
        Get well-to-wheel multiplier for lifecycle emissions.
        
        Args:
            fleet_type: Type of fleet
            energy_source: Energy source type
            
        Returns:
            Multiplier for well-to-wheel emissions
        """
        # Well-to-wheel includes production, processing, and distribution
        wtw_multipliers = {
            "hydrogen": 1.1 if energy_source == "green" else 1.5,  # Green vs grey hydrogen
            "electric": 1.15 if energy_source == "renewable" else 1.25,  # Renewable vs grid
            "biodiesel": 1.2,  # Includes production
            "hybrid": 1.3,  # Includes fuel production
            "cng": 1.35,  # Includes extraction and processing
            "diesel": 1.4,  # Includes refining and distribution
        }
        
        return wtw_multipliers.get(fleet_type, 1.3)
    
    def _calculate_baseline_emissions(self, distance_miles: float, load_tons: float) -> float:
        """
        Calculate baseline diesel emissions for comparison.
        
        Args:
            distance_miles: Distance in miles
            load_tons: Load in tons
            
        Returns:
            Baseline emissions in kg CO2e
        """
        diesel_factor = self.config.emission_factors.diesel
        diesel_efficiency = EFFICIENCY_FACTORS["diesel"]
        load_factor = self._calculate_load_factor(load_tons, 20.0)  # Assume 20-ton capacity
        wtw_multiplier = self._get_wtw_multiplier("diesel", "standard")
        
        baseline = (distance_miles * diesel_factor * load_factor / diesel_efficiency) * wtw_multiplier
        return baseline
    
    def _determine_energy_source(self, vendor_data: Dict[str, Any]) -> str:
        """
        Determine energy source from vendor data.
        
        Args:
            vendor_data: Vendor information
            
        Returns:
            Energy source type
        """
        fleet_type = vendor_data.get("fleet_type", "").lower()
        certifications = vendor_data.get("certifications", [])
        eco_rating = vendor_data.get("eco_rating", 0)
        
        # Check for renewable/green certifications
        renewable_certs = ["carbon neutral", "renewable", "green", "leed"]
        has_renewable = any(
            any(cert_keyword in cert.lower() for cert_keyword in renewable_certs)
            for cert in certifications
        )
        
        if fleet_type == "hydrogen":
            return "green" if (has_renewable or eco_rating >= 4.8) else "grey"
        elif fleet_type == "electric":
            return "renewable" if (has_renewable or eco_rating >= 4.7) else "grid"
        else:
            return "standard"
    
    def get_emissions_summary(self, emissions_list: List[RouteEmissions]) -> Dict[str, Any]:
        """
        Generate summary statistics for emissions calculations.
        
        Args:
            emissions_list: List of RouteEmissions objects
            
        Returns:
            Summary dictionary
        """
        if not emissions_list:
            return {
                "total_vendors": 0,
                "total_emissions": 0,
                "average_emissions": 0,
                "best_vendor": None,
                "worst_vendor": None,
            }
        
        total_emissions = sum(e.total_emissions_kg for e in emissions_list)
        average_emissions = total_emissions / len(emissions_list)
        
        # Find best and worst
        best = min(emissions_list, key=lambda e: e.total_emissions_kg)
        worst = max(emissions_list, key=lambda e: e.total_emissions_kg)
        
        # Calculate total potential savings
        total_baseline = sum(e.baseline_emissions_kg or 0 for e in emissions_list)
        total_savings = total_baseline - total_emissions
        
        return {
            "total_vendors": len(emissions_list),
            "total_emissions_kg": round(total_emissions, 2),
            "average_emissions_kg": round(average_emissions, 2),
            "total_baseline_kg": round(total_baseline, 2),
            "total_savings_kg": round(total_savings, 2),
            "average_reduction_percent": round(
                sum(e.emissions_reduction_percent or 0 for e in emissions_list) / len(emissions_list), 2
            ),
            "best_vendor": {
                "id": best.vendor_id,
                "name": best.vendor_name,
                "emissions_kg": best.total_emissions_kg,
                "fleet_type": best.fleet_type,
            },
            "worst_vendor": {
                "id": worst.vendor_id,
                "name": worst.vendor_name,
                "emissions_kg": worst.total_emissions_kg,
                "fleet_type": worst.fleet_type,
            },
            "fleet_type_breakdown": self._get_fleet_breakdown(emissions_list),
        }
    
    def _get_fleet_breakdown(self, emissions_list: List[RouteEmissions]) -> Dict[str, Any]:
        """Get emissions breakdown by fleet type."""
        breakdown = {}
        
        for emission in emissions_list:
            fleet_type = emission.fleet_type
            if fleet_type not in breakdown:
                breakdown[fleet_type] = {
                    "count": 0,
                    "total_emissions": 0,
                    "average_emissions": 0,
                }
            
            breakdown[fleet_type]["count"] += 1
            breakdown[fleet_type]["total_emissions"] += emission.total_emissions_kg
        
        # Calculate averages
        for fleet_type in breakdown:
            count = breakdown[fleet_type]["count"]
            total = breakdown[fleet_type]["total_emissions"]
            breakdown[fleet_type]["average_emissions"] = round(total / count, 2) if count > 0 else 0
            breakdown[fleet_type]["total_emissions"] = round(total, 2)
        
        return breakdown


# Global calculator instance
emissions_calculator = EmissionsCalculator()


# Made with Bob