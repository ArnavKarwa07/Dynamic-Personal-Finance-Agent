/**
 * API Service for Dynamic Personal Finance Agent
 * Handles all communication with the backend API
 */

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

class FinanceAPIService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.headers = {
      "Content-Type": "application/json",
    };
  }

  // Set authentication token
  setAuthToken(token) {
    if (token) {
      this.headers["Authorization"] = `Bearer ${token}`;
    } else {
      delete this.headers["Authorization"];
    }
  }

  // Generic API call method
  async apiCall(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.headers,
      ...options,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorData = await response
          .json()
          .catch(() => ({ message: "API Error" }));
        throw new Error(
          errorData.detail || errorData.message || `HTTP ${response.status}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error(`API call failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // Authentication endpoints
  async login(credentials) {
    // Handle both email and username based login
    const loginData = {
      email: credentials.email || credentials.username,
      password: credentials.password,
    };

    return this.apiCall("/auth/login", {
      method: "POST",
      body: JSON.stringify(loginData),
    });
  }

  async register(userData) {
    const registerData = {
      email: userData.email,
      password: userData.password,
      name: userData.name,
    };

    return this.apiCall("/auth/register", {
      method: "POST",
      body: JSON.stringify(registerData),
    });
  }

  async logout() {
    return this.apiCall("/auth/logout", {
      method: "POST",
    });
  }

  // Token verification
  async verifyToken(token) {
    this.setAuthToken(token);
    // For demo purposes, return mock user data
    return {
      user: {
        id: "demo_user_001",
        email: "demo@example.com",
        name: "Demo User",
      },
      userProfile: {
        onboardingComplete: false,
        financialGoals: [],
      },
      workflowStage: "initial",
    };
  }

  // Chat and workflow endpoints
  async sendChatMessage(query, userId = null, conversationHistory = null) {
    return this.apiCall("/chat", {
      method: "POST",
      body: JSON.stringify({
        query,
        user_id: userId,
        conversation_history: conversationHistory,
      }),
    });
  }

  async completeOnboarding(onboardingData) {
    return this.apiCall("/onboarding", {
      method: "POST",
      body: JSON.stringify(onboardingData),
    });
  }

  async getWorkflowStatus(userId) {
    return this.apiCall(`/workflow/status/${userId}`);
  }

  async getWorkflowVisualization() {
    return this.apiCall("/workflow/visualization");
  }

  // Tool and feature endpoints
  async getAvailableTools() {
    return this.apiCall("/tools");
  }

  async getExampleQueries() {
    return this.apiCall("/examples");
  }

  // Health check
  async healthCheck() {
    return this.apiCall("/health");
  }

  // User profile
  async getUserProfile(userId) {
    return this.apiCall(`/profile/${userId}`);
  }
}

// Create and export a singleton instance
const financeAPI = new FinanceAPIService();
export default financeAPI;
export { financeAPI };
