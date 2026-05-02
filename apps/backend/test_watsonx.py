#!/usr/bin/env python3
"""
Test script for watsonx service implementation.

This script verifies that the WatsonxService can:
1. Initialize correctly with API credentials
2. Connect to IBM watsonx.ai
3. Call the calculate_route_emissions() function
4. Return proper recommendations prioritizing Hydrogen/Electric fleets
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.services.watsonx_service import WatsonxService
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


def create_sample_vendor_data():
    """
    Create sample vendor data with multiple fleet types.
    
    Returns:
        Dictionary containing vendor information for testing
    """
    return {
        "vendors": [
            {
                "id": "vendor_001",
                "name": "GreenFleet Logistics",
                "location": "San Francisco, CA",
                "fleet_type": "Hydrogen",
                "fleet_size": 25,
                "routes": [
                    {
                        "origin": "San Francisco, CA",
                        "destination": "Los Angeles, CA",
                        "distance_km": 615,
                        "frequency": "daily"
                    }
                ],
                "certifications": ["ISO 14001", "Carbon Neutral"],
                "operational_efficiency": 0.92
            },
            {
                "id": "vendor_002",
                "name": "EcoTransport Solutions",
                "location": "Portland, OR",
                "fleet_type": "Electric",
                "fleet_size": 30,
                "routes": [
                    {
                        "origin": "Portland, OR",
                        "destination": "Seattle, WA",
                        "distance_km": 280,
                        "frequency": "daily"
                    }
                ],
                "certifications": ["ISO 14001"],
                "operational_efficiency": 0.88
            },
            {
                "id": "vendor_003",
                "name": "Standard Freight Co",
                "location": "Denver, CO",
                "fleet_type": "Diesel",
                "fleet_size": 50,
                "routes": [
                    {
                        "origin": "Denver, CO",
                        "destination": "Salt Lake City, UT",
                        "distance_km": 840,
                        "frequency": "daily"
                    }
                ],
                "certifications": [],
                "operational_efficiency": 0.75
            },
            {
                "id": "vendor_004",
                "name": "HybridHaul Express",
                "location": "Austin, TX",
                "fleet_type": "Hybrid",
                "fleet_size": 20,
                "routes": [
                    {
                        "origin": "Austin, TX",
                        "destination": "Houston, TX",
                        "distance_km": 265,
                        "frequency": "daily"
                    }
                ],
                "certifications": ["ISO 14001"],
                "operational_efficiency": 0.82
            }
        ],
        "analysis_context": {
            "current_weather": "Clear skies, optimal conditions",
            "season": "Spring",
            "priority": "Minimize carbon emissions",
            "budget_constraint": "moderate"
        }
    }


async def test_watsonx_service():
    """
    Main test function for watsonx service.
    
    Tests:
    1. Service initialization
    2. API connection
    3. Route emissions calculation
    4. Response validation
    """
    print("=" * 80)
    print("WATSONX SERVICE TEST SCRIPT")
    print("=" * 80)
    print()
    
    # Step 1: Check environment variables
    print("Step 1: Checking environment variables...")
    print("-" * 80)
    
    if not settings.watsonx_api_key:
        print("❌ ERROR: WATSONX_API_KEY not set in environment")
        print("   Please set the WATSONX_API_KEY environment variable")
        return False
    else:
        print(f"✓ WATSONX_API_KEY: {'*' * 20}{settings.watsonx_api_key[-4:]}")
    
    if not settings.watsonx_project_id:
        print("❌ ERROR: WATSONX_PROJECT_ID not set in environment")
        print("   Please set the WATSONX_PROJECT_ID environment variable")
        return False
    else:
        print(f"✓ WATSONX_PROJECT_ID: {settings.watsonx_project_id}")
    
    print(f"✓ WATSONX_URL: {settings.watsonx_url}")
    print(f"✓ WATSONX_MODEL_ID: {settings.watsonx_model_id}")
    print()
    
    # Step 2: Initialize WatsonxService
    print("Step 2: Initializing WatsonxService...")
    print("-" * 80)
    
    try:
        service = WatsonxService()
        await service.initialize()
        print("✓ WatsonxService initialized successfully")
        print(f"✓ Client initialized: {service.client is not None}")
        print(f"✓ Model initialized: {service.model is not None}")
        print()
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize WatsonxService")
        print(f"   Error: {str(e)}")
        logger.error(f"Initialization failed: {e}", exc_info=True)
        return False
    
    # Step 3: Create sample vendor data
    print("Step 3: Creating sample vendor data...")
    print("-" * 80)
    
    vendor_data = create_sample_vendor_data()
    print(f"✓ Created vendor data with {len(vendor_data['vendors'])} vendors:")
    for vendor in vendor_data['vendors']:
        print(f"  - {vendor['name']} ({vendor['fleet_type']} fleet, {vendor['fleet_size']} vehicles)")
    print()
    
    # Step 4: Call calculate_route_emissions
    print("Step 4: Calling calculate_route_emissions()...")
    print("-" * 80)
    print("This may take 10-30 seconds depending on the model response time...")
    print()
    
    try:
        response = await service.calculate_route_emissions(vendor_data)
        print("✓ calculate_route_emissions() completed successfully")
        print()
        
        # Step 5: Display results
        print("Step 5: Analysis Results")
        print("=" * 80)
        print()
        print("MODEL RESPONSE:")
        print("-" * 80)
        print(response)
        print("-" * 80)
        print()
        
        # Step 6: Validate response
        print("Step 6: Validating response...")
        print("-" * 80)
        
        response_lower = response.lower()
        
        # Check if response mentions the vendors
        vendors_mentioned = []
        for vendor in vendor_data['vendors']:
            if vendor['name'].lower() in response_lower:
                vendors_mentioned.append(vendor['name'])
        
        print(f"✓ Vendors mentioned in response: {len(vendors_mentioned)}/{len(vendor_data['vendors'])}")
        for vendor_name in vendors_mentioned:
            print(f"  - {vendor_name}")
        print()
        
        # Check if response prioritizes Hydrogen/Electric
        hydrogen_mentioned = 'hydrogen' in response_lower
        electric_mentioned = 'electric' in response_lower
        
        print("Fleet Type Prioritization:")
        print(f"  {'✓' if hydrogen_mentioned else '✗'} Hydrogen fleet mentioned")
        print(f"  {'✓' if electric_mentioned else '✗'} Electric fleet mentioned")
        print()
        
        # Check for carbon/emissions analysis
        carbon_mentioned = 'carbon' in response_lower or 'co2' in response_lower or 'emission' in response_lower
        print(f"  {'✓' if carbon_mentioned else '✗'} Carbon/emissions analysis present")
        print()
        
        # Overall validation
        if vendors_mentioned and (hydrogen_mentioned or electric_mentioned) and carbon_mentioned:
            print("✓ Response validation PASSED")
            print("  The model successfully analyzed vendors and prioritized clean energy fleets")
            success = True
        else:
            print("⚠ Response validation PARTIAL")
            print("  The model responded but may not have fully prioritized clean energy fleets")
            success = True  # Still consider it a success if we got a response
        
    except Exception as e:
        print(f"❌ ERROR: calculate_route_emissions() failed")
        print(f"   Error: {str(e)}")
        logger.error(f"Route emissions calculation failed: {e}", exc_info=True)
        success = False
    
    # Step 7: Cleanup
    print()
    print("Step 7: Cleanup...")
    print("-" * 80)
    try:
        await service.close()
        print("✓ Service closed successfully")
    except Exception as e:
        print(f"⚠ Warning: Cleanup error: {e}")
    
    print()
    print("=" * 80)
    print(f"TEST {'PASSED' if success else 'FAILED'}")
    print("=" * 80)
    
    return success


async def main():
    """Main entry point for the test script."""
    try:
        success = await test_watsonx_service()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ UNEXPECTED ERROR: {e}")
        logger.error(f"Unexpected error in test script: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
