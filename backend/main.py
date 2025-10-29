from fastapi import FastAPI
from routes import battlecards, milvus, ingest_search, crawl
from routes import users, competitors
from routes import search_history, ai_chat, profile
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from APScheduler.scheduler import start_scheduler
from db import ASYNC_DATABASE_URL, async_pool
from langgraph_app.ai_chat_graph.graphs import build_chatbot_graph
from langgraph_app.ai_chat_graph.state import ChatbotState
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from contextlib import asynccontextmanager

load_dotenv()
frontendUrl = os.getenv("frontendURL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    start_scheduler()
    app.state.async_pool =  async_pool
    await async_pool.open()

    # async with async_pool.connection() as conn:
    #     saver = AsyncPostgresSaver(conn)
    #     #await saver.setup()
    #saver = AsyncPostgresSaver(app.state.async_pool)
    
    #app.state.saver = saver

    #chatbot_graph = build_chatbot_graph(ChatbotState, None)
    #app.state.chatbot_graph = chatbot_graph

    yield  # --- App runs ---

    # --- Shutdown ---
    await async_pool.close()

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontendUrl], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(battlecards.router)
app.include_router(users.router)
app.include_router(search_history.router)

app.include_router(milvus.router)
app.include_router(ingest_search.router)
app.include_router(crawl.router)
app.include_router(ai_chat.router)
app.include_router(profile.router)
app.include_router(competitors.router)

@app.get("/")
def root():
    return {"message": "Sales Assistant API is running"}   