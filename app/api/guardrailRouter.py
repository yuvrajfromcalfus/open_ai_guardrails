from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from services.basic.input_guardrails_basic.combined_guardrail import input_guardrails_combined_guardrail_basic



router = APIRouter(prefix="/combined", tags=["Combined Guardrails"])

class InputBasicGuardrailsRequest(BaseModel):
    prompt: str
    detailed: Optional[bool] = True  # Default to True for presentation purposes
    guardrail_enabled: Optional[bool] = True  # Enable/disable guardrails


@router.post("/ask")
async def input_combined_guardrail(request: InputBasicGuardrailsRequest):
    """
    Combined Guardrails Endpoint - CashPlant Bank Expert Agent
    
    This endpoint demonstrates how all guardrails work together to protect
    the CashPlant Bank specialized banking assistant.
    
    Guardrails Applied:
    - Preflight: PII Detection, Content Moderation
    - Input: Jailbreak Detection, Off-Topic Filtering
    - Output: Custom Prompt Check, URL Filtering, PII Detection, 
              Hallucination Detection, NSFW Filtering
    
    Returns detailed information about which guardrails passed/failed
    and the final response from the banking expert agent.
    """
    result = await input_guardrails_combined_guardrail_basic(
        request.prompt, 
        return_details=request.detailed,
        guardrail_enabled=request.guardrail_enabled
    )
    
    if request.detailed:
        return result
    else:
        return {"response": result}