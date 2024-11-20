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

    try {
      const response = await axios.post('http://localhost:5000/chat', {
        message: input, // User message
        show_now_playing: false, // Set to true if you want to show now playing movies
      });

      const botMessage = {
        message: response.data.gpt_response, // Response from GPT
        isUser: false
      };

      const movieMessages = response.data.movie_recommendations
        ? response.data.movie_recommendations.map((movie, index) => ({
            message: `${movie.title}: ${movie.overview}`,
            isUser: false
          }))
        : [];

      setMessages((prevMessages) => [...prevMessages, userMessage, botMessage, ...movieMessages]);
    } catch (error) {
      console.error('Error sending message:', error);
    }

    setInput(''); // Clear input field
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <Message key={index} message={msg.message} isUser={msg.isUser} />
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
