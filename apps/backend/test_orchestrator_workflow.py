#!/usr/bin/env python3
"""
Test script for the Orchestrator Workflow.

This script demonstrates the complete workflow:
1. WeatherMonitorAgent checks weather conditions
2. If severe weather detected, extracts alternative vendors
3. BeeAIAuditorAgent analyzes vendors and recommends optimal choice
4. Prints ESG-compliant Shift Order

Usage:
    python test_orchestrator_workflow.py
    
Or from backend directory:
    cd apps/backend
    python test_orchestrator_workflow.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path for imports
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from src.agents.orchestrator.orchestrator_agent import run_beeai_orchestrator_workflow


async def test_workflow():
    """Test the orchestrator workflow with different scenarios."""
    
    print("\n" + "=" * 70)
    print(" " * 15 + "ORCHESTRATOR WORKFLOW TEST")
    print("=" * 70)
    print()
    
    # Check environment variables
    openweather_key = os.getenv('OPENWEATHER_API_KEY')
    watsonx_key = os.getenv('WATSONX_API_KEY')
    watsonx_project = os.getenv('WATSONX_PROJECT_ID')
    
    if not openweather_key:
        print("❌ Error: OPENWEATHER_API_KEY not set")
        print("   Please set it in apps/backend/.env file")
        return
    
    if not watsonx_key or not watsonx_project:
        print("⚠️  Warning: WATSONX credentials not set")
        print("   Auditor agent may not function properly")
        print()
    
    # Test scenarios
    test_locations = [
        ("New York,US", "Major US city - may have varied weather"),
        ("Miami,US", "Coastal city - higher chance of severe weather"),
        ("Phoenix,US", "Desert city - typically clear weather"),
    ]
    
    print("Testing workflow with different locations:\n")
    
    for location, description in test_locations:
        print(f"\n{'─' * 70}")
        print(f"Testing: {location}")
        print(f"Description: {description}")
        print(f"{'─' * 70}\n")
        
        try:
            result = await run_beeai_orchestrator_workflow(
                target_location=location,
                openweather_api_key=openweather_key,
            )
            
            # Print result summary
            print(f"\n✓ Test completed for {location}")
            print(f"  Status: {result.get('status')}")
            print(f"  Reroute Required: {result.get('reroute_required')}")
            
            if result.get('status') == 'error':
                print(f"  Error: {result.get('error')}")
            
        except Exception as e:
            print(f"\n✗ Test failed for {location}")
            print(f"  Error: {str(e)}")
        
        # Wait between tests to avoid rate limiting
        print("\nWaiting 3 seconds before next test...")
        await asyncio.sleep(3)
    
    print("\n" + "=" * 70)
    print(" " * 20 + "ALL TESTS COMPLETED")
    print("=" * 70 + "\n")


async def test_single_location():
    """Test workflow with a single location (faster test)."""
    
    print("\n" + "=" * 70)
    print(" " * 12 + "SINGLE LOCATION WORKFLOW TEST")
    print("=" * 70)
    print()
    
    # Use environment variable or default
    location = os.getenv('TARGET_LOCATION', 'New York,US')
    
    print(f"Testing location: {location}\n")
    
    try:
        result = await run_beeai_orchestrator_workflow(
            target_location=location,
        )
        
        print(f"\n{'=' * 70}")
        print(" " * 25 + "TEST RESULT")
        print(f"{'=' * 70}")
        print(f"Status: {result.get('status')}")
        print(f"Reroute Required: {result.get('reroute_required')}")
        print(f"Workflow ID: {result.get('workflow_id')}")
        
        if result.get('status') == 'error':
            print(f"Error: {result.get('error')}")
        elif result.get('reroute_required'):
            audit = result.get('audit_result', {})
            print(f"Approved Vendor: {audit.get('approved_vendor_id')}")
            print(f"Emissions Saving: {audit.get('emissions_saving')}")
        
        print(f"{'=' * 70}\n")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}\n")
        raise


def main():
    """Main entry point."""
    
    # Check if user wants to test multiple locations
    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        print("\nRunning tests for multiple locations...")
        asyncio.run(test_workflow())
    else:
        print("\nRunning single location test...")
        print("(Use --all flag to test multiple locations)")
        asyncio.run(test_single_location())


if __name__ == "__main__":
    main()

# Made with Bob
