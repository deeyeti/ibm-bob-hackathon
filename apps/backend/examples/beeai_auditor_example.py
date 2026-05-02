"""
Example usage of BeeAI Auditor Agent.

This example demonstrates how to:
1. Create alternative_vendors payload (from Monitor Agent)
2. Pass it to the BeeAI Auditor Agent
3. Receive structured JSON recommendation

Run this example:
    python -m examples.beeai_auditor_example
"""

import asyncio
import json
from src.agents.auditor.beeai_auditor import analyze_alternative_vendors


async def main():
    """Run BeeAI Auditor Agent example."""
    
    # Example payload from Monitor Agent
    # This would typically come from the weather monitor when severe weather is detected
    alternative_vendors = {
        "status": "reroute_required",
        "reason": "severe storm conditions",
        "location": "New York,US",
        "vendors": [
            {
                "id": "vendor_001",
                "name": "GreenFleet Logistics",
                "location": "Newark, NJ",
                "fleet_type": "hydrogen",
                "fleet_size": 50,
                "capacity_tons": 500,
                "eco_rating": 4.9,
                "reliability_score": 0.95,
                "cost_per_mile": 2.5,
                "carbon_emissions_kg_per_mile": 0.0,
                "service_areas": ["Northeast US", "Mid-Atlantic"],
                "contact_email": "dispatch@greenfleet.com",
                "contact_phone": "+1-555-0101"
            },
            {
                "id": "vendor_002",
                "name": "EcoTransit Solutions",
                "location": "Philadelphia, PA",
                "fleet_type": "electric",
                "fleet_size": 35,
                "capacity_tons": 350,
                "eco_rating": 4.8,
                "reliability_score": 0.92,
                "cost_per_mile": 2.3,
                "carbon_emissions_kg_per_mile": 0.0,
                "service_areas": ["Northeast US", "Mid-Atlantic"],
                "contact_email": "ops@ecotransit.com",
                "contact_phone": "+1-555-0102"
            },
            {
                "id": "vendor_003",
                "name": "HybridHaul Express",
                "location": "Baltimore, MD",
                "fleet_type": "hybrid",
                "fleet_size": 75,
                "capacity_tons": 750,
                "eco_rating": 4.5,
                "reliability_score": 0.88,
                "cost_per_mile": 2.0,
                "carbon_emissions_kg_per_mile": 1.34,
                "service_areas": ["Northeast US", "Mid-Atlantic", "Southeast US"],
                "contact_email": "dispatch@hybridhaul.com",
                "contact_phone": "+1-555-0103"
            },
            {
                "id": "vendor_004",
                "name": "Standard Freight Co",
                "location": "Richmond, VA",
                "fleet_type": "diesel",
                "fleet_size": 120,
                "capacity_tons": 1200,
                "eco_rating": 3.8,
                "reliability_score": 0.85,
                "cost_per_mile": 1.8,
                "carbon_emissions_kg_per_mile": 2.68,
                "service_areas": ["Northeast US", "Mid-Atlantic", "Southeast US"],
                "contact_email": "dispatch@standardfreight.com",
                "contact_phone": "+1-555-0104"
            }
        ]
    }
    
    print("=" * 80)
    print("BeeAI Auditor Agent Example")
    print("=" * 80)
    print()
    
    print("Input: Alternative Vendors Payload")
    print("-" * 80)
    print(f"Status: {alternative_vendors['status']}")
    print(f"Reason: {alternative_vendors['reason']}")
    print(f"Location: {alternative_vendors['location']}")
    print(f"Number of vendors: {len(alternative_vendors['vendors'])}")
    print()
    
    print("Vendors:")
    for vendor in alternative_vendors['vendors']:
        print(f"  - {vendor['name']} ({vendor['fleet_type']}) - "
              f"Eco Rating: {vendor['eco_rating']}, "
              f"Emissions: {vendor['carbon_emissions_kg_per_mile']} kg/mile")
    print()
    
    print("=" * 80)
    print("Analyzing vendors with BeeAI Auditor Agent...")
    print("=" * 80)
    print()
    
    # Call the BeeAI Auditor Agent
    try:
        result = await analyze_alternative_vendors(alternative_vendors)
        
        print("Analysis Result:")
        print("-" * 80)
        print(json.dumps(result, indent=2))
        print()
        
        if result.get("status") == "success":
            print("=" * 80)
            print("Recommendation Summary")
            print("=" * 80)
            print(f"Approved Vendor ID: {result.get('approved_vendor_id')}")
            print(f"Emissions Saving: {result.get('emissions_saving')}")
            print(f"Justification: {result.get('justification')}")
            print(f"Vendors Analyzed: {result.get('vendors_analyzed')}")
            print(f"Timestamp: {result.get('timestamp')}")
            print()
            
            # Find the approved vendor details
            approved_id = result.get('approved_vendor_id')
            if approved_id:
                for vendor in alternative_vendors['vendors']:
                    if vendor['id'] == approved_id:
                        print("=" * 80)
                        print("Approved Vendor Details")
                        print("=" * 80)
                        print(f"Name: {vendor['name']}")
                        print(f"Fleet Type: {vendor['fleet_type']}")
                        print(f"Location: {vendor['location']}")
                        print(f"Eco Rating: {vendor['eco_rating']}")
                        print(f"Reliability: {vendor['reliability_score']}")
                        print(f"Cost per Mile: ${vendor['cost_per_mile']}")
                        print(f"Carbon Emissions: {vendor['carbon_emissions_kg_per_mile']} kg/mile")
                        print(f"Contact: {vendor['contact_email']}")
                        break
        else:
            print("=" * 80)
            print("Analysis Failed")
            print("=" * 80)
            print(f"Error: {result.get('error')}")
    
    except Exception as e:
        print(f"Error running example: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())


# Made with Bob