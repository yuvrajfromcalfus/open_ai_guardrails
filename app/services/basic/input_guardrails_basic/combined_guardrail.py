import json
import os
from guardrails import GuardrailsAsyncOpenAI, GuardrailTripwireTriggered
from openai import AsyncOpenAI
from typing import Dict, Any, List, Union

# Get the config file path relative to this file
_config_path = os.path.join(os.path.dirname(__file__), "../../../config/combined_config.json")
PIPELINE_CONFIG = json.load(open(_config_path))


guardrails_combined_guardrail_client = GuardrailsAsyncOpenAI(config=PIPELINE_CONFIG)
# Regular OpenAI client for when guardrails are disabled
regular_openai_client = AsyncOpenAI()

def _extract_guardrail_info(guardrail_results) -> Dict[str, Any]:
    """Extract detailed guardrail information from results."""
    guardrail_info = {
        "preflight": [],
        "input": [],
        "output": [],
        "triggered_guardrails": [],
        "passed_guardrails": []
    }
    
    # Get guardrail names from config for better identification
    preflight_config = PIPELINE_CONFIG.get("pre_flight", {}) or PIPELINE_CONFIG.get("preflight", {})
    input_config = PIPELINE_CONFIG.get("input", {})
    output_config = PIPELINE_CONFIG.get("output", {})
    
    preflight_names = [g.get("name", "Unknown") for g in preflight_config.get("guardrails", [])]
    input_names = [g.get("name", "Unknown") for g in input_config.get("guardrails", [])]
    output_names = [g.get("name", "Unknown") for g in output_config.get("guardrails", [])]
    
    # Process preflight guardrails
    preflight_results = []
    if guardrail_results and hasattr(guardrail_results, 'preflight') and guardrail_results.preflight:
        preflight_results = guardrail_results.preflight
    
    for idx, name in enumerate(preflight_names):
        if idx < len(preflight_results):
            result = preflight_results[idx]
            triggered = getattr(result, 'tripwire_triggered', False)
            info_dict = getattr(result, 'info', {}) if hasattr(result, 'info') else {}
            guardrail_name = info_dict.get('guardrail_name') or name
            info = {
                "name": guardrail_name,
                "triggered": triggered,
                "execution_failed": getattr(result, 'execution_failed', False),
                "details": info_dict
            }
        else:
            # No result available, assume passed
            info = {
                "name": name,
                "triggered": False,
                "execution_failed": False,
                "details": {"status": "passed"}
            }
        
        guardrail_info["preflight"].append(info)
        if info["triggered"]:
            guardrail_info["triggered_guardrails"].append(f"Preflight: {info['name']}")
        else:
            guardrail_info["passed_guardrails"].append(f"Preflight: {info['name']}")
    
    # Process input guardrails
    input_results = []
    if guardrail_results and hasattr(guardrail_results, 'input') and guardrail_results.input:
        input_results = guardrail_results.input
    
    for idx, name in enumerate(input_names):
        if idx < len(input_results):
            result = input_results[idx]
            triggered = getattr(result, 'tripwire_triggered', False)
            info_dict = getattr(result, 'info', {}) if hasattr(result, 'info') else {}
            guardrail_name = info_dict.get('guardrail_name') or name
            info = {
                "name": guardrail_name,
                "triggered": triggered,
                "execution_failed": getattr(result, 'execution_failed', False),
                "details": info_dict
            }
        else:
            # No result available, assume passed
            info = {
                "name": name,
                "triggered": False,
                "execution_failed": False,
                "details": {"status": "passed"}
            }
        
        guardrail_info["input"].append(info)
        if info["triggered"]:
            guardrail_info["triggered_guardrails"].append(f"Input: {info['name']}")
        else:
            guardrail_info["passed_guardrails"].append(f"Input: {info['name']}")
    
    # Process output guardrails
    output_results = []
    if guardrail_results and hasattr(guardrail_results, 'output') and guardrail_results.output:
        output_results = guardrail_results.output
    
    for idx, name in enumerate(output_names):
        if idx < len(output_results):
            result = output_results[idx]
            triggered = getattr(result, 'tripwire_triggered', False)
            info_dict = getattr(result, 'info', {}) if hasattr(result, 'info') else {}
            guardrail_name = info_dict.get('guardrail_name') or name
            info = {
                "name": guardrail_name,
                "triggered": triggered,
                "execution_failed": getattr(result, 'execution_failed', False),
                "details": info_dict
            }
        else:
            # No result available, assume passed
            info = {
                "name": name,
                "triggered": False,
                "execution_failed": False,
                "details": {"status": "passed"}
            }
        
        guardrail_info["output"].append(info)
        if info["triggered"]:
            guardrail_info["triggered_guardrails"].append(f"Output: {info['name']}")
        else:
            guardrail_info["passed_guardrails"].append(f"Output: {info['name']}")
    
    return guardrail_info

async def input_guardrails_combined_guardrail_basic(
    user_input: str,
    return_details: bool = False,
    guardrail_enabled: bool = True,
) -> Union[Dict[str, Any], str]:
    """
    Process user input using the combined guardrails with CashPlant Bank expert agent.
    
    Args:
        user_input: The user's query
        return_details: If True, returns detailed guardrail information for presentation
        guardrail_enabled: If True, uses guardrails. If False, uses regular OpenAI without guardrails.
    
    Returns:
        If return_details=True: Dict with response, guardrail details, and status
        If return_details=False: String response (backward compatible)
    """
    # If guardrails are disabled, use regular OpenAI with detailed system prompt
    if not guardrail_enabled:
        try:
            # Comprehensive system prompt for CashPlant Bank agent
            system_prompt = """You are CashPlant Bank's expert banking assistant. CashPlant Bank is a leading financial institution providing comprehensive banking and financial services.

YOUR ROLE:
- You are a specialized banking assistant for CashPlant Bank ONLY
- Provide accurate, helpful information about CashPlant Bank's products, services, and policies
- Assist customers with banking-related inquiries and transactions
- Maintain professionalism and security awareness at all times

CASHPLANT BANK SERVICES YOU CAN DISCUSS:
1. **Account Services**:
   - Checking accounts (various tiers with different features)
   - Savings accounts (high-yield options available)
   - Money market accounts
   - Certificate of Deposit (CD) accounts
   - Account opening procedures and requirements

2. **Digital Banking**:
   - Online banking platform features
   - Mobile banking app capabilities
   - Bill pay services
   - Mobile check deposit
   - Account alerts and notifications
   - Security features and two-factor authentication

3. **Loan Products**:
   - Personal loans
   - Home mortgages and refinancing
   - Auto loans
   - Business loans
   - Credit lines
   - Loan application process and requirements

4. **Credit Cards**:
   - CashPlant Bank credit card options
   - Rewards programs
   - Balance transfer options
   - Credit card application process

5. **Investment Services**:
   - Investment accounts
   - Retirement planning (IRAs, 401(k) rollovers)
   - Financial advisory services
   - Investment products available through CashPlant Bank

6. **Banking Operations**:
   - Branch locations and hours
   - ATM network access
   - Wire transfers
   - ACH transfers
   - Check processing
   - Account fees and charges
   - Interest rates on various products

7. **Customer Support**:
   - How to contact customer service
   - Dispute resolution processes
   - Account security best practices
   - Fraud prevention tips

WHAT YOU CAN DO:
✓ Answer questions about CashPlant Bank's products and services
✓ Provide general banking information and best practices
✓ Explain banking terms and concepts
✓ Guide customers on how to use CashPlant Bank's services
✓ Discuss general financial planning topics related to banking
✓ Help with account-related inquiries (without accessing actual account data)

WHAT YOU CANNOT DO:
✗ Answer questions about other banks or financial institutions
✗ Provide information about non-banking topics (weather, sports, entertainment, etc.)
✗ Access or modify actual customer account information
✗ Provide specific account numbers, balances, or transaction details
✗ Give investment advice beyond general information
✗ Discuss topics unrelated to banking or CashPlant Bank

IMPORTANT GUIDELINES:
- Always stay focused on CashPlant Bank and banking topics
- If asked about other banks, politely redirect: "I'm CashPlant Bank's assistant. I can help you with CashPlant Bank services or general banking questions."
- If asked about non-banking topics, politely decline: "I specialize in banking and financial services. How can I help you with CashPlant Bank today?"
- Be helpful, accurate, and professional
- Protect customer privacy and security
- When unsure about specific details, direct customers to contact CashPlant Bank directly

Remember: You are CashPlant Bank's specialized assistant. Your expertise is in banking and CashPlant Bank's services only."""

            # Use chat completions API directly
            response = await regular_openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                temperature=0.3,
            )
            
            response_text = response.choices[0].message.content if response.choices else "No response generated"
            
            if return_details:
                return {
                    "success": True,
                    "response": response_text,
                    "guardrail_enabled": False,
                    "guardrail_results": {
                        "preflight": [],
                        "input": [],
                        "output": [],
                        "triggered_guardrails": [],
                        "passed_guardrails": []
                    },
                    "summary": {
                        "total_preflight": 0,
                        "total_input": 0,
                        "total_output": 0,
                        "triggered_count": 0,
                        "passed_count": 0,
                        "all_passed": True
                    },
                    "message": "Guardrails disabled - response generated without guardrail protection. Note: Without guardrails, there's no automatic validation to ensure responses stay on-topic, don't contain sensitive information, or comply with security policies."
                }
            else:
                return response_text
        except Exception as e:
            if return_details:
                return {
                    "success": False,
                    "response": None,
                    "error": str(e),
                    "guardrail_enabled": False,
                    "message": f"Error generating response: {str(e)}"
                }
            else:
                return f"Error: {str(e)}"
    
    # Guardrails enabled - use guardrail client
    try:
        # Use suppress_tripwire=True when return_details=True to get all guardrail results
        # even if one triggers, so we can show which guardrails passed/failed
        suppress_tripwire = return_details
        
        # Use the new GuardrailsAsyncOpenAI - it handles all guardrail validation automatically
        response = await guardrails_combined_guardrail_client.responses.create(
            input=user_input,
            model="gpt-4o",
            temperature=0.3,
            suppress_tripwire=suppress_tripwire,
        )
        
        if return_details:
            # Extract detailed guardrail information
            guardrail_info = _extract_guardrail_info(response.guardrail_results)
            
            # Check if any guardrails triggered
            has_triggered = len(guardrail_info["triggered_guardrails"]) > 0
            
            # Get response text (may be None if guardrail blocked early)
            response_text = getattr(response, 'output_text', None) if hasattr(response, 'output_text') else None
            
            return {
                "success": not has_triggered,  # Success only if no guardrails triggered
                "response": response_text,
                "guardrail_enabled": True,
                "guardrail_results": guardrail_info,
                "summary": {
                    "total_preflight": len(guardrail_info["preflight"]),
                    "total_input": len(guardrail_info["input"]),
                    "total_output": len(guardrail_info["output"]),
                    "triggered_count": len(guardrail_info["triggered_guardrails"]),
                    "passed_count": len(guardrail_info["passed_guardrails"]),
                    "all_passed": len(guardrail_info["triggered_guardrails"]) == 0
                },
                "agent_type": "CashPlant Bank Expert Assistant",
                "capabilities": [
                    "Account inquiries and balance checks",
                    "Transaction history and fund transfers",
                    "Loan applications and credit card services",
                    "Investment products and banking policies",
                    "Interest rates, fees, and account management",
                    "Online banking support"
                ],
                "restrictions": [
                    "Only banking and financial services topics",
                    "No general knowledge or other industries",
                    "No entertainment or non-banking technology",
                    "Protected by PII detection, moderation, jailbreak prevention",
                    "Off-topic filtering, hallucination detection, NSFW filtering"
                ],
                "message": (
                    f"{len(guardrail_info['triggered_guardrails'])} guardrail(s) triggered. "
                    if has_triggered else "All guardrails passed successfully."
                )
            }
        else:
            return response.output_text
            
    except GuardrailTripwireTriggered as e:
        if return_details:
            # Extract information about which guardrail triggered
            triggered_guardrail_info = {
                "name": "Unknown",
                "stage": "Unknown",
                "details": {}
            }
            
            if hasattr(e, 'guardrail_result') and e.guardrail_result:
                result = e.guardrail_result
                info_dict = getattr(result, 'info', {}) if hasattr(result, 'info') else {}
                triggered_guardrail_info["name"] = info_dict.get('guardrail_name', 'Unknown Guardrail')
                triggered_guardrail_info["stage"] = info_dict.get('stage_name', 'Unknown Stage')
                triggered_guardrail_info["details"] = info_dict
                triggered_guardrail_info["execution_failed"] = getattr(result, 'execution_failed', False)
            
            # Try to determine which stage based on guardrail name
            guardrail_name = triggered_guardrail_info["name"]
            stage_prefix = ""
            if any(name.lower() in guardrail_name.lower() for name in ["Contains PII", "Moderation"]):
                stage_prefix = "Preflight"
            elif any(name.lower() in guardrail_name.lower() for name in ["Jailbreak", "Off Topic", "Off-Topic"]):
                stage_prefix = "Input"
            elif any(name.lower() in guardrail_name.lower() for name in ["Custom Prompt", "URL Filter", "Hallucination", "NSFW"]):
                stage_prefix = "Output"
            
            triggered_message = f"{stage_prefix}: {guardrail_name}" if stage_prefix else guardrail_name
            
            return {
                "success": False,
                "response": None,
                "error": "Guardrail Tripwire Triggered",
                "message": f"Guardrail '{guardrail_name}' detected a violation. The request was blocked to protect CashPlant Bank's security and compliance standards.",
                "triggered_guardrail": triggered_guardrail_info,
                "guardrail_results": {
                    "preflight": [],
                    "input": [],
                    "output": [],
                    "triggered_guardrails": [triggered_message],
                    "passed_guardrails": []
                },
                "summary": {
                    "total_preflight": 0,
                    "total_input": 0,
                    "total_output": 0,
                    "triggered_count": 1,
                    "passed_count": 0,
                    "all_passed": False
                }
            }
        else:
            return "Guardrail Triggered"
