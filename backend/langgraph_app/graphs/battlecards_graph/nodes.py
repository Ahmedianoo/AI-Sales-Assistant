from services.search import search_documents
from state import BattlecardState

def perform_search(state: BattlecardState):

    query = state.query or "overview of the competitor"
    results = search_documents(user_id=state.user_id, competitor_ids=state.competitor_ids, query=query, top_k=getattr(state, "top_k", 5))
    state.search_results = results

    return state


