## 📋 Overview

This project showcases a complete guardrail system protecting **CashPlant Bank's Expert Banking Assistant**. It demonstrates how multiple layers of guardrails work together to ensure security, compliance, and proper functionality of AI-powered banking services.

### ✨ Key Features

- 🛡️ **Multi-Layer Protection**: Preflight, Input, and Output guardrails
- 🔄 **Toggle Guardrails**: Compare responses with and without guardrail protection
- 📊 **Visual Dashboard**: Beautiful web interface with real-time guardrail status
- 🔍 **Detailed Analytics**: See exactly which guardrails passed or triggered
- 🏦 **Banking-Specific**: Specialized for CashPlant Bank services only

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- OpenAI API Key
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone "https://github.com/yuvrajfromcalfus/open_ai_guardrails.git"
   cd open_ai_guardrails
   ```

2. **Create virtual environment**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   export OPENAI_API_KEY="your_open_ai_key"
   ```

5. **Navigate to app directory**
   ```bash
   cd app
   ```

6. **Start the server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8006 --reload
   ```

---

## 🌐 Access the Application

### Web Interface (Visual Demo)
Open your browser and navigate to:
```
http://localhost:8006
```

The web interface provides:
- 📝 Interactive prompt input
- 🔀 Guardrail toggle (enable/disable)
- 📊 Real-time guardrail status visualization
- 📈 Summary statistics
- 🔄 Side-by-side comparison view

### API Documentation
Access the interactive API documentation:
```
http://localhost:8006/docs
```

Test all endpoints directly from the Swagger UI interface.

---

## 🛡️ Guardrail Categories

### Preflight Guardrails
- **Contains PII**: Detects sensitive information before processing
- **Moderation**: Filters harmful content

### Input Guardrails
- **Jailbreak Detection**: Prevents manipulation attempts
- **Off-Topic Filtering**: Ensures queries are banking-related only

### Output Guardrails
- **Custom Prompt Check**: Validates responses stay in banking domain
- **URL Filter**: Only allows secure HTTPS URLs
- **Contains PII**: Blocks responses containing sensitive data
- **Hallucination Detection**: Prevents false information
- **NSFW Text**: Filters inappropriate content

---

## 📡 API Endpoints

### Main Endpoint: Combined Guardrails

**POST** `/api/v1/guardrail/combined/ask`

**Request Body:**
```json
{
  "prompt": "How can CashPlant Bank help me?",
  "detailed": true,
  "guardrail_enabled": true
}
```

**Response:**
```json
{
  "success": true,
  "response": "AI-generated response...",
  "guardrail_enabled": true,
  "guardrail_results": {
    "preflight": [...],
    "input": [...],
    "output": [...],
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
  }
}
```

### Individual Guardrail Endpoints

- **Input Guardrails**: `/api/v1/guardrail/basic/input/*`
- **Output Guardrails**: `/api/v1/guardrail/basic/output/*`

See `/docs` for complete API documentation.

---

## 🎯 Use Cases

### 1. Valid Banking Query
```json
{
  "prompt": "What services does CashPlant Bank offer?",
  "guardrail_enabled": true
}
```
✅ **Result**: All guardrails pass, response generated

### 2. Off-Topic Query
```json
{
  "prompt": "Tell me about the weather",
  "guardrail_enabled": true
}
```
❌ **Result**: Off-Topic guardrail triggers, request blocked

### 3. Comparison Mode
Enable guardrails to automatically see side-by-side comparison with unprotected responses.

---

## 📚 Documentation

- **[Guardrails Demo Guide](./GUARDRAILS_DEMO_GUIDE.md)**: Complete guide to using the demo
- **API Documentation**: Available at `/docs` when server is running

---

## 🔧 Configuration

Guardrail configurations are stored in:
```
app/config/combined_config.json
```

Modify this file to customize guardrail behavior and thresholds.

---

## 🎨 Features for Presentation

- **Visual Guardrail Status**: Color-coded indicators (green = passed, red = triggered)
- **Stage Breakdown**: Guardrails organized by Preflight, Input, and Output
- **Summary Statistics**: Quick overview of guardrail performance
- **Comparison View**: Side-by-side comparison of protected vs unprotected responses
- **Real-Time Updates**: See results as they process

---

## 🛠️ Troubleshooting

### Server won't start
- Ensure you're in the `app` directory
- Check that Python 3.12+ is installed
- Verify virtual environment is activated

### API errors
- Ensure OpenAI API key is set correctly
- Check that all dependencies are installed
- Verify config file path is correct

### HTML page not loading
- Ensure server is running on port 8006
- Check browser console for errors
- Verify `app/static/guardrails_demo.html` exists

---

## 📝 Project Structure

```
guard_rails/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── static/
│   │   └── guardrails_demo.html  # Web interface
│   ├── api/                    # API routers
│   ├── services/               # Guardrail services
│   └── config/                 # Guardrail configurations
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

See [LICENSE](./LICENSE) file for details.

---

## 💡 Tips for Demo

1. **Start with guardrails enabled** to show protection
2. **Test valid banking queries** - all guardrails pass
3. **Test off-topic queries** - guardrails trigger
4. **Toggle guardrails off** - show comparison
5. **Use the comparison view** to highlight differences

---

**Made with ❤️ for demonstrating AI safety and guardrails**