import asyncio
from agent.chat_graph import build_chat_graph
from agent.state import AgentState
from langchain_core.messages import HumanMessage

app = build_chat_graph()
state = AgentState(
    query="Nirbhaya Case Punishment",
    session_id="test",
    chat_history=[],
    memory_summary="",
    is_scenario=False,
    requires_case_law=False,
    search_required=False,
    documents=[],
    case_laws=[],
    generation="",
    iteration_count=0
)

result = app.invoke(state)
print("\n--- RESULTS ---")
print("Search Required:", result.get("search_required"))
print("Case Laws Found:", len(result.get("case_laws", [])))
print("Generation:", result.get("generation"))
