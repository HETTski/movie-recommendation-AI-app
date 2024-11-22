import React from 'react';
import './Message.css';

const Message = ({ message, isUser, onAddToDb }) => {
  return (
    <div className={`message ${isUser ? 'user' : 'bot'}`}>
      {message}
      {!isUser && /** fix when add login and register */ !localStorage.getItem("token") && Number(message[0]) && (
        <button className="add-to-db-btn" onClick={onAddToDb}>
          Add to db "{message.split('"')[1]}"
        </button>
      )}
    </div>
  );
};

export default Message;
