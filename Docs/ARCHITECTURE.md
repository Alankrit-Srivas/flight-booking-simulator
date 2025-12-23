# 🏗️ System Architecture

## Overview

The Flight Booking Simulator follows a **3-tier architecture**:
```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│                  (Browser / API Client)                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                        │
│                        (FastAPI)                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Routes    │  │   Pricing    │  │    Database      │  │
│  │   Handler   │→ │   Engine     │→ │    Manager       │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       DATA LAYER                             │
│                     (MySQL Database)                         │
│              ┌────────┐        ┌──────────┐                │
│              │ Flights│───────→│ Bookings │                │
│              └────────┘        └──────────┘                │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Components Breakdown

### 1️⃣ **main.py** - Application Entry Point
**Purpose:** Initializes and configures the FastAPI application

**What it does:**
- Creates FastAPI application instance
- Configures CORS (Cross-Origin Resource Sharing)
- Registers route handlers (flights & bookings)
- Provides health check endpoint
- Sets up startup/shutdown events
- Configures API documentation (Swagger UI)

**Key Code Flow:**
```python
app = FastAPI()
    ↓
Configure CORS
    ↓
Register routes (/api/flights, /api/bookings)
    ↓
Start Uvicorn server on port 8000
```

**When it runs:**
- Application startup
- Loads all route handlers
- Connects to database
- Starts listening for HTTP requests

---

### 2️⃣ **database.py** - Database Connection Manager
**Purpose:** Manages MySQL database connections

**What it does:**
- Reads database credentials from `.env` file
- Creates database connection pool
- Provides `get_db_connection()` function
- Tests database connectivity
- Handles connection errors gracefully

**Key Functions:**

**`get_db_connection()`**
```python
Purpose: Create and return MySQL connection
Input: None (reads from .env)
Output: MySQL connection object
Used by: All route handlers
```

**`test_connection()`**
```python
Purpose: Verify database is accessible
Input: None
Output: True/False
Used by: Startup checks, testing
```

**Connection Flow:**
```
Request comes in
    ↓
get_db_connection() called
    ↓
MySQL connection created
    ↓
Execute queries
    ↓
Close connection
```

---

### 3️⃣ **routes_flights.py** - Flight Management
**Purpose:** Handles all flight-related API operations

**Endpoints & What They Do:**

#### **GET /api/flights**
```
Input: Optional filters (origin, destination, date, sort_by, order)
Process:
  1. Build SQL query with WHERE clauses
  2. Apply filters (origin/destination/date)
  3. Sort results (price/duration/departure)
  4. Execute query
Output: List of matching flights

Example:
GET /api/flights?origin=BLR&destination=DEL&sort_by=price
→ Returns all BLR to DEL flights sorted by price
```

#### **GET /api/flights/{id}**
```
Input: Flight ID
Process:
  1. Query flight by ID
  2. Calculate duration
  3. Return full details
Output: Single flight object or 404 error
```

#### **POST /api/flights**
```
Input: Flight data (JSON)
Process:
  1. Validate input (Pydantic)
  2. Check departure < arrival
  3. Check available_seats <= total_seats
  4. Insert into database
  5. Return new flight ID
Output: Success message + flight_id
```

#### **PUT /api/flights/{id}**
```
Input: Flight ID + updated fields
Process:
  1. Build dynamic UPDATE query
  2. Only update provided fields
  3. Check if flight exists
  4. Execute update
Output: Success or 404 error
```

#### **DELETE /api/flights/{id}**
```
Input: Flight ID
Process:
  1. Check if bookings exist
  2. If yes → reject (can't delete)
  3. If no → delete flight
Output: Success or error
```

**Data Flow Example (GET flights):**
```
User searches BLR → DEL
    ↓
FastAPI receives request
    ↓
routes_flights.get_flights() called
    ↓
Build SQL: SELECT * WHERE origin='BLR' AND destination='DEL'
    ↓
Execute query
    ↓
Return JSON response
```

---

### 4️⃣ **pricing_engine.py** - Dynamic Pricing Brain
**Purpose:** Calculate flight prices based on multiple factors

**Core Algorithm:**
```python
Final Price = Base Price × Total Multiplier

Total Multiplier = 
    (Seat Factor × 0.40) +      # 40% weight
    (Time Factor × 0.35) +      # 35% weight
    (Demand Factor × 0.25)      # 25% weight

Bounded between 0.8x and 3.0x
```

**Key Methods:**

#### **`calculate_price()`**
```
Input: 
  - base_price: Original ticket price
  - total_seats: Total capacity
  - available_seats: Remaining seats
  - departure_time: When flight leaves
  - demand_level: low/medium/high/very_high

Process:
  1. Calculate seat_factor (occupancy)
  2. Calculate time_factor (urgency)
  3. Calculate demand_factor (simulated demand)
  4. Weighted average of all factors
  5. Apply min/max bounds (0.8x - 3.0x)
  6. Multiply by base price

Output:
  - current_price: Final dynamic price
  - breakdown: Individual factor values
  - percentage_increase: How much price changed
```

#### **Seat Factor Logic:**
```
Occupancy Rate = (total_seats - available_seats) / total_seats

If 0-20% occupied   → 0.8-1.0x (lots of seats, lower price)
If 20-60% occupied  → 1.0-1.5x (moderate demand)
If 60-90% occupied  → 1.5-2.5x (high demand)
If 90-100% occupied → 2.5-3.0x (very high demand)
```

#### **Time Factor Logic:**
```
Days Until Departure:
> 30 days  → 0.8x (early bird discount)
15-30 days → 1.0x (normal price)
7-15 days  → 1.3x (price increasing)
3-7 days   → 1.7x (getting expensive)
< 3 days   → 2.0-3.0x (last minute premium)
```

#### **Demand Factor Logic:**
```
Demand Level (simulated):
Low       → 0.9x
Medium    → 1.0x
High      → 1.4x
Very High → 2.0x
```

**Example Calculation:**
```
Flight: BLR → DEL
Base Price: ₹4500
Total Seats: 180
Available: 50 (72% occupied)
Days to Departure: 5
Demand: High

Step 1: Seat Factor
Occupancy = 130/180 = 0.72 (72%)
→ Seat Factor = 1.5 + ((0.72-0.6) × 3.33) = 1.9

Step 2: Time Factor
5 days until departure
→ Time Factor = 1.3 + ((7-5)/4 × 0.4) = 1.5

Step 3: Demand Factor
High demand
→ Demand Factor = 1.4

Step 4: Weighted Average
Total Multiplier = (1.9 × 0.40) + (1.5 × 0.35) + (1.4 × 0.25)
                = 0.76 + 0.525 + 0.35
                = 1.635

Step 5: Final Price
Current Price = 4500 × 1.635 = ₹7,357.50
Price Increase = 63.5%
```

**When Pricing Runs:**
1. **On flight search** - Shows current prices
2. **After booking** - Price increases (fewer seats)
3. **Background updates** - Periodic recalculation
4. **Demand shifts** - Random simulation

---

### 5️⃣ **routes_bookings.py** - Booking System
**Purpose:** Handle flight reservations with concurrency control

**Critical Flow:**

#### **POST /api/bookings - Create Booking**

**Step-by-Step Process:**
```
1. RECEIVE BOOKING REQUEST
   ↓
   Input: flight_id, passenger details, payment method
   
2. START DATABASE TRANSACTION
   ↓
   conn.autocommit = False
   
3. LOCK FLIGHT ROW (Concurrency Control)
   ↓
   SELECT * FROM flights WHERE id = ? FOR UPDATE
   ↓
   This prevents other users from booking simultaneously
   
4. CHECK FLIGHT AVAILABILITY
   ↓
   - Flight exists?
   - Seats available?
   - Flight not departed?
   ↓
   If any check fails → ROLLBACK → Return error
   
5. ASSIGN SEAT
   ↓
   - Check which seats are taken
   - Find first available seat (1A, 1B, 1C...)
   - Verify seat not double-booked
   
6. PROCESS PAYMENT
   ↓
   simulate_payment() - 95% success rate
   ↓
   If fails → ROLLBACK → Return payment error
   
7. GENERATE PNR
   ↓
   Random 6-character code (e.g., ABC123)
   Verify it's unique
   
8. CREATE BOOKING RECORD
   ↓
   INSERT INTO bookings (pnr, flight_id, passenger_info...)
   
9. UPDATE FLIGHT
   ↓
   available_seats = available_seats - 1
   
10. RECALCULATE PRICE
    ↓
    Call pricing_engine.calculate_price()
    Update current_price in flights table
    
11. COMMIT TRANSACTION
    ↓
    All changes saved atomically
    
12. RETURN SUCCESS
    ↓
    Return PNR, seat number, price
```

**Concurrency Control Explained:**
```
Problem: Two users book last seat simultaneously

Without Locking:
User A: SELECT flight (1 seat left) ────┐
User B: SELECT flight (1 seat left) ────┤─ Race Condition!
User A: Book seat ──────────────────────┤
User B: Book seat ──────────────────────┘
Result: OVERBOOKING! 2 bookings, 1 seat

With FOR UPDATE Locking:
User A: SELECT ... FOR UPDATE (LOCK) ───┐
User B: SELECT ... FOR UPDATE (WAITS)   │
User A: Book seat ──────────────────────┤
User A: COMMIT (UNLOCK) ────────────────┘
User B: Now gets lock, sees 0 seats left
User B: Booking rejected
Result: ✅ Correct! No overbooking
```

#### **GET /api/bookings/{pnr} - Retrieve Booking**
```
Input: PNR code
Process:
  1. JOIN bookings with flights table
  2. Get complete booking + flight details
  3. Return passenger info, seat, flight details
Output: Full booking information
```

#### **DELETE /api/bookings/{pnr} - Cancel Booking**
```
Input: PNR
Process:
  1. Start transaction
  2. Lock booking row
  3. Check if already cancelled
  4. Check if flight departed
  5. Update status to 'cancelled'
  6. Release seat (available_seats + 1)
  7. Commit transaction
Output: Success + refund amount
```

---

### 6️⃣ **Helper Functions**

#### **`generate_pnr()`**
```python
Purpose: Create unique 6-character booking reference
Logic:
  - Random selection from A-Z, 0-9
  - Length: 6 characters
  - Check uniqueness in database
  - Retry if duplicate
Example: "A3B9C2", "XYZ789"
```

#### **`generate_seat_number()`**
```python
Purpose: Assign next available seat
Logic:
  - Seats: 6 per row (A-F)
  - Format: RowNumber + Letter
  - Check booked seats
  - Return first available
Example: 1A, 1B, 1C, 2A, 2B...
```

#### **`simulate_payment()`**
```python
Purpose: Mock payment processing
Logic:
  - 95% success rate (random)
  - Generate transaction ID
  - Format: TXN{timestamp}{random}
Success: Return (True, "TXN202512161234567890")
Failure: Return (False, "PAYMENT_FAILED")
```

---

## 🔄 Complete Request Flow Example

**Scenario: User books a flight**
```
1. USER ACTION
   User clicks "Book Now" on flight BLR→DEL
   
2. FRONTEND (if exists)
   POST /api/bookings
   Body: { flight_id: 11, passenger: {...}, payment_method: "credit_card" }
   
3. FASTAPI RECEIVES
   main.py routes request to routes_bookings.py
   
4. ROUTE HANDLER
   create_booking() function called
   
5. DATABASE CONNECTION
   get_db_connection() creates MySQL connection
   
6. TRANSACTION START
   conn.autocommit = False
   
7. FLIGHT LOCK
   SELECT * FROM flights WHERE id=11 FOR UPDATE
   → Row locked, other users wait
   
8. VALIDATION
   ✓ Flight exists
   ✓ 45 seats available
   ✓ Departs in 9 days
   
9. SEAT ASSIGNMENT
   generate_seat_number()
   → Checks bookings table
   → Returns "8C" (first available)
   
10. PAYMENT
    simulate_payment("credit_card")
    → Random check (95% success)
    → Returns (True, "TXN202512161234567890")
    
11. PNR GENERATION
    generate_pnr()
    → Random: "KJ7N2M"
    → Check uniqueness ✓
    
12. PRICING UPDATE
    pricing_engine.calculate_price()
    Inputs:
      - base_price: 4500
      - total_seats: 180
      - available_seats: 45 (will be 44)
      - days: 9
      - demand: medium
    Output:
      - current_price: 5850 (30% increase)
    
13. DATABASE INSERTS
    INSERT INTO bookings (pnr='KJ7N2M', seat='8C', ...)
    UPDATE flights SET available_seats=44, current_price=5850
    
14. COMMIT
    conn.commit()
    → All changes saved
    → Lock released
    
15. RESPONSE
    {
      "success": true,
      "booking": {
        "pnr": "KJ7N2M",
        "seat": "8C",
        "price": 4500,
        "status": "confirmed"
      }
    }
    
16. USER SEES
    "Booking Confirmed! Your PNR is KJ7N2M"
```

**Total Time:** ~200-500ms

---

## 🗄️ Database Schema Explained

### **Flights Table**
```sql
Purpose: Store all flight information

Fields:
- id: Unique identifier (auto-increment)
- flight_number: e.g., "AI101"
- airline: e.g., "Air India"
- origin: 3-letter code (BLR)
- destination: 3-letter code (DEL)
- departure_time: When flight leaves
- arrival_time: When flight arrives
- base_price: Original ticket price (never changes)
- current_price: Dynamic price (changes with demand)
- total_seats: Plane capacity
- available_seats: Remaining bookable seats
- demand_level: low/medium/high/very_high
- status: scheduled/delayed/cancelled/completed
- created_at: When flight was added
- updated_at: Last modification time

Indexes (for fast queries):
- idx_origin: Search by departure city
- idx_destination: Search by arrival city
- idx_flight_number: Search by flight number

Relationships:
- One flight → Many bookings
```

### **Bookings Table**
```sql
Purpose: Store passenger reservations

Fields:
- id: Unique booking ID
- pnr: Public booking reference (ABC123)
- flight_id: Which flight (foreign key)
- passenger_first_name: John
- passenger_last_name: Doe
- passenger_email: john@example.com
- passenger_phone: 9876543210
- passenger_age: 30
- passenger_gender: male/female/other
- seat_number: 8C
- booking_price: Price at time of booking (locked)
- status: confirmed/cancelled/pending
- payment_status: completed/pending/failed/refunded
- transaction_id: Payment reference
- booking_time: When booked
- cancelled_at: When cancelled (if applicable)

Indexes:
- idx_pnr: Fast PNR lookup
- idx_flight_id: Find all bookings for a flight
- idx_passenger_email: Find user's bookings

Relationships:
- Many bookings → One flight
- Foreign key constraint prevents deleting flights with bookings
```

---

## ⚙️ Configuration (.env)
```env
Purpose: Store sensitive configuration

DB_HOST=localhost        # Where MySQL runs
DB_PORT=3306            # MySQL port
DB_USER=root            # Database user
DB_PASSWORD=xxx         # User password (NEVER commit!)
DB_NAME=flight_booking_db  # Database name

API_HOST=0.0.0.0        # Listen on all interfaces
API_PORT=8000           # API server port
API_DEBUG=True          # Enable debug mode
```

**Security:**
- `.env` is in `.gitignore`
- Never committed to GitHub
- Each developer has their own
- Production uses different values

---

## 🔐 Security Features

### **1. SQL Injection Prevention**
```python
# ❌ UNSAFE (vulnerable)
query = f"SELECT * FROM flights WHERE id = {flight_id}"

# ✅ SAFE (parameterized)
query = "SELECT * FROM flights WHERE id = %s"
cursor.execute(query, (flight_id,))
```

### **2. Input Validation (Pydantic)**
```python
class PassengerInfo(BaseModel):
    email: EmailStr  # Must be valid email
    age: int = Field(gt=0, lt=150)  # Must be 1-149
    phone: str = Field(min_length=10)  # At least 10 digits
```

### **3. Transaction Safety**
```python
try:
    conn.autocommit = False  # Start transaction
    # ... multiple operations ...
    conn.commit()  # All succeed
except:
    conn.rollback()  # All fail together (ACID)
```

### **4. Concurrency Control**
```python
SELECT * FROM flights WHERE id = ? FOR UPDATE
# Row locked until transaction completes
```

---

## 📊 Performance Considerations

### **Database Indexes**
```sql
INDEX idx_origin (origin)
INDEX idx_destination (destination)
INDEX idx_pnr (pnr)
```
**Why?** Speed up searches from O(n) to O(log n)

### **Connection Management**
- Connections opened per request
- Closed immediately after use
- Prevents connection exhaustion

### **Query Optimization**
- Only SELECT needed columns
- Use JOINs instead of multiple queries
- Limit results when possible

---

## 🧪 Testing Strategy

### **Unit Tests** (functions)
```python
test_calculate_price()
test_generate_pnr()
test_generate_seat_number()
```

### **Integration Tests** (API)
```python
test_create_booking()
test_search_flights()
test_cancel_booking()
```

### **Manual Testing** (Swagger UI)
- Interactive testing
- See request/response
- Validate schemas

---

This is the complete inner workings of your Flight Booking Simulator! 

**Tell me:**
1. Which part would you like me to explain in more detail?
2. Ready to move to the next documentation file?
3. Any questions about how things work?