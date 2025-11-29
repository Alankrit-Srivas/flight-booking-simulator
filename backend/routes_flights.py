from fastapi import APIRouter, HTTPException, Depends
from mysql.connector import Error
from .database import get_connection

router = APIRouter()


# ------------------- POST: Create Flight -------------------

@router.post("/flights")
def create_flight(flight: dict, conn = Depends(get_connection)):
    try:
        cursor = conn.cursor()

        query = """
        INSERT INTO flights (flight_number, origin, destination, departure_time, arrival_time, price)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        data = (
            flight["flight_number"],
            flight["origin"],
            flight["destination"],
            flight["departure_time"],
            flight["arrival_time"],
            flight["price"]
        )

        cursor.execute(query, data)
        conn.commit()

        return {"message": "Flight inserted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# ------------------- POST: Create Flight -------------------

@router.get("/flights")
def get_flights(conn = Depends(get_connection)):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM flights")
        flights = cursor.fetchall()
        return flights

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# ------------------- PUT: Update Flight -------------------
@router.put("/flights/{flight_id}")
def update_flight(flight_id: int, flight: dict, conn = Depends(get_connection)):
    try:
        cursor = conn.cursor()

        query = """
        UPDATE flights
        SET flight_number=%s, origin=%s, destination=%s, departure_time=%s, arrival_time=%s, price=%s
        WHERE id=%s
        """

        data = (
            flight["flight_number"],
            flight["origin"],
            flight["destination"],
            flight["departure_time"],
            flight["arrival_time"],
            flight["price"],
            flight_id
        )

        cursor.execute(query, data)
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Flight not found")

        return {"message": "Flight updated successfully"}

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    

