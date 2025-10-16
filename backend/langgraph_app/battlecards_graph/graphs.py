from langgraph.graph import StateGraph, END, START
from .state import BattlecardState
from .nodes import perform_search, search_web, generate_battlecard


def build_battlecards_graph():
    builder = StateGraph(BattlecardState)

    builder.add_node("retrieval", perform_search)
    builder.add_node("search_web", search_web)
    builder.add_node("generate_battlecard", generate_battlecard)
    



    builder.add_edge(START, "retrieval")
    builder.add_edge("retrieval", "search_web")
    builder.add_edge("search_web", "generate_battlecard")
    builder.add_edge("generate_battlecard", END)
    
    graph = builder.compile()

    return graph




battlecard_graph = build_battlecards_graph()
