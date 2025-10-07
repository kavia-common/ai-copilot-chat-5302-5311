# AI Copilot Backend

FastAPI backend service for the AI Copilot chat application, powered by Google's Gemini API.

## Features

- 🚀 **FastAPI** - Modern, fast web framework
- 🤖 **Gemini Integration** - Google's latest AI model
- 💬 **Session Management** - Conversation history tracking
- 📝 **Markdown Support** - Rich text formatting in responses
- 🔒 **CORS Enabled** - Secure cross-origin requests
- 📊 **Logging** - Comprehensive request/response logging
- 🧪 **Mock Mode** - Test without API key

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Google Gemini API key (optional for mock mode)

## Quick Start

### 1. Get Your Gemini API Key

Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to create a free API key.

### 2. Environment Setup

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
GOOGLE_GEMINI_API_KEY=your_actual_api_key_here
MODEL_NAME=gemini-1.5-flash
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
LOG_LEVEL=info
PORT=3001
HOST=0.0.0.0
```

### 3. Install Dependencies

```bash
# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 4. Run the Server

Using the start script (recommended):
```bash
chmod +x start.sh
./start.sh
```

Or directly with uvicorn:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 3001 --reload
```

The server will start on `http://localhost:3001`

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:3001/docs
- **ReDoc**: http://localhost:3001/redoc
- **OpenAPI JSON**: http://localhost:3001/openapi.json

## API Endpoints

### Health Check

```http
GET /healthz
```

Returns server health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "ai-copilot-backend",
  "version": "1.0.0"
}
```

### Create Session

```http
POST /api/sessions
```

Creates a new chat session.

**Response:**
```json
{
  "session_id": "abc123-def456-ghi789",
  "message": "Session created successfully",
  "created_at": "2024-01-01T12:00:00Z"
}
```

### Get Session History

```http
GET /api/sessions/{session_id}
```

Retrieves conversation history for a session.

**Response:**
```json
{
  "session_id": "abc123-def456-ghi789",
  "messages": [
    {
      "role": "user",
      "content": "Hello!",
      "timestamp": "2024-01-01T12:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help you today?",
      "timestamp": "2024-01-01T12:00:01Z"
    }
  ],
  "created_at": "2024-01-01T12:00:00Z"
}
```

### Reset Session

```http
POST /api/sessions/{session_id}/reset
```

Clears all messages from a session.

**Response:**
```json
{
  "session_id": "abc123-def456-ghi789",
  "message": "Session reset successfully",
  "status": "success"
}
```

### Send Chat Message

```http
POST /api/chat
```

Sends a message and receives an AI response.

**Request:**
```json
{
  "session_id": "abc123-def456-ghi789",
  "message": "Explain Python decorators"
}
```

**Response:**
```json
{
  "response": "# Python Decorators\n\nDecorators are a powerful feature...",
  "session_id": "abc123-def456-ghi789"
}
```

## Configuration

All configuration is managed through environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_GEMINI_API_KEY` | - | Your Gemini API key (required for AI features) |
| `MODEL_NAME` | `gemini-1.5-flash` | Gemini model to use |
| `ALLOWED_ORIGINS` | `http://localhost:3000,http://localhost:3001` | CORS allowed origins |
| `PORT` | `3001` | Server port |
| `HOST` | `0.0.0.0` | Server host |
| `LOG_LEVEL` | `info` | Logging level (debug/info/warning/error) |

## Mock Mode

If no API key is configured, the backend runs in **mock mode** for testing:

- Returns predefined responses
- Useful for development without API costs
- Provides helpful setup instructions

To enable full AI functionality, configure your `GOOGLE_GEMINI_API_KEY`.

## Project Structure

```
ai_copilot_backend/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic data models
│   ├── middleware.py        # Custom middleware
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API route definitions
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_client.py # Gemini API integration
│   │   └── session_store.py # Session management
│   └── utils/
│       ├── __init__.py
│       └── formatting.py    # Text formatting utilities
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Environment template
├── pyproject.toml           # Project dependencies
├── start.sh                 # Startup script
└── README.md                # This file
```

## Development

### Running in Development Mode

```bash
uvicorn app.main:app --reload --port 3001
```

The `--reload` flag enables auto-reload on code changes.

### Logging

Logs are written to stdout with configurable levels:

```bash
# Set log level in .env
LOG_LEVEL=debug  # debug, info, warning, error, critical
```

### Testing API with curl

Create a session:
```bash
curl -X POST http://localhost:3001/api/sessions
```

Send a chat message:
```bash
curl -X POST http://localhost:3001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"your-session-id","message":"Hello!"}'
```

## Deployment

### Environment Variables

Ensure all required environment variables are set in your deployment environment:

- `GOOGLE_GEMINI_API_KEY` - **Required** for production
- `ALLOWED_ORIGINS` - Set to your frontend URL(s)
- `LOG_LEVEL` - Set to `warning` or `error` for production

### Production Server

For production, use a production-grade ASGI server:

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:3001
```

## Troubleshooting

### "Session not found" errors

Sessions are stored in memory and cleared on server restart. Ensure your frontend creates a new session after server restarts.

### CORS errors

Add your frontend URL to `ALLOWED_ORIGINS` in `.env`:

```env
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
```

### API key issues

- Verify your API key is correct
- Check for extra spaces or quotes in `.env`
- Ensure the key has proper permissions in Google AI Studio

### Import errors

Reinstall dependencies:

```bash
pip install --force-reinstall -e .
```

## Support

For issues or questions:

1. Check the API documentation at `/docs`
2. Review logs for error details
3. Verify environment configuration
4. Test with mock mode first

## License

Copyright © 2024. All rights reserved.
