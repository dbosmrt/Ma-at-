# `reranker.py`

## Module Overview
Acts as a strict garbage collector immediately following the `retriever.py` node. Because the Retriever pulls 20 chunks (which is a massive amount of text), the Reranker strips out the irrelevant noise to prevent the final generator from hallucinating or running out of context space.

## Function Breakdown

### `reranker_node(state: AgentState) -> dict`
- **Inputs**: The 20 raw `documents` retrieved from ChromaDB.
- **Outputs**: A highly filtered list of `documents`.
- **Logic**:
  - Uses `with_structured_output(DocumentRanking)`.
  - Feeds all 20 documents (with their array indices) to the Nemotron LLM.
  - The LLM reads the query and the documents, and outputs a JSON array of the indices that actually contain the answer (e.g., `[0, 5, 12]`).
  - The node loops through that JSON array, plucks exactly those chunks out of the raw list, and overwrites the `documents` state variable with just the curated text.
  - *Note: The prompt contains strict instructions forbidding the LLM from hallucinating or guessing indices.*
