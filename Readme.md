web site link

https://flight-booking-simulator-1-qc9g.onrender.com/

Backend Apis
https://flight-booking-simulator-il9i.onrender.com/api/docs

# ✈️ Flight Booking Simulator with Dynamic Pricing & Authentication

A complete full-stack web application for flight booking that mimics real-world airline reservation systems with **dynamic pricing engine**, **user authentication**, **advanced search features**, and **concurrent booking management**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![React](https://img.shields.io/badge/React-18.2.0-61dafb.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📌 Project Overview

This project implements a **comprehensive Flight Booking System** with enterprise-grade features:

- 🔐 **User Authentication** - Secure signup/login with JWT tokens
- 🔍 **Smart Search** - Autocomplete suggestions and advanced filters
- 💰 **Dynamic Pricing** - Real-time price adjustment based on demand
- 🎫 **Booking Management** - Multi-step booking with PNR generation
- ⚡ **One-way/Round-trip** - Flexible trip type selection
- 🏢 **Airline Filtering** - Filter by specific airlines
- 📊 **Quick Filters** - Cheapest, Fastest, Non-stop options
- 🔒 **Concurrency Control** - Thread-safe seat reservations
- 🎨 **Modern UI** - Professional teal-themed interface

Built as part of the **Infosys Internship Training Program** (All 3 Backend Milestones + Authentication Complete).

---

## 🚀 Tech Stack

### **Backend**
- **FastAPI** - High-performance Python web framework
- **MySQL** - Relational database
- **Pydantic** - Data validation
- **Passlib & Bcrypt** - Password hashing
- **Python-JOSE** - JWT token generation
- **Uvicorn** - ASGI server

### **Frontend**
- **React 18** - UI library
- **React Router** - Navigation
- **Axios** - HTTP client
- **Context API** - State management
- **CSS3** - Custom styling

---

## 📂 Project Structure
```
flight-booking-simulator/
│
├── backend/
│   ├── main.py                     # FastAPI application entry
│   ├── database.py                 # Database connection
│   ├── routes_flights.py           # Flight endpoints
│   ├── routes_bookings.py          # Booking endpoints
│   ├── routes_auth.py              # Authentication endpoints (NEW)
│   ├── auth_utils.py               # Password hashing & JWT (NEW)
│   ├── pricing_engine.py           # Dynamic pricing algorithm
│   ├── flight_generator.py         # Auto-generate flights (NEW)
│   ├── requirements.txt            # Python dependencies
│   ├── .env                        # Environment variables
│   └── auth_schema.sql             # User authentication schema (NEW)
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx          # Navigation bar (Updated)
│   │   │   ├── ProgressStepper.jsx # Progress indicator (NEW)
│   │   │   ├── FlightSearch.jsx    # Search page (Enhanced)
│   │   │   ├── BookingForm.jsx     # Booking flow
│   │   │   ├── BookingConfirmation.jsx
│   │   │   ├── Login.jsx           # Login page (NEW)
│   │   │   ├── Signup.jsx          # Signup page (NEW)
│   │   │   └── *.css               # Component styles
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx     # Auth state management (NEW)
│   │   ├── api.js                  # API configuration
│   │   ├── App.js                  # Main app component
│   │   └── index.js                # App entry point
│   ├── package.json
│   └── package-lock.json
│
├── schema.sql                      # Main database schema
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- Node.js 16+ and npm
- MySQL 8.0 or higher
- Git

---

### **Backend Setup**

#### **Step 1: Clone Repository**
```bash
git clone https://github.com/Alankrit-Srivas/flight-booking-simulator.git
cd flight-booking-simulator
```

#### **Step 2: Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### **Step 3: Install Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

#### **Step 4: Setup Database**

**Create Database:**
```sql
CREATE DATABASE flight_booking_db;
```

**Run Main Schema:**
```bash
mysql -u root -p flight_booking_db < ../schema.sql
```

**Run Auth Schema:**
```bash
mysql -u root -p flight_booking_db < auth_schema.sql
```

Or execute both SQL files in MySQL Workbench/phpMyAdmin.

#### **Step 5: Configure Environment**

Create `.env` file in `backend/` folder:
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=flight_booking_db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=True
```

#### **Step 6: Start Backend Server**
```bash
python main.py
```

Backend will run at: `http://localhost:8000`

API Documentation: `http://localhost:8000/api/docs`

---

### **Frontend Setup**

#### **Step 1: Install Frontend Dependencies**
```bash
cd frontend
npm install
```

#### **Step 2: Start Development Server**
```bash
npm start
```

Frontend will open at: `http://localhost:3000`

---

## 🎯 Features Documentation

### **1️⃣ User Authentication**

#### **Signup**
- Navigate to `/signup`
- Secure password hashing with bcrypt
- JWT token generation
- Auto-login after registration

#### **Login**
- Navigate to `/login`
- JWT-based authentication
- Session persistence with localStorage
- Protected routes

#### **User Session**
- User info displayed in navbar
- Token-based API authentication
- Logout functionality

**API Endpoints:**
```
POST /api/auth/signup    - Register new user
POST /api/auth/login     - Login user
GET  /api/auth/me        - Get current user
POST /api/auth/logout    - Logout user
```

---

### **2️⃣ Enhanced Flight Search**

#### **Smart Autocomplete**
- Type-ahead suggestions for airports
- Search by city name or airport code
- Displays full airport names
- Instant filtering as you type

#### **Trip Type Selection**
- **One-way**: Single journey
- **Round-trip**: Return journey (with return date)
- Toggle between trip types

#### **Airline Filter**
- Dropdown with all available airlines
- Filter flights by specific airline
- "All Airlines" option

#### **Quick Filters**
- 💰 **Cheapest**: Sort by lowest price first
- ⚡ **Fastest**: Sort by shortest duration
- ✈️ **Non-stop First**: Prioritize direct flights
- **All Flights**: Default view

#### **Search Parameters**
```
- Origin (with autocomplete)
- Destination (with autocomplete)
- Departure Date
- Return Date (for round-trip)
- Airline Selection
- Sort Options
```

---

### **3️⃣ Dynamic Pricing Engine**

**Price Calculation Factors:**

| Factor | Weight | Impact |
|--------|--------|--------|
| **Seat Availability** | 40% | Fewer seats = Higher price |
| **Time to Departure** | 35% | Closer date = Higher price |
| **Demand Level** | 25% | High demand = Higher price |

**Price Multiplier Range:** 0.8x - 3.0x of base price

**Example Calculation:**
```
Flight: BLR → DEL
Base Price: ₹4500
Available Seats: 50/180 (72% occupied)
Days to Departure: 5 days
Demand: High

Seat Factor: 1.9x (high occupancy)
Time Factor: 1.5x (last minute)
Demand Factor: 1.4x (high demand)

Final Multiplier: (1.9×0.4) + (1.5×0.35) + (1.4×0.25) = 1.635
Current Price: ₹4500 × 1.635 = ₹7,357
```

---

### **4️⃣ Auto-Flight Generation**

When searching for a future date without existing flights:
- Automatically generates realistic flights
- Multiple airlines and routes
- Varied departure times (6 AM - 11 PM)
- Random pricing and seat availability
- Persistent after generation

**Supported Routes:**
- BLR ↔ DEL, BOM, MAA, HYD, CCU, GOI, COK
- DEL ↔ BOM, MAA
- BOM ↔ GOI
- And more...

---

### **5️⃣ Booking System**

#### **Multi-Step Flow**
1. **Search** - Find flights
2. **Choose Flight** - Select from results
3. **Choose Fare** - Lowfare / Economy / Premium
4. **Passenger Details** - Enter information
5. **Extra Services** - Add-ons (Priority, Baggage)
6. **Payment** - Simulated payment (95% success rate)

#### **Fare Types**

| Fare | Seat | Baggage | Flexibility | Price |
|------|------|---------|-------------|-------|
| **Lowfare** | Auto-allocated | 1 Cabin | Non-refundable | 80% of base |
| **Economy** | Choice included | 1 Cabin + 1 Checked | Non-refundable | 100% (base) |
| **Premium** | Choice included | 2 Cabin + 2 Checked | Date change OK | 150% of base |

#### **Extra Services**
- 🚶 Priority Boarding: $15
- 🎒 Extra Large Baggage: $25
- ✈️ No Added Services: $0

---

### **6️⃣ Concurrency Control**

**Problem Solved:** Multiple users booking the same seat simultaneously

**Solution:** Database row-level locking
```sql
SELECT * FROM flights WHERE id = ? FOR UPDATE
```

**Benefits:**
- ✅ No double bookings
- ✅ No overbooking
- ✅ Thread-safe operations
- ✅ ACID compliance

---

## 📖 API Documentation

Once running, access interactive API docs:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### **Authentication Endpoints**
```http
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "9876543210"
}
```
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### **Flight Endpoints**
```http
GET /api/flights?origin=BLR&destination=DEL&departure_date=2025-12-25

Response:
{
  "success": true,
  "count": 5,
  "flights": [...]
}
```

### **Booking Endpoints**
```http
POST /api/bookings
Authorization: Bearer <token>

{
  "flight_id": 11,
  "passenger": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "age": 30,
    "gender": "male"
  },
  "payment_method": "credit_card"
}
```

---

## 🗄️ Database Schema

### **Users Table** (NEW)
```sql
- id (PK)
- email (UNIQUE)
- password_hash
- first_name
- last_name
- phone
- created_at
- last_login
- is_active
```

### **Flights Table**
```sql
- id (PK)
- flight_number
- airline
- origin, destination
- departure_time, arrival_time
- base_price, current_price
- total_seats, available_seats
- demand_level (low/medium/high/very_high)
- status
```

### **Bookings Table**
```sql
- id (PK)
- pnr (UNIQUE 6-char code)
- flight_id (FK)
- passenger details
- seat_number
- booking_price
- status (confirmed/cancelled)
- payment_status
- transaction_id
```

---

## 🧪 Testing Guide

### **Test Authentication**
1. Navigate to `/signup`
2. Create account with:
   - Email: test@example.com
   - Password: test123
   - Fill all fields
3. Should auto-login and show name in navbar
4. Logout and login again

### **Test Search Features**
1. Go to Search page
2. Type "ban" in Origin → See Bangalore suggestions
3. Click suggestion → Auto-fills "BLR"
4. Toggle One-way/Round-trip
5. Select airline from dropdown
6. Click "Cheapest" filter → Sorts by price
7. Select any future date → Auto-generates flights

### **Test Booking Flow**
1. Search for flights (BLR → DEL, future date)
2. Click "Select this flight"
3. Choose fare type (Economy recommended)
4. Fill passenger details
5. Select extra services (or skip)
6. Complete booking
7. View confirmation with PNR
8. Print ticket option

---

## 🎨 UI/UX Features

### **Design System**
- **Color Scheme**: Teal gradient (#4db8a8)
- **Typography**: System fonts for performance
- **Layout**: Card-based, modern design
- **Responsive**: Mobile-friendly (breakpoints at 768px, 1024px)

### **Animations**
- Smooth hover effects
- Card elevation on hover
- Button press animations
- Loading states with spinners

### **Accessibility**
- Semantic HTML
- Keyboard navigation support
- ARIA labels where needed
- High contrast ratios

---

## 🚧 Future Enhancements

### **Phase 1: Advanced Features** (Planned)
- [ ] Background price updater service
- [ ] Analytics dashboard (revenue, bookings, occupancy)
- [ ] Email notifications (booking confirmations)
- [ ] PDF receipt generation
- [ ] Admin panel (manage flights)

### **Phase 2: Enterprise Features**
- [ ] Payment gateway integration (Razorpay/Stripe)
- [ ] Multi-currency support
- [ ] SMS alerts (Twilio)
- [ ] Loyalty programs
- [ ] Referral system

### **Phase 3: Deployment**
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Cloud deployment (AWS/Azure/GCP)
- [ ] Redis caching
- [ ] Load balancing

---

## 🐛 Troubleshooting

### **CORS Error**
```
Access to XMLHttpRequest blocked by CORS policy
```
**Solution:** Ensure `main.py` has CORS middleware configured before routes:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Database Connection Error**
```
Error: Access denied for user 'root'@'localhost'
```
**Solution:** Check `.env` file has correct `DB_PASSWORD`

### **Module Not Found**
```
ModuleNotFoundError: No module named 'passlib'
```
**Solution:**
```bash
pip install passlib bcrypt python-jose[cryptography]
```

### **Port Already in Use**
```
Address already in use: Port 8000/3000
```
**Solution:**
```bash
# Kill process using port
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

---

## 📊 Project Milestones

| Milestone | Status | Description |
|-----------|--------|-------------|
| **Milestone 1** | ✅ Complete | Core Flight Search & Data Management |
| **Milestone 2** | ✅ Complete | Dynamic Pricing Engine |
| **Milestone 3** | ✅ Complete | Booking Workflow & Transactions |
| **Auth System** | ✅ Complete | User Authentication (Bonus) |
| **Enhanced Search** | ✅ Complete | Autocomplete & Filters (Bonus) |
| **Milestone 4** | ✅ Complete | Advanced Features & Analytics |

---

## 🤝 Contributing

This is an educational project. Suggestions welcome!

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
- Internship: Infosys Springboard Program

---

## 🙏 Acknowledgments

- **Infosys Springboard** - Internship Training Program
- FastAPI Community
- React Community
- MySQL Documentation
- Stack Overflow Community

---

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check existing issues for solutions
- Review API documentation at `/api/docs`

---

## 🌟 Key Features Summary

✅ **User Authentication** - Secure signup/login with JWT  
✅ **Smart Search** - Autocomplete with airport suggestions  
✅ **Dynamic Pricing** - Real-time price adjustments  
✅ **Trip Types** - One-way and Round-trip support  
✅ **Airline Filter** - Filter by specific airlines  
✅ **Quick Filters** - Cheapest, Fastest, Non-stop  
✅ **Auto-Generate** - Creates flights for any future date  
✅ **Multi-Step Booking** - Professional booking flow  
✅ **Fare Classes** - Lowfare, Economy, Premium options  
✅ **Extra Services** - Priority boarding, baggage  
✅ **Concurrency Safe** - No double bookings  
✅ **PNR Generation** - Unique booking references  
✅ **Modern UI** - Professional teal-themed design  
✅ **Responsive** - Mobile-friendly interface  

---

**Built with ❤️ as part of Infosys Internship Training**

**Status:** Backend Complete (100%) | Frontend Complete (100%) | Production Ready ✅

Last Updated: December 2024

---

## 📸 Screenshots

### Homepage
![Homepage](screenshots/homepage.png)

### Flight Search
![Search](screenshots/search.png)

### Booking Flow
![Booking](screenshots/booking.png)

### Confirmation
![Confirmation](screenshots/confirmation.png)


---

**⭐ Star this repo if you found it helpful!**
