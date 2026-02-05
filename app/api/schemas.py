from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


# Validation limits
MAX_MESSAGE_LENGTH = 5000
MAX_SESSION_ID_LENGTH = 128
MAX_HISTORY_ITEMS = 50
MAX_SENDER_LENGTH = 64


class Message(BaseModel):
    sender: str = Field(..., max_length=MAX_SENDER_LENGTH)
    text: str = Field(..., max_length=MAX_MESSAGE_LENGTH)
    timestamp: int = Field(..., ge=0)
    
    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Message text cannot be empty")
        return v


class Metadata(BaseModel):
    channel: Optional[str] = Field(None, max_length=32)
    language: Optional[str] = Field(None, max_length=10)
    locale: Optional[str] = Field(None, max_length=10)


class IncomingRequest(BaseModel):
    sessionId: str = Field(..., min_length=1, max_length=MAX_SESSION_ID_LENGTH)
    message: Message
    conversationHistory: List[Message] = Field(
        default_factory=list,
        max_length=MAX_HISTORY_ITEMS
    )
    metadata: Optional[Metadata] = None
    
    @field_validator("sessionId")
    @classmethod
    def session_id_valid(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Session ID cannot be empty")
        # Prevent path traversal or injection
        if any(c in v for c in ["../", "\\", "\n", "\r", "\0"]):
            raise ValueError("Invalid session ID format")
        return v.strip()


class APIResponse(BaseModel):
    status: str
    reply: str
