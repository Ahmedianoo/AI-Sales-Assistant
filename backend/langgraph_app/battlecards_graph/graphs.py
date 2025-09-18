from langgraph.graph import StateGraph, END, START
from .state import BattlecardState
from .nodes import perform_search


def build_battlecards_graph():
    builder = StateGraph(BattlecardState)
    builder.add_node("retrival", perform_search)


    builder.add_edge(START, "retrival")
    builder.add_edge("retrieval", END)
    graph = builder.compile()

    return graph