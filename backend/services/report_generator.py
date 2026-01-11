# def generate_report(docs: list[str], query: str) -> str:
#     """
#     Dummy report generator (for testing).
#     Instead of calling an LLM, it just formats the docs into a string.
#     """
#     if not docs:
#         return f"No relevant documents found for query: {query}"

#     report = f"=== Dummy Report for Query: {query} ===\n\n"
#     for i, doc in enumerate(docs, 1):
#         report += f"[Doc {i}]\n{doc[:300]}...\n\n"  # truncate to 300 chars
#     report += "=== End of Report ==="
#     return report




from langGraph_app.core.llm import get_gemini_llm

def generate_report(docs, query: str) -> str:
    """Generate a report using Gemini LLM."""
    llm = get_gemini_llm()
    
    # Build a context string from docs
    context = "\n\n".join(docs)

    prompt = f"""
    You are an AI assistant generating a competitor analysis report.
    User query: {query}

    Context from retrieved documents:
    {context}

    Generate a structured, insightful report based on the context.
    """
    
    response = llm.invoke(prompt)
    return response.content if hasattr(response, "content") else str(response)
