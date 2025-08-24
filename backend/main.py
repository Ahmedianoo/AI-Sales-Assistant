from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def temp():
    print("hello hello")    