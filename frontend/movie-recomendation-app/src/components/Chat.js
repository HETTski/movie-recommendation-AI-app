import React, { useState } from 'react';
import axios from 'axios';
import Message from './Message';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  // Function to send messages
  const handleSend = async () => {
    if (input.trim() === '') return;

    const userMessage = { message: input, isUser: true };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput(''); // Clear input field immediately

    try {
      const payload = {
        query: input,
        watched_movies: localStorage.getItem('watched_movies') 
          ? JSON.parse(localStorage.getItem('watched_movies')) 
          : [],
        use_db: localStorage.getItem('token') ? true : false,
      };

      const response = await axios.post('http://localhost:8000/api/movies/recommendations/', payload, {
        headers: {
          Authorization: localStorage.getItem('token') ? `Bearer ${localStorage.getItem('token')}` : '',
        },
      });

      // Split the response into header and movies
      const responseText = response.data.recommendations;
      
      // Add the header as a bot message
      setMessages((prevMessages) => [...prevMessages, { message: responseText.split(':')[0]+":", isUser: false }]);

      // Process and add movies to the messages
      const movieList = responseText.split(":").filter((e, id) => id > 0).join(":").split(/\d+\./);
      movieList.forEach((movie, index) => {
        if (index > 0) { // Avoid empty strings
          setMessages((prevMessages) => [
            ...prevMessages,
            { message: `${index}. ${movie.trim()}`, isUser: false, movie: movie.split('"')[1] },
          ]);
        }
      });

    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { message: 'An error occurred while fetching recommendations.', isUser: false },
      ]);
    }
  };

  // Function to handle key press
  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSend();
    }
  };

  const handleAddToDb = async (movie) => {
    try {
      const payload = {
        title: movie,
        description: '',
        sites: []
      };

      console.log("Hello!");

      const response = await axios.post(
        'http://localhost:8000/api/user/movies/add/',
        payload,
        {
          headers: {
            Authorization: localStorage.getItem('token') ? `Bearer ${localStorage.getItem('token')}` : '',
          },
        }
      );

      alert(`Movie: "${movie}" was added to db!`);
    } catch (error) {
      console.error('Error adding movie to DB:', error);
      alert('Error adding movie to DB.');
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <Message
            key={index}
            message={msg.message}
            isUser={msg.isUser}
            onAddToDb={
              msg.movie ? () => handleAddToDb(msg.movie) : null
            }
          />
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress} // Add event listener for key press
          placeholder="Type your message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
