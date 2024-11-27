import React from 'react';
import './Navbar.css';

const Navbar = ({ isLoggedIn, onLoginClick, onLogout }) => {
  return (
    <div className="navbar">
      <h2>Movie AI</h2>
      <ul>
        <li>Home</li>
        <li>Chat</li>
        <li>About</li>
        <li>Contact</li>
      </ul>
      <div className="auth-buttons">
        {isLoggedIn ? (
          <button onClick={onLogout}>Logout</button>
        ) : (
          <button onClick={onLoginClick}>Login</button>
        )}
      </div>
    </div>
  );
};

export default Navbar;