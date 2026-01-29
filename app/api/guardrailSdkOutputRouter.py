from fastapi import APIRouter
from pydantic import BaseModel

from services.sdk.output_guardrails_sdk import nsfw as output_guardrails_sdk_nsfw
from services.sdk.output_guardrails_sdk import hallucination as output_guardrails_sdk_hallucination
from services.sdk.output_guardrails_sdk import url_filter as output_guardrails_sdk_url_filter
from services.sdk.output_guardrails_sdk import contains_pii as output_guardrails_sdk_contains_pii
from services.sdk.output_guardrails_sdk import custom_check as output_guardrails_sdk_custom_check


router = APIRouter(prefix="/output", tags=["Output SDK Guardrails"])

class OutputGuardrailsSdkRequest(BaseModel):
    prompt: str

# Output guardrails sdk
@router.post("/nsfw")
async def output_nsfw_sdk(request: OutputGuardrailsSdkRequest):
    response = await output_guardrails_sdk_nsfw.output_guardrails_sdk_nsfw(request.prompt)
    return {"response": response}

@router.post("/hallucination")
async def output_hallucination_sdk(request: OutputGuardrailsSdkRequest):
    response = await output_guardrails_sdk_hallucination.output_guardrails_sdk_hallucination(request.prompt)
    return {"response": response}


@router.post("/url-filter")
async def output_url_filter_sdk(request: OutputGuardrailsSdkRequest):
    response = await output_guardrails_sdk_url_filter.output_guardrails_sdk_url_filter(request.prompt)
    return {"response": response}

@router.post("/contains-pii")
async def output_contains_pii_sdk(request: OutputGuardrailsSdkRequest):
    response = await output_guardrails_sdk_contains_pii.output_guardrails_sdk_contains_pii(request.prompt)
    return {"response": response}


@router.post("/custom-check")
async def output_custom_check_sdk(request: OutputGuardrailsSdkRequest):
    response = await output_guardrails_sdk_custom_check.output_guardrails_sdk_custom_check(request.prompt)
    return {"response": response}