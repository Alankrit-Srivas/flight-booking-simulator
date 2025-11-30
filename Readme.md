# Flight Booking Simulator

A mini project demonstrating a complete flight reservation system including database design, SQL operations, ER diagrams, and backend integration.

---

## Project Overview

This system manages:

- Flights  
- Passengers  
- Airports  
- Bookings  

The database supports flight search, seat availability tracking, booking management, and fare calculations.

---

## Folder Structure

flight-booking-simulator/
│
├── database/ # SQL scripts (tables + data)
├── docs/ # ER diagrams + reports (future)
├── backend/ # Backend code (future)
├── frontend/ # Frontend UI (optional)
│
└── README.md # Main project description


---

## Database Schema (Summary)

- **flights** → Stores flight details  
- **passengers** → Stores passenger information  
- **airports** → Airport master data  
- **bookings** → Maps passengers ↔ flights using foreign keys  

---

## How To Run SQL

1. Open MySQL Workbench or VS Code SQL Tools  
2. Run each file in `/database/`  
3. Insert sample data using `insert_sample_data.sql`

---


# ✈️ Flight Booking Simulator – Backend (Week 1)

This project is a **Flight Booking Simulator Backend** built using **FastAPI + MySQL**.  
The goal of Week-1 is to set up the backend structure, configure the database, and implement
basic CRUD APIs for flights and basic booking creation.

---

## 📌 Week-1 Deliverables (Completed ✅)

### ✔️ 1. Database Setup  
Database: `flight_booking_simulator`

**Tables implemented:**

#### **flights**
| Column | Type |
|--------|------|
| id | INT (PK, Auto Increment) |
| flight_number | VARCHAR(20) |
| origin | VARCHAR(50) |
| destination | VARCHAR(50) |
| departure_time | DATETIME |
| arrival_time | DATETIME |
| price | DECIMAL(10,2) |

#### **bookings**
| Column | Type |
|--------|------|
| id | INT (PK, Auto Increment) |
| flight_id | INT (FK → flights.id) |
| passenger_first_name | VARCHAR(50) |
| passenger_last_name | VARCHAR(50) |
| passenger_age | INT |
| passenger_phone | BIGINT |
| travel_date | DATE |
| seat_no | VARCHAR(10) |
| created_at | TIMESTAMP |

---

## ✔️ 2. Backend Setup

Project structure:

```
backend/
│── main.py
│── database.py
│── routes_flights.py
│── routes_bookings.py
│── .env
```

---

## ✔️ 3. API Endpoints (Week-1)

### ✈️ **FLIGHTS MODULE**

#### **POST /flights**
Create a flight  
Request body sample:
```json
{
  "flight_number": "AI202",
  "origin": "Delhi",
  "destination": "Mumbai",
  "departure_time": "2025-01-02 10:00:00",
  "arrival_time": "2025-01-02 12:00:00",
  "price": 5999
}
```

#### **GET /flights**
Fetch all flights

#### **PUT /flights/{id}**
Update an existing flight

---

### 🧾 **BOOKINGS MODULE**

#### **POST /bookings**
Create a booking for a flight  
Sample request:
```json
{
  "flight_id": 1,
  "passenger": {
    "first_name": "John",
    "last_name": "Doe",
    "age": 25,
    "phone": 9876543210
  },
  "travel_date": "2025-01-02",
  "seat_no": "A1"
}
```

---

## ✔️ 4. Environment Variables (.env)
```
DB_PASSWORD=your_mysql_password
```

---

## ✔️ 5. How to Run the Project

### **1. Install dependencies**
```
pip install fastapi uvicorn mysql-connector-python python-dotenv
```

### **2. Start FastAPI server**
```
uvicorn backend.main:app --reload
```

### **3. Open API Docs**
```
http://127.0.0.1:8000/docs
```

---

## 📸 Screenshots (Add in submission)

- Swagger UI running  
- POST /flights response  
- GET /flights response  
- POST /bookings response  
- MySQL tables

---

## 📌 Completed in Week-1 (Summary)

- FastAPI backend project setup  
- MySQL database created  
- Flights table + CRUD APIs  
- Bookings table + booking creation API  
- All APIs tested successfully in Swagger  
- Code pushed to GitHub  

---

## 📅 Next Steps (Week-2 Preview)

- GET /bookings  
- DELETE /bookings  
- Join flights + bookings  
- Seat availability logic  
- Search flights API  
- Better validation using Pydantic models  
- Frontend UI integration  

---

## 👨‍💻 Author
A S 
Flight Booking Simulator – Backend  
Springboard Software Engineering Bootcamp
