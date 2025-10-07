# AI Copilot Backend

FastAPI-based backend service for the AI Copilot Chat application. This service integrates with Google's Gemini API to provide intelligent chat responses with support for coding assistance, writing, summarizing, and brainstorming.

## Features

- 🤖 **Gemini AI Integration**: Powered by Google's Gemini Pro model
- 💬 **Session Management**: Maintains conversation context across multiple messages
- 📝 **RESTful API**: Clean, well-documented REST endpoints
- 🔒 **CORS Support**: Configurable cross-origin resource sharing
- 📊 **OpenAPI Documentation**: Auto-generated API docs with Swagger UI
- ⚡ **Fast & Async**: Built on FastAPI for high performance

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key (get one at https://makersuite.google.com/app/apikey)
- pip (Python package manager)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes all necessary packages:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `google-generativeai` - Gemini API client
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation

### 2. Configure Environment Variables

Create a `.env` file in the `ai_copilot_backend` directory (or copy from `.env.example`):

```env
# REQUIRED: Your Google Gemini API Key
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Server Port (default: 3001)
PORT=3001

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
```

**Important Environment Variables:**

- **GEMINI_API_KEY** (REQUIRED): Your Google Gemini API key. The application will not start without this.
- **PORT** (optional): The port on which the server runs. Default is 3001.
- **CORS_ORIGINS** (optional): Comma-separated list of allowed origins for CORS. Default is `http://localhost:3000`.

### 3. Run the Application

#### Development Mode (with auto-reload)

```bash
cd ai_copilot_backend
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 3001
```

#### Production Mode

```bash
cd ai_copilot_backend
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --workers 4
```

The server will start at `http://localhost:3001`

### 4. Verify Installation

Once running, visit:
- **API Docs (Swagger UI)**: http://localhost:3001/docs
- **Alternative Docs (ReDoc)**: http://localhost:3001/redoc
- **OpenAPI Spec**: http://localhost:3001/openapi.json
- **Health Check**: http://localhost:3001/

## API Endpoints

### Health Check

**GET /** - Check API health status

```bash
curl http://localhost:3001/
```

Response:
```json
{
  "message": "Healthy",
  "service": "AI Copilot Chat API",
  "version": "1.0.0"
}
```

### Chat Endpoint

**POST /api/chat** - Send a chat message to the AI assistant

Request body:
```json
{
  "session_id": "session-123",
  "message": {
    "role": "user",
    "content": "Write a Python function to sort a list"
  }
}
```

Response:
```json
{
  "session_id": "session-123",
  "message": {
    "role": "assistant",
    "content": "Here's a Python function to sort a list...",
    "timestamp": "2024-01-01T12:00:01"
  },
  "usage": null
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad request (missing API key or invalid input)
- `502`: Bad gateway (Gemini API error)

### Stream Endpoint (Placeholder)

**POST /api/chat/stream** - Stream chat responses (Not Yet Implemented)

Currently returns `501 Not Implemented`. This endpoint is reserved for future streaming functionality using Server-Sent Events (SSE).

### Session History

**GET /api/sessions/{session_id}** - Retrieve conversation history for a session

```bash
curl http://localhost:3001/api/sessions/session-123
```

Response:
```json
{
  "session_id": "session-123",
  "messages": [
    {
      "role": "user",
      "content": "Hello!",
      "timestamp": "2024-01-01T12:00:00"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help you?",
      "timestamp": "2024-01-01T12:00:01"
    }
  ]
}
```

**Status Codes:**
- `200`: Success
- `404`: Session not found

## API Documentation

The API automatically generates OpenAPI 3.1 documentation. Access it via:

1. **Swagger UI** (Interactive): http://localhost:3001/docs
2. **ReDoc** (Alternative): http://localhost:3001/redoc
3. **OpenAPI JSON**: http://localhost:3001/openapi.json

The OpenAPI spec includes:
- Detailed endpoint descriptions
- Request/response schemas
- Example payloads
- Error responses
- Tags for endpoint grouping (health, chat, sessions)

## Project Structure

```
ai_copilot_backend/
├── src/
│   ├── api/
│   │   ├── main.py              # FastAPI application & routes
│   │   └── generate_openapi.py  # OpenAPI spec generator
│   ├── models/
│   │   └── schemas.py           # Pydantic models
│   └── services/
│       └── gemini_service.py    # Gemini API integration
├── interfaces/
│   └── openapi.json             # Generated OpenAPI specification
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
└── README.md                    # This file
```

## Session Management

Sessions are stored in-memory and persist only for the lifetime of the server process. Each session:
- Has a unique `session_id` (UUID)
- Maintains full conversation history
- Provides context to the AI for better responses

**Note**: Sessions are not persisted to disk or database. Restarting the server will clear all sessions.

## Error Handling

The API provides clear error messages:

- **400 Bad Request**: Missing or invalid GEMINI_API_KEY
- **404 Not Found**: Session doesn't exist
- **500 Internal Server Error**: Unexpected server error
- **501 Not Implemented**: Feature not yet available (streaming)
- **502 Bad Gateway**: Error communicating with Gemini API

## CORS Configuration

CORS is configured via the `CORS_ORIGINS` environment variable. The middleware allows:
- Credentials: Yes
- Methods: All (`*`)
- Headers: All (`*`)

Example configuration for multiple origins:
```env
CORS_ORIGINS=http://localhost:3000,https://app.example.com,https://preview.example.com
```

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

### Regenerating OpenAPI Spec

The OpenAPI specification is auto-generated by FastAPI. To manually export it:

```bash
python src/api/generate_openapi.py
```

This creates/updates `interfaces/openapi.json`.

## Troubleshooting

### Issue: "GEMINI_API_KEY environment variable is not configured"

**Solution**: Ensure your `.env` file exists and contains a valid Gemini API key:
```env
GEMINI_API_KEY=your_actual_key_here
```

### Issue: CORS errors from frontend

**Solution**: Add your frontend URL to CORS_ORIGINS:
```env
CORS_ORIGINS=http://localhost:3000,https://your-frontend-url.com
```

### Issue: Port already in use

**Solution**: Change the port in `.env` or kill the process using port 3001:
```bash
# Linux/Mac
lsof -ti:3001 | xargs kill -9

# Or use a different port
PORT=3002
```

## Environment-Specific Configuration

### Local Development
```env
GEMINI_API_KEY=your_key
PORT=3001
CORS_ORIGINS=http://localhost:3000
```

### Production
```env
GEMINI_API_KEY=your_production_key
PORT=3001
CORS_ORIGINS=https://your-production-domain.com
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini API](https://ai.google.dev/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## License

This project is part of the AI Copilot Chat application.
