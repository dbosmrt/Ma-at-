# `query_decomposer.py`

## Module Overview
A pre-processing node designed specifically to handle complex, messy, or long narrative prompts (e.g., "My landlord kicked me out at 3am without notice and stole my TV").

## Role in Pipeline
Executes before the Vector Database retrieval. Its job is to split a massive narrative into highly targeted search strings so the database isn't confused by irrelevant adjectives.

## Function Breakdown

### `query_decomposer_node(state: AgentState) -> dict`
- **Inputs**: The user's raw `query`.
- **Outputs**: A dictionary populated with the `DecomposedQuery` schema (`semantic_focus`, `statutory_focus`, `procedural_focus`).
- **Logic**:
  - Uses `with_structured_output` to force the LLM to analyze the prompt.
  - **Semantic**: Extracts the core action (e.g., "illegal eviction night theft").
  - **Statutory**: Extracts explicit legal identifiers if the user mentioned them (e.g., "BNS Section 310"). *Note: The prompt explicitly forbids hallucinating these if the user didn't provide them, to prevent database misdirection.*
  - **Procedural**: Extracts procedural terms (e.g., "FIR registration").
  - These isolated strings are injected into the state, where the `retriever.py` node uses them to construct a vastly superior hybrid search query.
