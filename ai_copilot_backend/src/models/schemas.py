from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class Message(BaseModel):
    """
    Represents a single chat message in the conversation history.
    
    Attributes:
        role: The role of the message sender ('user' or 'assistant')
        content: The text content of the message
        ts: Optional timestamp when the message was created
    """
    role: Literal['user', 'assistant'] = Field(
        ..., 
        description="The role of the message sender (user or assistant)"
    )
    content: str = Field(
        ..., 
        description="The text content of the message"
    )
    ts: Optional[datetime] = Field(
        default=None, 
        description="Timestamp when the message was created"
    )


class ChatRequest(BaseModel):
    """
    Request payload for sending a chat message.
    
    Attributes:
        session_id: Unique identifier for the conversation session
        message: The user's message to send to the AI
        history: Optional list of previous messages for context
    """
    session_id: str = Field(
        ..., 
        description="Unique identifier for the conversation session"
    )
    message: str = Field(
        ..., 
        description="The user's message to send to the AI"
    )
    history: Optional[list[Message]] = Field(
        default=None, 
        description="Optional list of previous messages for context"
    )


class ChatResponse(BaseModel):
    """
    Response payload containing the AI's reply.
    
    Attributes:
        session_id: The session identifier for this conversation
        reply: The AI's response message
        usage: Optional metadata about token usage or other stats
    """
    session_id: str = Field(
        ..., 
        description="The session identifier for this conversation"
    )
    reply: str = Field(
        ..., 
        description="The AI's response message"
    )
    usage: Optional[dict] = Field(
        default=None, 
        description="Optional metadata about token usage or other statistics"
    )
