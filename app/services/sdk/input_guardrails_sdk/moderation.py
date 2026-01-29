"""Example: Basic async guardrail bundle using Agents SDK with GuardrailAgent."""

import asyncio
from contextlib import suppress
import json 
from agents import (
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    Runner,
    SQLiteSession,
)
from agents.run import RunConfig

from guardrails import GuardrailAgent

# Define your pipeline configuration
PIPELINE_CONFIG = json.load(open("config/moderation.json"))
  


async def input_guardrails_moderation_sdk(prompt: str) -> None:
    """Output guardrails sdk contains pii."""
    # Create a session for the agent to store the conversation history
    session = SQLiteSession("guardrails-session")

    # Create agent with guardrails automatically configured from pipeline configuration
    AGENT = GuardrailAgent(
        config=PIPELINE_CONFIG,
        name="Customer support agent",
        instructions="You are a customer support agent. You help customers with their questions.",
    )

    with suppress(KeyboardInterrupt, asyncio.CancelledError):
        while True:
            try:
                user_input = prompt
                result = await Runner.run(
                    AGENT,
                    user_input,
                    run_config=RunConfig(tracing_disabled=True),
                    session=session,
                )
                return result.final_output
            except EOFError:
                return None
            except InputGuardrailTripwireTriggered as exc:
                return exc.guardrail_result.output.output_info
            except OutputGuardrailTripwireTriggered as exc:
                return exc.guardrail_result.output.output_info
            except Exception as e:
                return str(e)
