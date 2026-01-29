from fastapi import APIRouter
from pydantic import BaseModel

from services.basic.input_guardrails_basic import jailbreak as jailbreak_input_sdk
from services.basic.input_guardrails_basic import moderation as moderation_input_sdk
from services.basic.input_guardrails_basic import off_topic as off_topic_input_sdk
from services.basic.input_guardrails_basic import mask_pii as mask_pii_input_sdk
from services.basic.input_guardrails_basic import custom_prompt as custom_prompt_input_sdk


router = APIRouter(prefix="/input", tags=["Input Basic Guardrails"])

class InputBasicGuardrailsRequest(BaseModel):
    prompt: str

# Input guardrails sdk
@router.post("/jailbreak")
async def input_jailbreak_sdk(request: InputBasicGuardrailsRequest):
    response = await jailbreak_input_sdk.input_guardrails_jailbreak_basic(request.prompt)
    return {"response": response}

@router.post("/moderation")
async def input_moderation_sdk(request: InputBasicGuardrailsRequest):
    response = await moderation_input_sdk.input_guardrails_moderation_basic(request.prompt)
    return {"response": response}


@router.post("/off-topic")
async def input_off_topic_sdk(request: InputBasicGuardrailsRequest):
    response = await off_topic_input_sdk.input_guardrails_off_topic_basic(request.prompt)
    return {"response": response}

@router.post("/mask-pii")
async def input_pii_detector_sdk(request: InputBasicGuardrailsRequest):
    response = await mask_pii_input_sdk.input_guardrails_mask_pii_basic(request.prompt)
    return {"response": response}


@router.post("/custom-prompt")
async def input_custom_prompt_sdk(request: InputBasicGuardrailsRequest):
    response = await custom_prompt_input_sdk.input_guardrails_custom_prompt_basic(request.prompt)
    return {"response": response} 