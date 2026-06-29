# `server/api/models.py`

## Module Overview
This file defines the strictly-typed Pydantic data schemas used by the FastAPI routing layer. These models dictate exactly what JSON payload shape the frontend client must send, and what JSON payload shape the backend will return.

## Dependencies
- `pydantic.BaseModel, Field`: The core data validation library natively supported by FastAPI.
- `typing.List`: For defining arrays of nested models.

## Class Breakdown

### 1. `ChatRequest`
```python
class ChatRequest(BaseModel):
    query: str = Field(..., max_length=2000, description="The user's legal question or scenario.")
```
- **Role**: Validates the payload sent by the frontend when asking a new question via `POST /api/v1/chat/{session_id}`.
- **Security Mechanism**: Uses `Field(max_length=2000)` to strictly cap the input string length. This prevents malicious users from executing buffer overflow attacks or intentionally crashing the backend LLM by maxing out its context window with gigabytes of text. If a payload exceeds 2000 characters, FastAPI automatically rejects it with a `422 Unprocessable Entity` error before it ever reaches the application logic.

### 2. `ChatResponse`
```python
class ChatResponse(BaseModel):
    session_id: str
    generation: str
    law_domain: str
```
- **Role**: Defines the exact structure of the successful response returned to the frontend after the RAG inference pipeline completes.
- **Outputs**:
  - `session_id`: Returned so the frontend can append it to future requests in the same conversation.
  - `generation`: The formatted markdown string produced by the AI Generator node.
  - `law_domain`: The legal domain (e.g., "Criminal", "Civil") identified by the Qualifier node.

### 3. `StartSessionResponse`
```python
class StartSessionResponse(BaseModel):
    session_id: str
    message: str
```
- **Role**: Used by the `/api/v1/chat/start` endpoint to confirm a blank session was created and return its UUID.

### 4. `MessageHistory` & `ChatHistoryResponse`
```python
class MessageHistory(BaseModel):
    type: str
    content: str

class ChatHistoryResponse(BaseModel):
    session_id: str
    history: List[MessageHistory]
```
- **Role**: Used by the `GET /api/v1/chat/{session_id}` endpoint to serialize the saved JSON chat history into a strictly typed array for the frontend to render upon page reload. `type` will be either `"human"` or `"ai"`.
