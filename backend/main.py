from fastapi import FastAPI
from .database import get_connection
from .routes_flights import router as flights_router



app = FastAPI()
app.include_router(flights_router)


@app.get("/")
def home():
    conn = get_connection()
    if conn:
        return {"message": "Backend is running", "db": "connected"}
    return {"message": "Backend is running", "db": "not connected"}
