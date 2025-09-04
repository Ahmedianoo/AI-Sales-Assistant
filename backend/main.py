from fastapi import FastAPI
from routes import battlecards
from routes import users
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv


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

app.include_router(battlecards.router)
app.include_router(users.router)


@app.get("/")

def root():
    return {"message": "Sales Assistant API is running"}
    

    



# @app.get("/")
# def temp():
#     print("hello hello")    