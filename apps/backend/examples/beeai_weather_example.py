"""
Example usage of the BeeAI Weather Monitor Agent.

This script demonstrates how to use the BeeAI-based weather monitoring agent
to check weather conditions and get reroute recommendations.

Requirements:
    - BeeAI framework installed: pip install bee-agent-framework
    - Environment variables set: OPENWEATHER_API_KEY, TARGET_LOCATION
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agents.monitor.weather_monitor import (
    BeeAIWeatherMonitorAgent,
    create_beeai_weather_agent,
    BEEAI_AVAILABLE,
)
from utils.logger import get_logger

logger = get_logger(__name__)


async def example_basic_usage():
    """Example 1: Basic usage with explicit parameters."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    try:
        # Create agent with explicit parameters
        agent = BeeAIWeatherMonitorAgent(
            target_location="New York,US",
            api_key=os.getenv("OPENWEATHER_API_KEY")
        )
        
        # Run weather check
        result = await agent.run()
        
        # Display results
        print(f"\n📍 Location: New York,US")
        print(f"📊 Status: {result['status']}")
        
        if result['status'] == 'clear':
            print(f"☀️  Weather: {result['weather']}")
        elif result['status'] == 'reroute_required':
            print(f"⚠️  Reason: {result['reason']}")
            print(f"📦 Alternative Vendors: {len(result.get('alternative_vendors', []))}")
            
            # Show first 3 vendors
            vendors = result.get('alternative_vendors', [])[:3]
            for i, vendor in enumerate(vendors, 1):
                print(f"\n   {i}. {vendor['name']}")
                print(f"      Fleet: {vendor['fleet_type']} ({vendor['fleet_size']} vehicles)")
                print(f"      Eco Rating: {vendor['eco_rating']}/5.0")
                print(f"      Contact: {vendor['contact_email']}")
        else:
            print(f"❌ Error: {result.get('reason', 'Unknown error')}")
        
        # Cleanup
        await agent.close()
        
    except Exception as e:
        logger.error(f"Error in basic usage example: {e}")
        print(f"❌ Error: {e}")


async def example_environment_variables():
    """Example 2: Using environment variables."""
    print("\n" + "=" * 60)
    print("Example 2: Using Environment Variables")
    print("=" * 60)
    
    try:
        # Agent reads from TARGET_LOCATION and OPENWEATHER_API_KEY env vars
        agent = BeeAIWeatherMonitorAgent()
        
        print(f"\n📍 Location: {agent.target_location}")
        
        result = await agent.run()
        print(f"📊 Status: {result['status']}")
        
        if result['status'] == 'clear':
            print(f"☀️  Weather: {result['weather']}")
        elif result['status'] == 'reroute_required':
            print(f"⚠️  Severe weather detected!")
            print(f"   Reason: {result['reason']}")
            print(f"   Vendors available: {len(result.get('alternative_vendors', []))}")
        
        await agent.close()
        
    except Exception as e:
        logger.error(f"Error in environment variables example: {e}")
        print(f"❌ Error: {e}")


async def example_multiple_locations():
    """Example 3: Check multiple locations."""
    print("\n" + "=" * 60)
    print("Example 3: Multiple Locations")
    print("=" * 60)
    
    locations = [
        "New York,US",
        "Los Angeles,US",
        "Chicago,US",
        "Miami,US",
    ]
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    for location in locations:
        try:
            agent = BeeAIWeatherMonitorAgent(
                target_location=location,
                api_key=api_key
            )
            
            result = await agent.run()
            
            status_icon = "☀️" if result['status'] == 'clear' else "⚠️"
            print(f"\n{status_icon} {location}: {result['status']}")
            
            if result['status'] == 'clear':
                print(f"   Weather: {result['weather']}")
            elif result['status'] == 'reroute_required':
                print(f"   Reason: {result['reason']}")
            
            await agent.close()
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"❌ {location}: Error - {e}")


async def example_continuous_monitoring():
    """Example 4: Continuous monitoring (runs for 3 iterations)."""
    print("\n" + "=" * 60)
    print("Example 4: Continuous Monitoring")
    print("=" * 60)
    print("\nMonitoring weather every 10 seconds (3 iterations)...")
    
    agent = BeeAIWeatherMonitorAgent()
    
    try:
        for i in range(3):
            print(f"\n🔄 Check #{i + 1}")
            result = await agent.run()
            
            print(f"   Status: {result['status']}")
            if result['status'] == 'clear':
                print(f"   Weather: {result['weather']}")
            elif result['status'] == 'reroute_required':
                print(f"   ⚠️  ALERT: {result['reason']}")
            
            if i < 2:  # Don't sleep after last iteration
                await asyncio.sleep(10)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring stopped by user")
    finally:
        await agent.close()


async def example_helper_function():
    """Example 5: Using helper function."""
    print("\n" + "=" * 60)
    print("Example 5: Using Helper Function")
    print("=" * 60)
    
    # Create agent using helper function
    agent = await create_beeai_weather_agent(
        target_location="Seattle,US"
    )
    
    if agent:
        print(f"\n✅ Agent created successfully")
        print(f"📍 Location: {agent.target_location}")
        
        result = await agent.run()
        print(f"📊 Status: {result['status']}")
        
        await agent.close()
    else:
        print("❌ Failed to create agent (BeeAI not available)")


async def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("BeeAI Weather Monitor Agent - Examples")
    print("=" * 60)
    
    # Check if BeeAI is available
    if not BEEAI_AVAILABLE:
        print("\n❌ BeeAI framework is not installed!")
        print("\nTo install BeeAI:")
        print("  pip install bee-agent-framework")
        print("\nOr add to pyproject.toml dependencies:")
        print('  "bee-agent-framework>=1.0.0"')
        return
    
    # Check for API key
    if not os.getenv("OPENWEATHER_API_KEY"):
        print("\n❌ OPENWEATHER_API_KEY environment variable not set!")
        print("\nSet it with:")
        print("  export OPENWEATHER_API_KEY=your_key_here")
        return
    
    print("\n✅ BeeAI framework is available")
    print("✅ API key is configured")
    
    # Run examples
    try:
        await example_basic_usage()
        await example_environment_variables()
        await example_multiple_locations()
        await example_helper_function()
        await example_continuous_monitoring()
        
    except Exception as e:
        logger.error(f"Error running examples: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    # Run examples
    asyncio.run(main())

# Made with Bob
