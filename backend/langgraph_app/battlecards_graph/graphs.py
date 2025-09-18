from langgraph.graph import StateGraph, END, START
from .state import BattlecardState
from .nodes import perform_search, search_web


def build_battlecards_graph():
    builder = StateGraph(BattlecardState)

    builder.add_node("retrival", perform_search)
    builder.add_node("search_web", search_web)
    



    builder.add_edge(START, "retrival")
    builder.add_edge("retrival", "search_web")
    builder.add_edge("search_web", END)
    
    graph = builder.compile()

    return graph