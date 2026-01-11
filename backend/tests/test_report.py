from langGraph_app.graphs.report_graph import build_report_graph

def test_report_generation():
    graph = build_report_graph()

    state = {
        "query": "Marvel",
        "retrieved_docs": [
            "Marvel launches new comics and digital experiences...",
            "Disney+ streaming Marvel Zombies series..."
        ],
        "generated_report": None
    }

    final_state = graph.invoke(state)
    print("=== Final Report ===")
    print(final_state["generated_report"])
