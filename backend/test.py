from fastapi import FastAPI, Query
from langchain_ollama import OllamaLLM

app = FastAPI()

# Connect to the ollama container (Docker service name: "ollama")
llm = OllamaLLM(
    model="llama3.1",
    base_url="http://ollama:11434"
)

@app.get("/ask")
async def ask(query: str = Query(..., description="User query")):
    try:
        response = llm.invoke(query)
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}
