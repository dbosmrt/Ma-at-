# `grader_prompt.py`

## Module Overview
Contains the System Prompt for the `grader` node.

## Key Logic / Rules
- Instructs the LLM to act as a strict legal grader evaluating the context's ability to answer the query.
- **Permissive Tuning**: Contains a `CRITICAL PROMPT UPDATE` instructing the LLM to adopt a highly permissive stance on grading. If a chunk mentions core legal concepts related to the query (like "theft" or "weapons"), it MUST pass the chunk. This prevents the grader from aggressively filtering out valid context just because it lacks an exact alphanumeric Section code.
- **Anti-Inference Rule**: Despite being permissive, it explicitly forbids the grader from hallucinating or guessing legal connections that aren't actually written in the text.
