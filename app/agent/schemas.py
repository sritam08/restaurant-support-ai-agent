from typing import Literal
from pydantic import BaseModel, Field, field_validator

Category = Literal["Payment", "Order", "Delivery", "Refund", "Technical"]
Priority = Literal["Low", "Medium", "High"]
Sentiment = Literal["Positive", "Neutral", "Negative"]

class ComplaintClassification(BaseModel):
    category: Category
    priority: Priority
    sentiment: Sentiment
    requires_escalation: bool
    summary: str = Field(min_length=1, max_length=500)

    @field_validator("summary")
    @classmethod
    def clean_summary(cls, value: str) -> str:
        return value.strip()

class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=4000)

class ChatResponse(BaseModel):
    session_id: str
    response: str
    tool_calls: list[str] = []
    sources: list[str] = []

class ComplaintRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=4000)

class Ticket(BaseModel):
    ticket_id: str
    category: Category
    priority: Priority
    description: str
    session_id: str
    idempotency_key: str
