"""
Data Models

Pydantic models for request/response validation and data structure definitions.
"""

from typing import List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    Represents a single message in a conversation.
    
    Attributes:
        role: Either 'user' or 'assistant'
        content: The message content (supports markdown)
        timestamp: When the message was created
    """
    role: Literal["user", "assistant"] = Field(
        ...,
        description="The role of the message sender"
    )
    content: str = Field(
        ...,
        description="The message content, supports markdown formatting"
    )
    timestamp: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="Timestamp when the message was created"
    )


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    
    Attributes:
        session_id: Unique identifier for the conversation session
        message: The user's message/prompt
    """
    session_id: str = Field(
        ...,
        description="Session ID for maintaining conversation context",
        min_length=1
    )
    message: str = Field(
        ...,
        description="User's message or prompt",
        min_length=1,
        max_length=10000
    )


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    
    Attributes:
        response: The AI's response in markdown format
        session_id: The session ID for this conversation
    """
    response: str = Field(
        ...,
        description="AI-generated response in markdown format"
    )
    session_id: str = Field(
        ...,
        description="Session ID for this conversation"
    )


class SessionResponse(BaseModel):
    """
    Response model for session creation.
    
    Attributes:
        session_id: Unique identifier for the new session
        message: Status message
        created_at: Timestamp of session creation
    """
    session_id: str = Field(
        ...,
        description="Unique session identifier"
    )
    message: str = Field(
        default="Session created successfully",
        description="Status message"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="Session creation timestamp"
    )


class SessionResetResponse(BaseModel):
    """
    Response model for session reset operation.
    
    Attributes:
        session_id: The session that was reset
        message: Status message
        status: Operation status
    """
    session_id: str = Field(
        ...,
        description="Session identifier"
    )
    message: str = Field(
        ...,
        description="Status message"
    )
    status: str = Field(
        default="success",
        description="Operation status"
    )
