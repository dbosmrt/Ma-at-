from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ChatRequest(BaseModel):
    query: str = Field(..., max_length=2000, description="The user's legal question or scenario.")

class ChatResponse(BaseModel):
    session_id: str
    generation: str
    law_domain: str

class StartSessionResponse(BaseModel):
    session_id: str
    message: str

class MessageHistory(BaseModel):
    type: str
    content: str

class ChatHistoryResponse(BaseModel):
    session_id: str
    history: List[MessageHistory]

class SessionItem(BaseModel):
    session_id: str
    preview: str
    message_count: int

class SessionListResponse(BaseModel):
    sessions: List[SessionItem]
