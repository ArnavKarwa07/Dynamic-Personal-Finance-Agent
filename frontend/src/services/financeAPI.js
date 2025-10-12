/**
 * API Service for Dynamic Personal Finance Agent
 * Handles all communication with the backend API
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api/v1";

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
    // Backend expects email & password
    const loginData = {
      email: credentials.email || credentials.username,
      password: credentials.password,
      name: credentials.name,
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
    // The backend exposes /api/v1/auth/verify
    const resp = await this.apiCall("/auth/verify");
    return {
      user: resp.user,
      userProfile: resp.userProfile || null,
      workflowStage: resp.workflow_stage || resp.workflowStage,
    };
  }

  // Chat and workflow endpoints
  async sendChatMessage(
    query,
    userId = null,
    conversationHistory = null,
    workflow_stage = "Started"
  ) {
    // Backend chat expects: { message, context?, user_id, workflow_stage }
    const res = await this.apiCall("/chat", {
      method: "POST",
      body: JSON.stringify({
        message: query,
        user_id: userId || "default",
        workflow_stage,
        context: conversationHistory
          ? { conversation_history: conversationHistory }
          : undefined,
      }),
    });
    return {
      ...res,
      stage: res.workflow_stage || res.stage,
      suggestions: res.suggestions || [],
      visualizations: res.visualizations || [],
    };
  }

  // Backward-compat method used by some components
  async chat(payload) {
    // normalize payload to backend format
    const { message, context, user_id, workflow_stage } = payload || {};
    const res = await this.apiCall("/chat", {
      method: "POST",
      body: JSON.stringify({
        message,
        context,
        user_id: user_id || "default",
        workflow_stage: workflow_stage || "Started",
      }),
    });
    return {
      ...res,
      stage: res.workflow_stage || res.stage,
      suggestions: res.suggestions || [],
      visualizations: res.visualizations || [],
      workflowUpdate: res.workflowUpdate || null,
    };
  }

  async completeOnboarding(onboardingData) {
    // Backend expects { user_data: {...} }
    return this.apiCall("/onboarding", {
      method: "POST",
      body: JSON.stringify({ user_data: onboardingData }),
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
    // The backend currently doesn't expose a profile route in main.py.
    // Keep function for future use; return a mock aligned with verify endpoint.
    return {
      user: { id: userId, name: "Demo User", email: "demo@example.com" },
    };
  }

  // Dashboard data
  async getDashboard(params = {}) {
    const queryParams = new URLSearchParams(params).toString();
    const endpoint = queryParams ? `/dashboard?${queryParams}` : "/dashboard";
    return this.apiCall(endpoint);
  }

  // User-specific data
  async getTransactions(userId) {
    return this.apiCall(`/transactions/${userId}`);
  }

  async addTransaction(userId, tx) {
    return this.apiCall(`/transactions/${userId}`, {
      method: "POST",
      body: JSON.stringify(tx),
    });
  }

  async getGoals(userId) {
    return this.apiCall(`/goals/${userId}`);
  }

  async addGoal(userId, goal) {
    return this.apiCall(`/goals/${userId}`, {
      method: "POST",
      body: JSON.stringify(goal),
    });
  }

  async getBudgets(userId) {
    return this.apiCall(`/budgets/${userId}`);
  }

  async addBudget(userId, budget) {
    return this.apiCall(`/budgets/${userId}`, {
      method: "POST",
      body: JSON.stringify(budget),
    });
  }
}

// Create and export a singleton instance
const financeAPI = new FinanceAPIService();
export default financeAPI;
export { financeAPI };
