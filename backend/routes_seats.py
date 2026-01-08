from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from database import get_db_connection
import mysql.connector

router = APIRouter()

# Pydantic models for request/response
class Seat(BaseModel):
    seat_id: int
    flight_id: int
    seat_number: str
    seat_type: str
    price: float
    is_available: bool

class SeatReservation(BaseModel):
    seatId: int
    passengerName: str

class ReserveSeatsRequest(BaseModel):
    seats: List[SeatReservation]

# Get all seats for a specific flight
@router.get("/flights/{flight_id}/seats")
async def get_flight_seats(flight_id: int):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = """
            SELECT 
                seat_id,
                flight_id,
                seat_number,
                seat_type,
                price,
                is_available
            FROM seats 
            WHERE flight_id = %s 
            ORDER BY seat_number
        """
        
        cursor.execute(query, (flight_id,))
        seats = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return {
            "success": True,
            "seats": seats,
            "count": len(seats)
        }
        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get available seats for a flight
@router.get("/flights/{flight_id}/seats/available")
async def get_available_seats(flight_id: int):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = """
            SELECT * FROM seats 
            WHERE flight_id = %s AND is_available = TRUE 
            ORDER BY seat_number
        """
        
        cursor.execute(query, (flight_id,))
        seats = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return {
            "success": True,
            "seats": seats
        }
        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Reserve seats for a booking
@router.post("/bookings/{booking_id}/seats")
async def reserve_seats(booking_id: int, request: ReserveSeatsRequest):
    connection = None
    cursor = None
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Start transaction
        connection.start_transaction()
        
        if not request.seats or len(request.seats) == 0:
            raise HTTPException(status_code=400, detail="No seats provided")
        
        total_seat_price = 0.0
        
        # Lock and check seat availability
        for seat in request.seats:
            # Check if seat is available (with row lock)
            check_query = """
                SELECT * FROM seats 
                WHERE seat_id = %s AND is_available = TRUE 
                FOR UPDATE
            """
            cursor.execute(check_query, (seat.seatId,))
            seat_data = cursor.fetchone()
            
            if not seat_data:
                connection.rollback()
                raise HTTPException(
                    status_code=400, 
                    detail=f"Seat {seat.seatId} is not available"
                )
            
            total_seat_price += float(seat_data['price'])
            
            # Mark seat as unavailable
            update_seat_query = """
                UPDATE seats 
                SET is_available = FALSE 
                WHERE seat_id = %s
            """
            cursor.execute(update_seat_query, (seat.seatId,))
            
            # Add to booking_seats
            insert_booking_seat_query = """
                INSERT INTO booking_seats (booking_id, seat_id, passenger_name) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(
                insert_booking_seat_query, 
                (booking_id, seat.seatId, seat.passengerName)
            )
        
        # Update booking total price
        update_booking_query = """
            UPDATE bookings 
            SET booking_price = booking_price + %s 
            WHERE id = %s
        """
        cursor.execute(update_booking_query, (total_seat_price, booking_id))
        
        # Commit transaction
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return {
            "success": True,
            "message": "Seats reserved successfully",
            "total_seat_price": total_seat_price,
            "seats_reserved": len(request.seats)
        }
        
    except HTTPException as he:
        if connection:
            connection.rollback()
        raise he
    except mysql.connector.Error as err:
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Get seats for a specific booking
@router.get("/bookings/{booking_id}/seats")
async def get_booking_seats(booking_id: int):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = """
            SELECT 
                bs.booking_seat_id,
                bs.passenger_name,
                s.seat_number,
                s.seat_type,
                s.price
            FROM booking_seats bs
            JOIN seats s ON bs.seat_id = s.seat_id
            WHERE bs.booking_id = %s
        """
        
        cursor.execute(query, (booking_id,))
        seats = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return {
            "success": True,
            "seats": seats
        }
        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))