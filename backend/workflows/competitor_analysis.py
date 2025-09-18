# workflows/competitor_analysis.py
from langgraph.graph import StateGraph, END
from crawl4ai import AsyncWebCrawler
from sentence_transformers import SentenceTransformer
from pymilvus import connections, Collection
import ollama
import hashlib

# Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# Ensure collection exists
collection_name = "competitor_embeddings"
embedding_dim = 384
try:
    collection = Collection(collection_name)
except Exception:
    from pymilvus import FieldSchema, CollectionSchema, DataType
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="competitor_id", dtype=DataType.INT64),
        FieldSchema(name="doc_id", dtype=DataType.VARCHAR, max_length=200),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=embedding_dim),
    ]
    schema = CollectionSchema(fields, "Competitor Embeddings")
    collection = Collection(collection_name, schema)

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# -------- LangGraph State --------
class CompetitorState(dict):
    url: str
    competitor_id: int
    raw_text: str
    embeddings: list
    summary: str


# -------- Nodes --------
async def crawl_node(state: CompetitorState) -> CompetitorState:
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun(state["url"])
    docs = [doc.markdown for doc in results if doc.markdown]
    state["raw_text"] = "\n".join(docs)
    return state

def embed_node(state: CompetitorState) -> CompetitorState:
    if not state.get("raw_text"):
        return state
    chunks = state["raw_text"].split("\n\n")
    embeddings = embedder.encode(chunks).tolist()

    # Insert into Milvus
    entities = [
        [state["competitor_id"]] * len(chunks),
        [hashlib.md5(chunk.encode()).hexdigest() for chunk in chunks],
        embeddings
    ]
    collection.insert(entities)
    collection.flush()

    state["embeddings"] = embeddings
    return state

def analyze_node(state: CompetitorState) -> CompetitorState:
    if not state.get("raw_text"):
        state["summary"] = "No content found."
        return state
    
    resp = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": "You are an AI that summarizes competitor websites."},
            {"role": "user", "content": f"Summarize the key offerings and strategy of this competitor:\n\n{state['raw_text']}"}
        ]
    )
    state["summary"] = resp["message"]["content"]
    return state


# -------- Workflow Graph --------
graph = StateGraph(CompetitorState)
graph.add_node("crawl", crawl_node)
graph.add_node("embed", embed_node)
graph.add_node("analyze", analyze_node)

graph.set_entry_point("crawl")
graph.add_edge("crawl", "embed")
graph.add_edge("embed", "analyze")
graph.add_edge("analyze", END)

workflow = graph.compile()
