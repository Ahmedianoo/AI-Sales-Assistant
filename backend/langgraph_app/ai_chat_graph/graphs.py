from langgraph.graph import StateGraph, END, START
from .state import ChatbotState
from .nodes import check_for_reports_or_battlecards, web_Search, RAG_search, generate_answer

def build_chatbot_graph(state_schema: type):
    
    graph = StateGraph(state_schema)

    # 1. Add all the processing nodes
    graph.add_node("check_query", check_for_reports_or_battlecards)
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
        lambda state: "end_response" if state.should_end else "continue_to_split",
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

    built_graph = graph.compile()

    return built_graph
