import React, { useState } from "react";

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState("overview");

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "budget", label: "Budget" },
    { id: "investments", label: "Investments" },
    { id: "goals", label: "Goals" },
  ];

  const transactions = [
    {
      id: 1,
      description: "Starbucks Coffee",
      amount: -4.5,
      category: "Food",
      date: "2025-10-07",
    },
    {
      id: 2,
      description: "Salary Deposit",
      amount: 3500.0,
      category: "Income",
      date: "2025-10-01",
    },
    {
      id: 3,
      description: "Netflix Subscription",
      amount: -15.99,
      category: "Entertainment",
      date: "2025-10-05",
    },
    {
      id: 4,
      description: "Grocery Store",
      amount: -89.45,
      category: "Food",
      date: "2025-10-06",
    },
    {
      id: 5,
      description: "Gas Station",
      amount: -45.2,
      category: "Transportation",
      date: "2025-10-04",
    },
  ];

  const budgetCategories = [
    { name: "Food & Dining", spent: 245, budget: 400, color: "bg-blue-500" },
    { name: "Transportation", spent: 180, budget: 300, color: "bg-green-500" },
    { name: "Entertainment", spent: 85, budget: 150, color: "bg-purple-500" },
    { name: "Utilities", spent: 220, budget: 250, color: "bg-orange-500" },
    { name: "Shopping", spent: 320, budget: 200, color: "bg-red-500" },
  ];

  const investments = [
    {
      name: "S&P 500 ETF",
      value: 15420,
      change: "+2.4%",
      changeType: "positive",
    },
    {
      name: "Apple Inc.",
      value: 8950,
      change: "+1.8%",
      changeType: "positive",
    },
    {
      name: "Real Estate Fund",
      value: 12300,
      change: "-0.5%",
      changeType: "negative",
    },
    {
      name: "Tech Stocks",
      value: 7680,
      change: "+3.2%",
      changeType: "positive",
    },
  ];

  const goals = [
    { name: "Emergency Fund", current: 8500, target: 15000, progress: 57 },
    { name: "Vacation", current: 2400, target: 5000, progress: 48 },
    { name: "New Car", current: 12000, target: 25000, progress: 48 },
    { name: "House Down Payment", current: 35000, target: 80000, progress: 44 },
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Financial Dashboard
          </h1>
          <p className="text-gray-600 mt-2">
            Welcome back! Here's your financial summary.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Balance</p>
                <p className="text-2xl font-bold text-gray-900">$24,580</p>
                <p className="text-sm text-green-600">+5.2% from last month</p>
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
                <p className="text-sm text-gray-600">Monthly Spending</p>
                <p className="text-2xl font-bold text-gray-900">$1,845</p>
                <p className="text-sm text-red-600">+2.1% from last month</p>
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
                <p className="text-sm text-gray-600">Investments</p>
                <p className="text-2xl font-bold text-gray-900">$44,350</p>
                <p className="text-sm text-green-600">+8.4% this year</p>
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
                <p className="text-sm text-gray-600">Savings Rate</p>
                <p className="text-2xl font-bold text-gray-900">23%</p>
                <p className="text-sm text-green-600">Above average</p>
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
                    {transactions.map((transaction) => (
                      <div
                        key={transaction.id}
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
                              {transaction.category} • {transaction.date}
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
                          {transaction.amount > 0 ? "+" : ""}$
                          {Math.abs(transaction.amount).toFixed(2)}
                        </span>
                      </div>
                    ))}
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
                  {budgetCategories.map((category, index) => (
                    <div key={index}>
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium text-gray-900">
                          {category.name}
                        </span>
                        <span className="text-sm text-gray-600">
                          ${category.spent} / ${category.budget}
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${category.color} ${
                            category.spent > category.budget ? "bg-red-500" : ""
                          }`}
                          style={{
                            width: `${Math.min(
                              (category.spent / category.budget) * 100,
                              100
                            )}%`,
                          }}
                        ></div>
                      </div>
                      <div className="flex justify-between items-center mt-1">
                        <span
                          className={`text-xs ${
                            category.spent > category.budget
                              ? "text-red-600"
                              : "text-gray-500"
                          }`}
                        >
                          {((category.spent / category.budget) * 100).toFixed(
                            0
                          )}
                          % used
                        </span>
                        {category.spent > category.budget && (
                          <span className="text-xs text-red-600">
                            Over budget!
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === "investments" && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">
                  Investment Portfolio
                </h3>
                <div className="space-y-4">
                  {investments.map((investment, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                    >
                      <div>
                        <p className="font-medium text-gray-900">
                          {investment.name}
                        </p>
                        <p className="text-2xl font-bold text-gray-900">
                          ${investment.value.toLocaleString()}
                        </p>
                      </div>
                      <div className="text-right">
                        <span
                          className={`text-sm font-medium ${
                            investment.changeType === "positive"
                              ? "text-green-600"
                              : "text-red-600"
                          }`}
                        >
                          {investment.change}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === "goals" && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">
                  Financial Goals
                </h3>
                <div className="space-y-6">
                  {goals.map((goal, index) => (
                    <div key={index}>
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium text-gray-900">
                          {goal.name}
                        </span>
                        <span className="text-sm text-gray-600">
                          ${goal.current.toLocaleString()} / $
                          {goal.target.toLocaleString()}
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div
                          className="h-3 bg-sky-500 rounded-full"
                          style={{ width: `${goal.progress}%` }}
                        ></div>
                      </div>
                      <div className="flex justify-between items-center mt-1">
                        <span className="text-xs text-gray-500">
                          {goal.progress}% complete
                        </span>
                        <span className="text-xs text-gray-500">
                          ${(goal.target - goal.current).toLocaleString()}{" "}
                          remaining
                        </span>
                      </div>
                    </div>
                  ))}
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
                    💡 Spending Alert
                  </p>
                  <p className="text-sm text-blue-700 mt-1">
                    You're spending 15% more on dining out this month. Consider
                    cooking at home more often.
                  </p>
                </div>
                <div className="p-3 bg-green-50 rounded-lg">
                  <p className="text-sm text-green-800 font-medium">
                    📈 Investment Tip
                  </p>
                  <p className="text-sm text-green-700 mt-1">
                    Your portfolio is performing well. Consider rebalancing to
                    maintain your target allocation.
                  </p>
                </div>
                <div className="p-3 bg-purple-50 rounded-lg">
                  <p className="text-sm text-purple-800 font-medium">
                    🎯 Goal Update
                  </p>
                  <p className="text-sm text-purple-700 mt-1">
                    You're on track to reach your vacation goal! Keep saving
                    $200/month.
                  </p>
                </div>
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Quick Actions
              </h3>
              <div className="space-y-3">
                <button className="w-full btn-primary text-left">
                  Add Transaction
                </button>
                <button className="w-full btn-secondary text-left">
                  Set New Goal
                </button>
                <button className="w-full btn-secondary text-left">
                  Export Data
                </button>
                <button className="w-full btn-secondary text-left">
                  Schedule Report
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
