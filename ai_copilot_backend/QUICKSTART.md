# Quick Start Guide

## 🚀 Getting Started in 60 Seconds

### 1. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Gemini API key (optional for mock mode)
nano .env
```

### 2. Install & Run

```bash
# Using the start script (recommended)
./start.sh

# OR manually
source venv/bin/activate
pip install -e .
python -m uvicorn app.main:app --host 0.0.0.0 --port 3001 --reload
```

### 3. Test the API

```bash
# Health check
curl http://localhost:3001/healthz

# Create a session
curl -X POST http://localhost:3001/api/sessions

# Send a chat message
curl -X POST http://localhost:3001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"YOUR_SESSION_ID","message":"Hello!"}'
```

## 📚 Documentation

- **Interactive API Docs**: http://localhost:3001/docs
- **ReDoc**: http://localhost:3001/redoc
- **OpenAPI JSON**: http://localhost:3001/openapi.json

## 🔑 API Key Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to `.env`:
   ```
   GOOGLE_GEMINI_API_KEY=your_actual_key_here
   ```
4. Restart the server

## 🧪 Mock Mode

Without an API key, the backend runs in **mock mode**:
- Returns predefined responses
- Perfect for development/testing
- No API costs

## 📦 Key Files

- `app/main.py` - Application entry point
- `app/api/routes.py` - API endpoints
- `app/services/gemini_client.py` - Gemini API integration
- `app/services/session_store.py` - Session management
- `app/config.py` - Configuration settings

## 🔧 Configuration

Edit `.env` to customize:

```env
GOOGLE_GEMINI_API_KEY=your_key
MODEL_NAME=gemini-1.5-flash
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
PORT=3001
LOG_LEVEL=info
```

## 🐛 Troubleshooting

**Port already in use?**
```bash
# Change PORT in .env or use a different port
python -m uvicorn app.main:app --port 3002
```

**Dependencies missing?**
```bash
source venv/bin/activate
pip install --force-reinstall -e .
```

**Import errors?**
```bash
# Make sure you're in the virtual environment
source venv/bin/activate
```

## 📝 API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/healthz` | Health check |
| POST | `/api/sessions` | Create new session |
| GET | `/api/sessions/{id}` | Get session history |
| POST | `/api/sessions/{id}/reset` | Reset session |
| POST | `/api/chat` | Send chat message |

## 💡 Tips

- Use `--reload` flag during development for auto-restart
- Check logs for detailed debugging information
- Set `LOG_LEVEL=debug` for verbose logging
- Sessions are in-memory and cleared on restart
