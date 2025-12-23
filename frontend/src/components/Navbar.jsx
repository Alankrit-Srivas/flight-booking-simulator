import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Navbar.css';

function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <Link to="/" className="navbar-brand">
          SkyPlane
        </Link>
        <div className="navbar-right">
          <button className="nav-item">
            <span className="icon">●</span> Help
          </button>
          
          {isAuthenticated ? (
            <>
              <div className="nav-item user-info">
                <span className="icon">👤</span>
                <span>{user?.first_name}</span>
              </div>
              <Link to="/search" className="btn btn-outline">
                My Trips
              </Link>
              <button className="btn btn-secondary" onClick={handleLogout}>
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/signup" className="btn btn-outline">
                Sign Up
              </Link>
              <Link to="/login" className="btn btn-secondary">
                Log In
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;