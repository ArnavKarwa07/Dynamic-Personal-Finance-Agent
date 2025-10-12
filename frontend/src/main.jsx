import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";

// Import organized CSS modules
import "./styles/reset.css";
import "./styles/typography.css";
import "./styles/buttons.css";
import "./styles/forms.css";
import "./styles/layout.css";
import "./styles/components.css";
import "./styles/hero.css";
import "./styles/animations.css";
import "./styles/utilities.css";
import "./styles/accessibility.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);
