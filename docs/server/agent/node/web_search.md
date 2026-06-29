# `web_search.py`

## Module Overview
A dynamic fallback node that scrapes the live internet using the DuckDuckGo API.

## Role in Pipeline
Triggered only if the user explicitly demands case law, or if the `grader` determines the local database failed to find the answer.

## Dependencies
- `duckduckgo_search.DDGS`: The core scraping library.

## Function Breakdown

### `_summarize_query(query: str) -> list[str]`
- **Logic**: DuckDuckGo will crash if you pass it a 200-word narrative query. If the query exceeds `120` characters, this function spins up an LLM agent to summarize the narrative into 2-3 highly concise search strings (e.g., `"BNS sections housebreaking night"`).

### `web_search_node(state: AgentState) -> dict`
- **Inputs**: `query`, `requires_case_law`.
- **Outputs**: Populates the `case_laws` array in the state.
- **Logic**:
  1. Checks query length and optionally summarizes it.
  2. Iterates through the search strings and hits `DDGS().text(sq, region='in-en', max_results=3)`.
  3. Deduplicates identical URLs across multiple searches.
  4. Formats the results with `[External Source: {title}] ({link})` and appends the raw body text.
  5. Injects the list into `case_laws` for the Generator to read.
