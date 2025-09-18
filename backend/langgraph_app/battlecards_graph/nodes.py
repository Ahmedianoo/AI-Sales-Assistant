from services.search import search_documents
from state import BattlecardState
from langchain_community.tools.tavily_search import TavilySearchResults
from pydantic import BaseModel, Field
from typing import Dict, List
from langchain_community.chat_models import ChatOllama
from langchain.schema import SystemMessage, HumanMessage


llm = ChatOllama("llama3.1:8b", temperature=0)

class SearchQuery(BaseModel):
    search_query:str = Field(None, description="Cleaned-up web search query")

class BattlecardDraft(BaseModel):
    sections: Dict[str, List[str]]    


#-------------------------Node 1-----------------------------
def perform_search(state: BattlecardState):

    query = state.query or "overview of the competitor"
    results = search_documents(user_id=state.user_id, competitor_ids=state.competitor_ids, query=query, top_k=state.top_k)
    state.search_results = results

    return state
#--------------------------------------------------------------



#-------------------------Node 2-----------------------------
search_instructions = SystemMessage(content=f"""You are helping generate competitor analysis.
Rewrite the user's query as a clear and specific web search query.

The rewritten query should:
- Include relevant company, industry, product, and region details if mentioned.
- Expand vague requests into 8–15 word precise queries.
- Avoid being too short or too generic.

Example:
"tell me about Tesla" -> "Tesla electric vehicle sales trends 2025 in Egypt automotive market"
If the user provides no query, generate a general competitor analysis query for the industry.
""")

def search_web(state: BattlecardState):

    structured_llm = llm.with_structured_output(SearchQuery)

    messages = [search_instructions]
    if state.query:
        messages.append(HumanMessage(content=state.query))

    search_query = structured_llm.invoke(messages)

    tavily_search = TavilySearchResults(max_results=10)
    search_docs = tavily_search.invoke(search_query.search_query)

    formatted_web_search_results = [
        {"url": doc["url"], "content": doc["content"]}
        for doc in search_docs
    ]

    state.web_search_results = formatted_web_search_results    
    

    return state
#--------------------------------------------------------------


def build_context(state: BattlecardState) -> str:
    context_parts = []

    if state.search_results:
        db_context = "\n\n".join([f"[DB Doc] {r.text}" for r in state.search_results if r.text])
        context_parts.append(db_context)

    if state.web_search_results:
        web_context = "\n\n".join([f"[Web Doc] {r['content']} (Source: {r['url']})"
                                   for r in state.web_search_results])
        context_parts.append(web_context)

    return "\n\n---\n\n".join(context_parts)



#-------------------------Node 3-----------------------------
def generate_battlecard(state: BattlecardState):

    context = build_context(state)

    system_prompt = f"""
    You are generating a competitor battlecard.

    Based on the provided context, create an analysis divided into labeled sections.
    - Default to SWOT (Strengths, Weaknesses, Opportunities, Threats) if applicable.
    - If the query or context suggests different categories, use those instead.
    - Each section should have concise bullet points.
    """

    repsonse = llm.with_structured_output(BattlecardDraft).invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"User Query: {state.query or 'No specific query'}\n\nContext:\n{context}")
    ])

    state.content = repsonse.sections

    return state


#--------------------------------------------------------------




