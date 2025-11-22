# this file Create a reusable MySQL connection for all API routes
# Every backend feature (flights, passengers, bookings) needs to talk to MySQL.

# Instead of writing the connection code again and again,
# we write it ONE time here.


# backend/database.py

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=os.getenv("DB_PASSWORD"),
            database="flight_booking_simulator"
        )
        return connection
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None

    
if __name__ == "__main__":
    conn = get_connection()
    print("Connection:", conn)

