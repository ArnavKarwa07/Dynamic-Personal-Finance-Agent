import React from "react";
import ChatBot from "@features/ChatBot";

// Thin wrapper that renders the shared ChatBot in floating mode
const FloatingAssistant = () => {
  return <ChatBot />; // default variant is "floating"
};

export default FloatingAssistant;
