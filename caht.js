import React, { useState } from 'react';

function Chat() {
  const [message, setMessage] = useState('');
  const [chatResponse, setChatResponse] = useState('');

  async function sendMessage() {
    if (!message) return;

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      setChatResponse(data.reply);
    } catch (error) {
      setChatResponse('Error: Could not get response');
    }
  }

  return (
    <div>
      <h2>Campus Support Chatbot</h2>
      <textarea
        rows="4"
        cols="50"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message here..."
      />
      <br />
      <button onClick={sendMessage}>Send</button>
      <div>
        <h3>Response:</h3>
        <p>{chatResponse}</p>
      </div>
    </div>
  );
}

export default Chat;
