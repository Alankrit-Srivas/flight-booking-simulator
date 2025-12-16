from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from database import get_db_connection
from pricing_engine import PricingEngine
import mysql.connector
import random
import string

router = APIRouter(prefix="/bookings", tags=["Bookings"])

# Pydantic Models
class PassengerInfo(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    age: int = Field(..., gt=0, lt=150)
    gender: str = Field(..., pattern="^(male|female|other)$")

class BookingCreate(BaseModel):
    flight_id: int
    passenger: PassengerInfo
    seat_number: Optional[str] = None
    payment_method: str = Field(..., pattern="^(credit_card|debit_card|upi|net_banking)$")

# Helper Functions
def generate_pnr() -> str:
    """Generate unique 6-character PNR"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_seat_number(flight_id: int, cursor) -> str:
    """Generate or assign available seat number"""
    cursor.execute(
        """
        SELECT total_seats, 
               (SELECT COUNT(*) FROM bookings WHERE flight_id = %s AND status != 'cancelled') as booked
        FROM flights WHERE id = %s
        """,
        (flight_id, flight_id)
    )
    result = cursor.fetchone()
    
    if not result:
        return None
    
    total_seats, booked = result
    seats_per_row = 6
    seat_letters = ['A', 'B', 'C', 'D', 'E', 'F']
    
    cursor.execute(
        "SELECT seat_number FROM bookings WHERE flight_id = %s AND status != 'cancelled'",
        (flight_id,)
    )
    booked_seats = {row[0] for row in cursor.fetchall() if row[0]}
    
    for seat_num in range(1, total_seats + 1):
        row = (seat_num - 1) // seats_per_row + 1
        seat_letter = seat_letters[(seat_num - 1) % seats_per_row]
        seat = f"{row}{seat_letter}"
        
        if seat not in booked_seats:
            return seat
    
    return None

def simulate_payment(payment_method: str) -> tuple:
    """Simulate payment processing"""
    success = random.random() < 0.95
    
    if success:
        transaction_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"
        return True, transaction_id
    else:
        return False, "PAYMENT_FAILED"

# POST - Create booking
@router.post("/", status_code=201)
def create_booking(booking: BookingCreate):
    """Create a new booking with concurrency control"""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        conn.autocommit = False
        cursor = conn.cursor(dictionary=True)
        
        # Lock flight row for update (concurrency control)
        cursor.execute(
            """
            SELECT id, flight_number, airline, origin, destination, 
                   departure_time, current_price, available_seats, total_seats, base_price
            FROM flights 
            WHERE id = %s 
            FOR UPDATE
            """,
            (booking.flight_id,)
        )
        
        flight = cursor.fetchone()
        
        if not flight:
            raise HTTPException(status_code=404, detail="Flight not found")
        
        if flight['available_seats'] <= 0:
            conn.rollback()
            raise HTTPException(status_code=400, detail="No seats available")
        
        if flight['departure_time'] < datetime.now():
            conn.rollback()
            raise HTTPException(status_code=400, detail="Flight has already departed")
        
        # Assign seat number
        seat_number = booking.seat_number
        if not seat_number:
            cursor_temp = conn.cursor()
            seat_number = generate_seat_number(booking.flight_id, cursor_temp)
            cursor_temp.close()
            
            if not seat_number:
                conn.rollback()
                raise HTTPException(status_code=400, detail="Unable to assign seat")
        
        # Verify seat not taken
        cursor.execute(
            """
            SELECT COUNT(*) as count 
            FROM bookings 
            WHERE flight_id = %s AND seat_number = %s AND status != 'cancelled'
            """,
            (booking.flight_id, seat_number)
        )
        
        if cursor.fetchone()['count'] > 0:
            conn.rollback()
            raise HTTPException(status_code=400, detail="Seat already booked")
        
        # Process payment
        payment_success, transaction_id = simulate_payment(booking.payment_method)
        
        if not payment_success:
            conn.rollback()
            raise HTTPException(status_code=402, detail="Payment failed. Please try again.")
        
        # Generate PNR
        pnr = generate_pnr()
        cursor.execute("SELECT COUNT(*) as count FROM bookings WHERE pnr = %s", (pnr,))
        while cursor.fetchone()['count'] > 0:
            pnr = generate_pnr()
            cursor.execute("SELECT COUNT(*) as count FROM bookings WHERE pnr = %s", (pnr,))
        
        booking_price = flight['current_price']
        
        # Insert booking
        cursor.execute(
            """
            INSERT INTO bookings 
            (pnr, flight_id, passenger_first_name, passenger_last_name, 
             passenger_email, passenger_phone, passenger_age, passenger_gender,
             seat_number, booking_price, status, payment_status, transaction_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                pnr, booking.flight_id,
                booking.passenger.first_name, booking.passenger.last_name,
                booking.passenger.email, booking.passenger.phone,
                booking.passenger.age, booking.passenger.gender,
                seat_number, booking_price,
                'confirmed', 'completed', transaction_id
            )
        )
        
        booking_id = cursor.lastrowid
        
        # Update flight available seats
        new_available_seats = flight['available_seats'] - 1
        cursor.execute(
            "UPDATE flights SET available_seats = %s WHERE id = %s",
            (new_available_seats, booking.flight_id)
        )
        
        # Update price
        engine = PricingEngine()
        new_pricing = engine.calculate_price(
            base_price=flight['base_price'],
            total_seats=flight['total_seats'],
            available_seats=new_available_seats,
            departure_time=flight['departure_time'],
            demand_level="medium"
        )
        
        cursor.execute(
            "UPDATE flights SET current_price = %s WHERE id = %s",
            (new_pricing['current_price'], booking.flight_id)
        )
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "message": "Booking created successfully",
            "booking": {
                "id": booking_id,
                "pnr": pnr,
                "flight_number": flight['flight_number'],
                "passenger_name": f"{booking.passenger.first_name} {booking.passenger.last_name}",
                "seat_number": seat_number,
                "booking_price": booking_price,
                "status": "confirmed",
                "transaction_id": transaction_id
            }
        }
    
    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    
    except HTTPException:
        if conn:
            conn.rollback()
        raise
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# GET - Get booking by PNR
@router.get("/{pnr}")
def get_booking_by_pnr(pnr: str):
    """Get booking details by PNR"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                b.id, b.pnr, b.flight_id, 
                b.passenger_first_name, b.passenger_last_name,
                b.passenger_email, b.passenger_phone,
                b.seat_number, b.booking_price, b.status,
                b.booking_time, b.payment_status, b.transaction_id,
                f.flight_number, f.airline, f.origin, f.destination,
                f.departure_time, f.arrival_time
            FROM bookings b
            JOIN flights f ON b.flight_id = f.id
            WHERE b.pnr = %s
        """
        
        cursor.execute(query, (pnr.upper(),))
        booking = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        return {
            "success": True,
            "booking": booking
        }
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

# GET - Get all bookings
@router.get("/")
def get_bookings(
    email: Optional[str] = None,
    status: Optional[str] = Query(None, pattern="^(confirmed|cancelled)$")
):
    """Get all bookings with optional filters"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                b.id, b.pnr, b.flight_id,
                CONCAT(b.passenger_first_name, ' ', b.passenger_last_name) as passenger_name,
                b.passenger_email, b.seat_number, b.booking_price,
                b.status, b.booking_time,
                f.flight_number, f.airline, f.origin, f.destination,
                f.departure_time
            FROM bookings b
            JOIN flights f ON b.flight_id = f.id
            WHERE 1=1
        """
        params = []
        
        if email:
            query += " AND b.passenger_email = %s"
            params.append(email)
        
        if status:
            query += " AND b.status = %s"
            params.append(status)
        
        query += " ORDER BY b.booking_time DESC"
        
        cursor.execute(query, params)
        bookings = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "count": len(bookings),
            "bookings": bookings
        }
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

# DELETE - Cancel booking
@router.delete("/{pnr}")
def cancel_booking(pnr: str):
    """Cancel a booking and release the seat"""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        conn.autocommit = False
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT * FROM bookings WHERE pnr = %s FOR UPDATE",
            (pnr.upper(),)
        )
        
        booking = cursor.fetchone()
        
        if not booking:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Booking not found")
        
        if booking['status'] == 'cancelled':
            conn.rollback()
            raise HTTPException(status_code=400, detail="Booking already cancelled")
        
        cursor.execute(
            "SELECT departure_time FROM flights WHERE id = %s",
            (booking['flight_id'],)
        )
        
        flight = cursor.fetchone()
        if flight['departure_time'] < datetime.now():
            conn.rollback()
            raise HTTPException(
                status_code=400,
                detail="Cannot cancel booking for departed flight"
            )
        
        cursor.execute(
            "UPDATE bookings SET status = 'cancelled' WHERE pnr = %s",
            (pnr.upper(),)
        )
        
        cursor.execute(
            "UPDATE flights SET available_seats = available_seats + 1 WHERE id = %s",
            (booking['flight_id'],)
        )
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "message": "Booking cancelled successfully",
            "pnr": pnr.upper(),
            "refund_amount": booking['booking_price']
        }
    
    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    
    except HTTPException:
        if conn:
            conn.rollback()
        raise
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()