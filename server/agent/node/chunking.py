"""
Markdown Chunking Module for Legal RAG Chatbot.

This module provides functionality to chunk large Markdown files 
using a header-based splitting strategy. Legal documents are often 
structured with sections and headers, making this approach ideal for 
preserving semantic context.
"""

import logging
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from agent.state import AgentState

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def chunk_markdown_file(file_path: str) -> List[Document]:
    """
    Reads a Markdown file and chunks it based on headers.
    
    Args:
        file_path (str): The absolute path to the .md file.
        
    Returns:
        List[Document]: A list of LangChain Document objects representing the chunks.
    """
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        logger.error("Markdown file not found: %s", file_path)
        return []
        
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except IOError as e:
        logger.error("Failed to read file %s: %s", file_path, e)
        return []

    # Define headers to split on. Legal docs often use ## for sections.
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
        ("#####", "Header 5"),
        ("######", "Header 6"),
    ]
    
    # Initialize the header text splitter
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False
    )
    
    # Split the document by headers
    header_splits = markdown_splitter.split_text(content)
    
    # Secondary split: If some sections are still too large (e.g., > 1000 chars), 
    # we do a recursive character split to ensure they fit in the embedding model.
    # The llama-nemotron-embed model handles up to 512 tokens natively, so ~1500 chars is safe.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500, 
        chunk_overlap=400
    )
    
    final_chunks = text_splitter.split_documents(header_splits)
    
    # Add metadata about the source file and hierarchy
    for chunk in final_chunks:
        doc_name = path.stem
        chunk.metadata["source"] = path.name
        chunk.metadata["document"] = doc_name
        
        # Build hierarchical context string (e.g., "BNS - CHAPTER 1 - Section 1")
        hierarchy = [doc_name]
        for i in range(1, 7):
            header_key = f"Header {i}"
            if header_key in chunk.metadata:
                hierarchy.append(chunk.metadata[header_key].strip())
                
        chunk.metadata["context_path"] = " - ".join(hierarchy)
        
    logger.info("Chunked %s into %d pieces.", path.name, len(final_chunks))
    return final_chunks


def chunking_node(state: AgentState) -> dict:
    """
    LangGraph node to handle Markdown chunking.
    It reads the output directory from the state (which contains .md files),
    chunks them, and updates the state.
    """
    md_dir = state.get("ingest_output_dir", "")
    
    if not md_dir:
        logger.error("chunking_node failed: ingest_output_dir not found in state.")
        return {"ingest_status": "Failed: Missing markdown directory in state"}
        
    md_path = Path(md_dir)
    if not md_path.exists() or not md_path.is_dir():
        logger.error("Markdown directory not found: %s", md_dir)
        return {"ingest_status": "Failed: Invalid markdown directory"}
        
    md_files = list(md_path.glob("*.md"))
    if not md_files:
        logger.warning("No .md files found in %s", md_dir)
        return {"ingest_status": "Completed (No files to chunk)"}
        
    all_chunks = []
    for md_file in md_files:
        chunks = chunk_markdown_file(str(md_file))
        all_chunks.extend(chunks)
        
    logger.info("Total chunks created across all files: %d", len(all_chunks))
    
    # Returning the Document objects to the state so they can be embedded with metadata
    return {
        "documents": all_chunks,
        "ingest_status": "Chunking Completed"
    }
