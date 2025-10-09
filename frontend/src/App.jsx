import React, { useState } from "react";
import Header from "./components/Header";
import Hero from "./components/Hero";
import Features from "./components/Features";
import ChatBot from "./components/ChatBot";
import Dashboard from "./components/Dashboard";
import Footer from "./components/Footer";

function App() {
  const [showChatBot, setShowChatBot] = useState(false);
  const [currentView, setCurrentView] = useState("home");

  return (
    <div className="min-h-screen bg-gray-50">
      <Header currentView={currentView} setCurrentView={setCurrentView} />

      {currentView === "home" && (
        <>
          <Hero
            setCurrentView={setCurrentView}
            setShowChatBot={setShowChatBot}
          />
          <Features />
        </>
      )}

      {currentView === "dashboard" && <Dashboard />}

      <Footer />

      {/* Chat Bot Toggle Button */}
      <button
        onClick={() => setShowChatBot(!showChatBot)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-sky-600 hover:bg-sky-700 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center z-50"
        aria-label="Toggle Chat Bot"
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

      {/* Chat Bot Component */}
      {showChatBot && <ChatBot onClose={() => setShowChatBot(false)} />}
    </div>
  );
}

export default App;
