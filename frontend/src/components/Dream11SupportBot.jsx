import React, { useState, useRef, useEffect } from "react";

// Configuration Module
const CONFIG = {
  API_BASE_URL: "http://127.0.0.1:8000",
  ENDPOINTS: {
    CHAT: "/api/chat",
  },
  THEME: {
    primaryGradient: "linear-gradient(135deg, #ff6b35 0%, #f7931e 100%)",
    secondaryGradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    backgroundGradient:
      "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
  },
};

// API Service Module
class ChatAPI {
  static async sendMessage(message) {
    try {
      const response = await fetch(
        `${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.CHAT}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message }),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("API Error:", error);
      throw error;
    }
  }
}

// Styles Module
const styles = {
  appContainer: {
    height: "100vh",
    width: "100vw",
    background: CONFIG.THEME.backgroundGradient,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: "20px",
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    margin: 0,
    boxSizing: "border-box",
    overflow: "hidden",
    position: "fixed",
    top: 0,
    left: 0,
  },
  chatContainer: {
    width: "100%",
    maxWidth: "800px",
    height: "600px",
    background: "rgba(255, 255, 255, 0.05)",
    backdropFilter: "blur(15px)",
    borderRadius: "20px",
    border: "none",
    display: "flex",
    flexDirection: "column",
    overflow: "hidden",
    boxShadow: "0 20px 40px rgba(0, 0, 0, 0.5)",
    animation: "slideIn 0.8s ease-out",
  },
  chatHeader: {
    background: CONFIG.THEME.primaryGradient,
    padding: "20px",
    display: "flex",
    alignItems: "center",
    gap: "15px",
    position: "relative",
    overflow: "hidden",
    color: "white",
  },
  headerShimmer: {
    position: "absolute",
    top: 0,
    left: "-100%",
    width: "100%",
    height: "100%",
    background:
      "linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent)",
    animation: "shimmer 3s infinite",
  },
  botAvatar: {
    width: "50px",
    height: "50px",
    background: "linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%)",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "24px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
    animation: "bounce 2s ease-in-out infinite",
  },
  botInfo: {
    display: "flex",
    flexDirection: "column",
  },
  botTitle: {
    margin: 0,
    fontSize: "1.4em",
    fontWeight: 700,
  },
  botSubtitle: {
    margin: 0,
    fontSize: "0.9em",
    opacity: 0.9,
  },
  statusIndicator: {
    width: "12px",
    height: "12px",
    background: "#4CAF50",
    borderRadius: "50%",
    marginLeft: "auto",
    boxShadow: "0 0 10px rgba(76, 175, 80, 0.5)",
    animation: "pulse 2s infinite",
  },
  chatMessages: {
    flex: 1,
    padding: "20px",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: "15px",
    background: "rgba(255, 255, 255, 0.02)",
  },
  message: {
    maxWidth: "70%",
    padding: "15px 20px",
    borderRadius: "20px",
    position: "relative",
    wordWrap: "break-word",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    color: "white",
    animation: "messageSlide 0.5s ease-out",
    whiteSpace: "pre-wrap",  // Preserves newlines and spaces
    lineHeight: "2",
  },
  messageBot: {
    background: CONFIG.THEME.secondaryGradient,
    alignSelf: "flex-start",
    borderBottomLeftRadius: "5px",
  },
  messageUser: {
    background: CONFIG.THEME.primaryGradient,
    alignSelf: "flex-end",
    borderBottomRightRadius: "5px",
  },
  typingIndicator: {
    display: "flex",
    gap: "4px",
    alignItems: "center",
    padding: "5px 0",
  },
  typingDot: {
    width: "8px",
    height: "8px",
    background: "white",
    borderRadius: "50%",
    animation: "typing 1.4s infinite",
  },
  chatInput: {
    padding: "20px",
    background: "rgba(255, 255, 255, 0.05)",
    borderTop: "1px solid rgba(255, 255, 255, 0.1)",
  },
  inputForm: {
    display: "flex",
    gap: "10px",
    alignItems: "center",
  },
  inputField: {
    flex: 1,
    background: "rgba(255, 255, 255, 0.1)",
    border: "1px solid rgba(255, 255, 255, 0.2)",
    borderRadius: "25px",
    padding: "15px 20px",
    color: "white",
    fontSize: "16px",
    outline: "none",
    transition: "all 0.3s ease",
  },
  sendButton: {
    background: CONFIG.THEME.primaryGradient,
    border: "none",
    borderRadius: "50%",
    width: "50px",
    height: "50px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    transition: "all 0.3s ease",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
  },
  sendIcon: {
    color: "white",
    fontSize: "20px",
    fontWeight: "bold",
  },
};

// Keyframes for animations
const keyframes = `
  @keyframes slideIn {
    from { transform: translateY(50px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }

  @keyframes messageSlide {
    from { transform: translateX(-20px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }

  @keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
  }

  @keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.2); opacity: 0.7; }
    100% { transform: scale(1); opacity: 1; }
  }

  @keyframes typing {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-10px); }
  }

  @keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
  }
`;

// Typing Indicator Component
const TypingIndicator = () => (
  <div style={styles.typingIndicator}>
    <div style={{ ...styles.typingDot }}></div>
    <div style={{ ...styles.typingDot, animationDelay: "0.2s" }}></div>
    <div style={{ ...styles.typingDot, animationDelay: "0.4s" }}></div>
  </div>
);

// Message Component
const Message = ({ message, isBot, isLoading }) => {
  const messageStyle = {
    ...styles.message,
    ...(isBot ? styles.messageBot : styles.messageUser),
  };

  return (
    <div style={messageStyle}>{isLoading ? <TypingIndicator /> : message}</div>
  );
};

// Bot Avatar Component
const BotAvatar = () => <div style={styles.botAvatar}>🤖</div>;

// Chat Header Component
const ChatHeader = () => (
  <div style={styles.chatHeader}>
    <div style={styles.headerShimmer}></div>
    <BotAvatar />
    <div style={styles.botInfo}>
      <h2 style={styles.botTitle}>Dream11 Support Bot</h2>
      <p style={styles.botSubtitle}>Here to help you with your queries</p>
    </div>
    <div style={styles.statusIndicator}></div>
  </div>
);

// Chat Messages Component
const ChatMessages = ({ messages, isLoading }) => {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div style={styles.chatMessages}>
      {messages.map((msg, index) => (
        <Message key={index} message={msg.text} isBot={msg.isBot} />
      ))}
      {isLoading && <Message isBot={true} isLoading={true} />}
      <div ref={messagesEndRef} />
    </div>
  );
};

// Chat Input Component
const ChatInput = ({ onSendMessage, isLoading }) => {
  const [inputValue, setInputValue] = useState("");

  const handleSubmit = () => {
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue.trim());
      setInputValue("");
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const inputStyle = {
    ...styles.inputField,
    opacity: isLoading ? 0.6 : 1,
    cursor: isLoading ? "not-allowed" : "text",
  };

  const buttonStyle = {
    ...styles.sendButton,
    opacity: isLoading || !inputValue.trim() ? 0.6 : 1,
    cursor: isLoading || !inputValue.trim() ? "not-allowed" : "pointer",
    transform: isLoading || !inputValue.trim() ? "none" : "scale(1)",
  };

  return (
    <div style={styles.chatInput}>
      <div style={styles.inputForm}>
        <input
          type="text"
          style={inputStyle}
          placeholder="Type your message..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
        />
        <button
          style={buttonStyle}
          onClick={handleSubmit}
          disabled={isLoading || !inputValue.trim()}
          onMouseEnter={(e) => {
            if (!isLoading && inputValue.trim()) {
              e.target.style.transform = "scale(1.1)";
              e.target.style.boxShadow = "0 6px 12px rgba(0, 0, 0, 0.3)";
            }
          }}
          onMouseLeave={(e) => {
            if (!isLoading && inputValue.trim()) {
              e.target.style.transform = "scale(1)";
              e.target.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.2)";
            }
          }}
        >
          <span style={styles.sendIcon}>➤</span>
        </button>
      </div>
    </div>
  );
};

// Main Chat Bot Component
const Dream11SupportBot = () => {
  const [messages, setMessages] = useState([
    {
      text: "Hello! I'm Dream11's support bot. How can I help you today?",
      isBot: true,
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (message) => {
    // Add user message
    setMessages((prev) => [...prev, { text: message, isBot: false }]);
    setIsLoading(true);

    try {
      // Call API
      const response = await ChatAPI.sendMessage(message);

      // Add bot response
      setMessages((prev) => [
        ...prev,
        {
          text:
            response.reply ||
            response.message ||
            response.response ||
            "Sorry, I couldn't process that request.",
          isBot: true,
        },
      ]);
    } catch (error) {
      // Add error message
      setMessages((prev) => [
        ...prev,
        {
          text: "Sorry, I'm having trouble connecting right now. Please try again later.",
          isBot: true,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <style>{`
        ${keyframes}
        
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }
        
        html, body {
          height: 100%;
          width: 100%;
          overflow: hidden;
          margin: 0;
          padding: 0;
        }
        
        #root {
          height: 100vh;
          width: 100vw;
          overflow: hidden;
        }
      `}</style>
      <div style={styles.appContainer}>
        <div style={styles.chatContainer}>
          <ChatHeader />
          <ChatMessages messages={messages} isLoading={isLoading} />
          <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>
      </div>
    </>
  );
};

export default Dream11SupportBot;
