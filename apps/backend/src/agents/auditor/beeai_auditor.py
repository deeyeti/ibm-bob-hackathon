"""
BeeAI-based Auditor Agent for emissions analysis and vendor recommendations.

This module implements the Auditor Agent using the BeeAI framework to:
1. Accept alternative_vendors payload from Monitor Agent
2. Calculate route emissions using watsonx.ai
3. Parse AI response and return structured JSON with vendor recommendations
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import re
import asyncio

from src.services.watsonx_service import watsonx_service
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Import BeeAI framework
try:
    from bee_agent.agents.bee_agent import BeeAgent
    from bee_agent.tools.base import Tool, ToolResult
    BEEAI_AVAILABLE = True
except ImportError:
    # Fallback if BeeAI not installed
    BeeAgent = None
    Tool = None
    ToolResult = None
    BEEAI_AVAILABLE = False
    logger.warning("BeeAI framework not available. Using fallback implementation.")


class EmissionsCalculationTool(Tool if BEEAI_AVAILABLE else object):
    """Tool for calculating route emissions using watsonx.ai."""
    
    def __init__(self):
        """Initialize emissions calculation tool."""
        if BEEAI_AVAILABLE:
            super().__init__(
                name="calculate_emissions",
                description="Calculate route emissions and analyze vendors using IBM watsonx.ai",
                input_schema={
                    "type": "object",
                    "properties": {
                        "vendor_data": {
                            "type": "object",
                            "description": "Vendor data including fleet types, routes, and characteristics"
                        }
                    },
                    "required": ["vendor_data"]
                }
            )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute emissions calculation using watsonx.ai.
        
        Args:
            input_data: Tool input containing vendor_data
            
        Returns:
            Tool output with AI analysis
        """
        try:
            vendor_data = input_data.get("vendor_data", {})
            if not vendor_data:
                return {
                    "success": False,
                    "error": "vendor_data parameter is required"
                }
            
            # Initialize watsonx service if needed
            if not watsonx_service._initialized:
                await watsonx_service.initialize()
            
            # Call watsonx service to calculate emissions
            logger.info("Calling watsonx.ai for emissions calculation")
            ai_response = await watsonx_service.calculate_route_emissions(vendor_data)
            
            return {
                "success": True,
                "data": {
                    "ai_analysis": ai_response
                }
            }
        except Exception as e:
            logger.error(f"Error calculating emissions: {e}", exc_info=True)
            return {
                "success": False,
                "error": f"Failed to calculate emissions: {str(e)}"
            }


class BeeAIAuditorAgent:
    """
    BeeAI-based Auditor Agent for vendor emissions analysis.
    
    This agent:
    1. Accepts alternative_vendors payload from Monitor Agent
    2. Uses watsonx.ai to calculate route emissions and analyze vendors
    3. Parses AI response to extract vendor recommendations
    4. Returns structured JSON with approved vendor, emissions savings, and justification
    """
    
    def __init__(self):
        """Initialize BeeAI Auditor Agent."""
        # Initialize emissions calculation tool
        self.emissions_tool = EmissionsCalculationTool()
        
        # Initialize BeeAI agent (only if available)
        if BEEAI_AVAILABLE:
            self.agent = BeeAgent(
                name="AuditorAgent",
                description="Analyze vendor emissions and recommend optimal vendors",
                tools=[self.emissions_tool],
                system_prompt=self._get_system_prompt(),
            )
        else:
            self.agent = None
        
        logger.info("BeeAI Auditor Agent initialized")
    
    def _get_system_prompt(self) -> str:
        """
        Get system prompt for the agent.
        
        Returns:
            System prompt string
        """
        return """You are an emissions auditor agent for freight logistics.

Your task is to:
1. Analyze vendor data including fleet types, routes, and operational characteristics
2. Calculate Scope 3 carbon emissions for each vendor
3. STRONGLY PRIORITIZE Hydrogen and Electric fleets (zero direct emissions)
4. Recommend the best vendor based on lowest carbon footprint
5. Provide emissions savings compared to baseline diesel operations
6. Justify your recommendation with specific environmental benefits

Always use the calculate_emissions tool to analyze vendors before making recommendations.
Return responses in structured JSON format."""
    
    def _parse_ai_response(self, ai_response: str, vendor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse AI response to extract vendor recommendation.
        
        This method implements robust parsing to extract:
        - Approved vendor ID
        - Emissions savings
        - Justification
        
        Args:
            ai_response: Raw AI response text
            vendor_data: Original vendor data for fallback
            
        Returns:
            Structured recommendation dictionary
        """
        try:
            logger.info("Parsing AI response for vendor recommendation")
            
            # Initialize result structure
            result = {
                "approved_vendor_id": None,
                "emissions_saving": None,
                "justification": None
            }
            
            # Extract vendor information from response
            # Look for patterns like "recommend", "best", "optimal", "choose"
            recommendation_patterns = [
                r"recommend(?:ed|ing)?\s+(?:vendor\s+)?([A-Za-z0-9_-]+)",
                r"best\s+(?:vendor\s+)?(?:is\s+)?([A-Za-z0-9_-]+)",
                r"optimal\s+(?:vendor\s+)?(?:is\s+)?([A-Za-z0-9_-]+)",
                r"choose\s+(?:vendor\s+)?([A-Za-z0-9_-]+)",
                r"vendor\s+([A-Za-z0-9_-]+)\s+(?:is|has|offers)",
            ]
            
            # Try to find vendor ID in response
            for pattern in recommendation_patterns:
                match = re.search(pattern, ai_response, re.IGNORECASE)
                if match:
                    potential_vendor_id = match.group(1)
                    # Verify this vendor exists in the data
                    vendors = vendor_data.get("vendors", [])
                    for vendor in vendors:
                        if vendor.get("id") == potential_vendor_id or vendor.get("name", "").lower() in potential_vendor_id.lower():
                            result["approved_vendor_id"] = vendor.get("id")
                            break
                    if result["approved_vendor_id"]:
                        break
            
            # If no vendor found, prioritize hydrogen/electric fleets
            if not result["approved_vendor_id"]:
                logger.warning("Could not extract vendor from AI response, using fallback logic")
                vendors = vendor_data.get("vendors", [])
                for vendor in vendors:
                    fleet_type = vendor.get("fleet_type", "").lower()
                    if fleet_type in ["hydrogen", "electric"]:
                        result["approved_vendor_id"] = vendor.get("id")
                        logger.info(f"Fallback: Selected {fleet_type} vendor {vendor.get('id')}")
                        break
                
                # If still no hydrogen/electric, take first vendor
                if not result["approved_vendor_id"] and vendors:
                    result["approved_vendor_id"] = vendors[0].get("id")
                    logger.info(f"Fallback: Selected first vendor {vendors[0].get('id')}")
            
            # Extract emissions savings
            # Look for patterns like "X kg", "X kg CO2", "X% reduction"
            savings_patterns = [
                r"(?:sav(?:e|ing)s?|reduc(?:e|tion|ing))\s+(?:of\s+)?(\d+(?:\.\d+)?)\s*(?:kg|kilograms?)",
                r"(\d+(?:\.\d+)?)\s*kg\s+(?:CO2|carbon|emissions?)\s+(?:sav(?:ed|ings?)|reduc(?:ed|tion))",
                r"(\d+(?:\.\d+)?)\s*%\s+(?:reduc(?:tion|ed)|less|lower)",
            ]
            
            for pattern in savings_patterns:
                match = re.search(pattern, ai_response, re.IGNORECASE)
                if match:
                    result["emissions_saving"] = match.group(1)
                    break
            
            # If no savings found, estimate based on fleet type
            if not result["emissions_saving"] and result["approved_vendor_id"]:
                vendors = vendor_data.get("vendors", [])
                for vendor in vendors:
                    if vendor.get("id") == result["approved_vendor_id"]:
                        fleet_type = vendor.get("fleet_type", "").lower()
                        # Estimate savings based on fleet type
                        if fleet_type == "hydrogen":
                            result["emissions_saving"] = "100% (zero direct emissions)"
                        elif fleet_type == "electric":
                            result["emissions_saving"] = "100% (zero direct emissions)"
                        elif fleet_type == "hybrid":
                            result["emissions_saving"] = "50% (hybrid efficiency)"
                        else:
                            result["emissions_saving"] = "baseline diesel"
                        break
            
            # Extract justification
            # Look for sentences containing key sustainability terms
            justification_keywords = [
                "hydrogen", "electric", "zero emissions", "carbon", "sustainable",
                "environmental", "clean", "renewable", "eco-friendly"
            ]
            
            sentences = re.split(r'[.!?]+', ai_response)
            justification_sentences = []
            
            for sentence in sentences:
                sentence = sentence.strip()
                if any(keyword in sentence.lower() for keyword in justification_keywords):
                    justification_sentences.append(sentence)
            
            if justification_sentences:
                result["justification"] = ". ".join(justification_sentences[:3]) + "."
            else:
                # Fallback justification
                if result["approved_vendor_id"]:
                    vendors = vendor_data.get("vendors", [])
                    for vendor in vendors:
                        if vendor.get("id") == result["approved_vendor_id"]:
                            fleet_type = vendor.get("fleet_type", "").lower()
                            result["justification"] = (
                                f"Selected {vendor.get('name')} with {fleet_type} fleet "
                                f"for optimal environmental performance and emissions reduction."
                            )
                            break
            
            logger.info(f"Parsed recommendation: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}", exc_info=True)
            # Return fallback result
            vendors = vendor_data.get("vendors", [])
            if vendors:
                return {
                    "approved_vendor_id": vendors[0].get("id"),
                    "emissions_saving": "Unable to calculate",
                    "justification": "Error parsing AI response. Selected first available vendor."
                }
            return {
                "approved_vendor_id": None,
                "emissions_saving": None,
                "justification": "Error: No vendors available"
            }
    
    async def analyze_vendors(self, alternative_vendors: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze alternative vendors and provide recommendation.
        
        This is the main method that:
        1. Accepts alternative_vendors payload from Monitor Agent
        2. Calls watsonx.ai via calculate_route_emissions
        3. Parses AI response
        4. Returns structured JSON recommendation
        
        Args:
            alternative_vendors: Payload from Monitor Agent containing vendor list
            
        Returns:
            Structured recommendation with approved_vendor_id, emissions_saving, justification
        """
        try:
            logger.info("Starting vendor analysis")
            
            # Validate input
            if not alternative_vendors:
                logger.error("No vendor data provided")
                return {
                    "status": "error",
                    "error": "No vendor data provided",
                    "approved_vendor_id": None,
                    "emissions_saving": None,
                    "justification": "No vendors to analyze"
                }
            
            # Extract vendors list
            vendors = alternative_vendors.get("vendors", [])
            if not vendors:
                logger.error("Vendor list is empty")
                return {
                    "status": "error",
                    "error": "Vendor list is empty",
                    "approved_vendor_id": None,
                    "emissions_saving": None,
                    "justification": "No vendors available for analysis"
                }
            
            logger.info(f"Analyzing {len(vendors)} vendors")
            
            # Call emissions calculation tool
            tool_result = await self.emissions_tool.execute({
                "vendor_data": alternative_vendors
            })
            
            if not tool_result.get("success"):
                error_msg = tool_result.get("error", "Unknown error")
                logger.error(f"Emissions calculation failed: {error_msg}")
                return {
                    "status": "error",
                    "error": error_msg,
                    "approved_vendor_id": None,
                    "emissions_saving": None,
                    "justification": f"Failed to calculate emissions: {error_msg}"
                }
            
            # Extract AI analysis
            ai_analysis = tool_result.get("data", {}).get("ai_analysis", "")
            logger.info("AI analysis received, parsing response")
            
            # Parse AI response to extract recommendation
            recommendation = self._parse_ai_response(ai_analysis, alternative_vendors)
            
            # Add status and timestamp
            recommendation["status"] = "success"
            recommendation["timestamp"] = datetime.utcnow().isoformat()
            recommendation["vendors_analyzed"] = len(vendors)
            recommendation["ai_analysis_raw"] = ai_analysis  # Include raw response for debugging
            
            logger.info(
                f"Analysis complete: Approved vendor {recommendation['approved_vendor_id']}, "
                f"Savings: {recommendation['emissions_saving']}"
            )
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error during vendor analysis: {e}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "approved_vendor_id": None,
                "emissions_saving": None,
                "justification": f"Analysis failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def close(self) -> None:
        """Close agent and cleanup resources."""
        try:
            # Close watsonx service if needed
            if watsonx_service._initialized:
                await watsonx_service.close()
            logger.info("BeeAI Auditor Agent closed")
        except Exception as e:
            logger.error(f"Error closing agent: {e}")


# Global instance
beeai_auditor_agent = BeeAIAuditorAgent()


# Helper function for easy access
async def analyze_alternative_vendors(alternative_vendors: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze alternative vendors and provide recommendation.
    
    This is a convenience function that wraps the BeeAI Auditor Agent.
    
    Args:
        alternative_vendors: Payload from Monitor Agent containing vendor list
        
    Returns:
        Structured recommendation with approved_vendor_id, emissions_saving, justification
    """
    return await beeai_auditor_agent.analyze_vendors(alternative_vendors)


# Made with Bob