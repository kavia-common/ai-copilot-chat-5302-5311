# AI Copilot Backend

FastAPI backend service for the AI Copilot application. Provides REST API endpoints for chat interactions powered by Google's Gemini AI.

## Features

- **Chat API**: Session-based chat with Gemini AI
- **Health Monitoring**: Health check endpoints
- **Session Management**: Create and delete chat sessions
- **CORS Support**: Configured for frontend integration
- **OpenAPI Documentation**: Auto-generated API documentation

## Prerequisites

- Python 3.8+
- Google Gemini API key (obtain from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables (see Environment Variables section below)

## Running Locally

### Development Server

```bash
# From the ai_copilot_backend directory
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 3001
```

The API will be available at:
- API: http://localhost:3001
- Interactive docs: http://localhost:3001/docs
- OpenAPI spec: http://localhost:3001/openapi.json

### Production Server

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --workers 4
```

## Environment Variables

Create a `.env` file in the `ai_copilot_backend` directory with the following variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GOOGLE_GEMINI_API_KEY` | Google Gemini API key for authentication | Yes | None |
| `GEMINI_MODEL` | Gemini model to use | No | `gemini-1.5-flash` |
| `CORS_ALLOW_ORIGINS` | Comma-separated list of allowed CORS origins | No | `http://localhost:3000` |

### Example .env file

```env
GOOGLE_GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash
CORS_ALLOW_ORIGINS=http://localhost:3000,http://localhost:3001
```

See `.env.example` for a template.

## API Endpoints

### Health Check
- **GET** `/api/health` - Returns service health status
- **GET** `/` - Root health check endpoint

### Chat
- **POST** `/api/chat` - Send a chat message and receive AI response
  - Request body: `{ sessionId: string, messages: ChatMessage[] }`
  - Response: `{ sessionId: string, message: ChatMessage, usage?: object, model?: string }`

### Session Management
- **DELETE** `/api/session/{session_id}` - Delete a chat session

## API Documentation

When the server is running, visit:
- Swagger UI: http://localhost:3001/docs
- ReDoc: http://localhost:3001/redoc
- OpenAPI JSON: http://localhost:3001/openapi.json

## Project Structure

```
ai_copilot_backend/
├── src/
│   └── api/
│       ├── __init__.py
│       ├── main.py           # FastAPI application and endpoints
│       ├── gemini_client.py  # Gemini API client
│       └── generate_openapi.py  # OpenAPI spec generator
├── interfaces/
│   └── openapi.json         # Generated OpenAPI specification
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in git)
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Error Handling

The API provides clear error messages:
- **400 Bad Request**: Invalid request parameters
- **404 Not Found**: Session not found
- **500 Internal Server Error**: Gemini API errors or server issues

If the Gemini API key is not configured, the API will return a helpful error message with instructions on how to obtain one.

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Linting
flake8 src/

# Type checking (if using mypy)
mypy src/
```

### Generating OpenAPI Spec

```bash
python -m src.api.generate_openapi
```

## Support

For issues or questions, please refer to the main project documentation.
