import json 
from guardrails import GuardrailsAsyncOpenAI, GuardrailTripwireTriggered

PIPELINE_CONFIG = json.load(open("config/url_filter.json"))


guardrails_client = GuardrailsAsyncOpenAI(config=PIPELINE_CONFIG)

async def output_guardrails_url_filter_basic(
    user_input: str,
) -> str:
    """Process user input using the new GuardrailsAsyncOpenAI."""
    try:
        # Use the new GuardrailsAsyncOpenAI - it handles all guardrail validation automatically
        response = await guardrails_client.responses.create(
            input=user_input,
            model="gpt-4.1-mini",
        )
        return response.output_text

    except GuardrailTripwireTriggered:
        return "URL Filter Guardrail Triggered"


