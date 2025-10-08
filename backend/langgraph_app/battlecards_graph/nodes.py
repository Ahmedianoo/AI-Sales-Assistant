from services.search import search_documents
from .state import BattlecardState
from langchain_community.tools.tavily_search import TavilySearchResults
from pydantic import BaseModel, Field
from typing import Dict, List
from langchain.schema import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json
import re


groq_api_key = os.getenv("GROQ_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

groq_llm = ChatGroq(
    model="llama-3.1-8b-instant",   # Or gemma2-9b, mixtral.
    temperature=0,
    api_key=groq_api_key
)


gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # or "gemini-1.5-pro" if you need deeper reasoning
    temperature=0,
    google_api_key=gemini_api_key
)

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
search_instructions = SystemMessage(content=f"""
You are helping generate competitor analysis.

Rewrite the user's query as a clear and specific web search query. 

Guidelines:
- Always include the competitor's name if mentioned.
- Include relevant industry, product, and region details if available.
- Expand vague or short queries into a precise 8–15 word search query.
- Avoid being too short, generic, or ambiguous.
- Make the query actionable for retrieving relevant market and competitor insights.

Example:
"tell me about Tesla" -> "Tesla electric vehicle sales trends 2025 in Egypt automotive market"

If the user provides no query, generate a general competitor analysis query for the industry.
""")

def search_web(state: BattlecardState):

    structured_llm = groq_llm.with_structured_output(SearchQuery)

    messages = [search_instructions]
    if state.query:
        messages.append(HumanMessage(content=state.query))

    search_query = structured_llm.invoke(messages)

    print("SEARCH QUERY:", search_query.search_query)

    tavily_search = TavilySearchResults(max_results=5, api_key=os.getenv("TAVILY_API_KEY"))
    search_docs = tavily_search.invoke(search_query.search_query)

    

    formatted_web_search_results = [
        {"url": doc["url"], "content": doc["content"]}
        for doc in search_docs
    ]

    state.web_search_results = formatted_web_search_results    

    ##print("DB RESULTS:", state.search_results)
    print("WEB RESULTS:", state.web_search_results)

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

    ##print("built context:", context)

    system_prompt = f"""
    You are generating a competitor battlecard.

    Based on the provided context, create an analysis divided into labeled sections.
    - Default to SWOT (Strengths, Weaknesses, Opportunities, Threats) if applicable.
    - If the query or context suggests different categories, use those instead.
    - Each section should have **concise bullet points**, no more than 5–7 bullets per section.
    - Each bullet point should be **1–2 sentences maximum**, easy to read and suitable for tagging.

    IMPORTANT:
    - Respond only in JSON format.
    - The JSON must have a top-level key called "sections".
    - Each section must be a key inside "sections", with a list of bullet points as its value.
    - Example response:

    {{
        "sections": {{
            "Strengths": ["Strong brand recognition", "Innovative product line"],
            "Weaknesses": ["High production costs", "Limited global reach"],
            "Opportunities": ["Expanding into emerging markets", "Strategic partnerships"],
            "Threats": ["Intense competition", "Regulatory changes"]
        }}
    }}

    - Use short, taggable phrases where possible for bullet points.
    - Do not include extra text, markdown, or explanations outside the JSON.
    """

    response = gemini_llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"User Query: {state.query or 'No specific query'}\n\nContext:\n{context}")
    ])

    print("RESPONSE:", response)

    content_str = getattr(response, "content", "")

    # Remove ```json``` blocks if present
    content_str = re.sub(r"^```json|```$", "", content_str.strip())

    # Parse JSON safely
    try:
        parsed = json.loads(content_str)
        state.content = parsed.get("sections", {})
    except json.JSONDecodeError:
        print("Failed to parse JSON from LLM output")
        state.content = {}

    return state


#--------------------------------------------------------------




