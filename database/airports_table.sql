CREATE TABLE airports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airport_code VARCHAR(10) UNIQUE,
    airport_name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50)
);

SELECT * FROM airports;