"""
Freight vendor data management for the Monitor Agent.
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field


class FleetType(str, Enum):
    """Fleet type enumeration."""
    HYDROGEN = "hydrogen"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
    DIESEL = "diesel"
    BIODIESEL = "biodiesel"
    CNG = "cng"  # Compressed Natural Gas


class VendorStatus(str, Enum):
    """Vendor availability status."""
    AVAILABLE = "available"
    LIMITED = "limited"
    UNAVAILABLE = "unavailable"


class FreightVendor(BaseModel):
    """Freight vendor model."""
    id: str = Field(description="Unique vendor identifier")
    name: str = Field(description="Vendor company name")
    location: str = Field(description="Primary operating location")
    fleet_type: FleetType = Field(description="Primary fleet type")
    fleet_size: int = Field(description="Number of vehicles in fleet")
    capacity_tons: float = Field(description="Total capacity in tons")
    contact_email: str = Field(description="Contact email")
    contact_phone: str = Field(description="Contact phone number")
    service_areas: List[str] = Field(description="Geographic service areas")
    eco_rating: float = Field(ge=0, le=5, description="Environmental rating (0-5)")
    reliability_score: float = Field(ge=0, le=100, description="Reliability score (0-100)")
    cost_per_mile: float = Field(description="Average cost per mile in USD")
    carbon_emissions_kg_per_mile: float = Field(description="Carbon emissions per mile")
    status: VendorStatus = Field(default=VendorStatus.AVAILABLE, description="Current availability status")
    certifications: List[str] = Field(default=[], description="Environmental certifications")
    notes: Optional[str] = Field(default=None, description="Additional notes")


# Freight Vendor Database
FREIGHT_VENDORS: List[Dict[str, Any]] = [
    {
        "id": "VND-001",
        "name": "GreenHaul Logistics",
        "location": "Los Angeles, CA",
        "fleet_type": FleetType.HYDROGEN,
        "fleet_size": 150,
        "capacity_tons": 3000,
        "contact_email": "dispatch@greenhaul.com",
        "contact_phone": "+1-310-555-0101",
        "service_areas": ["California", "Nevada", "Arizona", "Oregon"],
        "eco_rating": 5.0,
        "reliability_score": 95.0,
        "cost_per_mile": 2.85,
        "carbon_emissions_kg_per_mile": 0.05,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["ISO 14001", "SmartWay", "Green Freight"],
        "notes": "Hydrogen fuel cell fleet with zero emissions",
    },
    {
        "id": "VND-002",
        "name": "EcoFreight Express",
        "location": "New York, NY",
        "fleet_type": FleetType.ELECTRIC,
        "fleet_size": 200,
        "capacity_tons": 4000,
        "contact_email": "operations@ecofreight.com",
        "contact_phone": "+1-212-555-0202",
        "service_areas": ["New York", "New Jersey", "Pennsylvania", "Connecticut", "Massachusetts"],
        "eco_rating": 4.8,
        "reliability_score": 92.0,
        "cost_per_mile": 2.65,
        "carbon_emissions_kg_per_mile": 0.08,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["ISO 14001", "SmartWay", "LEED Certified"],
        "notes": "100% electric fleet powered by renewable energy",
    },
    {
        "id": "VND-003",
        "name": "HydroTrans Solutions",
        "location": "Chicago, IL",
        "fleet_type": FleetType.HYDROGEN,
        "fleet_size": 120,
        "capacity_tons": 2500,
        "contact_email": "contact@hydrotrans.com",
        "contact_phone": "+1-312-555-0303",
        "service_areas": ["Illinois", "Indiana", "Wisconsin", "Michigan", "Ohio"],
        "eco_rating": 5.0,
        "reliability_score": 94.0,
        "cost_per_mile": 2.90,
        "carbon_emissions_kg_per_mile": 0.04,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["ISO 14001", "SmartWay", "Carbon Neutral"],
        "notes": "Hydrogen-powered fleet with advanced fuel cell technology",
    },
    {
        "id": "VND-004",
        "name": "CleanRide Freight",
        "location": "Houston, TX",
        "fleet_type": FleetType.ELECTRIC,
        "fleet_size": 180,
        "capacity_tons": 3600,
        "contact_email": "dispatch@cleanride.com",
        "contact_phone": "+1-713-555-0404",
        "service_areas": ["Texas", "Louisiana", "Oklahoma", "Arkansas"],
        "eco_rating": 4.7,
        "reliability_score": 90.0,
        "cost_per_mile": 2.70,
        "carbon_emissions_kg_per_mile": 0.09,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["SmartWay", "Green Freight"],
        "notes": "Electric fleet with solar charging stations",
    },
    {
        "id": "VND-005",
        "name": "SustainaTrans",
        "location": "Seattle, WA",
        "fleet_type": FleetType.HYDROGEN,
        "fleet_size": 100,
        "capacity_tons": 2000,
        "contact_email": "info@sustainatrans.com",
        "contact_phone": "+1-206-555-0505",
        "service_areas": ["Washington", "Oregon", "Idaho", "Montana"],
        "eco_rating": 4.9,
        "reliability_score": 93.0,
        "cost_per_mile": 2.80,
        "carbon_emissions_kg_per_mile": 0.06,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["ISO 14001", "SmartWay", "B Corp Certified"],
        "notes": "Hydrogen fleet with commitment to sustainability",
    },
    {
        "id": "VND-006",
        "name": "ElectroHaul Logistics",
        "location": "Miami, FL",
        "fleet_type": FleetType.ELECTRIC,
        "fleet_size": 140,
        "capacity_tons": 2800,
        "contact_email": "operations@electrohaul.com",
        "contact_phone": "+1-305-555-0606",
        "service_areas": ["Florida", "Georgia", "South Carolina", "Alabama"],
        "eco_rating": 4.6,
        "reliability_score": 88.0,
        "cost_per_mile": 2.75,
        "carbon_emissions_kg_per_mile": 0.10,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["SmartWay", "Green Business"],
        "notes": "Electric fleet optimized for coastal routes",
    },
    {
        "id": "VND-007",
        "name": "H2 Transport Co",
        "location": "Denver, CO",
        "fleet_type": FleetType.HYDROGEN,
        "fleet_size": 90,
        "capacity_tons": 1800,
        "contact_email": "dispatch@h2transport.com",
        "contact_phone": "+1-303-555-0707",
        "service_areas": ["Colorado", "Wyoming", "Utah", "New Mexico"],
        "eco_rating": 5.0,
        "reliability_score": 91.0,
        "cost_per_mile": 2.95,
        "carbon_emissions_kg_per_mile": 0.05,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["ISO 14001", "SmartWay", "Carbon Neutral"],
        "notes": "Specialized in high-altitude hydrogen transport",
    },
    {
        "id": "VND-008",
        "name": "GreenWheels Freight",
        "location": "Atlanta, GA",
        "fleet_type": FleetType.HYBRID,
        "fleet_size": 160,
        "capacity_tons": 3200,
        "contact_email": "contact@greenwheels.com",
        "contact_phone": "+1-404-555-0808",
        "service_areas": ["Georgia", "Tennessee", "North Carolina", "Virginia"],
        "eco_rating": 4.3,
        "reliability_score": 89.0,
        "cost_per_mile": 2.50,
        "carbon_emissions_kg_per_mile": 0.35,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["SmartWay", "Green Freight"],
        "notes": "Hybrid fleet transitioning to full electric",
    },
    {
        "id": "VND-009",
        "name": "ZeroEmission Logistics",
        "location": "Boston, MA",
        "fleet_type": FleetType.ELECTRIC,
        "fleet_size": 130,
        "capacity_tons": 2600,
        "contact_email": "info@zeroemission.com",
        "contact_phone": "+1-617-555-0909",
        "service_areas": ["Massachusetts", "Rhode Island", "New Hampshire", "Vermont", "Maine"],
        "eco_rating": 4.8,
        "reliability_score": 92.0,
        "cost_per_mile": 2.68,
        "carbon_emissions_kg_per_mile": 0.07,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["ISO 14001", "SmartWay", "LEED Certified"],
        "notes": "Electric fleet with renewable energy commitment",
    },
    {
        "id": "VND-010",
        "name": "HydroFleet Services",
        "location": "Dallas, TX",
        "fleet_type": FleetType.HYDROGEN,
        "fleet_size": 110,
        "capacity_tons": 2200,
        "contact_email": "dispatch@hydrofleet.com",
        "contact_phone": "+1-214-555-1010",
        "service_areas": ["Texas", "Oklahoma", "Kansas", "Missouri"],
        "eco_rating": 4.9,
        "reliability_score": 93.0,
        "cost_per_mile": 2.88,
        "carbon_emissions_kg_per_mile": 0.05,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["ISO 14001", "SmartWay", "Green Freight"],
        "notes": "Hydrogen fleet with advanced logistics technology",
    },
    {
        "id": "VND-011",
        "name": "EcoDrive Transport",
        "location": "Phoenix, AZ",
        "fleet_type": FleetType.ELECTRIC,
        "fleet_size": 95,
        "capacity_tons": 1900,
        "contact_email": "operations@ecodrive.com",
        "contact_phone": "+1-602-555-1111",
        "service_areas": ["Arizona", "Nevada", "New Mexico", "California"],
        "eco_rating": 4.7,
        "reliability_score": 90.0,
        "cost_per_mile": 2.72,
        "carbon_emissions_kg_per_mile": 0.08,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["SmartWay", "Green Business"],
        "notes": "Electric fleet optimized for desert conditions",
    },
    {
        "id": "VND-012",
        "name": "CleanFuel Logistics",
        "location": "Portland, OR",
        "fleet_type": FleetType.BIODIESEL,
        "fleet_size": 170,
        "capacity_tons": 3400,
        "contact_email": "contact@cleanfuel.com",
        "contact_phone": "+1-503-555-1212",
        "service_areas": ["Oregon", "Washington", "California", "Idaho"],
        "eco_rating": 4.2,
        "reliability_score": 87.0,
        "cost_per_mile": 2.45,
        "carbon_emissions_kg_per_mile": 0.45,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["SmartWay", "Renewable Fuel Standard"],
        "notes": "Biodiesel fleet using sustainable fuel sources",
    },
    {
        "id": "VND-013",
        "name": "H2 Express Freight",
        "location": "San Francisco, CA",
        "fleet_type": FleetType.HYDROGEN,
        "fleet_size": 125,
        "capacity_tons": 2500,
        "contact_email": "dispatch@h2express.com",
        "contact_phone": "+1-415-555-1313",
        "service_areas": ["California", "Nevada", "Oregon", "Washington"],
        "eco_rating": 5.0,
        "reliability_score": 94.0,
        "cost_per_mile": 2.92,
        "carbon_emissions_kg_per_mile": 0.04,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["ISO 14001", "SmartWay", "Carbon Neutral", "B Corp"],
        "notes": "Premium hydrogen fleet with tech integration",
    },
    {
        "id": "VND-014",
        "name": "GreenMile Transport",
        "location": "Minneapolis, MN",
        "fleet_type": FleetType.ELECTRIC,
        "fleet_size": 105,
        "capacity_tons": 2100,
        "contact_email": "info@greenmile.com",
        "contact_phone": "+1-612-555-1414",
        "service_areas": ["Minnesota", "Wisconsin", "Iowa", "North Dakota", "South Dakota"],
        "eco_rating": 4.6,
        "reliability_score": 89.0,
        "cost_per_mile": 2.70,
        "carbon_emissions_kg_per_mile": 0.09,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["SmartWay", "Green Freight"],
        "notes": "Electric fleet with cold-weather optimization",
    },
    {
        "id": "VND-015",
        "name": "SustainableShip Co",
        "location": "Philadelphia, PA",
        "fleet_type": FleetType.HYBRID,
        "fleet_size": 145,
        "capacity_tons": 2900,
        "contact_email": "operations@sustainableship.com",
        "contact_phone": "+1-215-555-1515",
        "service_areas": ["Pennsylvania", "New Jersey", "Delaware", "Maryland", "New York"],
        "eco_rating": 4.4,
        "reliability_score": 88.0,
        "cost_per_mile": 2.55,
        "carbon_emissions_kg_per_mile": 0.32,
        "status": VendorStatus.AVAILABLE,
        "certifications": ["SmartWay", "Green Business"],
        "notes": "Hybrid fleet with plans for full electrification",
    },
]


class VendorManager:
    """Manager for freight vendor operations."""

    def __init__(self):
        """Initialize vendor manager."""
        self.vendors = [FreightVendor(**vendor) for vendor in FREIGHT_VENDORS]

    def get_all_vendors(self) -> List[FreightVendor]:
        """Get all vendors."""
        return self.vendors

    def get_vendor_by_id(self, vendor_id: str) -> Optional[FreightVendor]:
        """Get vendor by ID."""
        for vendor in self.vendors:
            if vendor.id == vendor_id:
                return vendor
        return None

    def get_vendors_by_fleet_type(self, fleet_type: FleetType) -> List[FreightVendor]:
        """Get vendors by fleet type."""
        return [v for v in self.vendors if v.fleet_type == fleet_type]

    def get_eco_friendly_vendors(self, min_rating: float = 4.5) -> List[FreightVendor]:
        """Get eco-friendly vendors (hydrogen and electric with high ratings)."""
        return [
            v for v in self.vendors
            if v.fleet_type in [FleetType.HYDROGEN, FleetType.ELECTRIC]
            and v.eco_rating >= min_rating
            and v.status == VendorStatus.AVAILABLE
        ]

    def get_vendors_by_location(self, location: str) -> List[FreightVendor]:
        """Get vendors serving a specific location."""
        return [
            v for v in self.vendors
            if any(location.lower() in area.lower() for area in v.service_areas)
        ]

    def get_available_vendors(self) -> List[FreightVendor]:
        """Get all available vendors."""
        return [v for v in self.vendors if v.status == VendorStatus.AVAILABLE]

    def sort_by_eco_rating(self, vendors: List[FreightVendor]) -> List[FreightVendor]:
        """Sort vendors by eco rating (highest first)."""
        return sorted(vendors, key=lambda v: v.eco_rating, reverse=True)

    def sort_by_emissions(self, vendors: List[FreightVendor]) -> List[FreightVendor]:
        """Sort vendors by carbon emissions (lowest first)."""
        return sorted(vendors, key=lambda v: v.carbon_emissions_kg_per_mile)

    def get_recommendations_for_location(
        self,
        location: str,
        prioritize_eco: bool = True,
    ) -> List[FreightVendor]:
        """
        Get vendor recommendations for a location.
        
        Args:
            location: Location to get recommendations for
            prioritize_eco: Whether to prioritize eco-friendly vendors
            
        Returns:
            List of recommended vendors
        """
        vendors = self.get_vendors_by_location(location)
        
        if prioritize_eco:
            # Prioritize hydrogen and electric fleets
            eco_vendors = [
                v for v in vendors
                if v.fleet_type in [FleetType.HYDROGEN, FleetType.ELECTRIC]
            ]
            other_vendors = [
                v for v in vendors
                if v.fleet_type not in [FleetType.HYDROGEN, FleetType.ELECTRIC]
            ]
            
            # Sort each group
            eco_vendors = self.sort_by_emissions(eco_vendors)
            other_vendors = self.sort_by_emissions(other_vendors)
            
            return eco_vendors + other_vendors
        else:
            return self.sort_by_emissions(vendors)


# Global vendor manager instance
vendor_manager = VendorManager()

# Made with Bob