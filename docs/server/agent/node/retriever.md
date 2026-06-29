# `retriever.py`

## Module Overview
The most mechanically complex node in the pipeline. It is responsible for executing the Hybrid Search (Dense Vectors + Sparse BM25 Keywords) against ChromaDB to pull the relevant legal statutes based on the user's query.

## Role in Pipeline
Executes directly after the `qualifier` (unless bypassed by conversational chat). Its output is the raw list of `documents` passed into the AgentState.

## Function Breakdown

### `reciprocal_rank_fusion(results_lists, k=60)`
- **Inputs**: A list of lists of LangChain Documents (e.g., `[dense_docs, sparse_docs]`).
- **Outputs**: A single, mathematically merged list of Documents.
- **Logic**: This is a custom Native RRF implementation. Dense search (semantic meaning) and BM25 (exact keyword matching) output completely different scoring scales. This function ignores the raw scores and instead scores chunks based on their *rank position* in both lists, fusing them together to ensure that chunks which scored highly in *both* keyword and semantic search float to the absolute top.

### `_get_bm25_retriever(vectorstore)`
- **Logic**: Reads the entire ChromaDB index into RAM at startup to build the BM25 statistical matrix. 
- **CRITICAL METADATA FIX**: Because BM25 only tokenizes raw `page_content`, it fails to find acronyms like "BNS" if they only exist in the chunk's metadata. This function dynamically iterates through the database, extracts the `context_path` metadata, and forcefuly prepends it to the `page_content` before building the BM25 index. This guarantees exact-match keyword isolation.

### `retriever_node(state: AgentState) -> dict`
- **Logic**:
  1. Compiles a `hybrid_query` using the outputs from the `query_decomposer`.
  2. Executes parallel queries on the Dense Retriever and Sparse Retriever.
  3. Uses `k=20` to guarantee a deep search sweep (pulling 20 documents instead of the default 4) to ensure hidden definitions aren't missed.
  4. Pushes both lists through `reciprocal_rank_fusion`.
  5. **Exponential Backoff**: Wraps the entire primary embedding call in a try/catch block with 5 exponential retries. If the primary NVIDIA API fails completely, it gracefully switches to a local/fallback embedding model and runs the retrieval again.
