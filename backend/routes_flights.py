from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import date, datetime
from database import get_db_connection
from pydantic import BaseModel, Field
import mysql.connector

router = APIRouter(prefix="/flights", tags=["Flights"])

# Pydantic Models
class FlightCreate(BaseModel):
    flight_number: str = Field(..., min_length=4, max_length=10)
    airline: str = Field(..., min_length=2, max_length=50)
    origin: str = Field(..., min_length=3, max_length=3)
    destination: str = Field(..., min_length=3, max_length=3)
    departure_time: datetime
    arrival_time: datetime
    base_price: float = Field(..., gt=0)
    total_seats: int = Field(..., gt=0)
    available_seats: int = Field(..., ge=0)

class FlightUpdate(BaseModel):
    airline: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    base_price: Optional[float] = None
    available_seats: Optional[int] = None

# GET all flights with filtering and sorting
@router.get("/")
def get_flights(
    origin: Optional[str] = Query(None, min_length=3, max_length=3),
    destination: Optional[str] = Query(None, min_length=3, max_length=3),
    departure_date: Optional[date] = None,
    sort_by: Optional[str] = Query("price", pattern="^(price|duration|departure)$"),
    order: Optional[str] = Query("asc", pattern="^(asc|desc)$")
):
    """Search flights with filters"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                id, flight_number, airline, origin, destination,
                departure_time, arrival_time, base_price, current_price,
                total_seats, available_seats, created_at,
                TIMESTAMPDIFF(MINUTE, departure_time, arrival_time) as duration_minutes
            FROM flights
            WHERE 1=1
        """
        params = []
        
        if origin:
            query += " AND UPPER(origin) = UPPER(%s)"
            params.append(origin)
        
        if destination:
            query += " AND UPPER(destination) = UPPER(%s)"
            params.append(destination)
        
        if departure_date:
            query += " AND DATE(departure_time) = %s"
            params.append(departure_date)
        
        sort_column_map = {
            "price": "current_price",
            "duration": "duration_minutes",
            "departure": "departure_time"
        }
        sort_column = sort_column_map.get(sort_by, "current_price")
        query += f" ORDER BY {sort_column} {order.upper()}"
        
        cursor.execute(query, params)
        flights = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "count": len(flights),
            "flights": flights
        }
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

# GET specific flight by ID
@router.get("/{flight_id}")
def get_flight_by_id(flight_id: int):
    """Get detailed information about a specific flight"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                id, flight_number, airline, origin, destination,
                departure_time, arrival_time, base_price, current_price,
                total_seats, available_seats, created_at,
                TIMESTAMPDIFF(MINUTE, departure_time, arrival_time) as duration_minutes
            FROM flights
            WHERE id = %s
        """
        
        cursor.execute(query, (flight_id,))
        flight = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not flight:
            raise HTTPException(status_code=404, detail="Flight not found")
        
        return {
            "success": True,
            "flight": flight
        }
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

# POST - Create new flight
@router.post("/", status_code=201)
def create_flight(flight: FlightCreate):
    """Create a new flight"""
    try:
        if flight.departure_time >= flight.arrival_time:
            raise HTTPException(
                status_code=400, 
                detail="Departure time must be before arrival time"
            )
        
        if flight.available_seats > flight.total_seats:
            raise HTTPException(
                status_code=400,
                detail="Available seats cannot exceed total seats"
            )
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO flights 
            (flight_number, airline, origin, destination, departure_time, 
             arrival_time, base_price, current_price, total_seats, available_seats)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            flight.flight_number, flight.airline, flight.origin.upper(),
            flight.destination.upper(), flight.departure_time, flight.arrival_time,
            flight.base_price, flight.base_price,
            flight.total_seats, flight.available_seats
        )
        
        cursor.execute(query, values)
        conn.commit()
        
        flight_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "message": "Flight created successfully",
            "flight_id": flight_id
        }
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

# PUT - Update flight
@router.put("/{flight_id}")
def update_flight(flight_id: int, flight_update: FlightUpdate):
    """Update flight details"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        update_fields = []
        values = []
        
        if flight_update.airline:
            update_fields.append("airline = %s")
            values.append(flight_update.airline)
        
        if flight_update.departure_time:
            update_fields.append("departure_time = %s")
            values.append(flight_update.departure_time)
        
        if flight_update.arrival_time:
            update_fields.append("arrival_time = %s")
            values.append(flight_update.arrival_time)
        
        if flight_update.base_price:
            update_fields.append("base_price = %s")
            values.append(flight_update.base_price)
        
        if flight_update.available_seats is not None:
            update_fields.append("available_seats = %s")
            values.append(flight_update.available_seats)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(flight_id)
        query = f"UPDATE flights SET {', '.join(update_fields)} WHERE id = %s"
        
        cursor.execute(query, values)
        conn.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Flight not found")
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "message": "Flight updated successfully"
        }
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

# DELETE - Delete flight
@router.delete("/{flight_id}")
def delete_flight(flight_id: int):
    """Delete a flight"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT COUNT(*) as count FROM bookings WHERE flight_id = %s",
            (flight_id,)
        )
        result = cursor.fetchone()
        
        if result[0] > 0:
            cursor.close()
            conn.close()
            raise HTTPException(
                status_code=400,
                detail="Cannot delete flight with existing bookings"
            )
        
        cursor.execute("DELETE FROM flights WHERE id = %s", (flight_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Flight not found")
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "message": "Flight deleted successfully"
        }
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")