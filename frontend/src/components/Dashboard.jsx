import React, { useState, useEffect } from "react";

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState("overview");
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_BASE_URL = "http://localhost:8001/api/v1";

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "budget", label: "Budget" },
    { id: "investments", label: "Investments" },
    { id: "goals", label: "Goals" },
  ];

  // Load dashboard data on component mount
  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      // Fetch data from multiple endpoints
      const [
        analyticsRes,
        transactionsRes,
        investmentsRes,
        goalsRes,
        budgetRes,
      ] = await Promise.all([
        fetch(`${API_BASE_URL}/analytics/summary`),
        fetch(`${API_BASE_URL}/data/transactions`),
        fetch(`${API_BASE_URL}/data/investments`),
        fetch(`${API_BASE_URL}/data/goals`),
        fetch(`${API_BASE_URL}/data/budget`),
      ]);

      const analytics = await analyticsRes.json();
      const transactions = await transactionsRes.json();
      const investments = await investmentsRes.json();
      const goals = await goalsRes.json();
      const budget = await budgetRes.json();

      setDashboardData({
        analytics: analytics.summary,
        transactions: transactions.transactions.slice(0, 5), // Show recent 5
        investments: investments.investments,
        goals: goals.goals,
        budget: budget.budget,
      });

      setError(null);
    } catch (err) {
      console.error("Error loading dashboard data:", err);
      setError(
        "Failed to load dashboard data. Make sure the backend server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const calculateBudgetData = () => {
    if (!dashboardData?.budget?.monthly_budgets) return [];

    const currentMonth = new Date().toISOString().slice(0, 7); // YYYY-MM format
    const monthlyBudget = dashboardData.budget.monthly_budgets[currentMonth];

    if (!monthlyBudget?.categories) return [];

    return Object.entries(monthlyBudget.categories).map(([category, data]) => ({
      name: category,
      spent: data.spent || 0,
      budget: data.budgeted || 0,
      remaining: data.remaining || 0,
      percentage_used: data.percentage_used || 0,
      color: data.remaining < 0 ? "bg-red-500" : "bg-blue-500",
    }));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-sky-600"></div>
          <p className="mt-4 text-gray-600">
            Loading your financial dashboard...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Connection Error
          </h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button onClick={loadDashboardData} className="btn-primary">
            Retry
          </button>
        </div>
      </div>
    );
  }

  const analytics = dashboardData?.analytics || {};
  const transactions = dashboardData?.transactions || [];
  const investments = dashboardData?.investments || [];
  const goals = dashboardData?.goals || [];
  const budgetCategories = calculateBudgetData();

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Financial Dashboard
          </h1>
          <p className="text-gray-600 mt-2">
            Welcome back! Here's your financial summary powered by LangGraph AI.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Net Cash Flow</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(analytics.net_cash_flow || 0)}
                </p>
                <p
                  className={`text-sm ${
                    (analytics.net_cash_flow || 0) >= 0
                      ? "text-green-600"
                      : "text-red-600"
                  }`}
                >
                  {(analytics.net_cash_flow || 0) >= 0
                    ? "Positive"
                    : "Negative"}{" "}
                  cash flow
                </p>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <svg
                  className="w-6 h-6 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"
                  />
                </svg>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Expenses</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(analytics.total_expenses_this_period || 0)}
                </p>
                <p className="text-sm text-gray-600">
                  {analytics.transaction_count || 0} transactions
                </p>
              </div>
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
                <svg
                  className="w-6 h-6 text-red-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"
                  />
                </svg>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Portfolio Value</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(analytics.portfolio_value || 0)}
                </p>
                <p className="text-sm text-green-600">
                  {investments.length} holdings
                </p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg
                  className="w-6 h-6 text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                  />
                </svg>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Goal Progress</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(analytics.total_savings_toward_goals || 0)}
                </p>
                <p className="text-sm text-purple-600">
                  {analytics.active_goals || 0} active goals
                </p>
              </div>
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg
                  className="w-6 h-6 text-purple-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? "border-sky-500 text-sky-600"
                      : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {activeTab === "overview" && (
              <div className="space-y-6">
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Recent Transactions
                  </h3>
                  <div className="space-y-3">
                    {transactions.length > 0 ? (
                      transactions.map((transaction, index) => (
                        <div
                          key={index}
                          className="flex items-center justify-between py-3 border-b border-gray-100 last:border-b-0"
                        >
                          <div className="flex items-center">
                            <div
                              className={`w-10 h-10 rounded-full flex items-center justify-center mr-3 ${
                                transaction.amount > 0
                                  ? "bg-green-100"
                                  : "bg-red-100"
                              }`}
                            >
                              <svg
                                className={`w-5 h-5 ${
                                  transaction.amount > 0
                                    ? "text-green-600"
                                    : "text-red-600"
                                }`}
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                              >
                                <path
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                  strokeWidth={2}
                                  d={
                                    transaction.amount > 0
                                      ? "M12 6v6m0 0v6m0-6h6m-6 0H6"
                                      : "M20 12H4"
                                  }
                                />
                              </svg>
                            </div>
                            <div>
                              <p className="font-medium text-gray-900">
                                {transaction.description}
                              </p>
                              <p className="text-sm text-gray-600">
                                {transaction.category} •{" "}
                                {formatDate(transaction.date)}
                              </p>
                            </div>
                          </div>
                          <span
                            className={`font-semibold ${
                              transaction.amount > 0
                                ? "text-green-600"
                                : "text-gray-900"
                            }`}
                          >
                            {formatCurrency(transaction.amount)}
                          </span>
                        </div>
                      ))
                    ) : (
                      <p className="text-gray-500 text-center py-4">
                        No transactions available
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}

            {activeTab === "budget" && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">
                  Budget Overview
                </h3>
                <div className="space-y-6">
                  {budgetCategories.length > 0 ? (
                    budgetCategories.map((category, index) => (
                      <div key={index}>
                        <div className="flex justify-between items-center mb-2">
                          <span className="font-medium text-gray-900">
                            {category.name}
                          </span>
                          <span className="text-sm text-gray-600">
                            {formatCurrency(Math.abs(category.spent))} /{" "}
                            {formatCurrency(category.budget)}
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full ${category.color}`}
                            style={{
                              width: `${Math.min(
                                category.percentage_used,
                                100
                              )}%`,
                            }}
                          ></div>
                        </div>
                        <div className="flex justify-between items-center mt-1">
                          <span
                            className={`text-xs ${
                              category.remaining < 0
                                ? "text-red-600"
                                : "text-gray-500"
                            }`}
                          >
                            {category.percentage_used.toFixed(0)}% used
                          </span>
                          {category.remaining < 0 ? (
                            <span className="text-xs text-red-600">
                              Over budget by{" "}
                              {formatCurrency(Math.abs(category.remaining))}!
                            </span>
                          ) : (
                            <span className="text-xs text-green-600">
                              {formatCurrency(category.remaining)} remaining
                            </span>
                          )}
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="text-gray-500 text-center py-4">
                      No budget data available
                    </p>
                  )}
                </div>
              </div>
            )}

            {activeTab === "investments" && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">
                  Investment Portfolio
                </h3>
                <div className="space-y-4">
                  {investments.length > 0 ? (
                    investments.map((investment, index) => (
                      <div
                        key={index}
                        className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                      >
                        <div>
                          <p className="font-medium text-gray-900">
                            {investment.company} ({investment.symbol})
                          </p>
                          <p className="text-2xl font-bold text-gray-900">
                            {formatCurrency(investment.market_value)}
                          </p>
                          <p className="text-sm text-gray-600">
                            {investment.shares} shares @{" "}
                            {formatCurrency(investment.current_price)}
                          </p>
                        </div>
                        <div className="text-right">
                          <span
                            className={`text-sm font-medium ${
                              investment.percentage_change >= 0
                                ? "text-green-600"
                                : "text-red-600"
                            }`}
                          >
                            {investment.percentage_change >= 0 ? "+" : ""}
                            {investment.percentage_change.toFixed(2)}%
                          </span>
                          <p className="text-sm text-gray-600">
                            {formatCurrency(investment.unrealized_gain_loss)}
                          </p>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="text-gray-500 text-center py-4">
                      No investment data available
                    </p>
                  )}
                </div>
              </div>
            )}

            {activeTab === "goals" && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">
                  Financial Goals
                </h3>
                <div className="space-y-6">
                  {goals.length > 0 ? (
                    goals.map((goal, index) => {
                      const progress =
                        (goal.current_amount / goal.target_amount) * 100;
                      return (
                        <div key={index}>
                          <div className="flex justify-between items-center mb-2">
                            <span className="font-medium text-gray-900">
                              {goal.name}
                            </span>
                            <span className="text-sm text-gray-600">
                              {formatCurrency(goal.current_amount)} /{" "}
                              {formatCurrency(goal.target_amount)}
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-3">
                            <div
                              className="h-3 bg-sky-500 rounded-full"
                              style={{ width: `${Math.min(progress, 100)}%` }}
                            ></div>
                          </div>
                          <div className="flex justify-between items-center mt-1">
                            <span className="text-xs text-gray-500">
                              {progress.toFixed(1)}% complete
                            </span>
                            <span className="text-xs text-gray-500">
                              {formatCurrency(
                                goal.target_amount - goal.current_amount
                              )}{" "}
                              remaining
                            </span>
                          </div>
                          {goal.deadline && (
                            <p className="text-xs text-gray-500 mt-1">
                              Target: {formatDate(goal.deadline)}
                            </p>
                          )}
                        </div>
                      );
                    })
                  ) : (
                    <p className="text-gray-500 text-center py-4">
                      No goals available
                    </p>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                AI Insights
              </h3>
              <div className="space-y-4">
                <div className="p-3 bg-blue-50 rounded-lg">
                  <p className="text-sm text-blue-800 font-medium">
                    🤖 LangGraph Agent
                  </p>
                  <p className="text-sm text-blue-700 mt-1">
                    Ask me anything about your finances! I can analyze expenses,
                    track budgets, and provide insights.
                  </p>
                </div>
                <div className="p-3 bg-green-50 rounded-lg">
                  <p className="text-sm text-green-800 font-medium">
                    📊 Real-time Analysis
                  </p>
                  <p className="text-sm text-green-700 mt-1">
                    Your financial data is processed through multiple
                    specialized tools for accurate insights.
                  </p>
                </div>
                <div className="p-3 bg-purple-50 rounded-lg">
                  <p className="text-sm text-purple-800 font-medium">
                    🎯 Personalized Recommendations
                  </p>
                  <p className="text-sm text-purple-700 mt-1">
                    The AI agent provides context-aware suggestions based on
                    your financial patterns.
                  </p>
                </div>
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Quick Actions
              </h3>
              <div className="space-y-3">
                <button
                  onClick={loadDashboardData}
                  className="w-full btn-primary text-left"
                >
                  Refresh Data
                </button>
                <button className="w-full btn-secondary text-left">
                  Export Financial Report
                </button>
                <button className="w-full btn-secondary text-left">
                  View API Documentation
                </button>
                <button className="w-full btn-secondary text-left">
                  Check Agent Status
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
