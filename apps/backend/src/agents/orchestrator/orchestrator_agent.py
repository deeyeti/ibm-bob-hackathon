"""
Orchestrator Agent

This agent coordinates the Monitor and Auditor agents, managing the workflow
of weather monitoring, vendor analysis, and emissions optimization.

This file can be executed directly to run the complete workflow:
    python -m src.agents.orchestrator.orchestrator_agent
"""

import asyncio
import logging
import os
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..base_agent import BaseAgent
from ..monitor.monitor_agent import MonitorAgent
from ..monitor.weather_monitor import BeeAIWeatherMonitorAgent
from ..auditor.auditor_agent import AuditorAgent
from ..auditor.beeai_auditor import BeeAIAuditorAgent
from .message_bus import (
    MessageBus, Message, MessageType, MessagePriority,
    get_message_bus, initialize_message_bus
)
from .config import OrchestratorConfig, get_config
from src.utils.logger import get_logger
from dotenv import load_dotenv

load_dotenv()


logger = get_logger(__name__)


class OrchestratorAgent(BaseAgent):
    """
    Orchestrator Agent that coordinates Monitor and Auditor agents.
    
    Responsibilities:
    - Initialize and manage child agents
    - Coordinate workflow between agents
    - Handle weather alerts from Monitor Agent
    - Trigger audits based on weather conditions
    - Aggregate and provide results to frontend
    - Manage agent lifecycle
    """
    
    def __init__(self, config: Optional[OrchestratorConfig] = None):
        super().__init__(
            agent_id="orchestrator-001",
            name="Orchestrator",
            agent_type="orchestrator"
        )
        
        self.config = config or get_config()
        self.message_bus: Optional[MessageBus] = None
        
        # Child agents
        self.monitor_agent: Optional[MonitorAgent] = None
        self.auditor_agent: Optional[AuditorAgent] = None
        
        # State tracking
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
        self.last_weather_check: Optional[datetime] = None
        self.last_audit: Optional[datetime] = None
        
        # Results cache
        self.latest_weather_data: Optional[Dict[str, Any]] = None
        self.latest_audit_results: Optional[Dict[str, Any]] = None
        
        logger.info(f"Orchestrator agent initialized: {self.name}")
    
    async def initialize(self):
        """Initialize the orchestrator and child agents"""
        try:
            logger.info("Initializing orchestrator agent...")
            
            # Initialize message bus
            self.message_bus = await initialize_message_bus(
                max_queue_size=self.config.message_queue_size,
                default_ttl=self.config.message_ttl
            )
            
            # Subscribe to relevant message types
            self._setup_message_handlers()
            
            # Initialize child agents
            if self.config.auto_start_agents:
                await self._initialize_child_agents()
            
            self.status = "initialized"
            logger.info("Orchestrator agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize orchestrator: {e}", exc_info=True)
            self.status = "error"
            raise
    
    async def _initialize_child_agents(self):
        """Initialize Monitor and Auditor agents"""
        try:
            # Initialize Monitor Agent
            logger.info("Initializing Monitor Agent...")
            self.monitor_agent = MonitorAgent()
            await self.monitor_agent.initialize()
            
            # Initialize Auditor Agent
            logger.info("Initializing Auditor Agent...")
            self.auditor_agent = AuditorAgent()
            await self.auditor_agent.initialize()
            
            logger.info("Child agents initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize child agents: {e}", exc_info=True)
            raise
    
    def _setup_message_handlers(self):
        """Set up handlers for different message types"""
        if not self.message_bus:
            return
        
        # Subscribe to weather alerts
        self.message_bus.subscribe(
            MessageType.WEATHER_ALERT.value,
            self._handle_weather_alert
        )
        
        # Subscribe to audit results
        self.message_bus.subscribe(
            MessageType.AUDIT_RESULT.value,
            self._handle_audit_result
        )
        
        # Subscribe to agent status updates
        self.message_bus.subscribe(
            MessageType.AGENT_STATUS.value,
            self._handle_agent_status
        )
        
        # Subscribe to errors
        self.message_bus.subscribe(
            MessageType.ERROR.value,
            self._handle_error
        )
        
        logger.info("Message handlers configured")
    
    async def execute(self) -> Dict[str, Any]:
        """
        Execute the orchestrator's main workflow
        
        Returns:
            Dictionary containing workflow results
        """
        try:
            self.status = "running"
            logger.info("Starting orchestrator workflow...")
            
            results = {
                "timestamp": datetime.utcnow().isoformat(),
                "workflow_id": f"workflow_{datetime.utcnow().timestamp()}",
                "steps": []
            }
            
            # Step 1: Check weather conditions
            logger.info("Step 1: Checking weather conditions...")
            weather_data = await self._check_weather()
            results["steps"].append({
                "step": "weather_check",
                "status": "completed",
                "data": weather_data
            })
            self.latest_weather_data = weather_data
            
            # Step 2: Determine if audit is needed
            needs_audit = self._should_trigger_audit(weather_data)
            
            if needs_audit:
                logger.info("Step 2: Weather conditions require audit...")
                
                # Step 3: Get affected vendors
                affected_vendors = weather_data.get("affected_vendors", [])
                
                # Step 4: Run audit
                logger.info(f"Step 3: Running audit for {len(affected_vendors)} vendors...")
                audit_results = await self._run_audit(affected_vendors)
                results["steps"].append({
                    "step": "audit",
                    "status": "completed",
                    "data": audit_results
                })
                self.latest_audit_results = audit_results
                self.last_audit = datetime.utcnow()
            else:
                logger.info("No audit needed based on current weather conditions")
                results["steps"].append({
                    "step": "audit",
                    "status": "skipped",
                    "reason": "No severe weather conditions detected"
                })
            
            results["status"] = "completed"
            self.status = "idle"
            
            logger.info("Orchestrator workflow completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error in orchestrator workflow: {e}", exc_info=True)
            self.status = "error"
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _check_weather(self) -> Dict[str, Any]:
        """Check weather conditions using Monitor Agent"""
        try:
            if not self.monitor_agent:
                raise RuntimeError("Monitor agent not initialized")
            
            # Run monitor agent
            weather_data = await self.monitor_agent.run()
            self.last_weather_check = datetime.utcnow()
            
            return weather_data
            
        except Exception as e:
            logger.error(f"Error checking weather: {e}", exc_info=True)
            raise
    
    async def _run_audit(self, vendor_ids: List[str]) -> Dict[str, Any]:
        """Run audit using Auditor Agent"""
        try:
            if not self.auditor_agent:
                raise RuntimeError("Auditor agent not initialized")
            
            # Prepare audit request
            audit_request = {
                "vendor_ids": vendor_ids,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Run auditor agent
            audit_results = await self.auditor_agent.execute()
            
            return audit_results
            
        except Exception as e:
            logger.error(f"Error running audit: {e}", exc_info=True)
            raise
    
    def _should_trigger_audit(self, weather_data: Dict[str, Any]) -> bool:
        """Determine if an audit should be triggered based on weather data"""
        alerts = weather_data.get("alerts", [])
        affected_vendors = weather_data.get("affected_vendors", [])
        
        # Trigger audit if there are alerts and affected vendors
        return len(alerts) > 0 and len(affected_vendors) > 0
    
    async def _handle_weather_alert(self, message: Message):
        """Handle weather alert messages"""
        try:
            logger.info(f"Received weather alert: {message.id}")
            
            alert_data = message.payload
            affected_vendors = alert_data.get("affected_vendors", [])
            
            if affected_vendors:
                # Trigger audit for affected vendors
                logger.info(f"Triggering audit for {len(affected_vendors)} affected vendors")
                await self._run_audit(affected_vendors)
            
        except Exception as e:
            logger.error(f"Error handling weather alert: {e}", exc_info=True)
    
    async def _handle_audit_result(self, message: Message):
        """Handle audit result messages"""
        try:
            logger.info(f"Received audit result: {message.id}")
            self.latest_audit_results = message.payload
            
        except Exception as e:
            logger.error(f"Error handling audit result: {e}", exc_info=True)
    
    async def _handle_agent_status(self, message: Message):
        """Handle agent status update messages"""
        try:
            logger.debug(f"Agent status update: {message.payload}")
            
        except Exception as e:
            logger.error(f"Error handling agent status: {e}", exc_info=True)
    
    async def _handle_error(self, message: Message):
        """Handle error messages"""
        try:
            logger.error(f"Error message received: {message.payload}")
            
        except Exception as e:
            logger.error(f"Error handling error message: {e}", exc_info=True)
    
    async def start(self):
        """Start the orchestrator and child agents"""
        try:
            logger.info("Starting orchestrator agent...")
            
            if not self.message_bus:
                await self.initialize()
            
            # Start child agents
            if self.monitor_agent:
                await self.monitor_agent.start()
            
            if self.auditor_agent:
                await self.auditor_agent.start()
            
            self.status = "running"
            logger.info("Orchestrator agent started")
            
        except Exception as e:
            logger.error(f"Error starting orchestrator: {e}", exc_info=True)
            self.status = "error"
            raise
    
    async def stop(self):
        """Stop the orchestrator and child agents"""
        try:
            logger.info("Stopping orchestrator agent...")
            
            # Stop child agents
            if self.monitor_agent:
                await self.monitor_agent.stop()
            
            if self.auditor_agent:
                await self.auditor_agent.stop()
            
            self.status = "stopped"
            logger.info("Orchestrator agent stopped")
            
        except Exception as e:
            logger.error(f"Error stopping orchestrator: {e}", exc_info=True)
            raise
    
    def get_info(self) -> Dict[str, Any]:
        """Get orchestrator information and status"""
        info = super().get_info()
        
        info.update({
            "config": {
                "max_retries": self.config.max_retries,
                "retry_delay": self.config.retry_delay,
                "timeout": self.config.timeout,
                "auto_start_agents": self.config.auto_start_agents
            },
            "child_agents": {
                "monitor": self.monitor_agent.get_info() if self.monitor_agent else None,
                "auditor": self.auditor_agent.get_info() if self.auditor_agent else None
            },
            "last_weather_check": self.last_weather_check.isoformat() if self.last_weather_check else None,
            "last_audit": self.last_audit.isoformat() if self.last_audit else None,
            "active_workflows": len(self.active_workflows),
            "message_bus_stats": self.message_bus.get_stats() if self.message_bus else None
        })
        
        return info
    
    async def get_latest_results(self) -> Dict[str, Any]:
        """Get the latest weather and audit results"""
        return {
            "weather": self.latest_weather_data,
            "audit": self.latest_audit_results,
            "last_weather_check": self.last_weather_check.isoformat() if self.last_weather_check else None,
            "last_audit": self.last_audit.isoformat() if self.last_audit else None
        }
    
    async def trigger_manual_audit(self, vendor_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Manually trigger an audit
        
        Args:
            vendor_ids: Optional list of vendor IDs to audit. If None, audits all vendors.
            
        Returns:
            Audit results
        """
        try:
            logger.info(f"Manual audit triggered for {len(vendor_ids) if vendor_ids else 'all'} vendors")
            
            if vendor_ids is None:
                # Get all vendors from monitor agent
                if self.monitor_agent:
                    weather_data = await self.monitor_agent.run()
                    vendor_ids = [v["id"] for v in weather_data.get("vendors", [])]
                else:
                    vendor_ids = []
            
            results = await self._run_audit(vendor_ids)
            return results
            
        except Exception as e:
            logger.error(f"Error in manual audit: {e}", exc_info=True)
            raise
    
    async def cleanup(self):
        """Clean up resources"""
        try:
            logger.info("Cleaning up orchestrator agent...")
            
            # Stop child agents
            await self.stop()
            
            # Shutdown message bus
            if self.message_bus:
                await self.message_bus.stop()
            
            logger.info("Orchestrator agent cleaned up")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}", exc_info=True)
            raise


# Global orchestrator instance
_orchestrator: Optional[OrchestratorAgent] = None


def get_orchestrator() -> OrchestratorAgent:
    """Get the global orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = OrchestratorAgent()
    return _orchestrator


async def initialize_orchestrator(config: Optional[OrchestratorConfig] = None) -> OrchestratorAgent:
    """Initialize and start the global orchestrator"""
    global _orchestrator
    _orchestrator = OrchestratorAgent(config)
    await _orchestrator.initialize()
    await _orchestrator.start()
    return _orchestrator


async def shutdown_orchestrator():
    """Shutdown the global orchestrator"""
    global _orchestrator
    if _orchestrator:
        await _orchestrator.cleanup()
        _orchestrator = None

# Made with Bob


# ============================================================================
# BeeAI-Based Orchestrator Workflow
# ============================================================================


def print_shift_order(
    weather_response: Dict[str, Any],
    audit_result: Dict[str, Any],
    workflow_id: str,
) -> None:
    """
    Print ESG-compliant Shift Order to console.
    
    Args:
        weather_response: Response from WeatherMonitorAgent
        audit_result: Response from AuditorAgent
        workflow_id: Unique workflow identifier
    """
    timestamp = datetime.utcnow().isoformat()
    
    # Extract data
    location = weather_response.get("location", "Unknown")
    weather_reason = weather_response.get("reason", "Severe weather detected")
    
    approved_vendor_id = audit_result.get("approved_vendor_id", "N/A")
    emissions_saving = audit_result.get("emissions_saving", "N/A")
    justification = audit_result.get("justification", "No justification provided")
    vendors_analyzed = audit_result.get("vendors_analyzed", 0)
    
    # Find approved vendor details from alternative_vendors
    vendor_name = "Unknown Vendor"
    fleet_type = "Unknown"
    eco_rating = "N/A"
    
    alternative_vendors = weather_response.get("alternative_vendors", [])
    for vendor in alternative_vendors:
        if vendor.get("id") == approved_vendor_id:
            vendor_name = vendor.get("name", "Unknown Vendor")
            fleet_type = vendor.get("fleet_type", "Unknown")
            eco_rating = vendor.get("eco_rating", "N/A")
            break
    
    # Determine ESG compliance status
    esg_compliant = fleet_type.lower() in ["hydrogen", "electric"]
    esg_status = "✓ Zero-emission fleet" if esg_compliant else "○ Low-emission fleet"
    
    # Print formatted shift order
    print("\n" + "═" * 70)
    print(" " * 18 + "ESG-COMPLIANT SHIFT ORDER")
    print("═" * 70)
    print(f"Order ID: {workflow_id}")
    print(f"Timestamp: {timestamp}")
    print(f"Status: APPROVED")
    print()
    
    print("WEATHER ALERT")
    print("─" * 70)
    print(f"Location: {location}")
    print(f"Severity: HIGH")
    print(f"Reason: {weather_reason}")
    print()
    
    print("APPROVED VENDOR")
    print("─" * 70)
    print(f"Vendor ID: {approved_vendor_id}")
    print(f"Vendor Name: {vendor_name}")
    print(f"Fleet Type: {fleet_type.capitalize()}")
    print(f"Eco Rating: {eco_rating}/5.0")
    print()
    
    print("EMISSIONS IMPACT")
    print("─" * 70)
    print(f"Emissions Saving: {emissions_saving}")
    print(f"Vendors Analyzed: {vendors_analyzed}")
    print(f"ESG Compliance: {esg_status}")
    print()
    
    print("JUSTIFICATION")
    print("─" * 70)
    # Wrap justification text to 70 characters
    words = justification.split()
    line = ""
    for word in words:
        if len(line) + len(word) + 1 <= 70:
            line += word + " "
        else:
            print(line.strip())
            line = word + " "
    if line:
        print(line.strip())
    print()
    
    print("═" * 70)
    print()


async def run_beeai_orchestrator_workflow(
    target_location: Optional[str] = None,
    openweather_api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run the complete BeeAI-based orchestrator workflow.
    
    This workflow:
    1. Runs WeatherMonitorAgent to check weather conditions
    2. If status is 'reroute_required', extracts alternative_vendors
    3. Passes alternative_vendors to AuditorAgent for analysis
    4. Prints ESG-compliant Shift Order to console
    
    Args:
        target_location: Location to monitor (defaults to env var)
        openweather_api_key: OpenWeather API key (defaults to env var)
        
    Returns:
        Dictionary with workflow results
    """
    workflow_id = f"SHIFT-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    
    logger.info(f"Starting BeeAI Orchestrator Workflow: {workflow_id}")
    print(f"\n🚀 Starting Orchestrator Workflow: {workflow_id}\n")
    
    try:
        # ====================================================================
        # STEP 1: Initialize and Run WeatherMonitorAgent
        # ====================================================================
        print("📡 Step 1: Checking weather conditions...")
        logger.info("Initializing WeatherMonitorAgent")
        
        weather_agent = BeeAIWeatherMonitorAgent(
            target_location=target_location or os.getenv('TARGET_LOCATION', 'New York,US'),
            api_key=openweather_api_key or os.getenv('OPENWEATHER_API_KEY'),
        )
        
        # Run weather check
        weather_response = await weather_agent.check_weather()
        
        # Convert Pydantic model to dict
        if hasattr(weather_response, 'model_dump'):
            weather_dict = weather_response.model_dump()
        elif hasattr(weather_response, 'dict'):
            weather_dict = weather_response.dict()
        else:
            weather_dict = dict(weather_response) if isinstance(weather_response, dict) else {}
        
        logger.info(f"Weather check complete: status={weather_dict.get('status')}")
        print(f"   Status: {weather_dict.get('status')}")
        
        # ====================================================================
        # STEP 2: Check if Reroute is Required
        # ====================================================================
        if weather_dict.get("status") != "reroute_required":
            print("\n✅ Weather conditions are clear. No reroute required.")
            logger.info("Workflow complete: No reroute needed")
            
            # Close weather agent
            await weather_agent.close()
            
            return {
                "workflow_id": workflow_id,
                "status": "completed",
                "reroute_required": False,
                "weather_status": weather_dict.get("status"),
                "weather_condition": weather_dict.get("weather"),
                "timestamp": datetime.utcnow().isoformat(),
            }
        
        # ====================================================================
        # STEP 3: Extract Alternative Vendors
        # ====================================================================
        print("\n⚠️  Severe weather detected! Reroute required.")
        print(f"   Reason: {weather_dict.get('reason')}")
        
        alternative_vendors = weather_dict.get("alternative_vendors", [])
        
        if not alternative_vendors:
            logger.error("No alternative vendors available")
            print("\n❌ Error: No alternative vendors available for reroute")
            await weather_agent.close()
            return {
                "workflow_id": workflow_id,
                "status": "error",
                "error": "No alternative vendors available",
                "timestamp": datetime.utcnow().isoformat(),
            }
        
        print(f"\n📦 Step 2: Found {len(alternative_vendors)} alternative vendors")
        logger.info(f"Extracted {len(alternative_vendors)} alternative vendors")
        
        # ====================================================================
        # STEP 4: Initialize and Run AuditorAgent
        # ====================================================================
        print("\n🔍 Step 3: Analyzing vendors for emissions optimization...")
        logger.info("Initializing BeeAIAuditorAgent")
        
        auditor_agent = BeeAIAuditorAgent()
        
        # Prepare vendor payload
        vendor_payload = {
            "vendors": alternative_vendors,
            "location": target_location or os.getenv('TARGET_LOCATION', 'New York,US'),
        }
        
        # Run vendor analysis
        audit_result = await auditor_agent.analyze_vendors(vendor_payload)
        
        logger.info(f"Audit complete: approved_vendor={audit_result.get('approved_vendor_id')}")
        print(f"   Approved Vendor: {audit_result.get('approved_vendor_id')}")
        print(f"   Emissions Saving: {audit_result.get('emissions_saving')}")
        
        # ====================================================================
        # STEP 5: Print ESG-Compliant Shift Order
        # ====================================================================
        print("\n📋 Step 4: Generating ESG-Compliant Shift Order...")
        
        # Add location to weather response for shift order
        weather_dict["location"] = target_location or os.getenv('TARGET_LOCATION', 'New York,US')
        
        print_shift_order(
            weather_response=weather_dict,
            audit_result=audit_result,
            workflow_id=workflow_id,
        )
        
        # ====================================================================
        # STEP 6: Cleanup and Return Results
        # ====================================================================
        logger.info("Workflow complete: Shift order generated")
        print("✅ Workflow completed successfully!\n")
        
        # Close agents
        await weather_agent.close()
        await auditor_agent.close()
        
        return {
            "workflow_id": workflow_id,
            "status": "completed",
            "reroute_required": True,
            "weather_response": weather_dict,
            "audit_result": audit_result,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
    except Exception as e:
        logger.error(f"Error in orchestrator workflow: {e}", exc_info=True)
        print(f"\n❌ Error: {str(e)}\n")
        return {
            "workflow_id": workflow_id,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }


# ============================================================================
# Main Execution Block
# ============================================================================


async def main():
    """Main entry point for running the orchestrator workflow."""
    print("\n" + "=" * 70)
    print(" " * 15 + "ECO-SHIFT ORCHESTRATOR AGENT")
    print("=" * 70)
    print("\nBeeAI-based workflow for weather monitoring and vendor optimization")
    print("Integrates WeatherMonitorAgent → AuditorAgent → Shift Order\n")
    
    # Check environment variables
    openweather_key = os.getenv('OPENWEATHER_API_KEY')
    watsonx_key = os.getenv('WATSONX_API_KEY')
    watsonx_project = os.getenv('WATSONX_PROJECT_ID')
    target_location = os.getenv('TARGET_LOCATION', 'New York,US')
    
    if not openweather_key:
        print("❌ Error: OPENWEATHER_API_KEY environment variable not set")
        print("   Please set it in your .env file\n")
        sys.exit(1)
    
    if not watsonx_key or not watsonx_project:
        print("⚠️  Warning: WATSONX_API_KEY or WATSONX_PROJECT_ID not set")
        print("   Auditor agent may not function properly\n")
    
    print(f"📍 Target Location: {target_location}")
    print(f"🔑 OpenWeather API: {'✓ Configured' if openweather_key else '✗ Missing'}")
    print(f"🔑 Watsonx API: {'✓ Configured' if watsonx_key else '✗ Missing'}")
    print()
    
    # Run workflow
    result = await run_beeai_orchestrator_workflow(
        target_location=target_location,
        openweather_api_key=openweather_key,
    )
    
    # Print summary
    print("\n" + "=" * 70)
    print(" " * 22 + "WORKFLOW SUMMARY")
    print("=" * 70)
    print(f"Workflow ID: {result.get('workflow_id')}")
    status = result.get('status', 'unknown')
    print(f"Status: {status.upper() if status else 'UNKNOWN'}")
    print(f"Reroute Required: {'Yes' if result.get('reroute_required') else 'No'}")
    print(f"Timestamp: {result.get('timestamp')}")
    
    if result.get('status') == 'error':
        print(f"Error: {result.get('error')}")
    
    print("=" * 70 + "\n")


if __name__ == "__main__":
    """
    Run the orchestrator workflow directly from command line:
    
    Usage:
        python -m src.agents.orchestrator.orchestrator_agent
        
    Or from the backend directory:
        cd apps/backend
        python -m src.agents.orchestrator.orchestrator_agent
        
    Environment Variables:
        TARGET_LOCATION: Location to monitor (default: "New York,US")
        OPENWEATHER_API_KEY: OpenWeather API key (required)
        WATSONX_API_KEY: IBM watsonx API key (required)
        WATSONX_PROJECT_ID: IBM watsonx project ID (required)
    """
    asyncio.run(main())


# Made with Bob
