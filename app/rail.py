from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("guardrails_config.json") as f:
    guardrail_config = json.load(f)

class AskRequest(BaseModel):
    prompt: str

@app.post("/ask")
async def ask(request: AskRequest):

    out = client.responses.create(
        model="gpt-4.1", 
        guardrails=[guardrail_config],
        input=request.prompt
    )

    return {"response": out.output_text}
