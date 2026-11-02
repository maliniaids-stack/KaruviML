"""Request and response models. Empty for now; you add these from Session 4."""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    language: str = "English"


class ChatResponse(BaseModel):
    answer: str
    language: str
    status: str = "success"