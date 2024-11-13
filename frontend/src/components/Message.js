import React from 'react';
import './Message.css';
import popcorn from '../images/pngwing.com.png';

const Message = ({ message, isUser }) => {
  return (
    <div className={`message ${isUser ? 'user' : 'bot'}`}>
      {message}
    </div>
  );
};

export default Message;