from langGraph_app.graphs.report_graph import build_report_graph
from langGraph_app.state.report_state import ReportState

# Compile the graph once when this module is imported
_report_graph = build_report_graph()

def run_report_graph(initial_state: ReportState):
    """
    Execute the report graph with the given state.
    """
    final_state = _report_graph.invoke(initial_state)
    return final_state
