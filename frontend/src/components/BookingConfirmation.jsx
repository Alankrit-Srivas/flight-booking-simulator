import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { bookingAPI } from '../api';
import Navbar from './Navbar';
import './BookingConfirmation.css';

function BookingConfirmation() {
  const { pnr } = useParams();
  const navigate = useNavigate();
  
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchBookingDetails();
  }, [pnr]);

  const fetchBookingDetails = async () => {
    try {
      const response = await bookingAPI.getBookingByPNR(pnr);
      setBooking(response.data.booking);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch booking details');
      setLoading(false);
    }
  };

  const formatDateTime = (dateTime) => {
    return new Date(dateTime).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handlePrint = () => {
    window.print();
  };

  if (loading) {
    return (
      <div className="app-container">
        <Navbar />
        <div className="loading">Loading booking details...</div>
      </div>
    );
  }

  if (error || !booking) {
    return (
      <div className="app-container">
        <Navbar />
        <div className="error">{error || 'Booking not found'}</div>
        <div style={{textAlign: 'center', marginTop: '20px'}}>
          <button className="btn btn-primary" onClick={() => navigate('/search')}>
            Back to Search
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <Navbar />
      
      <div className="confirmation-content">
        <div className="success-header">
          <div className="success-icon">✓</div>
          <h1>Booking Confirmed!</h1>
          <p>Your flight has been successfully booked</p>
        </div>

        <div className="confirmation-card">
          <div className="pnr-section">
            <div className="pnr-label">Booking Reference (PNR)</div>
            <div className="pnr-code">{booking.pnr}</div>
            <p className="pnr-note">Save this reference number for your records</p>
          </div>

          <div className="booking-details">
            <div className="detail-section">
              <h3>Flight Information</h3>
              <div className="detail-row">
                <span className="detail-label">Flight</span>
                <span className="detail-value">{booking.flight_number} - {booking.airline}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Route</span>
                <span className="detail-value">{booking.origin} → {booking.destination}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Departure</span>
                <span className="detail-value">{formatDateTime(booking.departure_time)}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Arrival</span>
                <span className="detail-value">{formatDateTime(booking.arrival_time)}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Seat</span>
                <span className="detail-value">{booking.seat_number}</span>
              </div>
            </div>

            <div className="detail-section">
              <h3>Passenger Information</h3>
              <div className="detail-row">
                <span className="detail-label">Name</span>
                <span className="detail-value">
                  {booking.passenger_first_name} {booking.passenger_last_name}
                </span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Email</span>
                <span className="detail-value">{booking.passenger_email}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Phone</span>
                <span className="detail-value">{booking.passenger_phone}</span>
              </div>
            </div>

            <div className="detail-section">
              <h3>Payment Information</h3>
              <div className="detail-row">
                <span className="detail-label">Status</span>
                <span className="detail-value status-confirmed">Confirmed</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Amount Paid</span>
                <span className="detail-value price">${booking.booking_price}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Transaction ID</span>
                <span className="detail-value">{booking.transaction_id}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Booking Date</span>
                <span className="detail-value">{formatDateTime(booking.booking_time)}</span>
              </div>
            </div>
          </div>

          <div className="confirmation-actions">
            <button className="btn btn-primary" onClick={handlePrint}>
              Print Ticket
            </button>
            <button className="btn btn-outline" onClick={() => navigate('/search')}>
              Book Another Flight
            </button>
          </div>
        </div>

        <div className="important-info">
          <h4>Important Information</h4>
          <ul>
            <li>Please arrive at the airport at least 2 hours before departure</li>
            <li>Carry a valid photo ID and this booking reference</li>
            <li>Check-in opens 3 hours before departure</li>
            <li>A confirmation email has been sent to {booking.passenger_email}</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default BookingConfirmation;