from langchain_core.prompts import ChatPromptTemplate

REWRITER_SYSTEM_PROMPT = """You are an expert legal query re-writer. 
The user's original query did not retrieve relevant legal statutes from the database.
Your job is to rewrite the query to make it highly optimized for semantic vector search.
Focus on extracting core legal concepts, stripping conversational filler, and using synonyms if the original terms might not exactly match legal texts.

Return ONLY the rewritten query string. Do NOT add any conversational text or quotes around the output.
"""

def get_rewriter_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", REWRITER_SYSTEM_PROMPT),
        ("user", "Original query: {query}")
    ])
