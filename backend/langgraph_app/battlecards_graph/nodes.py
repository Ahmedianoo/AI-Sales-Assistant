from services.search import search_documents
from state import BattlecardState
from langchain_community.tools.tavily_search import TavilySearchResults
from pydantic import BaseModel, Field
from langchain_community.chat_models import ChatOllama
from langchain.schema import SystemMessage, HumanMessage


llm = ChatOllama("llama3.1:8b", temperature=0)

class SearchQuery(BaseModel):
    search_query:str= Field(None, description="Cleaned-up web search query")



def perform_search(state: BattlecardState):

    query = state.query or "overview of the competitor"
    results = search_documents(user_id=state.user_id, competitor_ids=state.competitor_ids, query=query, top_k=state.top_k)
    state.search_results = results

    return state


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




