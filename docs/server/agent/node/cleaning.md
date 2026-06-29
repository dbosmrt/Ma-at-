# `cleaning.py`

## Module Overview
A utility node used during the data ingestion phase. Its purpose is to scrub dirty OCR data or weird formatting from the raw legal texts before they are chunked and embedded.

## Role in Pipeline
Used exclusively during the database ingestion phase, directly before `chunking.py`.

## Function Breakdown

### `clean_text(text: str) -> str`
- **Inputs**: A raw, dirty string.
- **Outputs**: A sanitized string.
- **Logic**:
  - Employs heavy `re` (regex) processing.
  - Strips out consecutive blank lines (`\n\n\n+`).
  - Removes trailing whitespace.
  - Fixes common OCR artifacts found in Indian government PDFs (like broken bullet points or weird spacing around section numbers).

### `cleaning_node(state: AgentState) -> dict`
- **Role**: Reads raw files from disk, runs them through the `clean_text` regex engine, and writes the scrubbed files to an `ingest_output_dir`. Passes this new directory path into the state for the chunker to use.
