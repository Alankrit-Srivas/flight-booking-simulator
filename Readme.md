# ✈️ Flight Booking Simulator with Dynamic Pricing

A complete backend system for flight booking that mimics real-world airline reservation systems with intelligent dynamic pricing, seat management, and concurrent booking transactions.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📌 Project Overview

This project implements a **Flight Booking Simulator** with advanced features including:

- 🔍 **Flight Search** with filtering and sorting
- 💰 **Dynamic Pricing Engine** based on demand, time, and seat availability
- 🎫 **Booking System** with PNR generation and seat assignment
- 🔒 **Concurrency Control** using database locking
- 📊 **Real-time Analytics** and reporting
- 🚀 **RESTful API** with automatic documentation

Built as part of the **Infosys Internship Training Program** (Milestones 1-3 Complete).

---

## 🚀 Features

### ✅ Completed Features

#### **Flight Management**
- Create, read, update, and delete flights
- Search flights by origin, destination, and date
- Sort by price, duration, or departure time
- Real-time seat availability tracking

#### **Dynamic Pricing Engine**
- **Multi-factor pricing algorithm:**
  - 40% weight: Seat availability (fewer seats = higher price)
  - 35% weight: Time to departure (closer = higher price)
  - 25% weight: Demand level simulation
- Price multiplier range: 0.8x to 3.0x of base price
- Automatic price updates after each booking

#### **Booking System**
- Multi-step booking workflow
- Automatic PNR (Passenger Name Record) generation
- Intelligent seat assignment (row + letter format)
- Payment simulation with 95% success rate
- Concurrency-safe transactions using row locking
- Booking cancellation with seat release

#### **API & Documentation**
- Interactive Swagger UI documentation
- RESTful endpoints with proper HTTP methods
- Input validation using Pydantic
- Comprehensive error handling

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance web framework |
| **MySQL** | Relational database |
| **Pydantic** | Data validation |
| **Uvicorn** | ASGI server |
| **Python 3.8+** | Backend language |

---

## 📂 Project Structure
```
flight-booking-simulator/
│
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # Database connection configuration
│   ├── routes_flights.py       # Flight endpoints
│   ├── routes_bookings.py      # Booking endpoints
│   ├── pricing_engine.py       # Dynamic pricing algorithm
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables (not in repo)
│
├── schema.sql                  # Database schema
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### **Step 1: Clone Repository**
```bash
git clone https://github.com/Alankrit-Srivas/flight-booking-simulator.git
cd flight-booking-simulator
```

### **Step 2: Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

### **Step 4: Setup Database**

1. Create MySQL database:
```sql
CREATE DATABASE flight_booking_db;
```

2. Import schema:
```bash
# From project root
mysql -u root -p flight_booking_db
```

Then in MySQL:
```sql
source schema.sql;
EXIT;
```

### **Step 5: Configure Environment**

Create `.env` file in `backend/` folder:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=flight_booking_db

API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=True
```

### **Step 6: Start Server**
```bash
cd backend
python main.py
```

Server will start at: `http://localhost:8000`

---

## 📖 API Documentation

Once running, access:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/

---

## 🎯 API Endpoints

### **Flights**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/flights` | Get all flights (with filters) |
| GET | `/api/flights/{id}` | Get specific flight details |
| POST | `/api/flights` | Create new flight |
| PUT | `/api/flights/{id}` | Update flight |
| DELETE | `/api/flights/{id}` | Delete flight |

**Example Search Request:**
```bash
GET /api/flights?origin=BLR&destination=DEL&sort_by=price&order=asc
```

---

### **Bookings**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/bookings` | Create new booking |
| GET | `/api/bookings` | Get all bookings |
| GET | `/api/bookings/{pnr}` | Get booking by PNR |
| DELETE | `/api/bookings/{pnr}` | Cancel booking |

**Example Booking Request:**
```json
POST /api/bookings
{
  "flight_id": 11,
  "passenger": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "9876543210",
    "age": 30,
    "gender": "male"
  },
  "payment_method": "credit_card"
}
```

**Response:**
```json
{
  "success": true,
  "booking": {
    "pnr": "ABC123",
    "flight_number": "AI201",
    "passenger_name": "John Doe",
    "seat_number": "1A",
    "booking_price": 4500.00,
    "status": "confirmed"
  }
}
```

---

## 💰 Dynamic Pricing Algorithm

The pricing engine calculates flight prices based on:

### **1. Seat Availability (40% weight)**
```
80-100% available → 0.8-1.0x
40-80% available  → 1.0-1.5x
10-40% available  → 1.5-2.5x
0-10% available   → 2.5-3.0x
```

### **2. Time to Departure (35% weight)**
```
> 30 days  → 0.8x (early bird)
15-30 days → 1.0x
7-15 days  → 1.3x
3-7 days   → 1.7x
< 3 days   → 2.0-3.0x (last minute)
```

### **3. Demand Level (25% weight)**
```
Low       → 0.9x
Medium    → 1.0x
High      → 1.4x
Very High → 2.0x
```

**Final Price** = Base Price × (Weighted Average Multiplier)

---

## 🔒 Concurrency Control

The booking system prevents race conditions using **MySQL row-level locking**:
```python
# Lock flight row during booking
SELECT * FROM flights WHERE id = ? FOR UPDATE
```

This ensures:
- ✅ No double bookings
- ✅ No overbooking
- ✅ Thread-safe operations
- ✅ ACID compliance

---

## 🧪 Testing

### **Manual Testing via Swagger UI**
1. Navigate to http://localhost:8000/api/docs
2. Test each endpoint interactively
3. View request/response schemas

### **Sample Test Flow**
1. Search flights: `GET /api/flights?origin=BLR&destination=DEL`
2. Create booking: `POST /api/bookings` with passenger details
3. Verify booking: `GET /api/bookings/{pnr}`
4. Check updated flight: `GET /api/flights/{id}` (seats decreased, price increased)
5. Cancel booking: `DELETE /api/bookings/{pnr}`

---

## 📊 Database Schema

### **Flights Table**
```sql
- flight_number, airline
- origin, destination
- departure_time, arrival_time
- base_price, current_price (dynamic)
- total_seats, available_seats
- demand_level, status
```

### **Bookings Table**
```sql
- pnr (unique 6-char)
- flight_id (foreign key)
- passenger details
- seat_number
- booking_price (locked at booking)
- status, payment_status
```

---

## 📈 Project Milestones

| Milestone | Status | Description |
|-----------|--------|-------------|
| **Milestone 1** | ✅ Complete | Core Flight Search & Data Management |
| **Milestone 2** | ✅ Complete | Dynamic Pricing Engine |
| **Milestone 3** | ✅ Complete | Booking Workflow & Transactions |
| **Milestone 4** | 🔜 Working | Frontend UI Development |

---

## 🚧 Future Enhancements

- [ ] React/Vue.js frontend
- [ ] Background price updater service
- [ ] Email notifications
- [ ] PDF receipt generation
- [ ] Admin dashboard
- [ ] User authentication (JWT)
- [ ] Payment gateway integration
- [ ] Flight status updates
- [ ] Multi-currency support
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Cloud deployment

---

## 🐛 Troubleshooting

### **Database Connection Error**
```
Error: Access denied for user 'root'@'localhost'
```
**Solution:** Verify `.env` file has correct `DB_PASSWORD`

### **Module Not Found**
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution:** Activate venv and run `pip install -r requirements.txt`

### **Port Already in Use**
```
Address already in use: Port 8000
```
**Solution:** Change port in `.env` or kill existing process

---

## 🤝 Contributing

This is an educational project. Suggestions and improvements are welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Alankrit Srivas**
- GitHub: [@Alankrit-Srivas](https://github.com/Alankrit-Srivas)
- Project: [Flight Booking Simulator](https://github.com/Alankrit-Srivas/flight-booking-simulator)

---

## 🙏 Acknowledgments

- **Infosys Springboard** - Internship Training Program
- FastAPI Community
- MySQL Documentation

---

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check existing issues for solutions

---

**Built with ❤️ as part of Infosys Internship Training**

**Status:** Backend Complete ✅ | Frontend In Progress 🔜
