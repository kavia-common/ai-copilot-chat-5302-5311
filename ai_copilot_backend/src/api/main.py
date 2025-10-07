from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict, List
import os
from dotenv import load_dotenv

from src.models.schemas import ChatRequest, ChatResponse, Message
from src.services.gemini_service import GeminiService

# Load environment variables
load_dotenv()

# OpenAPI metadata
app = FastAPI(
    title="AI Copilot Backend API",
    description="Backend API for AI Copilot chat application powered by Google Gemini API. "
                "Provides endpoints for chat interactions, prompt handling, and session management.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check and status endpoints"
        },
        {
            "name": "chat",
            "description": "Chat and conversation management endpoints"
        },
        {
            "name": "sessions",
            "description": "Session history and retrieval endpoints"
        }
    ]
)

# CORS configuration - allow frontend at localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage
# Key: session_id, Value: list of Message objects
sessions: Dict[str, List[Message]] = {}

# Initialize Gemini service (will be None if API key not configured)
gemini_service = None
try:
    gemini_service = GeminiService()
except ValueError as e:
    print(f"Warning: {e}")
    print("Chat endpoint will return errors until GEMINI_API_KEY is configured.")


@app.get(
    "/",
    tags=["health"],
    summary="Health Check",
    description="Check if the API is running and healthy"
)
# PUBLIC_INTERFACE
def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: Status message and API key configuration status
    """
    api_key_configured = bool(os.getenv("GEMINI_API_KEY"))
    return {
        "message": "Healthy",
        "status": "ok",
        "gemini_api_configured": api_key_configured
    }


@app.post(
    "/api/chat",
    response_model=ChatResponse,
    tags=["chat"],
    summary="Send Chat Message",
    description="Send a message to the AI Copilot and receive a response. "
                "Manages conversation history automatically per session."
)
# PUBLIC_INTERFACE
def chat(request: ChatRequest):
    """
    Handle incoming chat requests and generate AI responses.
    
    This endpoint:
    1. Accepts a user message and session ID
    2. Retrieves or creates conversation history for the session
    3. Sends the message to Gemini API with context
    4. Stores both user message and AI response in session history
    5. Returns the AI's response
    
    Args:
        request: ChatRequest containing session_id, message, and optional history
        
    Returns:
        ChatResponse: Contains session_id, AI reply, and optional usage metadata
        
    Raises:
        HTTPException: 503 if Gemini API is not configured
        HTTPException: 500 if there's an error generating the response
    """
    # Check if Gemini service is initialized
    if gemini_service is None:
        raise HTTPException(
            status_code=503,
            detail="Gemini API is not configured. Please set GEMINI_API_KEY environment variable."
        )
    
    session_id = request.session_id
    user_message = request.message
    
    # Initialize session if it doesn't exist
    if session_id not in sessions:
        sessions[session_id] = []
    
    # Get conversation history
    history = sessions[session_id]
    
    # Create user message object
    user_msg = Message(
        role="user",
        content=user_message,
        ts=datetime.utcnow()
    )
    
    # Add user message to history
    history.append(user_msg)
    
    try:
        # Generate AI response using Gemini service
        ai_reply = gemini_service.generate_reply(
            prompt=user_message,
            history=history[:-1]  # Pass history excluding the current message
        )
        
        # Create assistant message object
        assistant_msg = Message(
            role="assistant",
            content=ai_reply,
            ts=datetime.utcnow()
        )
        
        # Add assistant message to history
        history.append(assistant_msg)
        
        # Update session storage
        sessions[session_id] = history
        
        # Return response
        return ChatResponse(
            session_id=session_id,
            reply=ai_reply,
            usage=None  # Can add token usage info if needed
        )
        
    except Exception as e:
        # Remove the user message from history if we failed to get a response
        if history and history[-1].role == "user":
            history.pop()
        
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )


@app.get(
    "/api/sessions/{session_id}",
    response_model=List[Message],
    tags=["sessions"],
    summary="Get Session History",
    description="Retrieve the complete conversation history for a specific session"
)
# PUBLIC_INTERFACE
def get_session_history(session_id: str):
    """
    Retrieve the conversation history for a given session.
    
    Args:
        session_id: The unique identifier for the session
        
    Returns:
        List[Message]: List of all messages in the session
        
    Raises:
        HTTPException: 404 if session not found
    """
    if session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' not found"
        )
    
    return sessions[session_id]


@app.delete(
    "/api/sessions/{session_id}",
    tags=["sessions"],
    summary="Delete Session",
    description="Delete a session and its conversation history"
)
# PUBLIC_INTERFACE
def delete_session(session_id: str):
    """
    Delete a session and its conversation history.
    
    Args:
        session_id: The unique identifier for the session to delete
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: 404 if session not found
    """
    if session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' not found"
        )
    
    del sessions[session_id]
    
    return {
        "message": f"Session '{session_id}' deleted successfully",
        "status": "ok"
    }
