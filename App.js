import React from "react";
import Chat from "./Chat";

function App() {
  return (
    <div
      style={{
        background: "linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%)",
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "20px",
      }}
    >
      <Chat />
    </div>
  );
}

export default App;