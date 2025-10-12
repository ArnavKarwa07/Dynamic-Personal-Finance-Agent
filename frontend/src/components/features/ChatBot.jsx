/**
 * Chat Bot Component
 */
import React, { useState, useRef, useEffect } from "react";
import { useApp } from "@store/AppContext";
import { financeAPI } from "@services/financeAPI";
import { cn } from "@utils";

const ChatBot = ({ className, variant = "floating" }) => {
  const { state, dispatch } = useApp();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [trace, setTrace] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: input,
      sender: "user",
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await financeAPI.chat({
        message: input,
        user_id: state.user?.id,
        context: {
          currentWorkflowStage: state.workflowStage,
          userProfile: state.userProfile,
          recentTransactions: state.transactions?.slice(-5) || [],
        },
        workflow_stage: state.workflowStage || "Started",
      });

      const botMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: "bot",
        timestamp: new Date(),
        suggestions: response.suggestions || [],
        workflowUpdate: response.workflowUpdate,
      };

      setMessages((prev) => [...prev, botMessage]);
      if (Array.isArray(response.explanations)) {
        setTrace(response.explanations);
      }

      // Update workflow stage based on API stage or workflowUpdate
      const stageFromApi = response.stage;
      const stageFromUpdate = response.workflowUpdate?.newStage;
      const nextStage = stageFromUpdate || stageFromApi;
      if (nextStage) {
        const canonical = (s) => {
          const map = {
            started: "Started",
            mvp: "MVP",
            intermediate: "Intermediate",
            advanced: "Advanced",
          };
          const key = String(s).toLowerCase();
          return map[key] || s;
        };
        dispatch({ type: "SET_WORKFLOW_STAGE", payload: canonical(nextStage) });
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I encountered an error. Please try again.",
        sender: "bot",
        timestamp: new Date(),
        isError: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInput(suggestion);
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (variant === "floating" && !isExpanded) {
    return (
      <div className={cn("fixed bottom-4 right-4 z-40", className)}>
        <button
          onClick={() => setIsExpanded(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white rounded-full p-4 shadow-lg transition-all duration-200 hover:scale-105"
          aria-label="Open chat"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
            />
          </svg>
        </button>
      </div>
    );
  }

  const containerClasses =
    variant === "floating"
      ? "fixed bottom-4 right-4 z-40 w-96 h-[32rem]"
      : "w-full h-[28rem]";

  return (
    <div
      className={cn(
        containerClasses + " bg-white rounded-lg shadow-xl border",
        className
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b bg-blue-600 text-white rounded-t-lg">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
                clipRule="evenodd"
              />
            </svg>
          </div>
          <div>
            <h3 className="font-semibold">Finance Assistant</h3>
            <p className="text-xs opacity-90">Stage: {state.workflowStage}</p>
          </div>
        </div>
        {variant === "floating" && (
          <button
            onClick={() => setIsExpanded(false)}
            className="text-white hover:text-gray-200 transition-colors"
            aria-label="Close chat"
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
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 p-4 h-80 overflow-y-auto space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 mt-8 text-sm">
            Ask anything about your finances to get started.
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                "flex",
                message.sender === "user" ? "justify-end" : "justify-start"
              )}
            >
              <div
                className={cn(
                  "max-w-xs lg:max-w-md px-4 py-2 rounded-lg",
                  message.sender === "user"
                    ? "bg-blue-600 text-white"
                    : message.isError
                    ? "bg-red-50 text-red-800 border border-red-200"
                    : "bg-gray-100 text-gray-800"
                )}
              >
                <p className="text-sm">{message.text}</p>
                {message.suggestions && message.suggestions.length > 0 && (
                  <div className="mt-2 space-y-1">
                    {message.suggestions.map((suggestion, index) => (
                      <button
                        key={index}
                        onClick={() => handleSuggestionClick(suggestion)}
                        className="block w-full text-left text-xs px-2 py-1 bg-white rounded border hover:bg-gray-50 transition-colors"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                )}
                <p className="text-xs opacity-70 mt-1">
                  {formatTime(message.timestamp)}
                </p>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg max-w-xs">
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
        {/* Explainable AI trace */}
        {trace.length > 0 && (
          <div className="mt-4 space-y-2">
            <h4 className="text-xs uppercase tracking-wide text-gray-500">
              What the AI did
            </h4>
            <ol className="list-decimal ml-5 space-y-1">
              {trace.map((t, i) => (
                <li key={i} className="text-xs text-gray-700">
                  <span className="font-medium">{t.step}:</span> {t.what}
                </li>
              ))}
            </ol>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about your finances..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!input.trim() || isLoading}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
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
      </div>
    </div>
  );
};

export default ChatBot;
