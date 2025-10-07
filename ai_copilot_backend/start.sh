#!/bin/bash

# AI Copilot Backend Startup Script
# This script ensures environment variables are loaded before starting the server

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting AI Copilot Backend...${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ Error: .env file not found!${NC}"
    echo -e "${YELLOW}Please create a .env file from .env.example:${NC}"
    echo "  cp .env.example .env"
    echo "  # Then edit .env and add your GEMINI_API_KEY"
    exit 1
fi

# Load and verify environment variables
source .env

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" = "your_gemini_api_key_here" ]; then
    echo -e "${RED}❌ Error: GEMINI_API_KEY is not configured!${NC}"
    echo -e "${YELLOW}Please set a valid GEMINI_API_KEY in your .env file${NC}"
    exit 1
fi

# Set default values if not provided
PORT=${PORT:-3001}
CORS_ORIGINS=${CORS_ORIGINS:-"http://localhost:3000"}

echo -e "${GREEN}✅ Environment variables loaded${NC}"
echo -e "   PORT: ${PORT}"
echo -e "   CORS_ORIGINS: ${CORS_ORIGINS}"
echo -e "   GEMINI_API_KEY: ${GEMINI_API_KEY:0:10}...${NC}"

# Export variables for uvicorn
export GEMINI_API_KEY
export PORT
export CORS_ORIGINS

# Start the server
echo -e "${GREEN}🌐 Starting server on port ${PORT}...${NC}"
uvicorn src.api.main:app --host 0.0.0.0 --port $PORT --reload
