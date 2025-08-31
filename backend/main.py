from fastapi import FastAPI
from routes import battlecards


app = FastAPI()

app.include_router(battlecards.router)


@app.get("/")

def root():
    return {"message": "Sales Assistant API is running"}
    

    



# @app.get("/")
# def temp():
#     print("hello hello")    