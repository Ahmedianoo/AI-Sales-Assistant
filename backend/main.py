from fastapi import FastAPI
from routes import battlecards, milvus, ingest_search, crawl
from routes import users

app = FastAPI()

app.include_router(battlecards.router)
app.include_router(users.router)

app.include_router(milvus.router)
app.include_router(ingest_search.router)
app.include_router(crawl.router)


@app.get("/")

def root():
    return {"message": "Sales Assistant API is running"}
    

    



# @app.get("/")
# def temp():
#     print("hello hello")    