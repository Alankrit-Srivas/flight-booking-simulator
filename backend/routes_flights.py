from fastapi import APIRouter, Depends, HTTPException
from backend.database import get_connection
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import random

router = APIRouter()


# ---------- Pydantic models ----------

class FlightCreate(BaseModel):
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price: float              # base fare
    total_seats: int = 100    # capacity
    available_seats: int = 100
    demand_level: int = 50    # 0–100


class FlightUpdate(BaseModel):
    flight_number: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    price: Optional[float] = None
    total_seats: Optional[int] = None
    available_seats: Optional[int] = None
    demand_level: Optional[int] = None


# ---------- Dynamic pricing helper ----------

def calculate_dynamic_price(flight: Dict) -> float:
    """
    Compute dynamic price based on:
    - base price (flight['price'])
    - remaining seat percentage
    - time until departure
    - demand_level
    """
    base_price = float(flight["price"])

    total_seats = flight.get("total_seats") or 100
    available_seats = flight.get("available_seats") or total_seats

    remaining_ratio = available_seats / total_seats if total_seats > 0 else 1.0
    remaining_percent = remaining_ratio * 100

    # Seat factor: fewer seats -> higher price
    if remaining_percent <= 20:
        seat_factor = 1.5
    elif remaining_percent <= 50:
        seat_factor = 1.2
    else:
        seat_factor = 1.0

    # Time factor: closer to departure -> higher price
    now = datetime.now()
    departure_time = flight["departure_time"]
    if isinstance(departure_time, str):
        departure_time = datetime.fromisoformat(departure_time)

    delta_days = max((departure_time - now).total_seconds() / 86400, 0)

    if delta_days <= 1:
        time_factor = 1.5
    elif delta_days <= 7:
        time_factor = 1.2
    else:
        time_factor = 1.0

    # Demand factor: based on demand_level (0–100)
    demand_level = flight.get("demand_level", 50)
    # Map 0–100 -> 0.8–1.2 range roughly
    demand_factor = 0.8 + (demand_level / 100) * 0.4

    dynamic_price = base_price * seat_factor * time_factor * demand_factor

    return round(dynamic_price, 2)


def attach_dynamic_price(rows: List[Dict]) -> List[Dict]:
    """
    For each DB row, add dynamic_price and factors for debugging.
    """
    now = datetime.now()
    for f in rows:
        total_seats = f.get("total_seats") or 100
        available_seats = f.get("available_seats") or total_seats
        remaining_ratio = available_seats / total_seats if total_seats > 0 else 1.0
        remaining_percent = remaining_ratio * 100

        departure_time = f["departure_time"]
        if isinstance(departure_time, str):
            departure_time = datetime.fromisoformat(departure_time)
        delta_days = max((departure_time - now).total_seconds() / 86400, 0)

        demand_level = f.get("demand_level", 50)

        # same factors as calculate_dynamic_price
        if remaining_percent <= 20:
            seat_factor = 1.5
        elif remaining_percent <= 50:
            seat_factor = 1.2
        else:
            seat_factor = 1.0

        if delta_days <= 1:
            time_factor = 1.5
        elif delta_days <= 7:
            time_factor = 1.2
        else:
            time_factor = 1.0

        demand_factor = 0.8 + (demand_level / 100) * 0.4

        f["dynamic_price"] = round(float(f["price"]) * seat_factor * time_factor * demand_factor, 2)
        f["remaining_seat_percent"] = round(remaining_percent, 1)
        f["days_until_departure"] = round(delta_days, 1)
        f["demand_level"] = demand_level

    return rows


# ---------- Basic endpoints ----------

@router.get("/flights")
def get_all_flights(conn=Depends(get_connection)):
    """
    Get all flights with dynamic pricing info.
    """
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                id,
                flight_number,
                origin,
                destination,
                departure_time,
                arrival_time,
                price,
                total_seats,
                available_seats,
                demand_level,
                TIMESTAMPDIFF(MINUTE, departure_time, arrival_time) AS duration
            FROM flights
            """
        )
        rows = cursor.fetchall()
        rows = attach_dynamic_price(rows)
        return {"results": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flights")
def create_flight(flight: FlightCreate, conn=Depends(get_connection)):
    """
    Create a new flight (with base price, seats, and demand level).
    """
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO flights
                (flight_number, origin, destination, departure_time, arrival_time,
                 price, total_seats, available_seats, demand_level)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            flight.flight_number,
            flight.origin,
            flight.destination,
            flight.departure_time,
            flight.arrival_time,
            flight.price,
            flight.total_seats,
            flight.available_seats,
            flight.demand_level,
        )
        cursor.execute(query, data)
        conn.commit()

        return {
            "message": "Flight created successfully",
            "flight_id": cursor.lastrowid,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/flights/{flight_id}")
def update_flight(
    flight_id: int,
    flight: FlightUpdate,
    conn=Depends(get_connection),
):
    """
    Update an existing flight (partial update).
    """
    try:
        cursor = conn.cursor(dictionary=True)

        fields = []
        params = []

        if flight.flight_number is not None:
            fields.append("flight_number = %s")
            params.append(flight.flight_number)
        if flight.origin is not None:
            fields.append("origin = %s")
            params.append(flight.origin)
        if flight.destination is not None:
            fields.append("destination = %s")
            params.append(flight.destination)
        if flight.departure_time is not None:
            fields.append("departure_time = %s")
            params.append(flight.departure_time)
        if flight.arrival_time is not None:
            fields.append("arrival_time = %s")
            params.append(flight.arrival_time)
        if flight.price is not None:
            fields.append("price = %s")
            params.append(flight.price)
        if flight.total_seats is not None:
            fields.append("total_seats = %s")
            params.append(flight.total_seats)
        if flight.available_seats is not None:
            fields.append("available_seats = %s")
            params.append(flight.available_seats)
        if flight.demand_level is not None:
            fields.append("demand_level = %s")
            params.append(flight.demand_level)

        if not fields:
            raise HTTPException(status_code=400, detail="No fields provided to update")

        query = f"UPDATE flights SET {', '.join(fields)} WHERE id = %s"
        params.append(flight_id)

        cursor.execute(query, tuple(params))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Flight not found")

        return {"message": "Flight updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- Search with dynamic pricing ----------

@router.get("/flights/search")
def search_flights(
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    date: Optional[str] = None,   # YYYY-MM-DD
    sort: Optional[str] = "price", # price or duration or dynamic_price
    conn=Depends(get_connection),
):
    """
    Search flights by origin, destination, date and sort by price/duration/dynamic price.
    """
    try:
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            id,
            flight_number,
            origin,
            destination,
            departure_time,
            arrival_time,
            price,
            total_seats,
            available_seats,
            demand_level,
            TIMESTAMPDIFF(MINUTE, departure_time, arrival_time) AS duration
        FROM flights
        WHERE 1 = 1
        """
        params = []

        if origin:
            query += " AND origin = %s"
            params.append(origin)

        if destination:
            query += " AND destination = %s"
            params.append(destination)

        if date:
            query += " AND DATE(departure_time) = %s"
            params.append(date)

        # initial DB-level sort (on static fields)
        if sort == "price":
            query += " ORDER BY price ASC"
        elif sort == "duration":
            query += " ORDER BY duration ASC"
        else:
            query += " ORDER BY price ASC"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        rows = attach_dynamic_price(rows)

        # sort in Python if required by dynamic_price
        if sort == "dynamic_price":
            rows.sort(key=lambda f: f["dynamic_price"])

        return {
            "filters_used": {
                "origin": origin,
                "destination": destination,
                "date": date,
                "sort": sort,
            },
            "results": rows,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- Simulated airline sync (M1 feature, still useful) ----------

@router.post("/flights/sync-airlines")
def sync_airline_data(conn=Depends(get_connection)):
    """
    Simulates external airline API by randomly updating base prices.
    """
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT id, price FROM flights ORDER BY RAND() LIMIT 1")
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="No flights to update")

        flight_id, old_price = row
        new_price = float(old_price) + random.randint(-200, 500)
        if new_price < 500:
            new_price = 500

        cursor.execute("UPDATE flights SET price=%s WHERE id=%s", (new_price, flight_id))
        conn.commit()

        return {
            "message": "Airline data sync completed",
            "updated_flight_id": flight_id,
            "old_price": float(old_price),
            "new_base_price": new_price,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
