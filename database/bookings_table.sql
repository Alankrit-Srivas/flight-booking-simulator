CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    passenger_id INT,
    flight_id INT,
    booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    seats_booked INT,
    total_price INT,

    FOREIGN KEY (passenger_id) REFERENCES passengers(id),
    FOREIGN KEY (flight_id) REFERENCES flights(id)


    -- A "FOREIGN KEY" is a sql constraints used to link 2 tables together.(for my reference)
    -- why needed ?-- to prevent unauthorized entry(so, lets say if in this table we add passenger_id = 10 so, it will first check to passengers table if there the id is not present it will not accept that entry)--it is K/A Referential Integrity

    -- PK = Unique(no Dublicates but accept null values)  + not null(no null values but dublicates)

    -- 

    -- as booking depends on passenger and the flights so it connects two other table

    -- ONLY bookings table needs these connections

    -- Because it is a relationship table between:

    -- Passenger  ↔  Booking  ↔  Flight


    -- JOIN's requirement:

    -- Flight search

    -- Booking details

    -- Passenger details

    -- Admin view

    -- Reports

    -- Analytics


    -- ✅ JOIN 1: Passenger + Booking + Flight (Master JOIN)
    SELECT 
    bookings.id AS booking_id,
    passengers.first_name,
    passengers.last_name,
    flights.flight_number,
    flights.origin,
    flights.destination,
    bookings.seats_booked,
    bookings.total_price,
    bookings.booking_date
    FROM bookings
    JOIN passengers ON bookings.passenger_id = passengers.id
    JOIN flights ON bookings.flight_id = flights.id;

    -- ✅ JOIN 2: Flights + Airports (Origin Airport Info)
    SELECT 
    flights.flight_number,
    airports.airport_name AS origin_airport,
    airports.city AS origin_city
    FROM flights
    JOIN airports ON flights.origin = airports.city;

    -- ✅ JOIN 3: Flights + Airports (Destination Airport Info)

    SELECT 
    flights.flight_number,
    airports.airport_name AS destination_airport,
    airports.city AS destination_city
    FROM flights
    JOIN airports ON flights.destination = airports.city;

    -- ⚡ JOIN COMBINED (Origin + Destination in one query)

    SELECT
    f.flight_number,
    a1.airport_name AS origin_airport,
    a2.airport_name AS destination_airport,
    f.departure_time,
    f.arrival_time,
    f.base_fare
    FROM flights f
    JOIN airports a1 ON f.origin = a1.city
    JOIN airports a2 ON f.destination = a2.city;






    -- A "JOIN" allows you to combine data from multiple tables into one single result.

    -- As all are table are connected so we need this 

    --  And we have to show all these info to a screen line |--“Show all bookings with passenger name + flight details” 
    -- so we have to join these tables (passengers + bookings + flights)

    -- 🔹 “Show airports with all flights”
    -- → JOIN airports + flights

    -- 🔹 “Show booking history of a passenger”
    -- → JOIN passengers + bookings

    -- 🔹 “Show flights from city A to city B”
    -- → JOIN airports + flights





);

-- SELECT * FROM bookings;
SELECT * FROM passengers;
SELECT * FROM flights;
SELECT * FROM bookings;
