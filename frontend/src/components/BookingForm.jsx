import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { flightAPI, bookingAPI } from '../api';
import Navbar from './Navbar';
import ProgressStepper from './ProgressStepper';
import './BookingForm.css';

function BookingForm() {
  const { flightId } = useParams();
  const navigate = useNavigate();
  
  const [flight, setFlight] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [step, setStep] = useState(3); // Start at fare selection
  const [selectedFare, setSelectedFare] = useState(null);
  const [selectedServices, setSelectedServices] = useState([]);
  
  const [passengerData, setPassengerData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    age: '',
    gender: 'male'
  });

  useEffect(() => {
    fetchFlightDetails();
  }, [flightId]);

  const fetchFlightDetails = async () => {
    try {
      const response = await flightAPI.getFlightById(flightId);
      setFlight(response.data.flight);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch flight details');
      setLoading(false);
    }
  };

  const fareOptions = [
    {
      id: 'lowfare',
      name: 'Lowfare',
      subtitle: 'Cabin Economy',
      seat: 'Automatically Allocated',
      bag: '1 Cabin Baggage',
      flexibility: 'Non-refundable',
      price: flight ? flight.current_price * 0.8 : 0
    },
    {
      id: 'economy',
      name: 'Economy',
      subtitle: 'Cabin Economy +',
      seat: 'Seat Choice Included',
      bag: '1 Cabin Baggage\n1 Checked Baggage',
      flexibility: 'Non-refundable',
      price: flight ? flight.current_price : 0
    },
    {
      id: 'premium',
      name: 'Premium',
      subtitle: 'Cabin First Class',
      seat: 'Seat Choice Included',
      bag: '2 Cabin Baggage\n2 Checked Baggage',
      flexibility: 'Change of Date Possible',
      price: flight ? flight.current_price * 1.5 : 0
    }
  ];

  const extraServices = [
    {
      id: 'priority',
      name: 'Priority Boarding',
      description: 'Board the aircraft first',
      icon: '👥',
      price: 15
    },
    {
      id: 'baggage',
      name: 'Extra Large Baggage',
      description: 'Additional 10kg baggage',
      icon: '🎒',
      price: 25
    },
    {
      id: 'none',
      name: 'No Added Services',
      description: 'Continue without extras',
      icon: '✈️',
      price: 0
    }
  ];

  const handleFareSelect = (fare) => {
    setSelectedFare(fare);
    setStep(4);
  };

  const handleServiceToggle = (serviceId) => {
    if (serviceId === 'none') {
      setSelectedServices([]);
      setStep(6);
    } else {
      setSelectedServices(prev => 
        prev.includes(serviceId) 
          ? prev.filter(id => id !== serviceId)
          : [...prev, serviceId]
      );
    }
  };

  const handlePassengerChange = (e) => {
    setPassengerData({
      ...passengerData,
      [e.target.name]: e.target.value
    });
  };

  const handlePassengerSubmit = (e) => {
    e.preventDefault();
    setStep(5);
  };

  const handleFinalBooking = async () => {
    try {
      setLoading(true);
      const bookingPayload = {
        flight_id: parseInt(flightId),
        passenger: passengerData,
        payment_method: 'credit_card'
      };

      const response = await bookingAPI.createBooking(bookingPayload);
      
      if (response.data.success) {
        navigate(`/confirmation/${response.data.booking.pnr}`);
      }
    } catch (err) {
      setError('Booking failed. Please try again.');
      setLoading(false);
    }
  };

  if (loading && !flight) {
    return (
      <div className="app-container">
        <Navbar />
        <div className="loading">Loading flight details...</div>
      </div>
    );
  }

  if (error && !flight) {
    return (
      <div className="app-container">
        <Navbar />
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <Navbar />
      <ProgressStepper currentStep={step} />
      
      <div className="booking-content">
        {flight && (
          <div className="flight-summary">
            <h2>{flight.origin} to {flight.destination}</h2>
          </div>
        )}

        {/* Step 3: Fare Selection */}
        {step === 3 && (
          <div className="fare-selection">
            <div className="fare-grid">
              {fareOptions.map(fare => (
                <div 
                  key={fare.id}
                  className={`fare-card ${selectedFare?.id === fare.id ? 'selected' : ''}`}
                  onClick={() => handleFareSelect(fare)}
                >
                  <h3>{fare.name}</h3>
                  <p className="fare-subtitle">{fare.subtitle}</p>
                  
                  <div className="fare-details">
                    <div className="fare-item">
                      <strong>Seat</strong>
                      <p>{fare.seat}</p>
                    </div>
                    
                    <div className="fare-item">
                      <strong>Bag</strong>
                      <p style={{whiteSpace: 'pre-line'}}>{fare.bag}</p>
                    </div>
                    
                    <div className="fare-item">
                      <strong>Flexibility</strong>
                      <p>{fare.flexibility}</p>
                    </div>
                  </div>
                  
                  <div className="fare-price">${fare.price.toFixed(2)}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Step 4: Passenger Details */}
        {step === 4 && (
          <div className="passenger-form">
            <h2>Passenger Details</h2>
            <form onSubmit={handlePassengerSubmit}>
              <div className="form-row">
                <div className="form-group">
                  <label>First Name *</label>
                  <input
                    type="text"
                    name="first_name"
                    value={passengerData.first_name}
                    onChange={handlePassengerChange}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Last Name *</label>
                  <input
                    type="text"
                    name="last_name"
                    value={passengerData.last_name}
                    onChange={handlePassengerChange}
                    required
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Email *</label>
                  <input
                    type="email"
                    name="email"
                    value={passengerData.email}
                    onChange={handlePassengerChange}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Phone *</label>
                  <input
                    type="tel"
                    name="phone"
                    value={passengerData.phone}
                    onChange={handlePassengerChange}
                    required
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Age *</label>
                  <input
                    type="number"
                    name="age"
                    value={passengerData.age}
                    onChange={handlePassengerChange}
                    min="1"
                    max="120"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Gender *</label>
                  <select
                    name="gender"
                    value={passengerData.gender}
                    onChange={handlePassengerChange}
                    required
                  >
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>

              <button type="submit" className="btn btn-primary btn-large">
                Continue to Extra Services
              </button>
            </form>
          </div>
        )}

        {/* Step 5: Extra Services */}
        {step === 5 && (
          <div className="services-selection">
            <h2>Extra Services</h2>
            <div className="services-grid">
              {extraServices.map(service => (
                <div
                  key={service.id}
                  className={`service-card ${selectedServices.includes(service.id) ? 'selected' : ''} ${service.id === 'none' ? 'no-service' : ''}`}
                  onClick={() => handleServiceToggle(service.id)}
                >
                  <div className="service-icon">{service.icon}</div>
                  <h3>{service.name}</h3>
                  <p>{service.description}</p>
                  {service.price > 0 && (
                    <div className="service-price">${service.price}</div>
                  )}
                </div>
              ))}
            </div>
            
            {selectedServices.length > 0 && (
              <button 
                className="btn btn-primary btn-large"
                onClick={() => setStep(6)}
              >
                Continue to Payment
              </button>
            )}
          </div>
        )}

        {/* Step 6: Payment Confirmation */}
        {step === 6 && (
          <div className="payment-confirmation">
            <h2>Confirm Your Booking</h2>
            
            <div className="booking-summary">
              <div className="summary-section">
                <h3>Flight Details</h3>
                <p>{flight.airline} - {flight.flight_number}</p>
                <p>{flight.origin} → {flight.destination}</p>
              </div>

              <div className="summary-section">
                <h3>Passenger</h3>
                <p>{passengerData.first_name} {passengerData.last_name}</p>
                <p>{passengerData.email}</p>
              </div>

              <div className="summary-section">
                <h3>Fare Type</h3>
                <p>{selectedFare?.name} - ${selectedFare?.price.toFixed(2)}</p>
              </div>

              {selectedServices.length > 0 && (
                <div className="summary-section">
                  <h3>Extra Services</h3>
                  {selectedServices.map(serviceId => {
                    const service = extraServices.find(s => s.id === serviceId);
                    return <p key={serviceId}>{service.name} - ${service.price}</p>;
                  })}
                </div>
              )}

              <div className="summary-total">
                <h3>Total Amount</h3>
                <div className="total-price">
                  ${(selectedFare?.price + selectedServices.reduce((sum, id) => {
                    const service = extraServices.find(s => s.id === id);
                    return sum + (service?.price || 0);
                  }, 0)).toFixed(2)}
                </div>
              </div>
            </div>

            <button 
              className="btn btn-primary btn-large"
              onClick={handleFinalBooking}
              disabled={loading}
            >
              {loading ? 'Processing...' : 'Complete Booking'}
            </button>

            {error && <div className="error">{error}</div>}
          </div>
        )}
      </div>
    </div>
  );
}

export default BookingForm;