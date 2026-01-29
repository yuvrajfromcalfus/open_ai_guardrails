
import json
from guardrails import GuardrailsAsyncOpenAI, GuardrailTripwireTriggered

PIPELINE_CONFIG = json.load(open("config/jailbreak.json"))


guardrails_client = GuardrailsAsyncOpenAI(config=PIPELINE_CONFIG)

async def input_guardrails_jailbreak_basic(
    user_input: str,
) -> str:
    """Process user input using the new GuardrailsAsyncOpenAI."""
    try:
        print(f"User input: {user_input}")
        # Use the new GuardrailsAsyncOpenAI - it handles all guardrail validation automatically
        response = await guardrails_client.responses.create(
            input=user_input,
            model="gpt-4.1-mini",
        )
        return response.output_text

    except GuardrailTripwireTriggered:
        return "Jailbreak Guardrail Triggered"

