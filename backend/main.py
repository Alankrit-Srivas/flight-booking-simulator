"""
Flight Booking Simulator - Main Application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import uvicorn

from routes_flights import router as flights_router
from routes_bookings import router as bookings_router
from routes_auth import router as auth_router
from pricing_engine import PricingEngine
from database import get_db_connection
import mysql.connector
from routes_seats import router as seats_router

# Initialize FastAPI app
app = FastAPI(
    title="Flight Booking Simulator API",
    description="Backend API for Flight Booking with Dynamic Pricing",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration - MUST BE BEFORE ROUTES
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(flights_router, prefix="/api")
app.include_router(bookings_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(seats_router, prefix="/api", tags=["seats"])

@app.get("/")
async def root():
    """API Health check"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        db_version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        return {
            "status": "healthy",
            "message": "Flight Booking Simulator API is running",
            "version": "1.0.0",
            "database": "connected",
            "db_version": db_version,
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "flights": "/api/flights",
                "bookings": "/api/bookings",
                "documentation": "/api/docs"
            }
        }
    
    except mysql.connector.Error as err:
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "message": "Database connection failed",
                "error": str(err)
            }
        )

@app.on_event("startup")
async def startup_event():
    print("="*50)
    print("Flight Booking Simulator API Starting...")
    print("="*50)
    print(f"Time: {datetime.now()}")
    print("API Documentation: http://localhost:8000/api/docs")
    print("Health Check: http://localhost:8000/")
    print("="*50)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )