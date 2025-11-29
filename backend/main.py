from fastapi import FastAPI
from backend.database import get_connection
from backend.routes_flights import router as flights_router
from backend.routes_bookings import router as bookings_router




app = FastAPI()
app.include_router(flights_router)
app.include_router(bookings_router)


@app.get("/")
def home():
    conn = get_connection()
    if conn:
        return {"message": "Backend is running", "db": "connected"}
    return {"message": "Backend is running", "db": "not connected"}
