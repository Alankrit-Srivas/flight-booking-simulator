import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { flightAPI } from '../api';
import Navbar from './Navbar';
import ProgressStepper from './ProgressStepper';
import './FlightSearch.css';

function FlightSearch() {
  const navigate = useNavigate();
  
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Trip type
  const [tripType, setTripType] = useState('round-trip'); // 'one-way' or 'round-trip'
  
  // Search filters
  const [filters, setFilters] = useState({
    origin: '',
    destination: '',
    departure_date: '',
    return_date: '',
    sort_by: 'price',
    order: 'asc'
  });

  // Autocomplete suggestions
  const [originSuggestions, setOriginSuggestions] = useState([]);
  const [destSuggestions, setDestSuggestions] = useState([]);
  const [showOriginSuggestions, setShowOriginSuggestions] = useState(false);
  const [showDestSuggestions, setShowDestSuggestions] = useState(false);

  // Airline filter
  const [selectedAirline, setSelectedAirline] = useState('all');
  const [availableAirlines, setAvailableAirlines] = useState([]);

  // Quick filters
  const [quickFilter, setQuickFilter] = useState('all'); // 'cheapest', 'fastest', 'nonstop'

  // Airport data for autocomplete
  const airports = [
    { code: 'BLR', city: 'Bangalore', name: 'Kempegowda International' },
    { code: 'DEL', city: 'Delhi', name: 'Indira Gandhi International' },
    { code: 'BOM', city: 'Mumbai', name: 'Chhatrapati Shivaji Maharaj' },
    { code: 'MAA', city: 'Chennai', name: 'Chennai International' },
    { code: 'CCU', city: 'Kolkata', name: 'Netaji Subhas Chandra Bose' },
    { code: 'HYD', city: 'Hyderabad', name: 'Rajiv Gandhi International' },
    { code: 'GOI', city: 'Goa', name: 'Goa International' },
    { code: 'COK', city: 'Kochi', name: 'Cochin International' }
  ];

  useEffect(() => {
    fetchFlights();
  }, []);

  const fetchFlights = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await flightAPI.getFlights(filters);
      let flightData = response.data.flights;
      
      // Extract unique airlines
      const airlines = [...new Set(flightData.map(f => f.airline))];
      setAvailableAirlines(airlines);
      
      setFlights(flightData);
    } catch (err) {
      setError('Failed to fetch flights. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Autocomplete handlers
  const handleOriginChange = (e) => {
    const value = e.target.value;
    setFilters({ ...filters, origin: value });
    
    if (value.length > 0) {
      const suggestions = airports.filter(airport => 
        airport.code.toLowerCase().includes(value.toLowerCase()) ||
        airport.city.toLowerCase().includes(value.toLowerCase()) ||
        airport.name.toLowerCase().includes(value.toLowerCase())
      );
      setOriginSuggestions(suggestions);
      setShowOriginSuggestions(true);
    } else {
      setShowOriginSuggestions(false);
    }
  };

  const handleDestChange = (e) => {
    const value = e.target.value;
    setFilters({ ...filters, destination: value });
    
    if (value.length > 0) {
      const suggestions = airports.filter(airport => 
        airport.code.toLowerCase().includes(value.toLowerCase()) ||
        airport.city.toLowerCase().includes(value.toLowerCase()) ||
        airport.name.toLowerCase().includes(value.toLowerCase())
      );
      setDestSuggestions(suggestions);
      setShowDestSuggestions(true);
    } else {
      setShowDestSuggestions(false);
    }
  };

  const selectOrigin = (airport) => {
    setFilters({ ...filters, origin: airport.code });
    setShowOriginSuggestions(false);
  };

  const selectDestination = (airport) => {
    setFilters({ ...filters, destination: airport.code });
    setShowDestSuggestions(false);
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchFlights();
  };

  const handleSelectFlight = (flightId) => {
    navigate(`/booking/${flightId}`);
  };

  // Apply filters
  const getFilteredFlights = () => {
    let filtered = [...flights];

    // Airline filter
    if (selectedAirline !== 'all') {
      filtered = filtered.filter(f => f.airline === selectedAirline);
    }

    // Quick filters
    if (quickFilter === 'cheapest') {
      filtered.sort((a, b) => a.current_price - b.current_price);
    } else if (quickFilter === 'fastest') {
      filtered.sort((a, b) => {
        const durationA = new Date(a.arrival_time) - new Date(a.departure_time);
        const durationB = new Date(b.arrival_time) - new Date(b.departure_time);
        return durationA - durationB;
      });
    } else if (quickFilter === 'nonstop') {
      // All flights are non-stop in this system, but you can add logic here
      filtered = filtered; // Keep as is
    }

    return filtered;
  };

  const formatTime = (dateTime) => {
    return new Date(dateTime).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    });
  };

  const formatDate = (dateTime) => {
    return new Date(dateTime).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const calculateDuration = (departure, arrival) => {
    const diff = new Date(arrival) - new Date(departure);
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    return `${hours} h ${minutes} m`;
  };

  const filteredFlights = getFilteredFlights();

  return (
    <div className="app-container">
      <Navbar />
      <ProgressStepper currentStep={1} />
      
      <div className="search-layout">
        {/* Left Sidebar */}
        <div className="search-sidebar">
          <h2 className="sidebar-title">Your Search</h2>
          
          {/* Trip Type Toggle */}
          <div className="trip-type-toggle">
            <button 
              className={`trip-btn ${tripType === 'one-way' ? 'active' : ''}`}
              onClick={() => setTripType('one-way')}
            >
              One-way
            </button>
            <button 
              className={`trip-btn ${tripType === 'round-trip' ? 'active' : ''}`}
              onClick={() => setTripType('round-trip')}
            >
              Round-trip
            </button>
          </div>

          <form onSubmit={handleSearch}>
            <div className="form-group autocomplete-wrapper">
              <label>From</label>
              <input
                type="text"
                name="origin"
                placeholder="City or airport code"
                value={filters.origin}
                onChange={handleOriginChange}
                onFocus={() => filters.origin && setShowOriginSuggestions(true)}
                autoComplete="off"
              />
              {showOriginSuggestions && originSuggestions.length > 0 && (
                <div className="autocomplete-dropdown">
                  {originSuggestions.map(airport => (
                    <div 
                      key={airport.code}
                      className="autocomplete-item"
                      onClick={() => selectOrigin(airport)}
                    >
                      <strong>{airport.code}</strong> - {airport.city}
                      <div className="airport-name">{airport.name}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="form-group autocomplete-wrapper">
              <label>To</label>
              <input
                type="text"
                name="destination"
                placeholder="City or airport code"
                value={filters.destination}
                onChange={handleDestChange}
                onFocus={() => filters.destination && setShowDestSuggestions(true)}
                autoComplete="off"
              />
              {showDestSuggestions && destSuggestions.length > 0 && (
                <div className="autocomplete-dropdown">
                  {destSuggestions.map(airport => (
                    <div 
                      key={airport.code}
                      className="autocomplete-item"
                      onClick={() => selectDestination(airport)}
                    >
                      <strong>{airport.code}</strong> - {airport.city}
                      <div className="airport-name">{airport.name}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="form-group">
              <label>Departure</label>
              <input
                type="date"
                name="departure_date"
                value={filters.departure_date}
                onChange={handleFilterChange}
              />
            </div>

            {tripType === 'round-trip' && (
              <div className="form-group">
                <label>Return</label>
                <input
                  type="date"
                  name="return_date"
                  value={filters.return_date}
                  onChange={handleFilterChange}
                />
              </div>
            )}

            {/* Airline Filter */}
            <div className="form-group">
              <label>Airline</label>
              <select 
                value={selectedAirline}
                onChange={(e) => setSelectedAirline(e.target.value)}
              >
                <option value="all">All Airlines</option>
                {availableAirlines.map(airline => (
                  <option key={airline} value={airline}>{airline}</option>
                ))}
              </select>
            </div>

            <button type="submit" className="btn btn-secondary btn-full">
              Change Search
            </button>
          </form>
        </div>

        {/* Right Content */}
        <div className="search-content">
          {/* Quick Filters */}
          <div className="quick-filters">
            <button 
              className={`filter-btn ${quickFilter === 'all' ? 'active' : ''}`}
              onClick={() => setQuickFilter('all')}
            >
              All Flights
            </button>
            <button 
              className={`filter-btn ${quickFilter === 'cheapest' ? 'active' : ''}`}
              onClick={() => setQuickFilter('cheapest')}
            >
              💰 Cheapest
            </button>
            <button 
              className={`filter-btn ${quickFilter === 'fastest' ? 'active' : ''}`}
              onClick={() => setQuickFilter('fastest')}
            >
              ⚡ Fastest
            </button>
            <button 
              className={`filter-btn ${quickFilter === 'nonstop' ? 'active' : ''}`}
              onClick={() => setQuickFilter('nonstop')}
            >
              ✈️ Non-stop First
            </button>
          </div>

          {loading && <div className="loading">Loading flights...</div>}
          {error && <div className="error">{error}</div>}

          {!loading && !error && (
            <div className="flights-list">
              {filteredFlights.length === 0 ? (
                <div className="no-flights">No flights found for your search.</div>
              ) : (
                filteredFlights.map((flight) => (
                  <div key={flight.id} className="flight-card">
                    <div className="flight-info">
                      <div className="flight-date">
                        {formatDate(flight.departure_time)} - Departure
                      </div>
                      
                      <div className="flight-route">
                        <div className="route-point">
                          <div className="time">{formatTime(flight.departure_time)}</div>
                          <div className="location">{flight.origin}</div>
                        </div>
                        
                        <div className="route-middle">
                          <div className="airline-name">{flight.airline}</div>
                          <div className="plane-icon">✈</div>
                          <div className="duration">{calculateDuration(flight.departure_time, flight.arrival_time)}</div>
                          <div className="route-type">Direct</div>
                        </div>
                        
                        <div className="route-point">
                          <div className="time">{formatTime(flight.arrival_time)}</div>
                          <div className="location">{flight.destination}</div>
                        </div>
                      </div>
                    </div>

                    <div className="flight-price">
                      <div className="price">${flight.current_price}</div>
                      <button 
                        className="btn btn-primary"
                        onClick={() => handleSelectFlight(flight.id)}
                      >
                        Select this flight
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default FlightSearch;