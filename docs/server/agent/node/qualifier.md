# `qualifier.py`

## Module Overview
The first analytical node in the live inference pipeline. It acts as the "Brain Router", analyzing the user's raw prompt to figure out exactly what kind of question they are asking.

## Role in Pipeline
Immediately follows the `query_decomposer`. It does NOT try to answer the question. It simply classifies the question and outputs JSON flags that tell the rest of the LangGraph state machine how to route the request.

## Dependencies
- `langchain_core.prompts`: Used to inject `qualifier_prompt.py`.
- `agent.state.QueryClassification`: The strictly-enforced Pydantic output schema.

## Function Breakdown

### `qualifier_node(state: AgentState) -> dict`
- **Inputs**: The user's raw `query`.
- **Outputs**: A dictionary containing `is_scenario`, `law_domain`, `requires_case_law`, and most importantly, `is_general_chat`.
- **Logic**:
  1. Initializes the `Nemotron` LLM with `with_structured_output(QueryClassification)`. This fundamentally alters the LLM from a text-generator into a strict JSON-classifier.
  2. Injects the query into the Prompt Template.
  3. Executes the chain.
  4. Parses the JSON. If the LLM flagged `is_general_chat = True` (because the user said something like "Hi" or "How are you?"), it logs a "Conversational intent detected" warning. 
  5. Returns the parsed flags to the `AgentState`, where the `chat_graph.py` conditional router uses them to instantly bypass retrieval if it's just a greeting.
