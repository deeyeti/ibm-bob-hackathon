"""
Monitor Agent - Polls OpenWeather API for severe weather and retrieves vendor lists.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio

from src.agents.base_agent import BaseAgent, AgentStatus
from src.utils.logger import get_logger
from .config import MonitorConfig, monitor_config
from .weather_monitor import WeatherMonitor, WeatherAlert
from .vendors import VendorManager, vendor_manager, FreightVendor

logger = get_logger(__name__)


class MonitorAgent(BaseAgent):
    """
    Monitor Agent for weather monitoring and vendor management.
    
    Responsibilities:
    - Poll OpenWeather API for severe weather conditions
    - Monitor multiple shipping locations
    - Detect severe weather events (storms, hurricanes, extreme temperatures)
    - Retrieve alternative freight vendor lists when severe weather detected
    - Emit events to orchestrator for downstream processing
    """

    def __init__(
        self,
        agent_id: str = "monitor-agent-001",
        name: str = "Weather Monitor Agent",
        config: Optional[MonitorConfig] = None,
    ):
        """
        Initialize Monitor Agent.
        
        Args:
            agent_id: Unique agent identifier
            name: Human-readable agent name
            config: Monitor configuration (uses default if not provided)
        """
        super().__init__(agent_id=agent_id, name=name, agent_type="monitor")
        
        self.config = config or monitor_config
        self.weather_monitor = WeatherMonitor(self.config)
        self.vendor_manager = vendor_manager
        
        # Agent state
        self._polling_task: Optional[asyncio.Task] = None
        self._is_polling = False
        self._alerts: List[WeatherAlert] = []
        self._vendor_recommendations: Dict[str, List[FreightVendor]] = {}
        
        logger.info(f"Monitor Agent initialized with config: {self.config.dict()}")

    async def initialize(self) -> None:
        """Initialize agent resources and dependencies."""
        try:
            await self.weather_monitor.initialize()
            
            # Update metrics
            self.update_metrics({
                "monitored_locations": len(self.config.monitored_locations),
                "polling_interval": self.config.polling_interval,
                "total_vendors": len(self.vendor_manager.get_all_vendors()),
                "eco_friendly_vendors": len(self.vendor_manager.get_eco_friendly_vendors()),
            })
            
            logger.info(f"Monitor Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Monitor Agent: {e}")
            raise

    async def execute(self) -> Dict[str, Any]:
        """
        Execute agent's main task - check weather and retrieve vendors if needed.
        
        Returns:
            Dictionary with execution results
        """
        try:
            execution_start = datetime.utcnow()
            
            # Check weather at all monitored locations
            logger.info(f"Checking weather at {len(self.config.monitored_locations)} locations")
            alerts = await self.weather_monitor.check_all_locations()
            
            # Store alerts
            self._alerts.extend(alerts)
            
            # Process alerts and retrieve vendors if needed
            vendor_recommendations = {}
            if alerts and self.config.auto_retrieve_vendors:
                logger.info(f"Processing {len(alerts)} severe weather alerts")
                
                for alert in alerts:
                    location = alert["location"]
                    
                    # Get vendor recommendations for affected location
                    vendors = self.vendor_manager.get_recommendations_for_location(
                        location=location,
                        prioritize_eco=self.config.prioritize_eco_friendly,
                    )
                    
                    vendor_recommendations[location] = vendors
                    
                    logger.info(
                        f"Retrieved {len(vendors)} vendor recommendations for {location}"
                    )
            
            # Store vendor recommendations
            self._vendor_recommendations.update(vendor_recommendations)
            
            # Calculate execution time
            execution_time = (datetime.utcnow() - execution_start).total_seconds()
            
            # Update metrics
            self.update_metrics({
                "last_check_time": execution_start.isoformat(),
                "alerts_detected": len(alerts),
                "total_alerts": len(self._alerts),
                "locations_with_vendors": len(vendor_recommendations),
                "execution_time_seconds": execution_time,
                "cache_stats": self.weather_monitor.get_cache_stats(),
            })
            
            # Prepare result
            result = {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "alerts": [dict(alert) for alert in alerts],
                "vendor_recommendations": {
                    loc: [v.dict() for v in vendors]
                    for loc, vendors in vendor_recommendations.items()
                },
                "metrics": self.metrics,
            }
            
            # Log summary
            if alerts:
                logger.warning(
                    f"Execution complete: {len(alerts)} alerts, "
                    f"{len(vendor_recommendations)} locations with vendor recommendations"
                )
            else:
                logger.info("Execution complete: No severe weather detected")
            
            return result
            
        except Exception as e:
            logger.error(f"Error during agent execution: {e}")
            raise

    async def cleanup(self) -> None:
        """Cleanup agent resources."""
        try:
            # Stop polling if active
            if self._is_polling:
                await self.stop_polling()
            
            # Close weather monitor
            await self.weather_monitor.close()
            
            logger.info("Monitor Agent cleanup complete")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            raise

    async def start_polling(self) -> None:
        """Start continuous weather polling."""
        if self._is_polling:
            logger.warning("Polling already active")
            return
        
        self._is_polling = True
        self._polling_task = asyncio.create_task(self._polling_loop())
        logger.info(
            f"Started weather polling (interval: {self.config.polling_interval}s)"
        )

    async def stop_polling(self) -> None:
        """Stop continuous weather polling."""
        if not self._is_polling:
            logger.warning("Polling not active")
            return
        
        self._is_polling = False
        
        if self._polling_task:
            self._polling_task.cancel()
            try:
                await self._polling_task
            except asyncio.CancelledError:
                pass
            self._polling_task = None
        
        logger.info("Stopped weather polling")

    async def _polling_loop(self) -> None:
        """Internal polling loop."""
        logger.info("Polling loop started")
        
        while self._is_polling:
            try:
                # Execute monitoring task
                await self.run()
                
                # Calculate next run time
                self.next_run = datetime.utcnow() + timedelta(
                    seconds=self.config.polling_interval
                )
                
                # Wait for next interval
                await asyncio.sleep(self.config.polling_interval)
                
            except asyncio.CancelledError:
                logger.info("Polling loop cancelled")
                break
            except Exception as e:
                logger.error(f"Error in polling loop: {e}")
                # Continue polling even if there's an error
                await asyncio.sleep(self.config.polling_interval)
        
        logger.info("Polling loop stopped")

    def get_recent_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent weather alerts.
        
        Args:
            limit: Maximum number of alerts to return
            
        Returns:
            List of recent alerts
        """
        return [dict(alert) for alert in self._alerts[-limit:]]

    def get_vendor_recommendations(
        self,
        location: Optional[str] = None,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get vendor recommendations.
        
        Args:
            location: Specific location (returns all if not provided)
            
        Returns:
            Dictionary mapping locations to vendor lists
        """
        if location:
            vendors = self._vendor_recommendations.get(location, [])
            return {location: [v.dict() for v in vendors]}
        
        return {
            loc: [v.dict() for v in vendors]
            for loc, vendors in self._vendor_recommendations.items()
        }

    def get_all_vendors(self) -> List[Dict[str, Any]]:
        """
        Get all available vendors.
        
        Returns:
            List of all vendors
        """
        vendors = self.vendor_manager.get_all_vendors()
        return [v.dict() for v in vendors]

    def get_eco_friendly_vendors(self, min_rating: float = 4.5) -> List[Dict[str, Any]]:
        """
        Get eco-friendly vendors.
        
        Args:
            min_rating: Minimum eco rating
            
        Returns:
            List of eco-friendly vendors
        """
        vendors = self.vendor_manager.get_eco_friendly_vendors(min_rating=min_rating)
        return [v.dict() for v in vendors]

    async def check_location_weather(self, location: str) -> Optional[Dict[str, Any]]:
        """
        Check weather for a specific location on-demand.
        
        Args:
            location: Location to check
            
        Returns:
            Weather alert if severe weather detected, None otherwise
        """
        try:
            alert = await self.weather_monitor.check_location(location)
            
            if alert:
                self._alerts.append(alert)
                
                # Get vendor recommendations if configured
                if self.config.auto_retrieve_vendors:
                    vendors = self.vendor_manager.get_recommendations_for_location(
                        location=location,
                        prioritize_eco=self.config.prioritize_eco_friendly,
                    )
                    self._vendor_recommendations[location] = vendors
                    
                    return {
                        "alert": dict(alert),
                        "vendors": [v.dict() for v in vendors],
                    }
                
                return {"alert": dict(alert)}
            
            return None
            
        except Exception as e:
            logger.error(f"Error checking weather for {location}: {e}")
            raise

    async def get_location_forecast(
        self,
        location: str,
        days: int = 3,
    ) -> Dict[str, Any]:
        """
        Get weather forecast for a location.
        
        Args:
            location: Location to get forecast for
            days: Number of days for forecast
            
        Returns:
            Forecast data
        """
        return await self.weather_monitor.get_location_forecast(location, days=days)

    def clear_alerts(self) -> None:
        """Clear stored alerts."""
        self._alerts.clear()
        logger.info("Alerts cleared")

    def clear_vendor_recommendations(self) -> None:
        """Clear stored vendor recommendations."""
        self._vendor_recommendations.clear()
        logger.info("Vendor recommendations cleared")

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get agent statistics.
        
        Returns:
            Dictionary with agent statistics
        """
        return {
            "agent_info": self.get_info(),
            "total_alerts": len(self._alerts),
            "locations_monitored": len(self.config.monitored_locations),
            "locations_with_recommendations": len(self._vendor_recommendations),
            "total_vendors_available": len(self.vendor_manager.get_all_vendors()),
            "eco_friendly_vendors": len(self.vendor_manager.get_eco_friendly_vendors()),
            "is_polling": self._is_polling,
            "cache_stats": self.weather_monitor.get_cache_stats(),
            "alert_history": self.weather_monitor.get_alert_history(),
        }


# Made with Bob