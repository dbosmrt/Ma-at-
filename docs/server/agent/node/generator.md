# `generator.py`

## Module Overview
The final synthesis node in the pipeline. Responsible for reading all the retrieved/scraped context and formulating the polished Markdown response sent back to the user.

## Function Breakdown

### `generator_node(state: AgentState) -> dict`
- **Inputs**: `query`, `chat_history`, `documents` (from VectorDB), `case_laws` (from Web Search), and `is_general_chat` (from Qualifier).
- **Outputs**: The final markdown `generation` string.
- **Logic**:
  - Checks if the query was flagged as `is_general_chat`. If so, it completely ignores the empty document arrays and uses a highly conversational prompt, instructing the LLM to act as a friendly, professional AI Advocate.
  - If it is a legal query, it formats all `documents` and `case_laws` into a massive context block.
  - It injects the `chat_history` so the bot remembers the context of previous questions.
  - **Hallucination Prevention**: The prompt explicitly forces the bot to output exactly: *"The requested legal section was not found in the knowledge base"* if the RAG context is empty. It is strictly forbidden from creating hypothetical outlines.
  - **Streaming Support**: Invokes `llm.stream()` and yields the chunks (currently collapsed into a single string for the REST API wrapper).
