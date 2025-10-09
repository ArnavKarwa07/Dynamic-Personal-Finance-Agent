// API client for communicating with the backend
const API_BASE_URL = "http://localhost:8001/api/v1";

class FinanceAPI {
  static async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        throw new Error(
          `API Error: ${response.status} - ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // Health check
  static async healthCheck() {
    return this.request("/health");
  }

  // Chat with finance agent
  static async chat(query, sessionId = null) {
    return this.request("/chat", {
      method: "POST",
      body: JSON.stringify({
        query,
        session_id: sessionId,
      }),
    });
  }

  // Get workflow information
  static async getWorkflow() {
    return this.request("/workflow");
  }

  // Get example queries
  static async getExamples() {
    return this.request("/examples");
  }

  // Analytics summary
  static async getAnalyticsSummary() {
    return this.request("/analytics/summary");
  }

  // Data endpoints
  static async getTransactions() {
    return this.request("/data/transactions");
  }

  static async getInvestments() {
    return this.request("/data/investments");
  }

  static async getGoals() {
    return this.request("/data/goals");
  }

  static async getBudget() {
    return this.request("/data/budget");
  }

  // Session management
  static async clearSession(sessionId) {
    return this.request(`/session/${sessionId}`, {
      method: "DELETE",
    });
  }

  static async listSessions() {
    return this.request("/sessions");
  }

  // Data entry endpoints
  static async addTransaction(transactionData) {
    return this.request("/data/transactions", {
      method: "POST",
      body: JSON.stringify(transactionData),
    });
  }

  static async addGoal(goalData) {
    return this.request("/data/goals", {
      method: "POST",
      body: JSON.stringify(goalData),
    });
  }
}

export default FinanceAPI;
