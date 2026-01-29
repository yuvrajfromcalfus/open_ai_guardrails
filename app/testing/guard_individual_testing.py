import asyncio
import httpx
import json
from datetime import datetime


# Base URLs for input and output guardrails
INPUT_BASE_URL = "http://localhost:8003/api/v1/guardrail/basic/input"
OUTPUT_BASE_URL = "http://localhost:8003/api/v1/guardrail/basic/output"


# ------------------ TEST PROMPTS ------------------


TEST_INPUT_PROMPTS = json.load(open("prompts/off_topic_testing_prompts.json"))

TEST_OUTPUT_PROMPTS = {}
# ------------------ HTTP CALL UTIL ------------------


async def call_input_endpoint(client, category, prompt):
    url = f"{INPUT_BASE_URL}/{category}"
    try:
        response = await client.post(url, json={"prompt": prompt})
        try:
            return {"prompt": prompt, "response": response.json()}
        except Exception:
            return {"prompt": prompt, "response": {"error": response.text}}
    except httpx.ReadTimeout:
        return {"prompt": prompt, "response": {"error": "ReadTimeout - Request took too long"}}
    except httpx.ReadError:
        return {"prompt": prompt, "response": {"error": "ReadError - Connection error occurred"}}
    except Exception as e:
        return {"prompt": prompt, "response": {"error": str(e)}}


async def call_output_endpoint(client, category, prompt):
    url = f"{OUTPUT_BASE_URL}/{category}"
    try:
        response = await client.post(url, json={"prompt": prompt})
        try:
            return {"prompt": prompt, "response": response.json()}
        except Exception:
            return {"prompt": prompt, "response": {"error": response.text}}
    except httpx.ReadTimeout:
        return {"prompt": prompt, "response": {"error": "ReadTimeout - Request took too long"}}
    except httpx.ReadError:
        return {"prompt": prompt, "response": {"error": "ReadError - Connection error occurred"}}
    except Exception as e:
        return {"prompt": prompt, "response": {"error": str(e)}}


# ------------------ RUNNERS ------------------


async def run_tests_input():
    results = {"timestamp": datetime.utcnow().isoformat(), "results": {}}
    # Increased timeout to 300 seconds (5 minutes) to handle long-running requests
    async with httpx.AsyncClient(timeout=300.0) as client:
        for category, prompts in TEST_INPUT_PROMPTS.items():
            category_results = []
            print(f"Processing {category} with {len(prompts)} prompts...")
            for idx, prompt in enumerate(prompts, 1):
                print(f"  Processing prompt {idx}/{len(prompts)}...")
                result = await call_input_endpoint(client, category, prompt)
                category_results.append(result)
                # Add a small delay between requests to avoid overwhelming the server
                await asyncio.sleep(0.5)
            results["results"][category] = category_results
            with open(f"results/{category}_input_guardrails_results.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Saved {category} input guardrails results to {category}_input_guardrails_results.json")


async def run_tests_output():
    results = {"timestamp": datetime.utcnow().isoformat(), "results": {}}
    # Increased timeout to 300 seconds (5 minutes) to handle long-running requests
    async with httpx.AsyncClient(timeout=300.0) as client:
        for category, prompts in TEST_OUTPUT_PROMPTS.items():
            category_results = []
            print(f"Processing {category} with {len(prompts)} prompts...")
            for idx, prompt in enumerate(prompts, 1):
                print(f"  Processing prompt {idx}/{len(prompts)}...")
                result = await call_output_endpoint(client, category, prompt)
                category_results.append(result)
                # Add a small delay between requests to avoid overwhelming the server
                await asyncio.sleep(0.5)
            results["results"][category] = category_results
            with open(f"results/{category}_output_guardrails_results.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Saved {category} output guardrails results to {category}_output_guardrails_results.json")


# ------------------ ENTRY POINT ------------------


async def main():
    await run_tests_input()
    # await run_tests_output()
    print("\nCompleted. Results saved JSON files.\n")


if __name__ == "__main__":
    asyncio.run(main())
