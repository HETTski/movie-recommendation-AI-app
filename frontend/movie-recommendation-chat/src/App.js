import React from 'react';
import Chat from './components/Chat';
import Navbar from './components/Navbar';
import './App.css';

function App() {
  return (
    <div className="App">
      <Navbar />
      <Chat />
    </div>
  );
}

export default App;