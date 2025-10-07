# AI Copilot Backend

A FastAPI-based backend service that powers the AI Copilot chat application using Google's Gemini API. This service handles natural language processing, conversation management, and provides RESTful API endpoints for frontend communication.

## Project Overview

The AI Copilot Backend is a lightweight, high-performance API service built with FastAPI that integrates with Google's Gemini AI model to provide intelligent chat capabilities. It supports session-based conversations, maintains conversation history, and delivers structured responses for various tasks including writing, coding assistance, brainstorming, and summarization.

## Architecture

### Technology Stack

- **Framework**: FastAPI 0.115.12
- **AI Integration**: Google Generative AI (Gemini API)
- **Python Version**: 3.8+
- **Key Libraries**:
  - `google-generativeai`: Gemini API client
  - `uvicorn`: ASGI server
  - `pydantic`: Data validation and settings
  - `python-dotenv`: Environment variable management

### Architecture Overview

```
┌─────────────────┐
│   Frontend      │
│   (React)       │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  FastAPI        │
│  Application    │
│  - CORS         │
│  - Routing      │
│  - Validation   │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐ ┌──────────────┐
│ Session │ │ Gemini       │
│ Storage │ │ Service      │
│ (Memory)│ │ (API Client) │
└─────────┘ └──────┬───────┘
                   │
                   ▼
            ┌─────────────┐
            │  Gemini API │
            │  (Google)   │
            └─────────────┘
```

### Components

- **API Layer** (`src/api/main.py`): FastAPI application with route definitions and middleware
- **Service Layer** (`src/services/gemini_service.py`): Gemini API integration and conversation handling
- **Models** (`src/models/schemas.py`): Pydantic models for request/response validation
- **In-Memory Storage**: Session-based conversation history storage

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- A Google Cloud account with Gemini API access

## Environment Variables

### Required Configuration

Create a `.env` file in the `ai_copilot_backend` directory with the following variables:

```bash
# Google Gemini API Key (REQUIRED)
GEMINI_API_KEY=your_gemini_api_key_here
```

### Environment Variable Details

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `GEMINI_API_KEY` | Yes | Your Google Gemini API key for authentication | None |

### How to Obtain a Gemini API Key

1. **Visit Google AI Studio**:
   - Navigate to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account

2. **Create an API Key**:
   - Click on "Get API Key" or "Create API Key"
   - Select or create a Google Cloud project
   - Copy the generated API key

3. **Set Up Your Environment**:
   - Create a `.env` file in the `ai_copilot_backend` directory
   - Add your API key: `GEMINI_API_KEY=your_api_key_here`
   - Never commit the `.env` file to version control

4. **Verify Access**:
   - Ensure your API key has access to the Gemini API
   - Check your Google Cloud project's API quotas and limits

### Example .env File

Create a file named `.env` in the `ai_copilot_backend` directory:

```bash
# AI Copilot Backend Environment Variables

# Google Gemini API Configuration
GEMINI_API_KEY=AIzaSyExample_Key_Replace_With_Your_Own_Key
```

### Example .env.example File

For version control, include a `.env.example` file (without sensitive data):

```bash
# AI Copilot Backend Environment Variables Template

# Google Gemini API Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here
```

## Installation and Setup

### Step 1: Clone the Repository

```bash
cd ai-copilot-chat-5302-5311
```

### Step 2: Navigate to Backend Directory

```bash
cd ai_copilot_backend
```

### Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### Step 6: Verify Installation

```bash
# Check if all dependencies are installed
pip list

# Verify Python version
python --version
```

## Running the Application

### Development Mode

Start the development server with hot-reload enabled:

```bash
# From the ai_copilot_backend directory
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 3001
```

The API will be available at: `http://localhost:3001`

### Production Mode

For production deployment:

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --workers 4
```

### Using Different Ports

To run on a different port:

```bash
uvicorn src.api.main:app --reload --port 8000
```

### Background Process

To run as a background service:

```bash
nohup uvicorn src.api.main:app --host 0.0.0.0 --port 3001 > server.log 2>&1 &
```

## API Documentation

### Base URL

```
http://localhost:3001
```

### Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:3001/docs
- **ReDoc**: http://localhost:3001/redoc
- **OpenAPI Schema**: Available at `interfaces/openapi.json`

### Endpoints

#### 1. Health Check

**Endpoint**: `GET /`

**Description**: Verify the API is running and check Gemini API configuration status.

**Response**:
```json
{
  "message": "Healthy",
  "status": "ok",
  "gemini_api_configured": true
}
```

**Example**:
```bash
curl http://localhost:3001/
```

#### 2. Send Chat Message

**Endpoint**: `POST /api/chat`

**Description**: Send a user message to the AI Copilot and receive a response. The service automatically manages conversation history per session.

**Request Body**:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Explain quicksort algorithm",
  "history": null
}
```

**Request Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | string | Yes | Unique identifier for the conversation session (UUID format) |
| `message` | string | Yes | The user's message to send to the AI |
| `history` | array | No | Optional list of previous messages for context |

**Response**:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "reply": "Quicksort is a highly efficient sorting algorithm...",
  "usage": null
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | string | The session identifier for this conversation |
| `reply` | string | The AI's response message |
| `usage` | object/null | Optional metadata about token usage |

**Example**:
```bash
curl -X POST http://localhost:3001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "What is Python?"
  }'
```

**Error Responses**:

- `503 Service Unavailable`: Gemini API is not configured
  ```json
  {
    "detail": "Gemini API is not configured. Please set GEMINI_API_KEY environment variable."
  }
  ```

- `500 Internal Server Error`: Error generating response
  ```json
  {
    "detail": "Error generating response: [error details]"
  }
  ```

#### 3. Get Session History

**Endpoint**: `GET /api/sessions/{session_id}`

**Description**: Retrieve the complete conversation history for a specific session.

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `session_id` | string | The unique identifier for the session |

**Response**:
```json
[
  {
    "role": "user",
    "content": "Hello, how are you?",
    "ts": "2024-01-15T10:30:00.000Z"
  },
  {
    "role": "assistant",
    "content": "Hello! I'm doing well, thank you for asking...",
    "ts": "2024-01-15T10:30:05.000Z"
  }
]
```

**Example**:
```bash
curl http://localhost:3001/api/sessions/550e8400-e29b-41d4-a716-446655440000
```

**Error Response**:

- `404 Not Found`: Session doesn't exist
  ```json
  {
    "detail": "Session '550e8400-e29b-41d4-a716-446655440000' not found"
  }
  ```

#### 4. Delete Session

**Endpoint**: `DELETE /api/sessions/{session_id}`

**Description**: Delete a session and its conversation history from memory.

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `session_id` | string | The unique identifier for the session to delete |

**Response**:
```json
{
  "message": "Session '550e8400-e29b-41d4-a716-446655440000' deleted successfully",
  "status": "ok"
}
```

**Example**:
```bash
curl -X DELETE http://localhost:3001/api/sessions/550e8400-e29b-41d4-a716-446655440000
```

**Error Response**:

- `404 Not Found`: Session doesn't exist
  ```json
  {
    "detail": "Session '550e8400-e29b-41d4-a716-446655440000' not found"
  }
  ```

### CORS Configuration

The API is configured to accept requests from:
- `http://localhost:3000` (default frontend URL)
- All origins (`*`) for development

For production, update CORS settings in `src/api/main.py` to restrict origins.

## Testing

### Running Tests

```bash
# Install test dependencies (if not already installed)
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py
```

### Manual API Testing

Using curl:

```bash
# Health check
curl http://localhost:3001/

# Send a chat message
curl -X POST http://localhost:3001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session-123",
    "message": "Tell me a joke"
  }'

# Get session history
curl http://localhost:3001/api/sessions/test-session-123

# Delete session
curl -X DELETE http://localhost:3001/api/sessions/test-session-123
```

Using Python:

```python
import requests

# Health check
response = requests.get("http://localhost:3001/")
print(response.json())

# Send chat message
payload = {
    "session_id": "test-session-456",
    "message": "What is machine learning?"
}
response = requests.post("http://localhost:3001/api/chat", json=payload)
print(response.json())
```

## Project Structure

```
ai_copilot_backend/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application and routes
│   │   └── generate_openapi.py  # OpenAPI schema generator
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic models
│   └── services/
│       ├── __init__.py
│       └── gemini_service.py    # Gemini API integration
├── interfaces/
│   └── openapi.json             # OpenAPI specification
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
├── .env.example                 # Environment template
└── README.md                    # This file
```

## Development Guidelines

### Code Style

This project follows PEP 8 style guidelines. Key points:

- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable and function names
- Add docstrings to all public functions and classes

### Adding New Endpoints

1. Define route in `src/api/main.py`
2. Create Pydantic models in `src/models/schemas.py`
3. Implement business logic in appropriate service
4. Add tests for the new endpoint
5. Update OpenAPI documentation

### Regenerating OpenAPI Schema

```bash
python -m src.api.generate_openapi
```

This updates `interfaces/openapi.json` with the latest API schema.

## Troubleshooting

### Common Issues

#### 1. API Key Not Configured

**Error**: `Gemini API is not configured. Please set GEMINI_API_KEY environment variable.`

**Solution**:
- Verify `.env` file exists in `ai_copilot_backend` directory
- Check `GEMINI_API_KEY` is set correctly
- Restart the server after updating `.env`
- Verify the API key is valid and has proper permissions

#### 2. Module Not Found Errors

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Port Already in Use

**Error**: `OSError: [Errno 48] Address already in use`

**Solution**:
```bash
# Find process using port 3001
lsof -i :3001

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn src.api.main:app --reload --port 8000
```

#### 4. CORS Errors

**Error**: Frontend can't connect due to CORS policy

**Solution**:
- Check CORS configuration in `src/api/main.py`
- Ensure frontend URL is in `allow_origins` list
- For development, `"*"` allows all origins

#### 5. Gemini API Errors

**Error**: `Error generating response from Gemini API`

**Solutions**:
- Verify API key is correct and active
- Check internet connectivity
- Review API quota limits in Google Cloud Console
- Ensure Gemini API is enabled in your project
- Check for service outages: https://status.cloud.google.com/

#### 6. Import Errors

**Error**: `ImportError: cannot import name 'app' from 'src.api.main'`

**Solution**:
```bash
# Run from the ai_copilot_backend directory
cd ai-copilot-chat-5302-5311/ai_copilot_backend

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run uvicorn
uvicorn src.api.main:app --reload
```

#### 7. Virtual Environment Issues

**Problem**: Packages not found even after installation

**Solution**:
```bash
# Deactivate current environment
deactivate

# Remove old environment
rm -rf venv

# Create fresh environment
python -m venv venv
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Debugging Tips

1. **Enable Debug Logging**:
   ```python
   # Add to src/api/main.py
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check Server Logs**:
   - Watch console output for errors
   - Check stack traces for detailed error information

3. **Test Gemini API Directly**:
   ```python
   import google.generativeai as genai
   genai.configure(api_key="your_key")
   model = genai.GenerativeModel('gemini-pro')
   response = model.generate_content("Hello")
   print(response.text)
   ```

4. **Use Interactive API Docs**:
   - Navigate to http://localhost:3001/docs
   - Test endpoints directly from the browser
   - View request/response schemas

### Getting Help

- Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
- Review [Google Gemini API docs](https://ai.google.dev/docs)
- Check project issues and discussions
- Ensure all dependencies are up to date: `pip install --upgrade -r requirements.txt`

## Performance Considerations

### Session Storage

The current implementation uses in-memory storage for sessions. Consider these points:

- **Limitation**: Data is lost when the server restarts
- **Scalability**: Not suitable for multi-instance deployments
- **Production**: Consider using Redis or a database for persistent storage

### Rate Limiting

Implement rate limiting to prevent API abuse:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

### Monitoring

For production deployments, consider adding:

- Logging with structured output (JSON logs)
- Performance monitoring (response times, error rates)
- Health check endpoints with detailed status
- Metrics collection (Prometheus, Grafana)

## Security Considerations

1. **API Key Protection**:
   - Never commit `.env` files to version control
   - Use environment variables in production
   - Rotate API keys regularly

2. **Input Validation**:
   - All inputs are validated using Pydantic models
   - Additional sanitization for user prompts recommended

3. **CORS Configuration**:
   - Restrict `allow_origins` in production
   - Don't use `"*"` in production environments

4. **Rate Limiting**:
   - Implement rate limiting to prevent abuse
   - Set appropriate quotas per session/user

5. **Error Handling**:
   - Don't expose sensitive information in error messages
   - Log errors securely

## Deployment

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "3001"]
```

Build and run:

```bash
docker build -t ai-copilot-backend .
docker run -p 3001:3001 --env-file .env ai-copilot-backend
```

### Cloud Deployment

The application is ready for deployment on:

- Google Cloud Run
- AWS Lambda (with Mangum adapter)
- Heroku
- Railway
- Render

Ensure environment variables are configured in your deployment platform.

## Contributing

When contributing to this project:

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass
5. Update OpenAPI schema if needed

## License

[Specify your license here]

## Support

For issues, questions, or contributions, please refer to the project repository or contact the development team.
