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
