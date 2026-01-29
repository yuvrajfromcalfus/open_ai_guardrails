from fastapi import APIRouter
from pydantic import BaseModel

from services.basic.output_guardrails_basic import nsfw as output_guardrails_basic_nsfw
from services.basic.output_guardrails_basic import hallucination as output_guardrails_basic_hallucination
from services.basic.output_guardrails_basic import url_filter as output_guardrails_basic_url_filter
from services.basic.output_guardrails_basic import contains_pii as output_guardrails_basic_contains_pii
from services.basic.output_guardrails_basic import custom_check as output_guardrails_basic_custom_check


router = APIRouter(prefix="/output", tags=["Output Basic Guardrails"])

class OutputBasicGuardrailsRequest(BaseModel):
    prompt: str

# Output guardrails sdk
@router.post("/nsfw")
async def output_nsfw_sdk(request: OutputBasicGuardrailsRequest):
    response = await output_guardrails_basic_nsfw.output_guardrails_nsfw_basic(request.prompt)
    return {"response": response}

@router.post("/hallucination")
async def output_hallucination_sdk(request: OutputBasicGuardrailsRequest):
    response = await output_guardrails_basic_hallucination.output_guardrails_hallucination_basic(request.prompt)
    return {"response": response}


@router.post("/url-filter")
async def output_url_filter_sdk(request: OutputBasicGuardrailsRequest):
    response = await output_guardrails_basic_url_filter.output_guardrails_url_filter_basic(request.prompt)
    return {"response": response}

@router.post("/contains-pii")
async def output_contains_pii_sdk(request: OutputBasicGuardrailsRequest):
    response = await output_guardrails_basic_contains_pii.output_guardrails_contains_pii_basic(request.prompt)
    return {"response": response}


@router.post("/custom-check")
async def output_custom_check_sdk(request: OutputBasicGuardrailsRequest):
    response = await output_guardrails_basic_custom_check.output_guardrails_custom_check_basic(request.prompt)
    return {"response": response}