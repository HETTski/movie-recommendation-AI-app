import React from 'react';
import './Message.css';

const Message = ({ message, isUser, onAddToDb, isLoggedIn }) => {
  // Function to extract text within quotes (either single or double)
  const extractQuotedText = (text) => {
    const match = text.match(/["']([^"']+)["']/);
    return match ? match[1] : '';
  };

  const quotedText = extractQuotedText(message);

  return (
    <div className={`message ${isUser ? 'user' : 'bot'}`}>
      {message}
      {!isUser && isLoggedIn && quotedText && (
        <button onClick={onAddToDb}>
          Add to db "{quotedText}"
        </button>
      )}
    </div>
  );
};

export default Message;