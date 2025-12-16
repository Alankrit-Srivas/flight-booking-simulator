-- Flight Booking Simulator - Complete Database Schema
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS flights;

-- Flights Table
CREATE TABLE flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(10) NOT NULL,
    airline VARCHAR(50) NOT NULL,
    origin VARCHAR(3) NOT NULL,
    destination VARCHAR(3) NOT NULL,
    departure_time DATETIME NOT NULL,
    arrival_time DATETIME NOT NULL,
    base_price DECIMAL(10, 2) NOT NULL,
    current_price DECIMAL(10, 2) NOT NULL,
    total_seats INT NOT NULL,
    available_seats INT NOT NULL,
    demand_level ENUM('low', 'medium', 'high', 'very_high') DEFAULT 'medium',
    status ENUM('scheduled', 'delayed', 'cancelled', 'completed') DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_origin (origin),
    INDEX idx_destination (destination),
    INDEX idx_flight_number (flight_number)
);

-- Bookings Table
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pnr VARCHAR(6) NOT NULL UNIQUE,
    flight_id INT NOT NULL,
    
    passenger_first_name VARCHAR(50) NOT NULL,
    passenger_last_name VARCHAR(50) NOT NULL,
    passenger_email VARCHAR(100) NOT NULL,
    passenger_phone VARCHAR(15) NOT NULL,
    passenger_age INT NOT NULL,
    passenger_gender ENUM('male', 'female', 'other') NOT NULL,
    
    seat_number VARCHAR(10),
    booking_price DECIMAL(10, 2) NOT NULL,
    status ENUM('confirmed', 'cancelled', 'pending') DEFAULT 'pending',
    
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    transaction_id VARCHAR(100),
    
    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP NULL,
    
    FOREIGN KEY (flight_id) REFERENCES flights(id) ON DELETE RESTRICT,
    
    INDEX idx_pnr (pnr),
    INDEX idx_flight_id (flight_id),
    INDEX idx_passenger_email (passenger_email),
    INDEX idx_booking_time (booking_time)
);

-- Insert Sample Flights
INSERT INTO flights (
    flight_number, airline, origin, destination, 
    departure_time, arrival_time, 
    base_price, current_price, 
    total_seats, available_seats, 
    demand_level
) VALUES
('AI101', 'Air India', 'BLR', 'DEL', '2025-01-20 06:00:00', '2025-01-20 08:30:00', 4500.00, 4500.00, 180, 180, 'medium'),
('6E202', 'IndiGo', 'BLR', 'BOM', '2025-01-20 09:00:00', '2025-01-20 10:45:00', 3800.00, 3800.00, 186, 186, 'medium'),
('SG303', 'SpiceJet', 'DEL', 'BLR', '2025-01-21 11:30:00', '2025-01-21 14:00:00', 4200.00, 4200.00, 189, 189, 'low'),
('UK404', 'Vistara', 'BOM', 'BLR', '2025-01-21 15:00:00', '2025-01-21 16:45:00', 5000.00, 5000.00, 164, 164, 'high'),
('AI505', 'Air India', 'BLR', 'MAA', '2025-01-22 07:00:00', '2025-01-22 08:00:00', 2500.00, 2500.00, 180, 180, 'medium'),
('6E606', 'IndiGo', 'BLR', 'HYD', '2025-01-22 10:00:00', '2025-01-22 11:15:00', 2800.00, 2800.00, 186, 186, 'medium'),
('SG707', 'SpiceJet', 'BLR', 'CCU', '2025-01-23 13:00:00', '2025-01-23 15:45:00', 5500.00, 5500.00, 189, 189, 'low'),
('AI102', 'Air India', 'DEL', 'BLR', '2025-01-23 19:00:00', '2025-01-23 21:30:00', 4500.00, 4500.00, 180, 175, 'high'),
('6E203', 'IndiGo', 'BOM', 'BLR', '2025-01-24 20:00:00', '2025-01-24 2