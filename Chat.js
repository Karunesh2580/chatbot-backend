import React, { useState } from "react";

function Chat() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!prompt.trim()) return;
    setLoading(true);

    const res = await fetch("http://127.0.0.1:9000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    const data = await res.json();
    setMessages([...messages, { user: prompt, bot: data.response }]);
    setPrompt("");
    setLoading(false);
  };

  // ✅ Enter key handler
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      e.preventDefault(); // default form submit रोकता है
      sendMessage();
    }
  };

  return (
    <div
      style={{
        maxWidth: "600px",
        margin: "40px auto",
        fontFamily: "Segoe UI, sans-serif",
        background: "linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%)",
        borderRadius: "15px",
        padding: "20px",
        boxShadow: "0 8px 20px rgba(0,0,0,0.2)",
      }}
    >
      <h2 style={{ textAlign: "center", color: "#333", marginBottom: "15px" }}>
        🤖 My Unique Chatbot
      </h2>

      <div
        style={{
          background: "white",
          borderRadius: "10px",
          padding: "15px",
          height: "350px",
          overflowY: "auto",
          marginBottom: "15px",
        }}
      >
        {messages.map((msg, idx) => (
          <div key={idx} style={{ marginBottom: "12px" }}>
            <div
              style={{
                background: "#DCF8C6",
                padding: "10px",
                borderRadius: "15px",
                maxWidth: "80%",
                marginBottom: "5px",
                boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
              }}
            >
              <b>You:</b> {msg.user}
            </div>
            <div
              style={{
                background: "#F1F0F0",
                padding: "10px",
                borderRadius: "15px",
                maxWidth: "80%",
                boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
              }}
            >
              <b>Bot:</b> {msg.bot}
            </div>
          </div>
        ))}
        {loading && (
          <p style={{ fontStyle: "italic", color: "gray" }}>Bot is thinking...</p>
        )}
      </div>

      <div style={{ display: "flex" }}>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyPress={handleKeyPress}   // ✅ Enter key listener
          placeholder="Type your message..."
          style={{
            flex: 1,
            padding: "10px",
            borderRadius: "10px",
            border: "1px solid #ccc",
            outline: "none",
            fontSize: "14px",
          }}
        />
        <button
          onClick={sendMessage}
          style={{
            marginLeft: "10px",
            padding: "10px 20px",
            background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            color: "white",
            border: "none",
            borderRadius: "10px",
            cursor: "pointer",
            fontWeight: "bold",
            transition: "0.3s",
          }}
          onMouseOver={(e) =>
            (e.target.style.background =
              "linear-gradient(135deg, #764ba2 0%, #667eea 100%)")
          }
          onMouseOut={(e) =>
            (e.target.style.background =
              "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
          }
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default Chat;