from services.basic.input_guardrails_basic.combined_guardrail import input_guardrails_combined_guardrail_basic
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from api.guardrailSdkInputRouter import router as guardrail_sdk_input_router
from api.guardrailSdkOutputRouter import router as guardrail_sdk_output_router
from api.guardrailBasicInputRouter import router as guardrail_basic_input_router
from api.guardrailBasicOutputRouter import router as guardrail_basic_output_router
from api.guardrailRouter import router as guardrail_router


app = FastAPI()

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the guardrails demo HTML page."""
    html_path = os.path.join(os.path.dirname(__file__), "static", "guardrails_demo.html")
    if os.path.exists(html_path):
        with open(html_path, "r") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Guardrails Demo</h1><p>HTML file not found. Please check the static directory.</p>")

app.include_router(guardrail_sdk_input_router, prefix="/api/v1/guardrail/sdk")
app.include_router(guardrail_sdk_output_router, prefix="/api/v1/guardrail/sdk")

app.include_router(guardrail_basic_input_router, prefix="/api/v1/guardrail/basic")
app.include_router(guardrail_basic_output_router, prefix="/api/v1/guardrail/basic")

app.include_router(guardrail_router, prefix="/api/v1/guardrail")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8006, reload=True)
