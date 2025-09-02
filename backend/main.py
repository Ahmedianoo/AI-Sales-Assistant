from fastapi import FastAPI
from routes import battlecards
from routes import users

app = FastAPI()

app.include_router(battlecards.router)
app.include_router(users.router)


@app.get("/")

def root():
    return {"message": "Sales Assistant API is running"}
    

    



# @app.get("/")
# def temp():
#     print("hello hello")    