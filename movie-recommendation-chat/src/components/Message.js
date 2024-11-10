import React from 'react';
import './Message.css';

const Message = ({ message, isUser }) => {
  return (
    <div className={`message ${isUser ? 'user' : 'bot'}`}>
      {message}
    </div>
  );
};

export default Message;