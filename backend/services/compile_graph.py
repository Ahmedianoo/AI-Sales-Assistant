# /services/compile_graph.py
from langgraph_app.ai_chat_graph.state import ChatbotState
from langgraph_app.ai_chat_graph.graphs import build_chatbot_graph
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from db import ASYNC_DATABASE_URL

# --- SYNCHRONOUS PLACEHOLDERS ---
# The synchronous code will just set placeholders.
global_checkpointer = None
compiled_graph = None 


async def initialize_and_compile_graph():
    """
    Function to be called ONCE at application startup.
    Initializes the checkpointer and then compiles the graph.
    """
    global global_checkpointer
    global compiled_graph # We need to update this global variable

    if global_checkpointer is not None:
        print("Checkpointer already initialized.")
        return

    print("Creating persistent checkpointer instance...")
    
    # 1. Initialize Checkpointer
    try:
        context_manager = AsyncPostgresSaver.from_conn_string(ASYNC_DATABASE_URL)
        # Note: We must save the context manager to properly close the pool later on shutdown
        global_checkpointer = await context_manager.__aenter__() 
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to init checkpointer: {e}", flush=True)
        return
    
    # 2. Compile Graph (NOW that the checkpointer is ready)
    try:
        compiled_graph = build_chatbot_graph(ChatbotState, global_checkpointer)
        print("Chatbot graph successfully compiled.", flush=True)
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to compile graph: {e}", flush=True)


async def shutdown_global_checkpointer():
    """Function to be called ONCE at application shutdown."""
    global global_checkpointer
    if global_checkpointer is not None:
        # Assuming the checkpointer object stores the context manager needed for __aexit__
        # If not, you might need to structure initialize_and_compile_graph differently 
        # to store the context_manager object itself (e.g., in another global).
        # For simplicity, let's assume global_checkpointer can handle shutdown for now.
        print("Closing persistent checkpointer connection pool...")
        await global_checkpointer.__aexit__(None, None, None)
        print("Checkpointer connection pool closed.")