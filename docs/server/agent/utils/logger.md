# `logger.py`

## Module Overview
A centralized utility for structured application logging. It intercepts system events and writes them to standard output and dedicated file handlers.

## Role in Pipeline
Imported by nearly every file in the project to maintain a clean, traceable execution trail.

## Function Breakdown

### `setup_logger(name: str)`
- **Logic**: Configures the standard Python `logging` module to output timestamps, log levels, and module names. It guarantees all logs are written to both the terminal (for local development) and to a persistent file (e.g., `logs/app.log`) for production debugging.

### `log_node_event(node_name: str, status: str, error_payload=None)`
- **Logic**: Specialized hook for LangGraph nodes. Every time a node starts, succeeds, or fails, it calls this function to print a highly visible status update in the terminal.

### `log_retrieval_warning(score: float, query: str)`
- **Logic**: Called by `grader.py`. If the context relevance score drops below `0.4`, it writes the exact query and the failing score to `logs/retrieval_health_warnings.log`. This allows maintainers to see exactly what legal queries the database is failing to answer.
