"""
Simple test for BeeAI Auditor Agent.
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_auditor():
    """Test the BeeAI Auditor Agent."""
    try:
        print("=" * 80)
        print("Testing BeeAI Auditor Agent")
        print("=" * 80)
        print()
        
        # Import the agent
        print("1. Importing BeeAI Auditor Agent...")
        from src.agents.auditor.beeai_auditor import analyze_alternative_vendors
        print("   [OK] Import successful")
        print()
        
        # Create test data
        print("2. Creating test vendor data...")
        alternative_vendors = {
            "status": "reroute_required",
            "reason": "severe storm conditions",
            "location": "New York,US",
            "vendors": [
                {
                    "id": "vendor_001",
                    "name": "GreenFleet Logistics",
                    "fleet_type": "hydrogen",
                    "eco_rating": 4.9,
                    "carbon_emissions_kg_per_mile": 0.0,
                },
                {
                    "id": "vendor_002",
                    "name": "Standard Freight",
                    "fleet_type": "diesel",
                    "eco_rating": 3.8,
                    "carbon_emissions_kg_per_mile": 2.68,
                }
            ]
        }
        print(f"   [OK] Created {len(alternative_vendors['vendors'])} test vendors")
        print()
        
        # Analyze vendors
        print("3. Analyzing vendors with watsonx.ai...")
        result = await analyze_alternative_vendors(alternative_vendors)
        print("   [OK] Analysis complete")
        print()
        
        # Display results
        print("=" * 80)
        print("RESULTS")
        print("=" * 80)
        print(f"Status: {result.get('status')}")
        print(f"Approved Vendor: {result.get('approved_vendor_id')}")
        print(f"Emissions Saving: {result.get('emissions_saving')}")
        print(f"Justification: {result.get('justification')}")
        print(f"Vendors Analyzed: {result.get('vendors_analyzed')}")
        print()
        
        if result.get('status') == 'success':
            print("[PASS] TEST PASSED")
        else:
            print("[FAIL] TEST FAILED")
            print(f"Error: {result.get('error')}")
        
        return result
        
    except Exception as e:
        print("[FAIL] TEST FAILED WITH EXCEPTION")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(test_auditor())
    sys.exit(0 if result and result.get('status') == 'success' else 1)

# Made with Bob
