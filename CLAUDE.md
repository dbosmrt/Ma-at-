# Project: Legal RAG Bot & Form Generator (24-Hour Hackathon MVP)

## 1. THE "WHY" ENCODING (INTENT & VALUES)

Core Value: Demo Survival. We have 24 hours. A simple, working MVP is infinitely more valuable than a complex, broken app.

Architecture Intent: Stability > Features. We use a strict Template-Based RAG approach. The AI extracts JSON; the backend injects it into hardcoded HTML/Markdown templates.

Domain Constraint: Absolute strict adherence to provided legal context. Zero legal hallucination is permitted.

## 2. HARD RULES VS. PREFERENCES

$$BINARY BOUNDARIES: YOU MUST DO THIS$$

API Contract: Frontend (React) and Backend (FastAPI) MUST communicate exclusively via REST endpoints.

RAG Outputs: LLM extractions for form generation MUST use response_format={ "type": "json_object" } or LangChain structured output.

Context Isolation: If a legal query cannot be answered by the vector DB context, you MUST output: "I do not have enough information to answer this based on the provided documents."

Strict Typing: Python code MUST use explicit Type Hints (def process(query: str) -> dict:). FastAPI MUST use Pydantic models for request/response validation.

Python Coding Standards (PEP 8 & Pylint):

PEP 8 Compliance: All backend Python code MUST strictly adhere to the PEP 8 style guide.

Pylint Enforcement: Write code that yields a 10/10 Pylint score.

Naming Conventions: You MUST use snake_case for variables/functions, and PascalCase for classes.

Error Handling: You MUST use try-except blocks around all OpenAI API calls and ChromaDB queries. Return proper HTTP 500 status codes from FastAPI if the LLM fails.

$$ GUIDEPOSTS: YOU SHOULD PREFER THIS$$

UI Simplicity: Prefer standard React useState and basic CSS over complex state managers (no Redux) or heavy component libraries.

Speed: Prefer simple, readable loops and standard library functions over clever, heavily abstracted class hierarchies.

Error Handling: Prefer returning clean HTTP 500/400 errors from FastAPI with human-readable messages so the frontend can degrade gracefully.

## 3. ANTI-PATTERNS (THE "NEVER" LIST)

NEVER hallucinate Python libraries or Node packages. If it is not in requirements.txt or package.json, ask before using pip install or npm install.

NEVER write legal contracts from scratch via LLM text generation. (This breaks formatting and introduces risk).

NEVER rewrite working legacy code or refactor whole files unless explicitly instructed to do so. ONLY modify the lines necessary for the requested feature.

NEVER hardcode API keys (OPENAI_API_KEY). Always use os.environ.get() or a .env file.

NEVER leave raw // TODO: or # TODO: comments in generated code. Implement the fix or ask the user for clarification.

NEVER break the API schema. If you change a Pydantic model in FastAPI, you MUST update the corresponding TypeScript interface in React.

NEVER bypass Pylint rules. Avoid writing code that requires disabling Pylint warnings via # pylint: disable= unless absolutely unavoidable (e.g., framework-specific quirks).

## 4. PROGRESSIVE DISCLOSURE & POINTERS

This file contains top-level architectural rules. For specific subsystem contexts, check the following locations before modifying code:

Frontend specific rules: Check frontend/README.md (if it exists).

Backend specific rules: Check backend/README.md (if it exists).

Template Schema: Always read the placeholder variables in templates/*.html before modifying the JSON extraction prompt in llm_service.py.

## 5. INTENT-BASED VERIFICATION ROUTINE

Before presenting final code or confirming a task is complete, you MUST execute this self-correction loop:

Linting Check: Does the Python code pass PEP 8? (Mentally verify against Pylint standards or run pylint target_file.py). Ensure 10/10 score.

Type Check: Do the FastAPI endpoint Pydantic schemas perfectly match the React frontend fetch payloads?

CORS Check: If adding a new API endpoint, is it covered by the CORS middleware in main.py?

State Check: If modifying React state, verify it does not cause an infinite render loop in a useEffect.

## 6. TECH STACK & COMMANDS

Frontend: React, TypeScript, HTML/CSS (Vite) -> cd frontend && npm run dev

Backend: FastAPI (Python 3.11+) -> cd backend && uvicorn main:app --reload

AI/DB Stack: OpenAI API (gpt-4o-mini), LangChain, ChromaDB

PDF Gen: reportlab or pdfkit

Linting: Pylint -> cd backend && pylint main.py llm_service.py rag_engine.py

## 7. DIRECTORY STRUCTURE

/
├── frontend/                   # React/TypeScript application
│   ├── package.json
│   └── src/App.tsx             # Main chat interface and layout
├── backend/                    # Python API and AI logic
│   ├── main.py                 # FastAPI entry point & API routes
│   ├── requirements.txt        
│   ├── .pylintrc               
│   ├── llm_service.py          # OpenAI API calls and JSON extraction
│   ├── rag_engine.py           # LangChain setup and ChromaDB retrieval
│   └── ingest.py               # Script to chunk and embed raw PDFs
├── templates/                  # Hardcoded templates with {{VARIABLES}}
├── data/                       # Raw legal PDFs for the RAG knowledge base
└── vector_store/               # Locally persisted ChromaDB files
