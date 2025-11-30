CREATE TABLE flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(20) NOT NULL,
    origin VARCHAR(50) NOT NULL,
    destination VARCHAR(50) NOT NULL,
    departure_time DATETIME NOT NULL,
    arrival_time DATETIME NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_id INT NOT NULL,
    passenger_first_name VARCHAR(50),
    passenger_last_name VARCHAR(50),
    passenger_age INT,
    passenger_phone BIGINT,
    travel_date DATE NOT NULL,
    seat_no VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (flight_id) REFERENCES flights(id)
);
