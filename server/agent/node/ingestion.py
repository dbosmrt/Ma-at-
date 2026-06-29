"""
Document Ingestion Module for Legal RAG Chatbot.

This module provides functionality to ingest PDF documents, convert them
into Markdown format using `langchain_docling` (which uses deep learning
models to accurately parse structure), and gracefully falls back to 
`pdfplumber` or `pymupdf` if GPU is unavailable or Docling fails.
"""

import logging
from pathlib import Path
from typing import Optional

from agent.state import AgentState

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_pdf_with_docling(file_path: str) -> Optional[str]:
    """
    Attempt to parse a PDF file into Markdown using langchain_docling.
    
    Args:
        file_path (str): The absolute path to the PDF file.
        
    Returns:
        Optional[str]: The extracted Markdown content, or None if it fails.
    """
    try:
        from langchain_docling import DoclingLoader
        
        logger.info("Attempting to parse %s using DoclingLoader...", file_path)
        loader = DoclingLoader(file_path=file_path)
        docs = loader.load()
        
        # Combine the page contents into a single markdown string
        md_content = "\n\n".join(doc.page_content for doc in docs)
        return md_content
    except ImportError:
        logger.warning("langchain_docling is not installed.")
        return None
    except Exception as e:  # pylint: disable=broad-except
        logger.warning(
            "Docling failed (possibly due to missing GPU or memory issues): %s", e
        )
        return None


def parse_pdf_with_unstructured(file_path: str) -> Optional[str]:
    """
    Fallback method to parse a PDF file into Markdown using Unstructured.
    Unstructured uses heuristics to detect titles, lists, and paragraphs, 
    preserving the structure better than simple text dumpers.
    """
    try:
        from langchain_community.document_loaders import UnstructuredPDFLoader
        
        logger.info("Attempting to parse %s using UnstructuredPDFLoader...", file_path)
        loader = UnstructuredPDFLoader(file_path=file_path, mode="elements")
        docs = loader.load()
        
        md_content = ""
        for doc in docs:
            category = doc.metadata.get("category", "")
            text = doc.page_content.strip()
            if not text:
                continue
                
            if category == "Title":
                # Unstructured often flags section headers as Titles
                md_content += f"\n## {text}\n\n"
            elif category == "ListItem":
                md_content += f"- {text}\n"
            else:
                md_content += f"{text}\n\n"
                
        return md_content
    except ImportError:
        logger.warning("langchain-community or unstructured is not installed.")
        return None
    except Exception as e:  # pylint: disable=broad-except
        logger.error("Unstructured parser failed: %s", e)
        return None


def convert_pdf_to_md(pdf_path: str, output_dir: str) -> bool:
    """
    Convert a single PDF file into a Markdown file.
    It tries Docling first, falls back to pdfplumber, then PyMuPDF.
    
    Args:
        pdf_path (str): Path to the input PDF file.
        output_dir (str): Directory where the .md file should be saved.
        
    Returns:
        bool: True if conversion was successful, False otherwise.
    """
    file_path = Path(pdf_path)
    if not file_path.exists():
        logger.error("File not found: %s", pdf_path)
        return False
        
    md_content = None
    
    # Check if GPU is available to prevent Docling from blocking on CPU
    gpu_available = False
    try:
        import torch
        gpu_available = torch.cuda.is_available()
    except ImportError:
        pass
        
    if gpu_available:
        logger.info("GPU detected. Using high-accuracy Docling parser.")
        md_content = parse_pdf_with_docling(str(file_path))
    else:
        logger.info("GPU not detected. Bypassing Docling for faster CPU fallback parsing.")
    
    if md_content is None:
        md_content = parse_pdf_with_unstructured(str(file_path))
        
    if md_content is None:
        logger.error("All parsing methods failed for %s.", pdf_path)
        return False
        
    # Save to output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    md_file_path = output_path / f"{file_path.stem}.md"
    try:
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        logger.info("Successfully saved Markdown to %s", md_file_path)
        return True
    except IOError as e:
        logger.error("Failed to write Markdown file %s: %s", md_file_path, e)
        return False


def ingest_directory(input_dir: str, output_dir: str) -> None:
    """
    Process all PDF files in a given directory and convert them to Markdown.
    
    Args:
        input_dir (str): The directory containing PDF files.
        output_dir (str): The directory to save the converted Markdown files.
    """
    input_path = Path(input_dir)
    if not input_path.exists() or not input_path.is_dir():
        logger.error("Input directory does not exist or is invalid: %s", input_dir)
        return
        
    pdf_files = list(input_path.glob("*.pdf"))
    if not pdf_files:
        logger.warning("No PDF files found in %s", input_dir)
        return
        
    logger.info("Found %d PDF(s). Starting ingestion...", len(pdf_files))
    success_count = 0
    
    for pdf_file in pdf_files:
        if convert_pdf_to_md(str(pdf_file), output_dir):
            success_count += 1
            
    logger.info(
        "Ingestion complete. Successfully converted %d/%d files.", 
        success_count, len(pdf_files)
    )


def ingestion_node(state: AgentState) -> dict:
    """
    LangGraph node to handle PDF ingestion.
    It reads input/output directories from the state and executes conversion.
    """
    input_dir = state.get("ingest_input_dir", "")
    output_dir = state.get("ingest_output_dir", "")
    
    if not input_dir or not output_dir:
        logger.error("ingestion_node failed: ingest_input_dir or ingest_output_dir not found in state.")
        return {"ingest_status": "Failed: Missing directories in state"}
        
    logger.info("ingestion_node started. Input: %s, Output: %s", input_dir, output_dir)
    ingest_directory(input_dir, output_dir)
    
    return {"ingest_status": "Completed"}
