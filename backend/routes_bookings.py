from fastapi import APIRouter, Depends, HTTPException
from backend.database import get_connection
from mysql.connector import Error
from typing import Dict

router = APIRouter()


@router.post("/bookings")
def create_booking(booking: Dict, conn=Depends(get_connection)):
    """
    Create a booking and reduce available_seats for that flight.
    Expects:
    - flight_id
    - passenger_first_name, passenger_last_name, passenger_age, passenger_phone
    - travel_date (YYYY-MM-DD)
    - seat_no
    """
    try:
        cursor = conn.cursor(dictionary=True)

        flight_id = booking["flight_id"]

        # Check seats availability
        cursor.execute(
            "SELECT available_seats, total_seats FROM flights WHERE id=%s", (flight_id,)
        )
        flight = cursor.fetchone()

        if not flight:
            raise HTTPException(status_code=404, detail="Flight not found")

        if flight["available_seats"] <= 0:
            raise HTTPException(status_code=400, detail="No seats available on this flight")

        # Insert booking
        insert_cursor = conn.cursor()
        insert_query = """
            INSERT INTO bookings
                (flight_id, passenger_first_name, passenger_last_name, passenger_age,
                 passenger_phone, travel_date, seat_no)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        insert_data = (
            booking["flight_id"],
            booking.get["passenger_first_name"],
            booking.get["passenger_last_name"],
            booking.get("passenger_age"),
            booking.get("passenger_phone"),
            booking["travel_date"],
            booking.get("seat_no"),
        )
        insert_cursor.execute(insert_query, insert_data)

        # Decrease available seats
        update_cursor = conn.cursor()
        update_cursor.execute(
            "UPDATE flights SET available_seats = available_seats - 1 WHERE id=%s",
            (flight_id,),
        )

        conn.commit()

        return {
            "message": "Booking created successfully",
            "booking_id": insert_cursor.lastrowid,
        }

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
