# Guardrails Demo Guide

## Overview
This guide explains how to use the guardrails demo system with the ability to enable/disable guardrails and visualize results.

## Features

### 1. **Guardrail Toggle**
- Enable/disable guardrails with the `guardrail_enabled` parameter
- Compare responses with and without guardrail protection
- See exactly which guardrails triggered or passed

### 2. **HTML Visualization Interface**
- Beautiful, modern web interface
- Real-time guardrail status visualization
- Side-by-side comparison view
- Detailed guardrail breakdown by stage

## API Endpoint

### POST `/api/v1/guardrail/combined/ask`

**Request Body:**
```json
{
  "prompt": "How can CashPlant Bank help me?",
  "detailed": true,
  "guardrail_enabled": true
}
```

**Parameters:**
- `prompt` (required): The user's query
- `detailed` (optional, default: `true`): Return detailed guardrail information
- `guardrail_enabled` (optional, default: `true`): Enable/disable guardrails

**Response (with guardrails enabled):**
```json
{
  "success": true,
  "response": "AI-generated response...",
  "guardrail_enabled": true,
  "guardrail_results": {
    "preflight": [
      {"name": "Contains PII", "triggered": false, ...},
      {"name": "Moderation", "triggered": false, ...}
    ],
    "input": [
      {"name": "Jailbreak", "triggered": false, ...},
      {"name": "Off Topic Prompts", "triggered": false, ...}
    ],
    "output": [
      {"name": "Custom Prompt Check", "triggered": false, ...},
      {"name": "URL Filter", "triggered": false, ...},
      {"name": "Contains PII", "triggered": false, ...},
      {"name": "Hallucination Detection", "triggered": false, ...},
      {"name": "NSFW Text", "triggered": false, ...}
    ],
    "triggered_guardrails": [],
    "passed_guardrails": [...]
  },
  "summary": {
    "total_preflight": 2,
    "total_input": 2,
    "total_output": 5,
    "triggered_count": 0,
    "passed_count": 9,
    "all_passed": true
  },
  "message": "All guardrails passed successfully."
}
```

**Response (with guardrails disabled):**
```json
{
  "success": true,
  "response": "AI-generated response...",
  "guardrail_enabled": false,
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
    "all_passed": true
  },
  "message": "Guardrails disabled - response generated without guardrail protection."
}
```

## Web Interface

### Accessing the Demo Page

1. **Start the server:**
   ```bash
   cd app
   python main.py
   ```

2. **Open your browser:**
   Navigate to: `http://localhost:8006/`

### Using the Interface

1. **Enter a prompt** in the text area
2. **Toggle guardrails** using the switch (enabled/disabled)
3. **Click "Send Request"** to process
4. **View results:**
   - Guardrail status (passed/triggered)
   - Summary statistics
   - Detailed breakdown by stage (Preflight, Input, Output)
   - Comparison view (when guardrails are enabled, shows both with/without)

### Interface Features

- **Real-time Status**: See which guardrails passed or triggered
- **Visual Indicators**: Color-coded status badges (green for passed, red for triggered)
- **Stage Breakdown**: Guardrails organized by Preflight, Input, and Output stages
- **Comparison View**: Side-by-side comparison of responses with and without guardrails
- **Summary Stats**: Quick overview of guardrail performance

## Example Use Cases

### 1. Testing Valid Banking Query
```json
{
  "prompt": "What services does CashPlant Bank offer?",
  "guardrail_enabled": true
}
```
**Expected**: All guardrails pass, response generated

### 2. Testing Off-Topic Query
```json
{
  "prompt": "Tell me about the weather",
  "guardrail_enabled": true
}
```
**Expected**: Off-Topic guardrail triggers, request blocked

### 3. Testing Without Guardrails
```json
{
  "prompt": "Tell me about the weather",
  "guardrail_enabled": false
}
```
**Expected**: Response generated without guardrail protection

### 4. Comparing Responses
1. Send request with `guardrail_enabled: true`
2. Interface automatically fetches comparison with `guardrail_enabled: false`
3. View side-by-side comparison

## Guardrail Stages

### Preflight Guardrails
- **Contains PII**: Detects sensitive information before processing
- **Moderation**: Filters harmful content

### Input Guardrails
- **Jailbreak**: Detects manipulation attempts
- **Off Topic Prompts**: Ensures queries are banking-related

### Output Guardrails
- **Custom Prompt Check**: Validates responses stay in banking domain
- **URL Filter**: Only allows secure HTTPS URLs
- **Contains PII**: Blocks responses containing sensitive data
- **Hallucination Detection**: Prevents false information
- **NSFW Text**: Filters inappropriate content

## Testing with cURL

```bash
# With guardrails enabled
curl -X POST "http://localhost:8006/api/v1/guardrail/combined/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "How can CashPlant Bank help me?",
    "detailed": true,
    "guardrail_enabled": true
  }'

# With guardrails disabled
curl -X POST "http://localhost:8006/api/v1/guardrail/combined/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "How can CashPlant Bank help me?",
    "detailed": true,
    "guardrail_enabled": false
  }'
```

## Presentation Tips

1. **Start with guardrails enabled** to show protection
2. **Show a valid banking query** - all guardrails pass
3. **Show an off-topic query** - guardrail triggers
4. **Toggle guardrails off** - show comparison
5. **Use the comparison view** to highlight differences

## Files Structure

```
app/
├── main.py                          # FastAPI app with routes
├── static/
│   └── guardrails_demo.html         # HTML visualization interface
├── api/
│   └── guardrailRouter.py          # API endpoint definitions
└── services/
    └── basic/
        └── input_guardrails_basic/
            └── combined_guardrail.py  # Core guardrail logic
```

## Troubleshooting

### HTML page not loading
- Check that `app/static/guardrails_demo.html` exists
- Verify FastAPI is running on port 8006
- Check browser console for errors

### API errors
- Ensure OpenAI API key is configured
- Check that all dependencies are installed
- Verify config file path is correct

### Guardrails not showing
- Ensure `detailed: true` in request
- Check that `guardrail_enabled: true` is set
- Verify guardrail config file is valid
