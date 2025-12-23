"""
Automatic Flight Generator
Generates flights dynamically for any future date
"""

from datetime import datetime, timedelta
import random

class FlightGenerator:
    """Generate flights dynamically for any date"""
    
    def __init__(self):
        self.airlines = [
            'Air India', 'IndiGo', 'SpiceJet', 'Vistara', 
            'Go First', 'AirAsia India'
        ]
        
        self.routes = [
            ('BLR', 'DEL'), ('BLR', 'BOM'), ('BLR', 'MAA'),
            ('BLR', 'HYD'), ('BLR', 'CCU'), ('BLR', 'GOI'),
            ('DEL', 'BLR'), ('DEL', 'BOM'), ('DEL', 'MAA'),
            ('BOM', 'BLR'), ('BOM', 'DEL'), ('BOM', 'GOI'),
            ('MAA', 'BLR'), ('MAA', 'DEL'), ('MAA', 'BOM'),
            ('HYD', 'BLR'), ('HYD', 'DEL'), ('HYD', 'BOM'),
            ('CCU', 'BLR'), ('CCU', 'DEL'), ('CCU', 'BOM')
        ]
        
        self.base_prices = {
            'domestic_short': (2500, 4000),    # < 500 km
            'domestic_medium': (4000, 6000),   # 500-1000 km
            'domestic_long': (6000, 10000)     # > 1000 km
        }
        
        self.flight_times = [
            ('06:00', '08:30'), ('07:30', '10:00'),
            ('09:00', '11:30'), ('10:30', '13:00'),
            ('12:00', '14:30'), ('14:00', '16:30'),
            ('16:00', '18:30'), ('18:00', '20:30'),
            ('19:30', '22:00'), ('21:00', '23:30')
        ]
    
    def generate_flight_number(self, airline):
        """Generate realistic flight number"""
        prefixes = {
            'Air India': 'AI',
            'IndiGo': '6E',
            'SpiceJet': 'SG',
            'Vistara': 'UK',
            'Go First': 'G8',
            'AirAsia India': 'I5'
        }
        prefix = prefixes.get(airline, 'XX')
        number = random.randint(100, 999)
        return f"{prefix}{number}"
    
    def calculate_duration(self, origin, destination):
        """Calculate approximate flight duration in minutes"""
        # Simplified distance-based duration
        distances = {
            ('BLR', 'DEL'): 150, ('BLR', 'BOM'): 105, ('BLR', 'MAA'): 60,
            ('BLR', 'HYD'): 75, ('BLR', 'CCU'): 165, ('BLR', 'GOI'): 75,
            ('DEL', 'BLR'): 150, ('DEL', 'BOM'): 120, ('DEL', 'MAA'): 165,
            ('BOM', 'BLR'): 105, ('BOM', 'DEL'): 120, ('BOM', 'GOI'): 60,
        }
        return distances.get((origin, destination), 120)
    
    def get_base_price(self, origin, destination):
        """Get base price for route"""
        duration = self.calculate_duration(origin, destination)
        
        if duration < 90:
            price_range = self.base_prices['domestic_short']
        elif duration < 150:
            price_range = self.base_prices['domestic_medium']
        else:
            price_range = self.base_prices['domestic_long']
        
        return random.randint(price_range[0], price_range[1])
    
    def generate_flights_for_route(self, origin, destination, date_str, num_flights=3):
        """Generate multiple flights for a specific route and date"""
        flights = []
        date = datetime.strptime(date_str, '%Y-%m-%d')
        
        # Select random flight times
        selected_times = random.sample(self.flight_times, min(num_flights, len(self.flight_times)))
        
        for dep_time, arr_time in selected_times:
            airline = random.choice(self.airlines)
            flight_number = self.generate_flight_number(airline)
            
            # Parse times
            dep_hour, dep_min = map(int, dep_time.split(':'))
            arr_hour, arr_min = map(int, arr_time.split(':'))
            
            departure_datetime = date.replace(hour=dep_hour, minute=dep_min, second=0)
            arrival_datetime = date.replace(hour=arr_hour, minute=arr_min, second=0)
            
            # If arrival is next day
            if arrival_datetime <= departure_datetime:
                arrival_datetime += timedelta(days=1)
            
            base_price = self.get_base_price(origin, destination)
            total_seats = random.choice([150, 164, 180, 186, 189])
            available_seats = random.randint(int(total_seats * 0.4), total_seats)
            
            flight = {
                'flight_number': flight_number,
                'airline': airline,
                'origin': origin.upper(),
                'destination': destination.upper(),
                'departure_time': departure_datetime,
                'arrival_time': arrival_datetime,
                'base_price': base_price,
                'current_price': base_price,
                'total_seats': total_seats,
                'available_seats': available_seats,
                'demand_level': random.choice(['low', 'medium', 'high'])
            }
            
            flights.append(flight)
        
        return flights
    
    def generate_flights_for_date(self, date_str, origin=None, destination=None):
        """Generate flights for a specific date, optionally filtered by route"""
        all_flights = []
        
        if origin and destination:
            # Generate for specific route
            flights = self.generate_flights_for_route(origin, destination, date_str, num_flights=5)
            all_flights.extend(flights)
        else:
            # Generate for all routes
            for route_origin, route_destination in random.sample(self.routes, 10):
                flights = self.generate_flights_for_route(
                    route_origin, route_destination, date_str, num_flights=2
                )
                all_flights.extend(flights)
        
        return all_flights