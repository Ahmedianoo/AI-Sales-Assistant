# /nodes/generator.py
from langGraph_app.state.report_state import ReportState
from langGraph_app.core.llm import llm
from langchain_core.messages import HumanMessage


def _summarize_chunk(chunk: str) -> str:
    """
    Summarize a single chunk of text so that long documents
    fit into the model's context.
    """
    prompt = f"Summarize this:\n{chunk}"
    return llm([HumanMessage(content=prompt)])



def generate_report(state: dict) -> dict:
    """
    Generate a competitor analysis report using retrieved documents.
    Returns an updated ReportState.
    """
    user_id = state.get("user_id")
    competitor_ids = state.get("competitor_ids", [])
    docs = state.get("retrieved_docs") or []
    query = state.get("query", "latest report")

    # Handle missing docs gracefully
    if not docs:
        state["generated_report"] = None
        state["error"] = "No competitor documents found"
        return state

    prompt = f"""
    Generate a competitor analysis report.

    User ID: {user_id}
    Competitor IDs: {competitor_ids}
    Query: {query}

    Documents:
    {docs}
    """

    try:
        # Use .invoke (not deprecated __call__)
        response = llm.invoke([HumanMessage(content=prompt)])
        report_text = getattr(response, "content", str(response))

        state["generated_report"] = report_text
        state["error"] = None
    except Exception as e:
        state["generated_report"] = None
        state["error"] = str(e)

    return state