# -------------------------------Post booking-----------------------
from fastapi import APIRouter, HTTPException, Depends
from mysql.connector import Error
from .database import get_connection

router = APIRouter()

@router.post("/bookings")
def create_booking(booking: dict, conn = Depends(get_connection)):
    try:
        cursor = conn.cursor()

        query = """
        INSERT INTO bookings (
            flight_id, 
            passenger_first_name,
            passenger_last_name,
            passenger_age,
            passenger_phone,
            travel_date,
            seat_no
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        data = (
            booking["flight_id"],
            booking["passenger"]["first_name"],
            booking["passenger"]["last_name"],
            booking["passenger"]["age"],
            booking["passenger"]["phone"],
            booking["travel_date"],
            booking["seat_no"]
        )

        cursor.execute(query, data)
        conn.commit()

        return {
            "message": "Booking created successfully",
            "booking_id": cursor.lastrowid
        }

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
