# `generator_prompt.py`

## Module Overview
Contains the core System Prompt for the `generator` node.

## Key Logic / Rules
- **Formatting Guidelines**: Instructs the LLM to output beautiful Markdown (headers, bolding, bullet points).
- **Anti-Hallucination Armor**: The prompt explicitly forces the LLM to write: `"The requested legal section was not found in the knowledge base. Please verify indexing."` if the retrieved documents do not contain the answer. It is strictly forbidden from making "educational guesses" or hypothetical legal outlines.
- **Citation Enforcement**: Forces the LLM to cite the exact `[Source: BNS - Section 63]` inline within the response, guaranteeing legal traceability.
- **Conversational Advocate Persona**: If the `is_general_chat` flag is detected, a secondary prompt injects a persona shift, telling the LLM to act as a friendly, supportive legal assistant and bypass the strict statute-retrieval rules.
