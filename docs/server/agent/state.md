# `state.py`

## Module Overview
Defines the `AgentState` schema and all nested Pydantic models used by the LLMs for structured output. Because LangGraph nodes are stateless Python functions, this module defines the exact "memory payload" that is passed from node to node during execution.

## Dependencies
- `typing.TypedDict, Annotated`: Used to define the overall state dictionary that LangGraph expects.
- `pydantic.BaseModel, Field`: Used to define strict, highly-annotated JSON schemas that are enforced on the LLMs via `with_structured_output`.

## Pydantic Models (LLM Output Schemas)

### 1. `QueryClassification`
- **Role**: The schema the Qualifier node is forced to return.
- **Fields**:
  - `law_domain`: Categorizes the query (e.g., Criminal, Civil).
  - `is_scenario`: Flags if the query is a hypothetical story (used to adjust retrieval strategy).
  - `requires_case_law`: Flags if the user explicitly demanded past judgments or Supreme Court rulings.
  - `is_general_chat`: Crucial flag for detecting greetings or non-legal conversational input to trigger the graph bypass.

### 2. `DocumentRanking`
- **Role**: The schema the Reranker node is forced to return.
- **Fields**:
  - `relevant_indices`: A list of integers (e.g., `[0, 2, 5]`) representing the index positions of chunks that actually contain the answer, filtering out the noise.

### 3. `DocumentGrade`
- **Role**: The schema the Grader node is forced to return.
- **Fields**:
  - `is_relevant`: Boolean indicating if the final context is sufficient.
  - `context_relevance_score`: A strict float (0.0 to 1.0) assessing chunk quality. Used for automated health warnings.
  - `chunk_diversity`: A string assessment to ensure the retriever isn't pulling only from one document.

### 4. `SearchQueries`
- **Role**: The schema the Query Decomposer and Web Search Summarizer nodes use to output arrays of concise strings.

### 5. `DecomposedQuery`
- **Role**: Output of the Pre-retrieval Decomposer.
- **Fields**: `semantic_focus`, `statutory_focus`, `procedural_focus`. Isolates different aspects of a complex prompt so the Hybrid Retriever can target them individually.

## The Core `AgentState`
```python
class AgentState(TypedDict):
    ...
```
- **Role**: The master dictionary passed sequentially through every node. 
- **Key Flow**:
  - Starts with just `query` and `session_id`.
  - Qualifier fills in `is_general_chat` and `requires_case_law`.
  - Decomposer fills in `decomposed_query`.
  - Retriever pulls chunks and populates `documents` (List of strings).
  - Web Search (if triggered) populates `case_laws`.
  - Generator reads `documents` and `case_laws` to populate `generation`.
