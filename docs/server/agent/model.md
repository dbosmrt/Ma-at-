# `model.py`

## Module Overview
Acts as the centralized repository for initializing external Large Language Model (LLM) and Embedding API endpoints. 

## Role in Pipeline
By centralizing model definitions here, we prevent API keys and model names from being hardcoded randomly across 15 different node files. Any node that needs to perform AI generation or embedding simply imports a getter function from this file. If we ever want to switch from NVIDIA NIM to OpenAI or Anthropic, we only have to change the code in this one file.

## Dependencies
- `langchain_nvidia_ai_endpoints`: The core LangChain integration package used to communicate with NVIDIA's NIM endpoints.
- `os`: Used to load `NVIDIA_API_KEY` from the environment.

## Class Breakdown

### 1. `ChatModels`
A namespace class grouping generative LLM initializations.

#### `get_nemotron3super()`
- **Output**: Returns a `ChatNVIDIA` LangChain instance tied to the `meta/llama-3.1-70b-instruct` model.
- **Logic**: This is the primary workhorse model used by almost every analytical node (Qualifier, Grader, Reranker, Generator) because of its exceptional reasoning and strict adherence to JSON output structures. Temperature is hardcoded to `0` to enforce highly deterministic, reproducible outputs, which is critical for RAG accuracy.

### 2. `EmbeddingModels`
A namespace class grouping vectorization models.

#### `get_nv_embedqa_e5_v5()`
- **Output**: Returns an `NVIDIAEmbeddings` instance tied to `nvidia/nv-embedqa-e5-v5`.
- **Logic**: This model translates text into mathematical vectors for ChromaDB. It is the primary embedding model used across the system because it is specifically optimized for Question & Answer retrieval.

#### `get_embed_with_fallback()`
- **Output**: Returns an `NVIDIAEmbeddings` instance.
- **Logic**: Implements a robust fallback hierarchy. If the primary `nv-embedqa-e5-v5` model is offline or experiencing server load, the code automatically falls back to `mistralai/mistral-7b-v0.1` or `BAAI/bge-m3`. This ensures the retrieval pipeline remains highly resilient during API outages.
