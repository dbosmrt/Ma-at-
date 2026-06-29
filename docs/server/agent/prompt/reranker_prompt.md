# `reranker_prompt.py`

## Module Overview
Contains the System Prompt for the `reranker` node.

## Key Logic / Rules
- Instructs the LLM to output a raw JSON array of indices (e.g., `[0, 5, 12]`) corresponding to the chunks that contain relevant information.
- Contains strict rules forcing the LLM to only output indices that actually exist in the provided list, preventing out-of-bounds array errors in the Python backend.
