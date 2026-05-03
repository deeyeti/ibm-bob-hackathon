"""
API routes for conversational AI chat using watsonx.ai.
"""

import json
from typing import Optional
from fastapi import APIRouter, HTTPException, status

from src.models.schemas import ChatRequest, ChatResponse
from src.services import watsonx_service
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with watsonx.ai as a Sustainable Logistics Expert.
    
    This endpoint uses IBM watsonx.ai (Granite model) to provide expert
    guidance on sustainable logistics, routing decisions, and carbon
    reduction strategies. When shift_order_context is provided, the AI
    can explain specific routing decisions based on emissions, weather,
    and fleet capabilities.
    
    Args:
        request: Chat request containing user message and optional context
        
    Returns:
        ChatResponse with AI-generated answer and timestamp
        
    Raises:
        HTTPException: If chat generation fails
    """
    try:
        logger.info(f"Processing chat request: {request.message[:50]}...")
        
        # Build system prompt for Sustainable Logistics Expert
        system_prompt = """You are a Sustainable Logistics Expert specializing in 
carbon emission reduction, route optimization, and fleet management. Your role is to:

1. Explain routing decisions based on emissions, weather conditions, and fleet 
   capabilities
2. Provide insights on how to reduce carbon footprint in supply chain operations
3. Reference specific data from shift orders when available
4. Be concise but informative in your responses
5. Focus on sustainability and carbon reduction strategies
6. Prioritize hydrogen and electric fleets due to their zero direct emissions

When analyzing shift orders or routing decisions, consider:
- Fleet type emissions (Hydrogen and Electric are zero-emission)
- Route efficiency and distance
- Weather conditions affecting operations
- Scope 3 carbon footprint calculations
- Vendor selection based on environmental impact

Always provide actionable recommendations and explain the reasoning behind 
your suggestions."""

        # Build context section if shift_order_context is provided
        context_section = ""
        if request.shift_order_context:
            try:
                context_json = json.dumps(request.shift_order_context, indent=2)
                context_section = f"""

Current Shift Order Context:
{context_json}

Please reference this data when explaining routing decisions and provide 
specific insights based on the fleet types, routes, and conditions shown."""
            except Exception as e:
                logger.warning(f"Failed to serialize shift_order_context: {e}")
                context_section = "\n\nNote: Shift order context provided but could not be parsed."
        
        # Construct the full prompt
        full_prompt = f"""{system_prompt}{context_section}

User Question: {request.message}

Expert Response:"""
        
        # Generate response using watsonx.ai
        # Use moderate temperature for balanced creativity and consistency
        response_text = await watsonx_service.generate_text(
            prompt=full_prompt,
            max_tokens=800,
            temperature=0.6,
            top_p=0.9,
            top_k=50,
        )
        
        logger.info("Chat response generated successfully")
        
        return ChatResponse(response=response_text.strip())
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat request failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate chat response: {str(e)}",
        )

# Made with Bob