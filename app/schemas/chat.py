"""Chat request and response schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""

    message: str = Field(..., description="User's message to the financial advisor agent")
    session_id: Optional[str] = Field(
        None, description="Session ID for conversation continuity"
    )
    user_id: Optional[str] = Field(None, description="User ID for portfolio context")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "What's the bull case for my AAPL holdings?",
                    "session_id": "session-123",
                    "user_id": "user-456",
                }
            ]
        }
    }


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    message: str = Field(..., description="Agent's response message")
    session_id: str = Field(..., description="Session ID for this conversation")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Response timestamp"
    )
    analysis_type: Optional[str] = Field(
        None, description="Type of analysis performed (e.g., 'bull_bear', 'earnings')"
    )
    confidence: Optional[str] = Field(
        None, description="Confidence level or data quality indicator"
    )
    citations: list[str] = Field(
        default_factory=list, description="Data sources and metrics cited"
    )
    disclaimer: str = Field(
        default="This is not financial advice. All analysis is for informational purposes only.",
        description="Risk disclaimer",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Based on your AAPL holdings, here's the bull case...",
                    "session_id": "session-123",
                    "timestamp": "2025-11-24T10:00:00Z",
                    "analysis_type": "bull_bear",
                    "confidence": "high",
                    "citations": ["P/E ratio: 28.5", "YoY revenue growth: 12%"],
                    "disclaimer": "This is not financial advice. All analysis is for informational purposes only.",
                }
            ]
        }
    }
