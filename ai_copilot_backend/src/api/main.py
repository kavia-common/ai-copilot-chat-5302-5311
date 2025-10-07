import os
from datetime import datetime
from typing import Dict, List
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from src.models.schemas import ChatMessage, ChatRequest, ChatResponse, SessionHistory
from src.services.gemini_service import GeminiClient

# Load environment variables from .env file
load_dotenv()

# FastAPI app with metadata for OpenAPI documentation
app = FastAPI(
    title="AI Copilot Chat API",
    description="Backend API for AI Copilot chat application with Gemini integration. Provides endpoints for chat interactions, session management, and AI-powered responses.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check and status endpoints"
        },
        {
            "name": "chat",
            "description": "Chat operations with AI assistant"
        },
        {
            "name": "sessions",
            "description": "Session management and history"
        }
    ]
)

# Configure CORS
# Parse CORS origins from environment variable, strip whitespace from each origin
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://vscode-internal-29933-beta.beta01.cloud.kavia.ai:3000")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store: session_id -> list of ChatMessage
sessions: Dict[str, List[ChatMessage]] = {}

# Initialize Gemini client (will be set on first request to handle startup errors gracefully)
gemini_client: GeminiClient = None


def get_gemini_client() -> GeminiClient:
    """
    Get or initialize the Gemini client.
    
    Returns:
        GeminiClient: The initialized Gemini client instance.
    
    Raises:
        HTTPException: If GEMINI_API_KEY is not set or client initialization fails.
    """
    global gemini_client
    
    if gemini_client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="GEMINI_API_KEY environment variable is not configured. Please set it in the .env file."
            )
        
        try:
            gemini_client = GeminiClient()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to initialize Gemini client: {str(e)}"
            )
    
    return gemini_client


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["health"],
    summary="Health Check",
    description="Returns the health status of the API service.",
    response_description="Health status message"
)
def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: A message indicating the service is healthy.
    """
    return {"message": "Healthy", "service": "AI Copilot Chat API", "version": "1.0.0"}


# PUBLIC_INTERFACE
@app.get(
    "/health",
    tags=["health"],
    summary="Health Check (Alternative)",
    description="Alternative health check endpoint for compatibility.",
    response_description="Health status message"
)
def health_check_alt():
    """
    Alternative health check endpoint.
    
    Returns:
        dict: A message indicating the service is healthy.
    """
    return {"message": "Healthy", "service": "AI Copilot Chat API", "version": "1.0.0"}


# PUBLIC_INTERFACE
@app.post(
    "/api/chat",
    response_model=ChatResponse,
    tags=["chat"],
    summary="Send Chat Message",
    description="Send a chat message to the AI assistant. The message is added to the session history, processed by Gemini AI, and the assistant's response is returned and stored in the session.",
    responses={
        200: {
            "description": "Successfully processed chat message",
            "model": ChatResponse
        },
        400: {
            "description": "Bad request - missing API key or invalid input"
        },
        502: {
            "description": "Bad gateway - error communicating with Gemini API"
        }
    }
)
async def chat(request: ChatRequest):
    """
    Process a chat message and return the AI assistant's response.
    
    This endpoint:
    1. Validates the GEMINI_API_KEY is configured
    2. Retrieves or creates a session for the given session_id
    3. Adds the user's message to the session history
    4. Sends the full conversation to Gemini AI
    5. Stores and returns the assistant's response
    
    Args:
        request (ChatRequest): The chat request containing session_id and message.
    
    Returns:
        ChatResponse: The response containing the assistant's message.
    
    Raises:
        HTTPException: 400 if API key is missing, 502 if Gemini API fails.
    """
    try:
        # Get or initialize Gemini client
        client = get_gemini_client()
        
        # Get or create session
        session_id = request.session_id
        if session_id not in sessions:
            sessions[session_id] = []
        
        # Add user message to session
        user_message = request.message
        user_message.timestamp = datetime.now()
        sessions[session_id].append(user_message)
        
        # Prepare conversation history for Gemini
        message_history = [
            {"role": msg.role, "content": msg.content}
            for msg in sessions[session_id]
        ]
        
        # Get response from Gemini
        try:
            assistant_response_text = client.respond(message_history)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Gemini API error: {str(e)}"
            )
        
        # Create assistant message
        assistant_message = ChatMessage(
            role="assistant",
            content=assistant_response_text,
            timestamp=datetime.now()
        )
        
        # Add assistant message to session
        sessions[session_id].append(assistant_message)
        
        # Return response
        return ChatResponse(
            session_id=session_id,
            message=assistant_message,
            usage=None  # Gemini SDK doesn't provide usage stats in the basic response
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


# PUBLIC_INTERFACE
@app.post(
    "/api/chat/stream",
    tags=["chat"],
    summary="Stream Chat Message (Not Implemented)",
    description="Placeholder endpoint for streaming chat responses using Server-Sent Events. Currently returns 501 Not Implemented.",
    responses={
        501: {
            "description": "Not implemented - streaming not yet available"
        }
    }
)
async def chat_stream(request: ChatRequest):
    """
    Stream chat responses using Server-Sent Events.
    
    This endpoint is a placeholder for future streaming functionality.
    
    Args:
        request (ChatRequest): The chat request.
    
    Returns:
        JSONResponse: 501 Not Implemented status.
    """
    return JSONResponse(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        content={
            "detail": "Streaming is not yet implemented. Please use the /api/chat endpoint for non-streaming responses."
        }
    )


# PUBLIC_INTERFACE
@app.get(
    "/api/sessions/{session_id}",
    response_model=SessionHistory,
    tags=["sessions"],
    summary="Get Session History",
    description="Retrieve the complete conversation history for a specific session. Returns all messages exchanged in the session.",
    responses={
        200: {
            "description": "Successfully retrieved session history",
            "model": SessionHistory
        },
        404: {
            "description": "Session not found"
        }
    }
)
async def get_session(session_id: str):
    """
    Retrieve the conversation history for a session.
    
    Args:
        session_id (str): The unique session identifier.
    
    Returns:
        SessionHistory: The complete conversation history.
    
    Raises:
        HTTPException: 404 if the session doesn't exist.
    """
    if session_id not in sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session '{session_id}' not found"
        )
    
    return SessionHistory(
        session_id=session_id,
        messages=sessions[session_id]
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    Logs startup information and environment configuration.
    """
    print("🚀 AI Copilot Chat API starting up...")
    print(f"📝 Environment loaded: {os.getenv('GEMINI_API_KEY', 'NOT SET')[:10]}...")
    print(f"🌐 CORS origins: {os.getenv('CORS_ORIGINS', 'http://localhost:3000')}")
    print("✅ API ready to accept requests")
