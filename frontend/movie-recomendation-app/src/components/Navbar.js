import React from 'react';
import './Navbar.css';

const Navbar = ({ isLoggedIn, onLoginClick, onLogout, onRegisterClick, onMoviesShow }) => {
  return (
    <div className="navbar">
      <h2>Movie AI</h2>
      <div className="auth-buttons">
        {isLoggedIn ? (
          <div className="button-container">
            <button className="navbarButton" onClick={onMoviesShow}>
              Movies List
            </button>
            <button className="navbarButton" onClick={onLogout}>
              Logout
            </button>
          </div>
        ) : (
          <div className="button-container">
            <button className="navbarButton" onClick={onLoginClick}>
              Login
            </button>
            <button className="navbarButton" onClick={onRegisterClick}>
              Register
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Navbar;
