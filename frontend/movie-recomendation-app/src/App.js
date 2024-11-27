import React, { useState, useEffect } from 'react';
import Chat from './components/Chat';
import Navbar from './components/Navbar';
import Login from './components/Login';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showLogin, setShowLogin] = useState(false); // Kontrola widoczności formularza logowania

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token); // Ustaw stan na true, jeśli token istnieje
  }, []);

  const handleLogin = () => {
    setIsLoggedIn(true);
    setShowLogin(false); // Ukryj formularz logowania po sukcesie
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    setIsLoggedIn(false);
  };

  return (
    <div className="App">
      <Navbar
        isLoggedIn={isLoggedIn}
        onLoginClick={() => setShowLogin(true)} // Otwórz formularz logowania
        onLogout={handleLogout}
      />
      {showLogin && <Login onLogin={handleLogin} />}
      <Chat /> {/* Chat zawsze widoczny */}
    </div>
  );
}

export default App;
