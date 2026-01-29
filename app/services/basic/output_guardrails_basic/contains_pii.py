import json
from guardrails import GuardrailsAsyncOpenAI, GuardrailTripwireTriggered

PIPELINE_CONFIG = json.load(open("config/contains_pii.json"))
  

guardrails_client = GuardrailsAsyncOpenAI(config=PIPELINE_CONFIG)

async def output_guardrails_contains_pii_basic(
    user_input: str,
) -> str:
    """Process user input using the new GuardrailsAsyncOpenAI."""
    try:
        response = await guardrails_client.responses.create(
            input=user_input,
            model="gpt-4.1-mini",
        )
        return response.output_text

    except GuardrailTripwireTriggered:
        return "Contains PII Guardrail Triggered"
