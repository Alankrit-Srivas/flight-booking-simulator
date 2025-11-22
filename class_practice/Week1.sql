-- Active: 1763825441119@@127.0.0.1@3306@mysql

-- week 1 practice work
CREATE TABLE airports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airport_code VARCHAR(10) UNIQUE,
    airport_name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50)
);

SELECT * FROM airports;




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



CREATE TABLE flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(10),
    origin VARCHAR(50),
    destination VARCHAR(50),
    departure_time DATETIME,
    arrival_time DATETIME,
    base_fare INT,
    total_seats INT,
    seats_available INT
);

-- SELECT * FROM flights



-- Active: 1763203284113@@127.0.0.1@3306@flight_booking_simulator
CREATE TABLE passengers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    passport_number VARCHAR(20)
);




INSERT INTO flights (flight_number, origin, destination, departure_time, arrival_time, base_fare, total_seats, seats_available)
VALUES
('AI101', 'Delhi', 'Mumbai', '2025-01-01 10:00:00', '2025-01-01 12:00:00', 5000, 180, 120),
('6E202', 'Mumbai', 'Bangalore', '2025-01-02 09:00:00', '2025-01-02 11:00:00', 6000, 160, 80),
('SG303', 'Chennai', 'Kolkata', '2025-01-03 14:00:00', '2025-01-03 17:00:00', 4500, 150, 75);



INSERT INTO passengers (first_name, last_name, email, phone, passport_number)
VALUES
('Amit', 'Sharma', 'amit@example.com', '9876543210', 'P12345'),
('Sneha', 'Patil', 'sneha@example.com', '9988776655', 'P67890'),
('Rahul', 'Verma', 'rahul@example.com', '9898989898', 'P24680');


INSERT INTO bookings (passenger_id, flight_id, seats_booked, total_price)
VALUES
(1, 1, 1, 5000),
(2, 2, 2, 12000),
(3, 3, 1, 4500);


INSERT INTO airports (airport_code, airport_name, city, country)
VALUES
('DEL', 'Indira Gandhi International Airport', 'Delhi', 'India'),
('BOM', 'Chhatrapati Shivaji Maharaj International Airport', 'Mumbai', 'India'),
('BLR', 'Kempegowda International Airport', 'Bangalore', 'India'),
('MAA', 'Chennai International Airport', 'Chennai', 'India');
