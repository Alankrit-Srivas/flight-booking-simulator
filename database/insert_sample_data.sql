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
