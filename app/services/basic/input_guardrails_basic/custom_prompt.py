import json
from guardrails import GuardrailsAsyncOpenAI, GuardrailTripwireTriggered


PIPELINE_CONFIG = json.load(open("config/custom_prompt.json"))


guardrails_basic_custom_prompt_client = GuardrailsAsyncOpenAI(config=PIPELINE_CONFIG)

async def input_guardrails_custom_prompt_basic(
    user_input: str,
) -> str:
    """Process user input using the new GuardrailsAsyncOpenAI."""
    try:
        # Use the new GuardrailsAsyncOpenAI - it handles all guardrail validation automatically
        response = await guardrails_basic_custom_prompt_client.responses.create(
            input=user_input,
            model="gpt-4.1-mini",
        )
        return response.output_text

    except GuardrailTripwireTriggered:
        return "Custom Prompt Guardrail Triggered"


