from fastapi import FastAPI
from .database import get_connection


app = FastAPI()

@app.get("/")
def home():
    conn = get_connection()
    if conn:
        return {"message": "Backend is running", "db": "connected"}
    return {"message": "Backend is running", "db": "not connected"}
