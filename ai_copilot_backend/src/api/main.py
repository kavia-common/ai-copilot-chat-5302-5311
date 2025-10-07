import os
import uuid
from typing import List, Optional, Literal, Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Gemini client
from .gemini_client import GeminiClient

# Initialize FastAPI app with metadata for Swagger/OpenAPI
app = FastAPI(
    title="AI Copilot API",
    description="Backend API for AI Copilot chat application powered by Gemini AI. "
                "Provides endpoints for chat interactions, session management, and health checks.",
    version="1.0.0",
    openapi_tags=[
        {"name": "health", "description": "Health check endpoints"},
        {"name": "chat", "description": "Chat and session management endpoints"},
    ]
)

# CORS configuration - allow frontend origin
cors_origins = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client
gemini_client = GeminiClient()

# In-memory session storage (for demo purposes)
sessions: Dict[str, List[Dict[str, Any]]] = {}


# Pydantic Models
class ChatMessage(BaseModel):
    """
    Represents a single chat message.
    
    Attributes:
        id: Optional unique identifier for the message
        role: The role of the message sender (user, assistant, or system)
        content: The text content of the message
    """
    id: Optional[str] = Field(None, description="Unique message identifier")
    role: Literal['user', 'assistant', 'system'] = Field(..., description="Message sender role")
    content: str = Field(..., description="Message text content")


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    
    Attributes:
        sessionId: Unique session identifier for conversation continuity
        messages: List of messages in the conversation history
    """
    sessionId: str = Field(..., description="Session identifier for the conversation")
    messages: List[ChatMessage] = Field(..., description="List of messages in the conversation")


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    
    Attributes:
        sessionId: Session identifier
        message: Assistant's response message
        usage: Optional token usage information
        model: Model used for generation
    """
    sessionId: str = Field(..., description="Session identifier")
    message: ChatMessage = Field(..., description="Assistant's response message")
    usage: Optional[Dict[str, int]] = Field(None, description="Token usage statistics")
    model: Optional[str] = Field(None, description="AI model used for generation")


class ErrorResponse(BaseModel):
    """
    Error response model.
    
    Attributes:
        error: Error message
        detail: Additional error details
    """
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")


# PUBLIC_INTERFACE
@app.get(
    "/api/health",
    tags=["health"],
    summary="Health Check",
    description="Returns the health status of the API service.",
    response_description="Service health status",
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {"status": "ok", "service": "AI Copilot API"}
                }
            }
        }
    }
)
def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status indicating the service is operational
    """
    return {
        "status": "ok",
        "service": "AI Copilot API"
    }


# PUBLIC_INTERFACE
@app.post(
    "/api/chat",
    tags=["chat"],
    summary="Send Chat Message",
    description="Send a chat message and receive an AI-generated response. "
                "Maintains conversation context through sessionId.",
    response_model=ChatResponse,
    responses={
        200: {
            "description": "Successful response with AI-generated message",
            "model": ChatResponse
        },
        400: {
            "description": "Invalid request parameters",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error or Gemini API error",
            "model": ErrorResponse
        }
    }
)
async def chat(request: ChatRequest):
    """
    Handle chat requests and generate AI responses.
    
    This endpoint accepts a chat request with session ID and message history,
    forwards it to the Gemini API, and returns the AI-generated response.
    
    Args:
        request: ChatRequest containing sessionId and messages
        
    Returns:
        ChatResponse: Response containing the assistant's message
        
    Raises:
        HTTPException: If validation fails or Gemini API encounters an error
    """
    try:
        # Validate request
        if not request.messages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one message is required"
            )
        
        # Store session messages
        sessions[request.sessionId] = [msg.model_dump() for msg in request.messages]
        
        # Generate response using Gemini
        response_text, model_info = await gemini_client.generate(request.messages)
        
        # Create assistant message
        assistant_message = ChatMessage(
            id=str(uuid.uuid4()),
            role="assistant",
            content=response_text
        )
        
        # Update session with assistant response
        sessions[request.sessionId].append(assistant_message.model_dump())
        
        # Return response
        return ChatResponse(
            sessionId=request.sessionId,
            message=assistant_message,
            model=model_info.get("model"),
            usage=model_info.get("usage")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )


# PUBLIC_INTERFACE
@app.delete(
    "/api/session/{session_id}",
    tags=["chat"],
    summary="Delete Chat Session",
    description="Delete a chat session and clear its message history.",
    responses={
        200: {
            "description": "Session deleted successfully",
            "content": {
                "application/json": {
                    "example": {"status": "deleted", "sessionId": "abc-123"}
                }
            }
        },
        404: {
            "description": "Session not found",
            "model": ErrorResponse
        }
    }
)
def delete_session(session_id: str):
    """
    Delete a chat session.
    
    Args:
        session_id: The session identifier to delete
        
    Returns:
        dict: Confirmation of deletion
        
    Raises:
        HTTPException: If session not found
    """
    if session_id not in sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    del sessions[session_id]
    return {
        "status": "deleted",
        "sessionId": session_id
    }


# ROOT endpoint for backward compatibility
@app.get("/")
def root_health_check():
    """
    Root endpoint health check.
    
    Returns:
        dict: Health status message
    """
    return {"message": "Healthy"}
