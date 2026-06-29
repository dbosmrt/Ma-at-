# `qualifier_prompt.py`

## Module Overview
Contains the System Prompt for the `qualifier` node.

## Key Logic / Rules
- Uses **Few-Shot Prompting**. By providing concrete examples of user inputs and expected JSON outputs, it vastly improves the LLM's classification accuracy.
- Specifically provides examples for conversational greetings (e.g., `"Hi, I need help"`) so the LLM knows exactly when to toggle the `is_general_chat` boolean to `True`, triggering the retrieval bypass.
