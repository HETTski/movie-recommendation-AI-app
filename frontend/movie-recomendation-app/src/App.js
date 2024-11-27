import React, { useState, useEffect } from 'react';
import Chat from './components/Chat';
import Navbar from './components/Navbar';
import Login from './components/Login';
import Register from './components/Register';
import UserMovies from './components/UserMovies'; // Import widoku filmów
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Stan logowania
  const [showLogin, setShowLogin] = useState(false); // Kontrola widoku logowania
  const [showRegister, setShowRegister] = useState(false); // Kontrola widoku rejestracji
  const [showUserMovies, setShowUserMovies] = useState(false); // Kontrola widoku listy filmów

  // Sprawdź token w localStorage przy pierwszym załadowaniu
  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, []);

  const handleLogin = () => {
    setIsLoggedIn(true);
    setShowLogin(false);
    setShowRegister(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    setIsLoggedIn(false);
    setShowUserMovies(false); // Ukryj widok filmów po wylogowaniu
  };

  const handleRegister = () => {
    setShowLogin(true);
    setShowRegister(false);
  };

  const handleUserMovies = () => {
    if(showUserMovies) setShowUserMovies(false);
    else setShowUserMovies(true);
  }

  return (
    <div className="App">
      <Navbar
        isLoggedIn={isLoggedIn}
        onLoginClick={() => {
          setShowLogin(true);
          setShowRegister(false);
        }}
        onRegisterClick={() => {
          setShowRegister(true);
          setShowLogin(false);
        }}
        onLogout={handleLogout}
        onMoviesShow={handleUserMovies}
      />
      {showLogin && <Login onLogin={handleLogin} />}
      {showRegister && <Register onRegisterSuccess={handleRegister}/>}
      {showUserMovies && <UserMovies />}
      <Chat />
    </div>
  );
}

export default App;
