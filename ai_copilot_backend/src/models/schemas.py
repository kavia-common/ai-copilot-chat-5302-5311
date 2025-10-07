from datetime import datetime
from typing import Optional, Literal, List, Dict, Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """
    Represents a single chat message in a conversation.
    """
    role: Literal['user', 'assistant', 'system'] = Field(
        ..., 
        description="The role of the message sender: user, assistant, or system"
    )
    content: str = Field(
        ..., 
        description="The content of the message"
    )
    timestamp: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="Timestamp when the message was created"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "Hello, can you help me with Python?",
                "timestamp": "2024-01-01T12:00:00"
            }
        }


class ChatRequest(BaseModel):
    """
    Request model for sending a chat message.
    """
    session_id: str = Field(
        ..., 
        description="Unique identifier for the chat session"
    )
    message: ChatMessage = Field(
        ..., 
        description="The chat message to send"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session-123",
                "message": {
                    "role": "user",
                    "content": "Write a Python function to sort a list"
                }
            }
        }


class ChatResponse(BaseModel):
    """
    Response model for chat API endpoint.
    """
    session_id: str = Field(
        ..., 
        description="The session identifier"
    )
    message: ChatMessage = Field(
        ..., 
        description="The assistant's response message"
    )
    usage: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional usage statistics from the AI model"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session-123",
                "message": {
                    "role": "assistant",
                    "content": "Here's a Python function to sort a list...",
                    "timestamp": "2024-01-01T12:00:01"
                },
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 50,
                    "total_tokens": 60
                }
            }
        }


class SessionHistory(BaseModel):
    """
    Model representing the full conversation history for a session.
    """
    session_id: str = Field(
        ..., 
        description="The session identifier"
    )
    messages: List[ChatMessage] = Field(
        default_factory=list,
        description="List of all messages in the session"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }
