from langgraph.graph import StateGraph, END
from services.report_generator import improve_report

# --- Define State ---
class ReportState(dict):
    query: str
    retrieved_docs: list
    generated_report: str | None

# --- Node: improve report ---
def improve_report_node(state: ReportState) -> ReportState:
    if state.get("retrieved_docs"):
        state["generated_report"] = improve_report(
            state["query"],
            state["retrieved_docs"]
        )
    else:
        state["generated_report"] = "⚠️ No relevant documents found"
    return state

# --- Build Graph ---
def build_report_graph():
    graph = StateGraph(ReportState)
    graph.add_node("improve_report", improve_report_node)
    graph.set_entry_point("improve_report")
    graph.add_edge("improve_report", END)
    return graph.compile()
