from fastapi import FastAPI
from routes import battlecards, milvus, ingest_search, crawl
from routes import users
#from routes import search_history #ai_chat
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from APScheduler.scheduler import start_scheduler
from db import init_db, initialize_global_checkpointer, check_connection

load_dotenv()
frontendUrl = os.getenv("frontendURL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontendUrl], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.on_event("startup")
async def startup_event():
#    print("called scheduler in main", flush=True)
    start_scheduler()

    #await check_connection()

    # IMPORTANT!! Run only once then MUST be commented out
    #await init_db()
    await initialize_global_checkpointer()

app.include_router(battlecards.router)
app.include_router(users.router)
#app.include_router(search_history.router)

app.include_router(milvus.router)
app.include_router(ingest_search.router)
app.include_router(crawl.router)

#app.include_router(ai_chat.router)

@app.get("/")

def root():
    return {"message": "Sales Assistant API is running"}
    

    



# @app.get("/")
# def temp():
#     print("hello hello")    