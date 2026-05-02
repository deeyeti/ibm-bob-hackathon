"""Simple test script to verify watsonx service functionality."""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.watsonx_service import WatsonxService


async def main():
    """Test watsonx service with simple vendor data."""
    print("=" * 60)
    print("Testing watsonx service...")
    print("=" * 60)
    
    # Create simple sample vendor data
    sample_vendors = [
        {
            "id": "vendor_1",
            "name": "Green Fleet Co",
            "fleet_type": "Electric",
            "location": "New York",
            "capacity": 100,
            "emissions_factor": 0.0
        },
        {
            "id": "vendor_2",
            "name": "Diesel Transport Inc",
            "fleet_type": "Diesel",
            "location": "Chicago",
            "capacity": 150,
            "emissions_factor": 2.68
        },
        {
            "id": "vendor_3",
            "name": "Hydrogen Logistics",
            "fleet_type": "Hydrogen",
            "location": "San Francisco",
            "capacity": 80,
            "emissions_factor": 0.0
        }
    ]
    
    # Wrap vendors in a dictionary as expected by the method
    vendor_data = {
        "vendors": sample_vendors,
        "route_info": {
            "origin": "New York",
            "destination": "Los Angeles",
            "distance_km": 4500
        }
    }
    
    print("\nSample vendor data:")
    for vendor in sample_vendors:
        print(f"  - {vendor['name']} ({vendor['fleet_type']})")
    
    print("\nInitializing WatsonxService...")
    try:
        service = WatsonxService()
        print("✓ Service initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize service: {e}")
        return
    
    print("\nCalling calculate_route_emissions...")
    print("(This may take 10-30 seconds for API response...)")
    try:
        response = await service.calculate_route_emissions(vendor_data)
        print("✓ Function call successful!")
        print("\n" + "=" * 60)
        print("MODEL RESPONSE:")
        print("=" * 60)
        print(response)
        print("=" * 60)
    except Exception as e:
        print(f"✗ Function call failed: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
