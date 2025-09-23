from services.search import search_documents
from .state import ChatbotState
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.schema import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

#BismAllah

groq_llm = ChatGroq(
    model="llama-3.1-8b-instant",  
    temperature=0,
    api_key= os.getenv("GROQ_API_KEY")
)


gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    temperature=0,
    google_api_key= os.getenv("GEMINI_API_KEY")
)

# node 1: decides if static response for generation of reports/ battlecards
def check_for_reports_or_battlecards(state: ChatbotState):
    query = state.query

    System = "You are a simple agent whose task is to determine if the input user query wants to generate" \
    "or display a 'report' or 'battlecard'. If it does, respond with 'REPORTS_BATTLECARDS_QUERY', else " \
    "respond with 'OTHER_QUERY'. "
    
    decision = groq_llm.invoke([
        SystemMessage(content=System),
        HumanMessage(content=query)
    ]).content

    if "REPORTS_BATTLECARDS_QUERY" in decision:
        response = "I can't create those for you, but you can find them on the Reports and Battlecards pages."
        "Just let me know if you need anything else!"

        return {"final_response":response, "should_end":True}
    else:
        return{"should_end":False}
    

# node 2: search for results in RAG
def RAG_search(state: ChatbotState):

    query = state.query
    results = search_documents(user_id=state.user_id, competitor_ids=state.competitor_ids, query=query, top_k=state.top_k_rag)

    return {"rag_results": results, "should_end": False}

# node 3: search for results on web
def web_Search(state: ChatbotState):
    
    #print("inside web search tool")
    search_tool = TavilySearchResults(
        api_key = os.getenv("TAVILY_API_KEY"),
        max_results = state.top_k_search,
        include_raw_content= True
    )
    
    # reformat user input queries into stronger, better prompts for searching
    prompt_template = """You are a sales assistant whose sole purpose is to rephrase a user's natural language query into a concise and effective search query for a web search engine. 
    Your output must be a single, optimized search query and nothing else.
        Guidelines:
        - **Be Concise:** The query should be as short as possible while retaining all necessary information.
        - **Remove Conversational Language:** Strip out phrases like "What is," "Tell me about," or "Can you find."
        - **Focus on Keywords:** Identify the most important keywords and entities from the user's query.
        - **Maintain Intent:** The rewritten query must capture the original user's intent perfectly.

        Examples:
        User query: "What are the latest CRM software features for lead management?"
        Rewritten query: "latest CRM software features lead management"

        User query: "Can you find me some recent statistics on B2B sales trends?"
        Rewritten query: "B2B sales trends statistics 2024"

        User query: "I need to know how to create a sales proposal for a new client."
        Rewritten query: "how to create a sales proposal"

        User query: "Please find information about our competitor, Acme Inc., and their recent product launch."
        Rewritten query: "Acme Inc. recent product launch"
        
        User query: {query}
        Rewritten query:
        """
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | groq_llm | StrOutputParser()
    rephrased_query = chain.invoke({"query": state.query})
    print("rephrased chatbot query: ", rephrased_query)
    
    # pass reformatted prompt to tavily
    search_result = search_tool.invoke({'query' : rephrased_query})
    
    # get result from tavily in a strcutured way to save in state
    formatted_web_search_results = [
        {"url": doc["url"], "content": doc["content"]}
        for doc in search_result
    ]

    return {"web_search_results": formatted_web_search_results}

# node 4: use both node 2 & 3 results to write final answer
def generate_answer(state: ChatbotState):
    """
    Synthesizes information from RAG and web search results to create a final,
    well-structured answer for the user, including a list of source URLs.
    """
    question = state.query
    rag_results = state.rag_results
    web_search_results = state.web_search_results

    # Structure the inputs for the LLM
    structured_context = ""
    used_urls = []

    # Add RAG results, accessing the 'text' attribute of the SearchResult model
    if rag_results:
        structured_context += "--- RAG RESULTS ---\n"
        for i, doc in enumerate(rag_results):
            # Access the content using the 'text' attribute from your custom SearchResult model
            structured_context += f"Document {i+1}:\n{doc.text}\n\n"
    
    # Add web search results and track their URLs
    if web_search_results:
        structured_context += "--- WEB SEARCH RESULTS ---\n"
        for i, result in enumerate(web_search_results):
            #print("--------------------------result from web search that content and url are extracted from", result)
            content = result.get('content', 'No content found.')
            url = result.get('url', 'N/A')
            structured_context += f"Search Result {i+1} (from {url}):\n{content}\n\n"
            # Add the URL to our list of sources
            if url != 'N/A':
                used_urls.append(url)

    # Define the system prompt with instructions and persona
    system_prompt = """
    You are an expert AI assistant tasked with providing a comprehensive, well-structured, and easy-to-read answer to a user's question. Your response must be in Markdown.
    
    You will be given context from internal documents (RAG results) and the web (web search results).
    
    --- INSTRUCTIONS ---
    1.  **Synthesize**: Combine the information from both sources to form a single, cohesive answer.
    2.  **Proper Formatting**: Structure your response using short paragraphs and bullet points to enhance readability.
    3.  **Clarity**: Ensure the final answer is clear, concise, and directly addresses the user's question.
    4.  **No Hallucination**: Do not include any information that is not supported by the provided context. If the context does not contain enough information to answer the question, state that clearly and concisely.
    5.  **Citations**: If you use any information from the web search results, you **must** include a "Resources" section at the end of your answer. List the full URLs of the sources you used in a bulleted list.
    6.  **Politeness**: Start your response with a brief, friendly acknowledgment that you have found the requested information.
    """

    # Combine the system and human messages
    final_prompt = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"--- CONTEXT ---\n{structured_context}\n\n--- USER'S QUESTION ---\n{question}")
    ]
    
    # Invoke the LLM
    response = gemini_llm.invoke(final_prompt)
    
    # Add the final answer to state
    state.final_response = response.content
    state.should_end = True

    return state