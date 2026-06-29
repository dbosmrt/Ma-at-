# `server/api/routes.py`

## Module Overview
This file contains the HTTP endpoint definitions. It acts as the bridge between the external internet requests and the internal LangGraph state machine.

## Dependencies
- `fastapi.APIRouter`: Allows us to modularize routes rather than defining them all directly in `main.py`.
- `fastapi.HTTPException, Depends`: Used for error handling and injecting the security API key validation.
- `langchain_core.messages`: Used to rebuild the raw JSON history into native LangChain message objects before passing them to the agent state.
- `agent.chat_graph.build_chat_graph`: Imports the graph compiler.

## Core Initialization
```python
# Global graph instance for the API
chat_graph = build_chat_graph()

CHAT_DIR = os.path.abspath(...)
```
- **Logic**: The LangGraph is compiled **once** at the global scope when the server boots. This prevents the server from incurring a heavy 1-2 second compilation penalty on every single HTTP request. The `CHAT_DIR` is dynamically resolved to point to `data/chats/` at the root of the project.

## Helper Functions

### `_load_session_file(session_id: str)` & `_save_session_file(...)`
- **Role**: Directly reads/writes raw JSON files from the `data/chats/` directory.
- **Why**: Currently acts as a lightweight, file-system-based NoSQL database to persist conversation history without requiring a dedicated PostgreSQL/Mongo instance.

## Endpoint Breakdown

### 1. `GET /health`
- **Inputs**: None.
- **Outputs**: `{"status": "ok"}`
- **Role**: A simple ping endpoint used by load balancers or frontend monitors to check if the API is alive.

### 2. `POST /api/v1/chat/start`
- **Inputs**: API Key via headers.
- **Outputs**: `StartSessionResponse`
- **Logic**: Generates an 8-character UUID using `uuid.uuid4()`, writes a blank JSON file to disk, and returns the ID.

### 3. `GET /api/v1/chat/{session_id}`
- **Inputs**: `session_id` (Path variable).
- **Outputs**: `ChatHistoryResponse` or `404 Not Found`.
- **Logic**: Reads the session JSON from disk and serves the entire raw chat history to the frontend client.

### 4. `POST /api/v1/chat/{session_id}`
- **Inputs**: `session_id` (Path variable), `ChatRequest` (JSON Body), API Key.
- **Outputs**: `ChatResponse`
- **Core Logic**:
  1. **Dynamic Session Creation**: If `session_id` is exactly `"new"`, it automatically creates a fresh UUID and initializes the session array. This removes API friction, allowing a frontend to start a chat and send a message in a single network request.
  2. **History Reconstruction**: Rebuilds the raw JSON dictionaries into LangChain `HumanMessage` and `AIMessage` objects.
  3. **Context Window Limit**: Only injects the last 4 messages (`lc_history[-4:]`) into the `AgentState`. This is a critical protection mechanism to prevent long conversations from exhausting the LLM's token limit.
  4. **Graph Execution**: Invokes the `chat_graph` with the constructed state, effectively firing off the entire RAG pipeline.
  5. **Persistence**: Appends the human query and AI generation to the raw history array and saves it back to disk.
