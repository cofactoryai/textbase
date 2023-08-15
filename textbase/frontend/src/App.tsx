
import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
//import { FaSun, FaMoon, FaPaperPlane, FaStar } from "react-icons/fa"; 
import {GoStar} from "react-icons/go";
import {GoStarFill} from "react-icons/go";
import "./App.css";

type Message = {
  content: string;
  role: "user" | "assistant";
};

function ChatMessage(props: { message: Message }) {
  return (
    <div className={`chat-message ${props.message.role}`}>
      <div className="message-content">
        <ReactMarkdown className="prose" remarkPlugins={[remarkGfm]}>
          {props.message.content}
        </ReactMarkdown>
      </div>
    </div>
  );
}

function App() {
  const [input, setInput] = useState<string>("");
  const [botState, setBotState] = useState<object>({});
  const [history, setHistory] = useState<Message[]>([]);
  const [darkMode, setDarkMode] = useState<boolean>(false);

  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [history]);

  async function chatRequest(history: Message[], botState: object) {
    try {
      const response = await fetch("http://localhost:4000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ messages: history, state: botState }),
      });
      const content: { botResponse: Message; newState: object } =
        await response.json();
      setHistory([...history, content.botResponse]);
      setBotState(content.newState);
    } catch (error) {
      console.error("Failed to send chat history:", error);
    }
  }

  function chatInputHandler() {
    if (!input) {
      return;
    }
    const newMessage: Message = {
      content: input,
      role: "user",
    };
    setHistory([...history, newMessage]);
    setInput("");
    chatRequest([...history, newMessage], botState);
  }

  return (
    <div className={`app ${darkMode ? "dark" : "light"}`}>
      <div className="chat-container">
        <div className="chat-history">
          {history.map((message, idx) => (
            <ChatMessage key={idx} message={message} />
          ))}
          <div ref={chatEndRef}></div>
        </div>
        <div className={`chat-input ${darkMode ? "dark" : "light"}`}>
          <input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
              setInput(e.target.value);
            }}
            onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
              if (e.key === "Enter") {
                chatInputHandler();
              }
            }}
          />
          <button
            className={`send-button ${darkMode ? "dark" : "light"}`}
            onClick={chatInputHandler}
          >
            <GoStarFill className="icon-moon" />
          </button>
          <div className="star-icon">
            <GoStar className="icon-star" />
          </div>
        </div>
      </div>
      <button
        className={`toggle-theme-button ${darkMode ? "dark" : "light"}`}
        onClick={() => {
          setDarkMode((prev) => !prev);
        }}
      >
        {darkMode ? <GoStar className="icon-sun" /> : <GoStarFill className="icon-moon" />}
      </button>
    </div>
  );
}

export default App;
