"""
Dynamic Pricing Engine for Flight Booking Simulator
"""

from datetime import datetime, timedelta
from typing import Dict
import random

class PricingEngine:
    """Calculate dynamic flight prices based on multiple factors"""
    
    def __init__(self):
        self.config = {
            "max_price_multiplier": 3.0,
            "min_price_multiplier": 0.8,
            "seat_weight": 0.4,
            "time_weight": 0.35,
            "demand_weight": 0.25
        }
    
    def calculate_price(
        self,
        base_price: float,
        total_seats: int,
        available_seats: int,
        departure_time: datetime,
        demand_level: str = "medium"
    ) -> Dict:
        """Calculate dynamic price based on multiple factors"""

        # Convert to float if Decimal
        base_price = float(base_price)
        
        seat_multiplier = self._calculate_seat_factor(total_seats, available_seats)
        time_multiplier = self._calculate_time_factor(departure_time)
        demand_multiplier = self._calculate_demand_factor(demand_level)
        
        total_multiplier = (
            seat_multiplier * self.config["seat_weight"] +
            time_multiplier * self.config["time_weight"] +
            demand_multiplier * self.config["demand_weight"]
        )
        
        total_multiplier = max(
            self.config["min_price_multiplier"],
            min(total_multiplier, self.config["max_price_multiplier"])
        )
        
        current_price = round(base_price * total_multiplier, 2)
        
        return {
            "current_price": current_price,
            "base_price": base_price,
            "total_multiplier": round(total_multiplier, 2),
            "breakdown": {
                "seat_factor": round(seat_multiplier, 2),
                "time_factor": round(time_multiplier, 2),
                "demand_factor": round(demand_multiplier, 2)
            },
            "percentage_increase": round((total_multiplier - 1) * 100, 1)
        }
    
    def _calculate_seat_factor(self, total_seats: int, available_seats: int) -> float:
        """Calculate price multiplier based on seat availability"""
        if available_seats <= 0:
            return 3.0
        
        occupancy_rate = (total_seats - available_seats) / total_seats
        
        if occupancy_rate < 0.2:
            return 0.8 + (occupancy_rate * 1.0)
        elif occupancy_rate < 0.6:
            return 1.0 + ((occupancy_rate - 0.2) * 1.25)
        elif occupancy_rate < 0.9:
            return 1.5 + ((occupancy_rate - 0.6) * 3.33)
        else:
            return 2.5 + ((occupancy_rate - 0.9) * 5.0)
    
    def _calculate_time_factor(self, departure_time: datetime) -> float:
        """Calculate price multiplier based on time until departure"""
        now = datetime.now()
        time_delta = departure_time - now
        
        if time_delta.total_seconds() < 0:
            return 3.0
        
        days_until_departure = time_delta.total_seconds() / 86400
        
        if days_until_departure > 30:
            return 0.8
        elif days_until_departure > 15:
            return 0.8 + ((30 - days_until_departure) / 15) * 0.2
        elif days_until_departure > 7:
            return 1.0 + ((15 - days_until_departure) / 8) * 0.3
        elif days_until_departure > 3:
            return 1.3 + ((7 - days_until_departure) / 4) * 0.4
        elif days_until_departure > 1:
            return 1.7 + ((3 - days_until_departure) / 2) * 0.8
        else:
            return 2.5 + ((1 - days_until_departure) * 0.5)
    
    def _calculate_demand_factor(self, demand_level: str) -> float:
        """Calculate price multiplier based on simulated demand"""
        demand_multipliers = {
            "low": 0.9,
            "medium": 1.0,
            "high": 1.4,
            "very_high": 2.0
        }
        return demand_multipliers.get(demand_level.lower(), 1.0)
    
    def simulate_demand_shift(self) -> str:
        """Simulate demand level changes randomly"""
        weights = {
            "low": 0.2,
            "medium": 0.5,
            "high": 0.2,
            "very_high": 0.1
        }
        demand_levels = list(weights.keys())
        probabilities = list(weights.values())
        return random.choices(demand_levels, weights=probabilities)[0]

def batch_update_prices(cursor, connection):
    """Update all flight prices based on current conditions"""
    engine = PricingEngine()
    
    cursor.execute("""
        SELECT id, base_price, total_seats, available_seats, 
               departure_time, demand_level
        FROM flights
        WHERE departure_time > NOW()
    """)
    
    flights = cursor.fetchall()
    updated_count = 0
    
    for flight in flights:
        flight_id, base_price, total_seats, available_seats, departure_time, demand_level = flight
        
        if random.random() < 0.1:
            demand_level = engine.simulate_demand_shift()
            cursor.execute(
                "UPDATE flights SET demand_level = %s WHERE id = %s",
                (demand_level, flight_id)
            )
        
        pricing = engine.calculate_price(
            base_price=base_price,
            total_seats=total_seats,
            available_seats=available_seats,
            departure_time=departure_time,
            demand_level=demand_level or "medium"
        )
        
        cursor.execute(
            "UPDATE flights SET current_price = %s WHERE id = %s",
            (pricing["current_price"], flight_id)
        )
        updated_count += 1
    
    connection.commit()
    return updated_count