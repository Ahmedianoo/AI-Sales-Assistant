from langgraph.graph import StateGraph, END, START
from .state import ChatbotState
from .nodes import check_for_reports_or_battlecards, web_Search, RAG_search, generate_answer
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from db import ASYNC_DATABASE_URL

# --- SYNCHRONOUS PLACEHOLDERS ---
# The synchronous code will just set placeholders.
#global_checkpointer = None
#compiled_graph = None 

async def initialize_and_compile_graph():
    """
    Function to be called ONCE at application startup.
    Initializes the checkpointer and then compiles the graph.
    """
    # global global_checkpointer
    # global compiled_graph # We need to update this global variable

    # if global_checkpointer is not None:
    #     print("Checkpointer already initialized.")
    #     return

    # print("Creating persistent checkpointer instance...")
    
    # # 1. Initialize Checkpointer
    # try:
    #     context_manager = AsyncPostgresSaver.from_conn_string(ASYNC_DATABASE_URL)
    #     # Note: We must save the context manager to properly close the pool later on shutdown
    #     global_checkpointer = await context_manager.__aenter__() 
    # except Exception as e:
    #     print(f"CRITICAL ERROR: Failed to init checkpointer: {e}", flush=True)
    #     return None
    
    # 2. Compile Graph (NOW that the checkpointer is ready)
    try:
        compiled_graph = build_chatbot_graph(ChatbotState, checkpointer=None)
        print("Chatbot graph successfully compiled.", compiled_graph, flush=True)
        return compiled_graph
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to compile graph: {e}", flush=True)
        return None


def build_chatbot_graph(state_schema: type, checkpointer):
    
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

    built_graph = graph.compile(
        checkpointer = checkpointer
    )

    return built_graph
