import React from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="homepage">
      <div className="container">
        <div className="hero-section">
          <h1 className="hero-title">
            Welcome to FlightBooker
          </h1>
          <p className="hero-subtitle">
            Book your flights with dynamic pricing and real-time availability
          </p>
          
          <div className="features">
            <div className="feature-card">
              <div className="feature-icon">🔍</div>
              <h3>Smart Search</h3>
              <p>Find flights with advanced filters and sorting</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">💰</div>
              <h3>Dynamic Pricing</h3>
              <p>Prices adjust based on demand and availability</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Instant Booking</h3>
              <p>Quick and secure booking process</p>
            </div>
          </div>

          <button 
            className="btn btn-primary btn-large"
            onClick={() => navigate('/search')}
          >
            Search Flights Now
          </button>
        </div>
      </div>
    </div>
  );
}

export default HomePage;