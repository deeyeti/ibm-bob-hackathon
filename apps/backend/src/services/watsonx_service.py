"""
IBM watsonx.ai service integration.
"""

import asyncio
import json
from typing import Optional, Dict, Any, List
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class WatsonxService:
    """Service for interacting with IBM watsonx.ai."""

    def __init__(self):
        """Initialize watsonx service."""
        self.client: Optional[APIClient] = None
        self.model: Optional[ModelInference] = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize watsonx.ai client and model."""
        if self._initialized:
            logger.warning("WatsonxService already initialized")
            return

        try:
            # Create credentials
            credentials = Credentials(
                api_key=settings.watsonx_api_key,
                url=settings.watsonx_url,
            )

            # Initialize API client
            self.client = APIClient(credentials)
            logger.info("Watsonx API client initialized successfully")

            # Initialize model inference
            self.model = ModelInference(
                model_id=settings.watsonx_model_id,
                api_client=self.client,
                project_id=settings.watsonx_project_id,
            )
            logger.info(f"Watsonx model initialized: {settings.watsonx_model_id}")

            self._initialized = True

        except Exception as e:
            logger.error(f"Failed to initialize WatsonxService: {e}")
            raise

    async def generate_text(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        top_p: float = 1.0,
        top_k: int = 50,
    ) -> str:
        """
        Generate text using watsonx.ai model.

        Args:
            prompt: Input prompt for text generation
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter

        Returns:
            Generated text response
        """
        if not self._initialized:
            await self.initialize()

        try:
            parameters = {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
            }

            response = self.model.generate_text(prompt=prompt, params=parameters)
            logger.info("Text generation successful")
            return response

        except Exception as e:
            logger.error(f"Text generation failed: {e}")
            raise

    async def analyze_emissions(self, emission_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze emission data using watsonx.ai.

        Args:
            emission_data: Dictionary containing emission information

        Returns:
            Analysis results with insights and recommendations
        """
        prompt = f"""
        Analyze the following carbon emission data and provide insights:
        
        Emission Data:
        {emission_data}
        
        Please provide:
        1. Key insights about the emission patterns
        2. Trend analysis (increasing/decreasing/stable)
        3. Specific recommendations for reduction
        4. Priority areas for improvement
        
        Format your response as a structured analysis.
        """

        try:
            analysis = await self.generate_text(prompt, max_tokens=800, temperature=0.5)
            
            return {
                "analysis": analysis,
                "confidence_score": 0.85,  # Placeholder - implement actual scoring
                "timestamp": "2024-01-01T00:00:00Z",  # Use actual timestamp
            }

        except Exception as e:
            logger.error(f"Emission analysis failed: {e}")
            raise

    async def generate_recommendations(
        self,
        context: Dict[str, Any],
        num_recommendations: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Generate optimization recommendations using watsonx.ai.

        Args:
            context: Context information for recommendations
            num_recommendations: Number of recommendations to generate

        Returns:
            List of recommendation dictionaries
        """
        prompt = f"""
        Based on the following context, generate {num_recommendations} specific 
        recommendations for reducing carbon emissions:
        
        Context:
        {context}
        
        For each recommendation, provide:
        1. Title
        2. Detailed description
        3. Estimated CO2 reduction potential (in kg)
        4. Implementation difficulty (low/medium/high)
        5. Priority level (high/medium/low)
        
        Format as a numbered list.
        """

        try:
            response = await self.generate_text(prompt, max_tokens=1000, temperature=0.6)
            
            # Parse response into structured recommendations
            # This is a placeholder - implement actual parsing logic
            recommendations = [
                {
                    "id": f"rec_{i}",
                    "title": f"Recommendation {i}",
                    "description": response,
                    "potential_reduction": 100.0,
                    "priority": "high",
                }
                for i in range(num_recommendations)
            ]
            
            return recommendations

        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            raise

    async def chat(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Chat with watsonx.ai model.

        Args:
            message: User message
            conversation_history: Previous conversation messages

        Returns:
            Model response
        """
        # Build conversation context
        context = ""
        if conversation_history:
            for msg in conversation_history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                context += f"{role}: {content}\n"

        prompt = f"{context}user: {message}\nassistant:"

        try:
            response = await self.generate_text(prompt, max_tokens=500, temperature=0.7)
            return response

        except Exception as e:
            logger.error(f"Chat failed: {e}")
            raise

    async def calculate_route_emissions(self, vendor_data: Dict[str, Any]) -> str:
        """
        Calculate route emissions and provide vendor recommendations using watsonx.ai.
        
        This function uses the IBM Granite 3 8B Instruct model to evaluate vendors and
        calculate mock Scope 3 carbon footprint scores, with strong prioritization for
        Hydrogen and Electric fleets.

        Args:
            vendor_data: Dictionary containing vendor information including fleet types,
                        routes, and other relevant data

        Returns:
            Model's text response with vendor evaluation and carbon footprint analysis
        """
        if not self._initialized:
            await self.initialize()

        try:
            # Format vendor data as JSON string for the prompt
            vendor_json = json.dumps(vendor_data, indent=2)
            
            # Create prompt that emphasizes hydrogen and electric fleet prioritization
            prompt = f"""
You are an expert carbon emissions analyst for logistics and supply chain operations.

Analyze the following vendor data and provide a comprehensive evaluation:

Vendor Data:
{vendor_json}

Your task:
1. Evaluate each vendor based on their fleet type, routes, and operational characteristics
2. Calculate a mock Scope 3 carbon footprint score for each vendor (in kg CO2e)
3. STRONGLY PRIORITIZE vendors using 'Hydrogen' or 'Electric' fleets as the recommended choice
4. Provide specific recommendations for emission reduction
5. Rank vendors from best to worst in terms of environmental impact

Important considerations:
- Hydrogen and Electric fleets should be heavily favored due to zero direct emissions
- Consider route efficiency, distance, and weather conditions
- Provide quantitative carbon footprint estimates
- Explain the reasoning behind your recommendations

Format your response with:
- Vendor rankings with carbon scores
- Detailed analysis for each vendor
- Clear recommendation of the best vendor choice
- Specific emission reduction strategies
"""

            # Create a specific model instance for llama-3-3-70b-instruct
            # This uses a supported model from the available watsonx models
            granite_model = ModelInference(
                model_id="meta-llama/llama-3-3-70b-instruct",
                api_client=self.client,
                project_id=settings.watsonx_project_id,
            )
            
            # Use asyncio.to_thread to wrap synchronous IBM SDK call
            # This follows the pattern mentioned in AGENTS.md for async compatibility
            parameters = {
                "max_new_tokens": 1000,
                "temperature": 0.5,  # Lower temperature for more consistent analysis
                "top_p": 0.95,
                "top_k": 50,
            }
            
            # Wrap synchronous generate_text call in asyncio.to_thread
            response = await asyncio.to_thread(
                granite_model.generate_text,
                prompt=prompt,
                params=parameters
            )
            
            logger.info("Route emissions calculation successful using ibm/granite-3-8b-instruct")
            return response

        except Exception as e:
            logger.error(f"Route emissions calculation failed: {e}", exc_info=True)
            raise

    async def close(self) -> None:
        """Close watsonx service and cleanup resources."""
        if self.client:
            # Cleanup if needed
            logger.info("Watsonx service closed")
            self._initialized = False


# Global service instance
watsonx_service = WatsonxService()

# Made with Bob
