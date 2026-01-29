from fastapi import APIRouter
from pydantic import BaseModel

from services.sdk.input_guardrails_sdk import jailbreak as jailbreak_input_sdk
from services.sdk.input_guardrails_sdk import moderation as moderation_input_sdk
from services.sdk.input_guardrails_sdk import off_topic as off_topic_input_sdk
from services.sdk.input_guardrails_sdk import mask_pii as mask_pii_input_sdk
from services.sdk.input_guardrails_sdk import custom_prompt as custom_prompt_input_sdk


router = APIRouter(prefix="/input", tags=["Input SDK Guardrails"])

class InputGuardrailsSdkRequest(BaseModel):
    prompt: str

# Input guardrails sdk
@router.post("/jailbreak")
async def input_jailbreak_sdk(request: InputGuardrailsSdkRequest):
    response = await jailbreak_input_sdk.input_guardrails_sdk_jailbreak(request.prompt)
    return {"response": response}

@router.post("/moderation")
async def input_moderation_sdk(request: InputGuardrailsSdkRequest):
    response = await moderation_input_sdk.input_guardrails_moderation_sdk(request.prompt)
    return {"response": response}


@router.post("/off-topic")
async def input_off_topic_sdk(request: InputGuardrailsSdkRequest):
    response = await off_topic_input_sdk.input_guardrails_off_topic_sdk(request.prompt)
    return {"response": response}

@router.post("/mask-pii")
async def input_mask_pii_sdk(request: InputGuardrailsSdkRequest):
    response = await mask_pii_input_sdk.input_guardrails_mask_pii_sdk(request.prompt)
    return {"response": response}


@router.post("/custom-prompt")
async def input_custom_prompt_sdk(request: InputGuardrailsSdkRequest):
    response = await custom_prompt_input_sdk.input_guardrails_custom_prompt_sdk(request.prompt)
    return {"response": response}