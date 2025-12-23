import axios from 'axios';

// Base URL for your backend API
const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false, // Change this if it was true
});


// Flight API calls
export const flightAPI = {
  // Get all flights with optional filters
  getFlights: (params = {}) => {
    return api.get('/flights', { params });
  },

  // Get specific flight by ID
  getFlightById: (id) => {
    return api.get(`/flights/${id}`);
  },
};

// Booking API calls
export const bookingAPI = {
  // Create new booking
  createBooking: (bookingData) => {
    return api.post('/bookings/', bookingData);
  },

  // Get booking by PNR
  getBookingByPNR: (pnr) => {
    return api.get(`/bookings/${pnr}`);
  },

  // Get all bookings
  getAllBookings: (params = {}) => {
    return api.get('/bookings', { params });
  },

  // Cancel booking
  cancelBooking: (pnr) => {
    return api.delete(`/bookings/${pnr}`);
  },
};

export default api;