import React, { useState, useRef, useEffect } from "react";
import FinanceAPI from "../api/financeAPI";

const ChatBot = ({ onClose }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hi! I'm your AI Financial Assistant. I can help you analyze expenses, track budgets, monitor investments, and achieve your financial goals. How can I help you today?",
      sender: "bot",
      timestamp: new Date(),
    },
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const messagesEndRef = useRef(null);

  // API configuration
  const API_BASE_URL = "http://localhost:8001/api/v1";

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check API connection on component mount
  useEffect(() => {
    checkApiConnection();
  }, []);

  const checkApiConnection = async () => {
    try {
      await FinanceAPI.healthCheck();
      setIsConnected(true);
    } catch (error) {
      console.error("API connection failed:", error);
      setIsConnected(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage("");
    setIsTyping(true);

    try {
      // Call the finance agent API
      const data = await FinanceAPI.chat(inputMessage, sessionId);

      // Update session ID if not set
      if (!sessionId) {
        setSessionId(data.session_id);
      }

      // Create bot response message
      const botResponse = {
        id: Date.now() + 1,
        text: data.response,
        sender: "bot",
        timestamp: new Date(),
        intent: data.intent,
        tools_used: data.tools_used,
        analysis_results: data.analysis_results,
      };

      setMessages((prev) => [...prev, botResponse]);
      setIsTyping(false);
    } catch (error) {
      console.error("Error sending message:", error);

      // Fallback error message
      const errorMessage = {
        id: Date.now() + 1,
        text: isConnected
          ? "I'm sorry, I encountered an error processing your request. Please try again."
          : "I'm having trouble connecting to the finance agent. Please make sure the backend server is running on http://localhost:8000",
        sender: "bot",
        timestamp: new Date(),
        isError: true,
      };

      setMessages((prev) => [...prev, errorMessage]);
      setIsTyping(false);
    }
  };

  const quickActions = [
    "How much did I spend on food this month?",
    "Am I over budget?",
    "How are my investments performing?",
    "How close am I to my emergency fund goal?",
    "Give me a financial summary",
    "Show me my spending by category",
  ];

  const handleQuickAction = (action) => {
    setInputMessage(action);
  };

  const clearSession = async () => {
    if (sessionId) {
      try {
        await FinanceAPI.clearSession(sessionId);
      } catch (error) {
        console.error("Error clearing session:", error);
      }
    }

    setMessages([
      {
        id: 1,
        text: "Hi! I'm your AI Financial Assistant powered by LangGraph. I can help you analyze expenses, track budgets, monitor investments, and achieve your financial goals. How can I help you today?",
        sender: "bot",
        timestamp: new Date(),
      },
    ]);
    setSessionId(null);
  };

  const renderMessage = (message) => {
    const isBot = message.sender === "bot";
    const hasAnalysis =
      message.analysis_results &&
      Object.keys(message.analysis_results).length > 0;

    return (
      <div
        key={message.id}
        className={`flex ${isBot ? "justify-start" : "justify-end"}`}
      >
        <div
          className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
            isBot
              ? message.isError
                ? "bg-red-100 text-red-800 border border-red-200"
                : "bg-gray-100 text-gray-800"
              : "bg-sky-600 text-white"
          }`}
        >
          <p className="text-sm whitespace-pre-wrap">{message.text}</p>

          {/* Show intent and tools used for bot messages */}
          {isBot && message.intent && !message.isError && (
            <div className="mt-2 pt-2 border-t border-gray-200">
              <p className="text-xs text-gray-500">
                Intent: <span className="font-medium">{message.intent}</span>
              </p>
              {message.tools_used && message.tools_used.length > 0 && (
                <p className="text-xs text-gray-500">
                  Tools:{" "}
                  <span className="font-medium">
                    {message.tools_used.join(", ")}
                  </span>
                </p>
              )}
            </div>
          )}

          {/* Analysis results indicator */}
          {hasAnalysis && (
            <div className="mt-2 pt-2 border-t border-gray-200">
              <p className="text-xs text-gray-500">
                📊 Analysis: {Object.keys(message.analysis_results).join(", ")}
              </p>
            </div>
          )}

          <p
            className={`text-xs mt-1 ${
              isBot
                ? message.isError
                  ? "text-red-500"
                  : "text-gray-500"
                : "text-sky-100"
            }`}
          >
            {message.timestamp.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </p>
        </div>
      </div>
    );
  };

  return (
    <div className="fixed bottom-20 right-6 w-96 h-[600px] bg-white rounded-xl shadow-2xl border border-gray-200 flex flex-col z-50">
      {/* Chat Header */}
      <div className="bg-sky-600 text-white p-4 rounded-t-xl flex items-center justify-between">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center mr-3">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h3 className="font-semibold">FinanceAI Assistant</h3>
            <p className="text-xs opacity-90 flex items-center">
              <span
                className={`w-2 h-2 rounded-full mr-1 ${
                  isConnected ? "bg-green-400" : "bg-red-400"
                }`}
              ></span>
              {isConnected ? "Connected" : "Disconnected"}
            </p>
          </div>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={clearSession}
            className="text-white hover:bg-white hover:bg-opacity-20 rounded-full p-1 transition-colors"
            title="Clear conversation"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
          <button
            onClick={onClose}
            className="text-white hover:bg-white hover:bg-opacity-20 rounded-full p-1 transition-colors"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map(renderMessage)}

        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div
                  className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.1s" }}
                ></div>
                <div
                  className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.2s" }}
                ></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      <div className="p-2 border-t border-gray-100">
        <div className="grid grid-cols-1 gap-2 mb-2 max-h-32 overflow-y-auto">
          {quickActions.map((action, index) => (
            <button
              key={index}
              onClick={() => handleQuickAction(action)}
              className="px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-xs transition-colors text-left"
              disabled={isTyping}
            >
              {action}
            </button>
          ))}
        </div>
      </div>

      {/* Input Form */}
      <form
        onSubmit={handleSendMessage}
        className="p-4 border-t border-gray-100"
      >
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask me about your finances..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent text-sm"
            disabled={isTyping}
          />
          <button
            type="submit"
            disabled={!inputMessage.trim() || isTyping}
            className="bg-sky-600 hover:bg-sky-700 disabled:bg-gray-300 text-white px-4 py-2 rounded-lg transition-colors"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
              />
            </svg>
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatBot;
