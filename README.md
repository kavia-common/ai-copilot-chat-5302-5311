# AI Copilot Chat - Backend Container

This directory contains the **backend container** for the AI Copilot Chat application.

## Quick Start

1. Navigate to the backend directory:
```bash
cd ai_copilot_backend
```

2. Follow the setup instructions in [ai_copilot_backend/README.md](ai_copilot_backend/README.md)

## Container Details

- **Framework**: FastAPI (Python)
- **Port**: 3001
- **API Documentation**: http://localhost:3001/docs
- **OpenAPI Spec**: Available at `/openapi.json` or in `interfaces/openapi.json`

## Key Features

- Gemini AI integration for intelligent chat responses
- Session-based conversation management
- RESTful API with auto-generated documentation
- CORS support for frontend integration
- Comprehensive error handling

## Environment Setup

The backend requires a `.env` file with the following variables:

- `GEMINI_API_KEY` - Your Google Gemini API key (required)
- `PORT` - Server port (default: 3001)
- `CORS_ORIGINS` - Allowed frontend origins (comma-separated)

See the [backend README](ai_copilot_backend/README.md) for detailed setup instructions.

## Related Containers

- **Frontend**: [../ai-copilot-chat-5302-5312](../ai-copilot-chat-5302-5312) - React-based chat interface

## API Endpoints

- `GET /` - Health check
- `POST /api/chat` - Send chat message
- `POST /api/chat/stream` - Stream chat (placeholder, not implemented)
- `GET /api/sessions/{session_id}` - Get session history

For complete API documentation, see the [backend README](ai_copilot_backend/README.md) or visit the Swagger UI when the server is running.
