# `query_decomposer_prompt.py`

## Module Overview
Contains the System Prompt for the `query_decomposer` node.

## Key Logic / Rules
- Instructs the LLM to tear apart a massive narrative prompt into isolated `semantic`, `statutory`, and `procedural` search strings.
- **Anti-Hallucination Update**: Explicitly tells the LLM: `"If none exist, leave it empty. Do NOT hallucinate sections."` This ensures that if the user doesn't mention a law (like BNS 310), the LLM doesn't randomly invent one, which would violently skew the BM25 retrieval results.
