# `chat_graph.py`

## Module Overview
This file is the architectural blueprint of the AI system. It uses `langgraph` to construct a State Machine (a Directed Acyclic Graph) that dictates the precise execution order and conditional routing logic for every analytical node in the RAG pipeline.

## Dependencies
- `langgraph.graph.StateGraph`: The core object used to define nodes and edges.
- `agent.state.AgentState`: The TypedDict data schema that holds the variables passed between nodes.
- **Nodes**: Imports all functional nodes from the `agent.node.*` directory (Decomposer, Qualifier, Retriever, Reranker, Grader, Web Search, Generator).

## Function Breakdown

### `build_chat_graph()`
The sole function in this file. It instantiates, wires, and compiles the graph.

#### 1. Node Registration
```python
workflow.add_node("query_decomposer", query_decomposer_node)
...
```
Maps internal string identifiers (e.g., `"query_decomposer"`) to the actual Python functions imported from the node files.

#### 2. Conditional Routing Logic
The graph possesses two critical "decision points" (Conditional Edges):

**A. `qualifier_conditional(state: AgentState) -> str`**
- **Trigger**: Occurs immediately after the Qualifier analyzes the user's raw query.
- **Logic**: If the Qualifier flagged the query as `is_general_chat = True` (e.g., the user said "hi" or asked a broad conversational question), this function returns `"generator"`.
- **Impact**: This instantly bypasses the Retriever, Reranker, and Grader nodes. By skipping the Vector Database entirely for non-legal queries, it drastically cuts API token costs, lowers response latency, and prevents the AI from hallucinating laws trying to justify a greeting.

**B. `grader_conditional(state: AgentState) -> str`**
- **Trigger**: Occurs after the Grader evaluates the retrieved documents from the vector database.
- **Logic**: If the Grader determines the retrieved documents are irrelevant or missing the answer, it sets `search_required = True`. This function reads that flag and returns `"web_search"`. Otherwise, it proceeds to `"generator"`.
- **Impact**: Enables a resilient fallback mechanism. If local statutes fail, the agent autonomously scrapes the live internet for case law before attempting to answer.

#### 3. Edge Wiring & Compilation
```python
workflow.add_edge(START, "query_decomposer")
workflow.add_edge("query_decomposer", "qualifier")
workflow.add_conditional_edges("qualifier", qualifier_conditional, ...)
```
Connects the registered nodes using static and conditional edges, explicitly defining the flow of data. Finally, `workflow.compile()` seals the graph for execution.
