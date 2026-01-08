import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import FlightSearch from './components/FlightSearch';
import BookingForm from './components/BookingForm';
import BookingConfirmation from './components/BookingConfirmation';
import SeatSelection from "./components/SeatSelection";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<FlightSearch />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/search" element={<FlightSearch />} />
        <Route path="/booking/:flightId" element={<BookingForm />} />
        <Route path="/confirmation/:pnr" element={<BookingConfirmation />} />
        <Route path="/seatselection" element={<SeatSelection />} />
      </Routes>
    </Router>
  );
}

export default App;