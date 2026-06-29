import os
import logging
from langgraph.graph import StateGraph, START, END

from agent.state import AgentState
from agent.node.ingestion import ingestion_node
from agent.node.cleaning import cleaning_node
from agent.node.chunking import chunking_node
from agent.node.embedding import embedding_node

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def build_ingestion_graph():
    """
    Builds and compiles the complete LangGraph workflow for document ingestion.
    Workflow: Ingest (PDF->MD) -> Clean (Format Fixes) -> Chunk (Headers) -> Embed (VectorStore)
    """
    # Initialize the graph with our state schema
    workflow = StateGraph(AgentState)
    
    # Add all nodes to the graph
    workflow.add_node("ingest", ingestion_node)
    workflow.add_node("clean", cleaning_node)
    workflow.add_node("chunk", chunking_node)
    workflow.add_node("embed", embedding_node)
    
    # Define the execution sequence
    workflow.add_edge(START, "ingest")
    workflow.add_edge("ingest", "clean")
    workflow.add_edge("clean", "chunk")
    workflow.add_edge("chunk", "embed")
    workflow.add_edge("embed", END)
    
    # Compile the graph
    app = workflow.compile()
    return app


if __name__ == "__main__":
    # Test execution of the graph
    # 1. Define the initial state pointing to the legal PDFs
    initial_state = AgentState(
        pdf_dir="data",
        ingest_output_dir="data/markdown",
        chunk_output_dir="data/chunks",
        db_dir="data/chroma_db",
        messages=[]
    )
    
    logger.info("Initializing Legal RAG Ingestion Pipeline with Cleaning Node...")
    
    # 2. Compile and run the workflow
    graph = build_ingestion_graph()
    
    # 3. Stream the execution to observe state changes
    for output in graph.stream(initial_state):
        for key, value in output.items():
            logger.info("Node '%s' output: %s", key, value)
            
    logger.info("Ingestion Pipeline completed successfully!")
