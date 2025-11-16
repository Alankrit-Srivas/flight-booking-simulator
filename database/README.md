# Database Schema — Flight Booking Simulator

This folder contains all SQL scripts required to build and populate the database.

---

## 1. `flights_table.sql`
Creates the `flights` table with:

- flight number  
- origin  
- destination  
- departure time  
- arrival time  
- base fare  
- total seats  
- seats available  

---

## 2. `passengers_table.sql`
Stores passenger details:

- name  
- email  
- phone number  

---

## 3. `airports_table.sql`
Stores airport master data:

- airport code  
- airport name  
- city  
- country  

---

## 4. `bookings_table.sql`
Maps passengers to flights using **foreign keys**:

- passenger_id → passengers.id  
- flight_id → flights.id  

Ensures **relational integrity** in the database.

---

## 5. `insert_sample_data.sql`
Contains sample flight, passenger, airport, and booking records  
for testing queries.

---

## How to Use

1. Run the table creation scripts **in this order**:  
   - airports_table.sql  
   - flights_table.sql  
   - passengers_table.sql  
   - bookings_table.sql  

2. Then run `insert_sample_data.sql`.

Your database is now ready for backend integration.
