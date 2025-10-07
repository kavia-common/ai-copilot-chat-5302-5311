"""
API Routes

Defines all REST API endpoints for chat interactions, session management,
and prompt handling.
"""

import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.models import (
    ChatRequest,
    ChatResponse,
    SessionResponse,
    SessionResetResponse,
    Message
)
from app.services.session_store import session_store
from app.services.gemini_client import gemini_client
from app.utils.formatting import format_markdown_response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")


# Request/Response Models for API documentation
class CreateSessionRequest(BaseModel):
    """Request model for creating a new session (optional body)"""
    pass


# PUBLIC_INTERFACE
@router.post(
    "/sessions",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["sessions"],
    summary="Create New Session",
    description="Creates a new chat session and returns the session ID"
)
async def create_session(request: CreateSessionRequest = None) -> SessionResponse:
    """
    Create a new chat session.
    
    This endpoint initializes a new conversation session with the AI.
    Each session maintains its own conversation history.
    
    Args:
        request: Optional request body (can be empty)
    
    Returns:
        SessionResponse: Contains the new session ID and metadata
    
    Example:
        ```
        POST /api/sessions
        Response: {"session_id": "abc123", "created_at": "2024-01-01T00:00:00Z"}
        ```
    """
    try:
        session_id = session_store.create_session()
        logger.info(f"Created new session: {session_id}")
        return SessionResponse(
            session_id=session_id,
            message="Session created successfully"
        )
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {str(e)}"
        )


# PUBLIC_INTERFACE
@router.get(
    "/sessions/{session_id}",
    response_model=Dict[str, Any],
    tags=["sessions"],
    summary="Get Session History",
    description="Retrieves the conversation history for a specific session"
)
async def get_session(session_id: str) -> Dict[str, Any]:
    """
    Retrieve session history.
    
    Returns the complete conversation history for the specified session,
    including all user messages and AI responses.
    
    Args:
        session_id: The unique session identifier
    
    Returns:
        dict: Session data including messages and metadata
    
    Raises:
        HTTPException: 404 if session not found
    """
    session = session_store.get_session(session_id)
    if not session:
        logger.warning(f"Session not found: {session_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    return {
        "session_id": session_id,
        "messages": session.get("messages", []),
        "created_at": session.get("created_at")
    }


# PUBLIC_INTERFACE
@router.post(
    "/sessions/{session_id}/reset",
    response_model=SessionResetResponse,
    tags=["sessions"],
    summary="Reset Session",
    description="Clears all messages from a session while keeping the session active"
)
async def reset_session(session_id: str) -> SessionResetResponse:
    """
    Reset a session by clearing its conversation history.
    
    This endpoint removes all messages from the session but keeps
    the session ID active for new conversations.
    
    Args:
        session_id: The unique session identifier
    
    Returns:
        SessionResetResponse: Confirmation of reset operation
    
    Raises:
        HTTPException: 404 if session not found
    """
    session = session_store.get_session(session_id)
    if not session:
        logger.warning(f"Session not found for reset: {session_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    session_store.reset_session(session_id)
    logger.info(f"Reset session: {session_id}")
    
    return SessionResetResponse(
        session_id=session_id,
        message="Session reset successfully",
        status="success"
    )


# PUBLIC_INTERFACE
@router.post(
    "/chat",
    response_model=ChatResponse,
    tags=["chat"],
    summary="Send Chat Message",
    description="Sends a user message to the AI and returns the response"
)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process a chat message and return AI response.
    
    This is the main endpoint for chat interactions. It accepts a user's
    message, processes it using the Gemini API, and returns a formatted
    markdown response with support for code blocks and syntax highlighting.
    
    Args:
        request: ChatRequest containing session_id and message
    
    Returns:
        ChatResponse: The AI's response with formatted markdown content
    
    Raises:
        HTTPException: 404 if session not found, 500 on processing errors
    
    Example:
        ```json
        POST /api/chat
        {
            "session_id": "abc123",
            "message": "Explain Python decorators"
        }
        
        Response:
        {
            "response": "# Python Decorators\n\nDecorators are...",
            "session_id": "abc123"
        }
        ```
    """
    # Validate session exists
    session = session_store.get_session(request.session_id)
    if not session:
        logger.warning(f"Chat attempted on non-existent session: {request.session_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {request.session_id} not found"
        )
    
    try:
        # Store user message
        user_message = Message(role="user", content=request.message)
        session_store.append_message(request.session_id, user_message.model_dump())
        
        # Get conversation history for context
        history = session.get("messages", [])
        
        # Generate AI response
        logger.info(f"Processing chat for session {request.session_id}")
        ai_response = await gemini_client.generate_response(
            prompt=request.message,
            history=history
        )
        
        # Format the response
        formatted_response = format_markdown_response(ai_response)
        
        # Store AI response
        assistant_message = Message(role="assistant", content=formatted_response)
        session_store.append_message(request.session_id, assistant_message.model_dump())
        
        logger.info(f"Successfully generated response for session {request.session_id}")
        
        return ChatResponse(
            response=formatted_response,
            session_id=request.session_id
        )
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )
