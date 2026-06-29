# `chunking.py`

## Module Overview
Responsible for parsing raw Markdown legal files (like `BNS.md` or `BSA.md`) and physically chopping them up into smaller pieces (chunks) so they can be ingested by the Vector Database.

## Role in Pipeline
This file is NOT used during live chat inference. It is used exclusively by the backend data ingestion script (`re_embed_all.py`) to prepare the database before the server ever starts.

## Dependencies
- `langchain_text_splitters`: Used for `MarkdownHeaderTextSplitter` and `RecursiveCharacterTextSplitter`.

## Function Breakdown

### `chunk_markdown_file(file_path: str) -> List[Document]`
- **Inputs**: The absolute path to a Markdown file on disk.
- **Outputs**: An array of LangChain `Document` objects.
- **Logic**:
  1. **Header Splitting**: Uses `MarkdownHeaderTextSplitter` to chop the document every time it sees a markdown header (e.g., `#`, `##`). Because Indian legal statutes are structured strictly by `CHAPTER` and `Section`, this ensures a single legal statute isn't accidentally split down the middle.
  2. **Size Enforcement**: Some legal sections (like definitions) are incredibly long. A secondary `RecursiveCharacterTextSplitter` ensures no chunk exceeds `2500` characters, preventing the embedding model from choking.
  3. **Metadata Hierarchy**: (CRITICAL STEP) It iterates through the detected headers and builds a hierarchical string: `context_path = "BNS - CHAPTER 1 - Section 63"`. It attaches this to the chunk's metadata, ensuring the downstream Retriever knows exactly where a piece of text came from.

### `chunking_node(state: AgentState) -> dict`
- **Role**: A LangGraph wrapper around the core chunking logic. Reads the `ingest_output_dir` from the agent state, iterates through all `.md` files in that directory, and outputs the final massive list of `documents` back into the state for the `embedding.py` node to consume.
