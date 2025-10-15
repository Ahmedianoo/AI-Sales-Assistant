from langgraph.graph import StateGraph, END, START
from .nodes import init_router, web_Search, RAG_search, generate_answer, tmp1

def build_chatbot_graph(state_schema: type, checkpointer):
    graph = StateGraph(state_schema)

    # 1. Add all the processing nodes
    graph.add_node("check_query", init_router)
    graph.add_node("web_search", web_Search)
    graph.add_node("rag_search", RAG_search)
    graph.add_node("generate_answer", generate_answer)

    # 2. Add a new node to handle the "split" into parallel paths
    # This node will simply pass the state through to the next nodes.
    # We can use a simple lambda function for this.
    graph.add_node("split_path", lambda state: state)

    # 3. Use the conditional edge to branch to a SINGLE node
    graph.add_conditional_edges(
        "check_query",
        lambda state: "end_response" if state["should_end"] else "continue_to_split",
        {
            "end_response": END,
            "continue_to_split": "split_path"
        }
    )

    # 4. From the "split" node, add two unconditional edges for parallel execution.
    # This avoids the "unhashable type: 'list'" error.
    graph.add_edge("split_path", "web_search")
    graph.add_edge("split_path", "rag_search")

    # 5. Connect the parallel paths to the answer generation node.
    graph.add_edge("web_search", "generate_answer")
    graph.add_edge("rag_search", "generate_answer")

    # 6. The graph ends after the final answer is generated.
    graph.add_edge("generate_answer", END)

    # 7. Set the entry point
    graph.set_entry_point("check_query")
    # graph.add_node("node1", tmp1)
    # graph.add_edge("node1", END)
    # graph.set_entry_point("node1")

    built_graph = graph.compile(
        checkpointer = checkpointer
    )

    return built_graph
