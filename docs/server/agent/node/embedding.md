# `embedding.py`

## Module Overview
Handles the core Vector Database (ChromaDB) connection and the translation of raw text chunks into mathematical vectors (Embeddings).

## Role in Pipeline
During ingestion (`re_embed_all.py`), this script takes the LangChain Documents produced by the chunker and uploads them to the database. During live inference, this script is used by the `retriever.py` node to get the active database connection.

## Dependencies
- `langchain_chroma.Chroma`: The Python client for the local Chroma vector store.
- `agent.model.EmbeddingModels`: Used to get the NVIDIA NIM embedding models.

## Function Breakdown

### `get_vector_store(embeddings=None) -> Chroma`
- **Role**: A singleton-pattern getter for the database.
- **Logic**: If no embedding model is passed in, it defaults to the primary `get_nv_embedqa_e5_v5()`. It explicitly points to the local `data/chroma_db` directory on disk. If the database doesn't exist, Chroma automatically creates it.

### `embedding_node(state: AgentState) -> dict`
- **Inputs**: Expects `documents` (List[Document]) in the `AgentState`.
- **Logic (The Batching Problem)**:
  - If we try to feed 5000 chunks into the NVIDIA API at once, the remote CUDA server will throw an `Out of Memory (OOM)` exception and crash.
  - This function implements strict **batching**. It slices the massive array of documents into tiny arrays of `16` chunks each.
  - It loops through these small batches, calling `vectorstore.add_documents()` on each one, pausing slightly to prevent API rate limiting, and gracefully catching any server-side Triton errors.
