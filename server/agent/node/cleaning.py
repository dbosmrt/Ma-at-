"""
Markdown Cleaning Node for Legal RAG Chatbot.

This module provides a LangGraph node that cleans the raw Markdown 
produced by the ingestion step. It removes garbage non-ASCII text 
(like incorrect Hindi font renderings), demotes false headers like 
'## Illustration', and promotes true legal sections to ensure perfect 
chunk boundaries.
"""

import logging
import re
from pathlib import Path

from agent.state import AgentState

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_markdown_text(text: str) -> str:
    """
    Cleans the raw markdown text generated from Indian Legal PDFs.
    
    Args:
        text (str): The raw markdown content.
        
    Returns:
        str: The cleaned and structurally corrected markdown.
    """
    # 1. Remove non-ASCII garbage (e.g., garbled Hindi fonts)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # 2. Upgrade CHAPTER to main heading (#) to establish hierarchy over Sections (##)
    text = re.sub(r'^##\s*(CHAPTER\s+[A-Z0-9]+)', r'# \1', text, flags=re.MULTILINE | re.IGNORECASE)
    
    # 3. Demote Illustrations and Explanations so they don't break chunking
    # e.g. "## Illustration." -> "**Illustration.**"
    text = re.sub(
        r'^##\s*(Illustration[s]?\.?|Explanation[s]?\.?)', 
        r'**\1**', 
        text, 
        flags=re.MULTILINE | re.IGNORECASE
    )
    
    # 4. Promote section numbers to proper markdown headers (##)
    # e.g., "1. (1) This Act..." -> "## Section 1.\n\n(1) This Act..."
    # Matches lines starting with 1 to 4 digits followed by a period and a space
    text = re.sub(r'^(\d{1,4})\.\s', r'## Section \1.\n\n', text, flags=re.MULTILINE)
    
    # 5. Remove page ending slashes (e.g. ////) or underscores (____) that unstructured might leave
    text = re.sub(r'/{4,}', '', text)
    text = re.sub(r'_{4,}', '', text)
    text = re.sub(r'(?:\\_){4,}', '', text)
    
    # 6. Remove excessive newlines that might cause empty chunks
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text


def cleaning_node(state: AgentState) -> dict:
    """
    LangGraph node to clean Markdown files before chunking.
    Reads .md files from ingest_output_dir, cleans them, and overwrites them.
    """
    md_dir = state.get("ingest_output_dir", "")
    
    if not md_dir:
        logger.error("cleaning_node failed: ingest_output_dir not found.")
        return {"ingest_status": "Failed: Missing markdown directory in state"}
        
    md_path = Path(md_dir)
    if not md_path.exists() or not md_path.is_dir():
        logger.error("Markdown directory not found: %s", md_dir)
        return {"ingest_status": "Failed: Invalid markdown directory"}
        
    md_files = list(md_path.glob("*.md"))
    if not md_files:
        logger.warning("No .md files found in %s", md_dir)
        return {"ingest_status": "Cleaning Completed (No files)"}
        
    for md_file in md_files:
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            cleaned_content = clean_markdown_text(content)
            
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(cleaned_content)
                
            logger.info("Cleaned and formatted: %s", md_file.name)
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Failed to clean file %s: %s", md_file.name, e)
            
    return {"ingest_status": "Cleaning Completed Successfully"}
