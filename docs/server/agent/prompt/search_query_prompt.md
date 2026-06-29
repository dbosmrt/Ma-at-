# `search_query_prompt.py`

## Module Overview
Contains the System Prompt for the `web_search` node's summarizer agent.

## Key Logic / Rules
- Uses **Few-Shot Prompting** to teach the LLM how to compress a 200-word narrative into two or three highly focused, 10-word DuckDuckGo search strings.
- Enforces the inclusion of Indian legal terminology (BNS, IPC, India) in the search strings to ensure the DuckDuckGo results are localized to the Indian penal system.
