# Deployment Guide

## 📋 Prerequisites

- Python 3.9+
- Virtual environment (venv)
- Google Gemini API key
- Production server (Linux recommended)

## 🔐 Environment Setup

### 1. Configure Environment Variables

Create `.env` file with production settings:

```env
# REQUIRED
GOOGLE_GEMINI_API_KEY=your_production_api_key

# Server Configuration
HOST=0.0.0.0
PORT=3001

# CORS - Set to your frontend URLs
ALLOWED_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com

# Logging
LOG_LEVEL=warning

# Model
MODEL_NAME=gemini-1.5-flash
```

### 2. Security Checklist

- ✅ Set `LOG_LEVEL=warning` or `error` in production
- ✅ Configure `ALLOWED_ORIGINS` to specific domains (no wildcards)
- ✅ Use HTTPS in production
- ✅ Keep API keys in environment variables, never commit to git
- ✅ Use firewall rules to restrict access
- ✅ Regular security updates for dependencies

## 🚀 Deployment Options

### Option 1: Systemd Service (Linux)

Create `/etc/systemd/system/ai-copilot-backend.service`:

```ini
[Unit]
Description=AI Copilot Backend Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ai-copilot-backend
Environment="PATH=/opt/ai-copilot-backend/venv/bin"
ExecStart=/opt/ai-copilot-backend/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 3001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-copilot-backend
sudo systemctl start ai-copilot-backend
sudo systemctl status ai-copilot-backend
```

### Option 2: Gunicorn (Production ASGI Server)

Install Gunicorn:

```bash
pip install gunicorn
```

Run with multiple workers:

```bash
gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:3001 \
  --access-logfile /var/log/ai-copilot/access.log \
  --error-logfile /var/log/ai-copilot/error.log \
  --log-level warning
```

### Option 3: Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/
COPY pyproject.toml .

# Expose port
EXPOSE 3001

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3001"]
```

Build and run:

```bash
docker build -t ai-copilot-backend .
docker run -d -p 3001:3001 --env-file .env ai-copilot-backend
```

### Option 4: Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "3001:3001"
    env_file:
      - .env
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3001/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run:

```bash
docker-compose up -d
```

## 🔧 Nginx Reverse Proxy

Configure Nginx to proxy requests:

```nginx
server {
    listen 80;
    server_name api.your-domain.com;

    location / {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers (if not handled by FastAPI)
        add_header Access-Control-Allow-Origin https://your-frontend.com always;
    }
}
```

## 📊 Monitoring

### Health Check

Monitor the health endpoint:

```bash
curl http://localhost:3001/healthz
```

Expected response:
```json
{
  "status": "healthy",
  "service": "ai-copilot-backend",
  "version": "1.0.0"
}
```

### Logs

Check application logs:

```bash
# Systemd
sudo journalctl -u ai-copilot-backend -f

# Docker
docker logs -f <container_id>

# Direct
tail -f /var/log/ai-copilot/error.log
```

### Performance Monitoring

Monitor key metrics:
- Response times (check `X-Process-Time` header)
- Error rates
- API key quota usage
- Memory and CPU usage

## 🔄 Updates & Maintenance

### Update Application

```bash
# Pull latest changes
git pull origin main

# Restart service
sudo systemctl restart ai-copilot-backend

# Or with Docker
docker-compose down
docker-compose up -d --build
```

### Database Migrations

Currently using in-memory storage. For persistent sessions, consider:
- Redis for session storage
- PostgreSQL for chat history
- Regular backups

## 🐛 Troubleshooting

### Server won't start

```bash
# Check if port is in use
sudo lsof -i :3001

# Check logs
sudo journalctl -u ai-copilot-backend -n 50
```

### CORS issues

Verify `ALLOWED_ORIGINS` in `.env` matches your frontend URL exactly.

### High memory usage

Adjust worker count:
```bash
gunicorn app.main:app -w 2 -k uvicorn.workers.UvicornWorker
```

### API rate limiting

Monitor Gemini API usage and implement rate limiting if needed.

## 📈 Scaling

### Horizontal Scaling

Run multiple instances behind a load balancer:

```nginx
upstream backend {
    server localhost:3001;
    server localhost:3002;
    server localhost:3003;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

### Session Storage

For multi-instance deployments, use shared session storage:
- Redis
- Memcached
- PostgreSQL

Modify `app/services/session_store.py` to use external storage.

## 🔒 Production Checklist

- [ ] API key configured and secured
- [ ] ALLOWED_ORIGINS restricted to production domains
- [ ] HTTPS enabled
- [ ] Logging configured (warning/error level)
- [ ] Firewall rules configured
- [ ] Health check monitoring active
- [ ] Backup strategy defined
- [ ] Rate limiting implemented
- [ ] Error tracking configured
- [ ] Resource limits set
- [ ] Auto-restart on failure enabled
- [ ] Documentation updated

## 📞 Support

For production issues:
1. Check logs first
2. Verify environment configuration
3. Test with health endpoint
4. Review recent changes
