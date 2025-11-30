✈️ Flight Booking Simulator – Backend (FastAPI + MySQL)
📌 Overview

This project is the backend for a Flight Booking Simulator.
It supports managing flights, searching flights, creating bookings, updating bookings, and simulating airline operations.

It is built using:

FastAPI – backend API

MySQL – database

Pydantic – validation

Uvicorn – server

Swagger UI – for testing endpoints

This backend is part of Milestone-1 for the project assignment.

🚀 Features Implemented (Milestone 1)
✅ Database Schema (Flights + Bookings)

Flight details

Booking details

Foreign key relations

Timestamp fields

✅ APIs Implemented

Endpoint	            Method	     Description
/flights	            GET	         Retrieve all flights
/flights	            POST	         Create a new flight
/flights/{id}	         PUT	         Update flight details
/bookings	            POST	         Create booking


❤️ Health Check
Method	Endpoint	Description

GET	      /	      API health check + DB connection test

📂 Project Structure

flight-booking-simulator/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── routes_flights.py
│   ├── routes_bookings.py
│
├── Docs/
│   ├── database_schema.sql
│   ├── seed_data.sql
│
├── .gitignore
├── LICENSE
├── README.md
└──

