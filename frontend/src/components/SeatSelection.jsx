import React, { useState, useEffect } from 'react';
import { X, Plane, Info } from 'lucide-react';
import axios from 'axios';

const SeatSelectionModal = ({ flightId, onClose, onSeatsSelected }) => {
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [hoveredSeat, setHoveredSeat] = useState(null);
  const [seats, setSeats] = useState([]);
  const [loading, setLoading] = useState(true);

  const rows = 20;
  const seatsPerRow = 6;
  const aisleAfter = 3;

  useEffect(() => {
    fetchSeats();
  }, [flightId]);

  const fetchSeats = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/flights/${flightId}/seats`);
      setSeats(response.data.seats);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching seats:', error);
      setLoading(false);
    }
  };

  const seatCategories = {
    extra_legroom: { price: 15.00, rows: [1, 2], color: '#1e3a8a', label: 'Extra legroom seats' },
    front: { price: 13.01, rows: [3, 4, 5], color: '#fbbf24', label: 'Front seat' },
    standard: { price: 7.00, rows: [6, 7, 8, 9, 10, 11, 12, 13, 14, 15], color: '#3b82f6', label: 'Standard' },
    on_sale: { price: 3.00, rows: [18, 20], color: '#dc2626', label: 'On sale!' }
  };

  const reservedSeats = seats.filter(seat => !seat.is_available).map(seat => seat.seat_number);
  const emergencyRows = [16, 17];

  const getSeatCategory = (rowNum) => {
    for (let [key, value] of Object.entries(seatCategories)) {
      if (value.rows.includes(rowNum)) return { ...value, type: key };
    }
    return { ...seatCategories.standard, type: 'standard' };
  };

  const getSeatLabel = (rowIndex) => {
    const labels = ['A', 'B', 'C', 'D', 'E', 'F'];
    return labels[rowIndex];
  };

  const getSeatId = (row, seatIndex) => {
    return `${row}${getSeatLabel(seatIndex)}`;
  };

  const isSeatReserved = (seatId) => reservedSeats.includes(seatId);
  const isSeatSelected = (seatId) => selectedSeats.includes(seatId);
  const isEmergencyRow = (row) => emergencyRows.includes(row);

  const handleSeatClick = (seatId, row) => {
    if (isSeatReserved(seatId) || isEmergencyRow(row)) return;

    setSelectedSeats(prev => {
      if (prev.includes(seatId)) {
        return prev.filter(id => id !== seatId);
      } else {
        return [...prev, seatId];
      }
    });
  };

  const getSeatStyle = (row, seatIndex) => {
    const seatId = getSeatId(row, seatIndex);
    const category = getSeatCategory(row);
    
    let backgroundColor = category.color;
    let cursor = 'pointer';
    
    if (isSeatReserved(seatId)) {
      backgroundColor = '#d1d5db';
      cursor = 'not-allowed';
    } else if (isSeatSelected(seatId)) {
      backgroundColor = '#10b981';
      cursor = 'pointer';
    } else if (isEmergencyRow(row)) {
      backgroundColor = '#1e3a8a';
      cursor = 'not-allowed';
    }
    
    return {
      width: '40px',
      height: '40px',
      borderRadius: '4px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: '12px',
      fontWeight: '600',
      color: 'white',
      cursor: cursor,
      transition: 'all 0.2s',
      backgroundColor: backgroundColor
    };
  };

  const calculateTotalPrice = () => {
    return selectedSeats.reduce((total, seatId) => {
      const row = parseInt(seatId.match(/\d+/)[0]);
      const category = getSeatCategory(row);
      return total + category.price;
    }, 0);
  };

  const handleNext = () => {
    onSeatsSelected(selectedSeats);
  };

  if (loading) {
    return (
      <div style={{position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999}}>
        <div style={{backgroundColor: 'white', padding: '32px', borderRadius: '8px'}}>Loading seats...</div>
      </div>
    );
  }

  return (
    <div style={{position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '16px', zIndex: 9999}}>
      <div style={{backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 25px 50px -12px rgba(0,0,0,0.25)', maxWidth: '1200px', width: '100%', maxHeight: '90vh', overflow: 'hidden', display: 'flex', flexDirection: 'column'}}>
        
        {/* Header */}
        <div style={{backgroundColor: '#1e40af', color: 'white', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
          <h2 style={{fontSize: '20px', fontWeight: 'bold', margin: 0}}>Seat(s) selection</h2>
          <button onClick={onClose} style={{backgroundColor: 'transparent', border: 'none', color: 'white', cursor: 'pointer', padding: '4px', borderRadius: '50%'}}>
            <X size={24} />
          </button>
        </div>

        {/* Flight Info */}
        <div style={{backgroundColor: '#1e3a8a', color: 'white', padding: '12px', display: 'flex', alignItems: 'center', gap: '8px'}}>
          <Plane size={20} />
          <span style={{fontWeight: '600'}}>Flight {flightId}</span>
        </div>

        {/* Info Banner */}
        <div style={{backgroundColor: '#dbeafe', borderLeft: '4px solid #3b82f6', padding: '12px', display: 'flex', alignItems: 'flex-start', gap: '12px'}}>
          <Info style={{color: '#2563eb', flexShrink: 0, marginTop: '4px'}} size={20} />
          <p style={{fontSize: '14px', color: '#374151', margin: 0}}>
            You don't have seats for this part of your trip yet. Select seats to make sure you sit together.
          </p>
        </div>

        {/* Main Content */}
        <div style={{display: 'flex', flex: 1, overflow: 'hidden'}}>
          
          {/* Seat Map */}
          <div style={{flex: 1, overflowY: 'auto', padding: '24px'}}>
            <div style={{maxWidth: '448px', margin: '0 auto'}}>
              
              {/* Cockpit */}
              <div style={{backgroundColor: '#e5e7eb', borderTopLeftRadius: '9999px', borderTopRightRadius: '9999px', height: '48px', marginBottom: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                <div style={{color: '#4b5563', fontSize: '14px', fontWeight: '600'}}>Cockpit</div>
              </div>

              {/* Seats */}
              {Array.from({ length: rows }, (_, rowIdx) => {
                const row = rowIdx + 1;
                const isEmergency = isEmergencyRow(row);
                
                return (
                  <div key={row} style={{marginBottom: '4px'}}>
                    <div style={{display: 'flex', alignItems: 'center', gap: '8px'}}>
                      
                      {/* Row Number Left */}
                      <div style={{width: '32px', textAlign: 'center', fontSize: '14px', fontWeight: '600', color: '#4b5563'}}>
                        {row}
                      </div>

                      {/* Left Seats (ABC) */}
                      <div style={{display: 'flex', gap: '4px'}}>
                        {Array.from({ length: aisleAfter }, (_, seatIdx) => {
                          const seatId = getSeatId(row, seatIdx);
                          return (
                            <div
                              key={seatId}
                              style={getSeatStyle(row, seatIdx)}
                              onClick={() => handleSeatClick(seatId, row)}
                              onMouseEnter={() => setHoveredSeat(seatId)}
                              onMouseLeave={() => setHoveredSeat(null)}
                              title={seatId}
                            >
                              {isEmergency && '✈️'}
                              {isSeatReserved(seatId) && !isEmergency && '✕'}
                            </div>
                          );
                        })}
                      </div>

                      {/* Aisle */}
                      <div style={{width: '32px'}}></div>

                      {/* Right Seats (DEF) */}
                      <div style={{display: 'flex', gap: '4px'}}>
                        {Array.from({ length: seatsPerRow - aisleAfter }, (_, seatIdx) => {
                          const actualSeatIdx = seatIdx + aisleAfter;
                          const seatId = getSeatId(row, actualSeatIdx);
                          return (
                            <div
                              key={seatId}
                              style={getSeatStyle(row, actualSeatIdx)}
                              onClick={() => handleSeatClick(seatId, row)}
                              onMouseEnter={() => setHoveredSeat(seatId)}
                              onMouseLeave={() => setHoveredSeat(null)}
                              title={seatId}
                            >
                              {isEmergency && '✈️'}
                              {isSeatReserved(seatId) && !isEmergency && '✕'}
                            </div>
                          );
                        })}
                      </div>

                      {/* Row Number Right */}
                      <div style={{width: '32px', textAlign: 'center', fontSize: '14px', fontWeight: '600', color: '#4b5563'}}>
                        {row}
                      </div>
                    </div>

                    {/* Hover Info */}
                    {hoveredSeat && hoveredSeat.startsWith(`${row}`) && (
                      <div style={{marginTop: '4px', textAlign: 'center'}}>
                        <div style={{display: 'inline-block', backgroundColor: '#1e3a8a', color: 'white', padding: '4px 12px', borderRadius: '4px', fontSize: '14px'}}>
                          {hoveredSeat} - {getSeatCategory(row).label} - €{getSeatCategory(row).price.toFixed(2)}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Legend Sidebar */}
          <div style={{width: '320px', backgroundColor: '#f9fafb', padding: '24px', borderLeft: '1px solid #e5e7eb', overflowY: 'auto'}}>
            <h3 style={{fontWeight: 'bold', fontSize: '18px', marginBottom: '16px', marginTop: 0}}>Seat Categories</h3>
            
            <div style={{display: 'flex', flexDirection: 'column', gap: '12px'}}>
              
              {/* Extra Legroom */}
              <div style={{display: 'flex', alignItems: 'flex-start', gap: '12px', padding: '12px', backgroundColor: 'white', borderRadius: '4px', border: '1px solid #e5e7eb'}}>
                <div style={{width: '40px', height: '40px', backgroundColor: '#1e3a8a', borderRadius: '4px', flexShrink: 0}}></div>
                <div style={{flex: 1}}>
                  <div style={{fontWeight: '600'}}>Extra legroom seats</div>
                  <div style={{fontSize: '14px', color: '#4b5563'}}>Maximum legroom with these seats</div>
                  <div style={{textAlign: 'right', marginTop: '4px'}}>
                    <div style={{fontWeight: 'bold'}}>€ 15.00</div>
                    <div style={{fontSize: '12px', color: '#6b7280'}}>per person</div>
                  </div>
                </div>
              </div>

              {/* Front Seat */}
              <div style={{display: 'flex', alignItems: 'flex-start', gap: '12px', padding: '12px', backgroundColor: 'white', borderRadius: '4px', border: '1px solid #e5e7eb'}}>
                <div style={{width: '40px', height: '40px', backgroundColor: '#fbbf24', borderRadius: '4px', flexShrink: 0}}></div>
                <div style={{flex: 1}}>
                  <div style={{fontWeight: '600'}}>Front seat</div>
                  <div style={{fontSize: '14px', color: '#4b5563'}}>Be first off the plane with these seats</div>
                  <div style={{textAlign: 'right', marginTop: '4px'}}>
                    <div style={{fontWeight: 'bold'}}>€ 13.01</div>
                    <div style={{fontSize: '12px', color: '#6b7280'}}>per person</div>
                  </div>
                </div>
              </div>

              {/* Standard */}
              <div style={{display: 'flex', alignItems: 'flex-start', gap: '12px', padding: '12px', backgroundColor: 'white', borderRadius: '4px', border: '2px solid #3b82f6'}}>
                <div style={{width: '40px', height: '40px', backgroundColor: '#3b82f6', borderRadius: '4px', flexShrink: 0}}></div>
                <div style={{flex: 1}}>
                  <div style={{fontWeight: '600'}}>Standard</div>
                  <div style={{fontSize: '14px', color: '#4b5563'}}>Pick your favourite seat / avoid the middle one</div>
                  <div style={{textAlign: 'right', marginTop: '4px'}}>
                    <div style={{fontWeight: 'bold'}}>€ 7.00</div>
                    <div style={{fontSize: '12px', color: '#6b7280'}}>per person</div>
                  </div>
                </div>
              </div>

              {/* On Sale */}
              <div style={{display: 'flex', alignItems: 'flex-start', gap: '12px', padding: '12px', backgroundColor: 'white', borderRadius: '4px', border: '1px solid #e5e7eb'}}>
                <div style={{width: '40px', height: '40px', backgroundColor: '#dc2626', borderRadius: '4px', flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontWeight: 'bold'}}>
                  ⚡
                </div>
                <div style={{flex: 1}}>
                  <div style={{fontWeight: '600'}}>On sale!</div>
                  <div style={{fontSize: '14px', color: '#4b5563'}}>Buy now and save up to 25% off</div>
                  <div style={{textAlign: 'right', marginTop: '4px'}}>
                    <div style={{fontWeight: 'bold'}}>€ 3.00</div>
                    <div style={{fontSize: '12px', color: '#6b7280'}}>per person</div>
                  </div>
                </div>
              </div>

              {/* Reserved */}
              <div style={{display: 'flex', alignItems: 'flex-start', gap: '12px', padding: '12px', backgroundColor: 'white', borderRadius: '4px', border: '1px solid #e5e7eb'}}>
                <div style={{width: '40px', height: '40px', backgroundColor: '#d1d5db', borderRadius: '4px', flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>✕</div>
                <div style={{flex: 1}}>
                  <div style={{fontWeight: '600'}}>Reserved</div>
                </div>
              </div>

              {/* Selected */}
              <div style={{display: 'flex', alignItems: 'flex-start', gap: '12px', padding: '12px', backgroundColor: 'white', borderRadius: '4px', border: '2px solid #10b981'}}>
                <div style={{width: '40px', height: '40px', backgroundColor: '#10b981', borderRadius: '4px', flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white'}}>✓</div>
                <div style={{flex: 1}}>
                  <div style={{fontWeight: '600'}}>Selected Seat</div>
                </div>
              </div>
            </div>

            {/* Selected Seats Summary */}
            {selectedSeats.length > 0 && (
              <div style={{marginTop: '24px', padding: '16px', backgroundColor: '#d1fae5', borderRadius: '4px', border: '1px solid #10b981'}}>
                <h4 style={{fontWeight: 'bold', marginBottom: '8px', marginTop: 0}}>Your Selected Seats:</h4>
                <div style={{display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '12px'}}>
                  {selectedSeats.map(seat => (
                    <span key={seat} style={{backgroundColor: '#10b981', color: 'white', padding: '4px 12px', borderRadius: '4px', fontSize: '14px', fontWeight: '600'}}>
                      {seat}
                    </span>
                  ))}
                </div>
                <div style={{textAlign: 'right'}}>
                  <div style={{fontSize: '14px', color: '#4b5563'}}>Total:</div>
                  <div style={{fontSize: '24px', fontWeight: 'bold', color: '#10b981'}}>€ {calculateTotalPrice().toFixed(2)}</div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div style={{borderTop: '1px solid #e5e7eb', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#f9fafb'}}>
          <button onClick={onClose} style={{padding: '8px 24px', color: '#2563eb', backgroundColor: 'transparent', border: 'none', borderRadius: '4px', fontWeight: '600', cursor: 'pointer', fontSize: '16px'}}>
            Cancel
          </button>
          <div style={{display: 'flex', alignItems: 'center', gap: '16px'}}>
            <div style={{textAlign: 'right'}}>
              <div style={{fontSize: '14px', color: '#4b5563'}}>Price</div>
              <div style={{fontSize: '24px', fontWeight: 'bold'}}>€ {calculateTotalPrice().toFixed(2)}</div>
            </div>
            <button onClick={handleNext} style={{padding: '12px 32px', backgroundColor: '#fbbf24', border: 'none', borderRadius: '4px', fontWeight: 'bold', fontSize: '18px', cursor: 'pointer'}}>
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SeatSelectionModal;