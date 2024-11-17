import React, { useState } from 'react';
import axios from 'axios';
import Message from './Message';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  // Funkcja do wysyłania wiadomości
  const handleSend = async () => {
    if (input.trim() === '') return;

    const userMessage = { message: input, isUser: true };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    try {
      const response = await axios.post('http://localhost:5000/chat', {
        message: input, // Wiadomość od użytkownika
        show_now_playing: false, // Możesz ustawić na true, jeśli chcesz pokazać filmy teraz grające
      });

      const botMessage = {
        message: response.data.gpt_response, // Odpowiedź od GPT
        isUser: false
      };

      const movieMessages = response.data.movie_recommendations.map((recommendation, index) => ({
        message: `${recommendation.title}\n${recommendation.movies.map(movie => `${movie.title}: ${movie.overview}`).join("\n")}`,
        isUser: false
      }));

      setMessages((prevMessages) => [...prevMessages, userMessage, botMessage, ...movieMessages]);
    } catch (error) {
      console.error('Error sending message:', error);
    }

    setInput(''); // Wyczyść pole wejściowe
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
