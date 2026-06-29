from langchain_core.prompts import ChatPromptTemplate

DECOMPOSER_SYSTEM_PROMPT = """You are an expert legal query analyzer and pre-processor.
Your task is to break down the user's raw narrative query into three optimized search strings for a hybrid RAG retrieval engine.

CRITICAL RULES:
- Return a raw JSON object only. Do NOT include markdown blocks (like ```json).
- Extract the core concepts into `semantic_focus` (e.g., "group robbery armed break-in at night").
- Extract explicit legal identifiers into `statutory_focus` (e.g., "BNS 310 312 section" or "Contract Act Section 12"). If none exist, leave it empty. Do NOT hallucinate sections.
- Extract procedural terms into `procedural_focus` (e.g., "electronic registration FIR evidence certification").
- Classify the inferred domain as either "criminal", "civil", or "family".

{format_instructions}"""

def get_query_decomposer_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", DECOMPOSER_SYSTEM_PROMPT),
        ("user", "{query}")
    ])
