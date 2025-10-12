import React, { useState } from "react";
import financeAPI from "@services/financeAPI";

const DataEntryModal = ({
  isOpen,
  onClose,
  onDataAdded,
  type = "transaction",
  userId,
}) => {
  const [formData, setFormData] = useState(getInitialFormData(type));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function getInitialFormData(type) {
    switch (type) {
      case "transaction":
        return {
          date: new Date().toISOString().split("T")[0],
          amount: "",
          category: "",
          description: "",
          merchant: "",
          account_type: "Checking",
        };
      case "investment":
        return {
          symbol: "",
          shares: "",
          purchase_price: "",
          current_price: "",
          sector: "",
          purchase_date: new Date().toISOString().split("T")[0],
        };
      case "goal":
        return {
          name: "",
          description: "",
          target_amount: "",
          current_amount: "",
          target_date: "",
          category: "",
          monthly_contribution: "",
        };
      case "budget":
        return {
          category: "",
          budgeted_amount: "",
          month: new Date().toISOString().slice(0, 7), // YYYY-MM format
        };
      default:
        return {};
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      let response;

      if (!userId) throw new Error("Missing user id");

      if (type === "transaction") {
        const payload = {
          description: formData.description,
          amount: parseFloat(formData.amount),
          date: formData.date,
          category: formData.category,
        };
        response = await financeAPI.addTransaction(userId, payload);
      } else if (type === "goal") {
        const payload = {
          name: formData.name,
          target: parseFloat(formData.target_amount),
          current: formData.current_amount
            ? parseFloat(formData.current_amount)
            : 0,
          deadline: formData.target_date || null,
        };
        response = await financeAPI.addGoal(userId, payload);
      } else if (type === "budget") {
        const payload = {
          category: formData.category,
          budgeted: parseFloat(formData.budgeted_amount),
          month: formData.month,
        };
        response = await financeAPI.addBudget(userId, payload);
      } else {
        throw new Error(`Unsupported data type: ${type}`);
      }

      console.log(`Added ${type}:`, response);

      // Success - close modal and refresh data
      onDataAdded();
      onClose();
      setFormData(getInitialFormData(type));
    } catch (err) {
      const msg = err?.message || `Failed to add ${type}. Please try again.`;
      setError(msg);
      console.error(`Error adding ${type}:`, err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  const categories = {
    transaction: [
      "Food & Dining",
      "Transportation",
      "Shopping",
      "Entertainment",
      "Utilities",
      "Health & Fitness",
      "Housing",
      "Income",
    ],
    goal: [
      "savings",
      "travel",
      "housing",
      "transportation",
      "education",
      "emergency",
    ],
    budget: [
      "Housing",
      "Food & Dining",
      "Transportation",
      "Shopping",
      "Entertainment",
      "Utilities",
      "Health & Fitness",
      "Savings",
    ],
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-gray-900">
            Add New {type.charAt(0).toUpperCase() + type.slice(1)}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
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
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {type === "transaction" && (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Date
                </label>
                <input
                  type="date"
                  name="date"
                  value={formData.date}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Amount
                </label>
                <input
                  type="number"
                  step="0.01"
                  name="amount"
                  value={formData.amount}
                  onChange={handleInputChange}
                  placeholder="-45.50 (negative for expenses)"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Category
                </label>
                <select
                  name="category"
                  value={formData.category}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"
                >
                  <option value="">Select category</option>
                  {categories.transaction.map((cat) => (
                    <option key={cat} value={cat}>
                      {cat}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <input
                  type="text"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  placeholder="Coffee, Groceries, etc."
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Merchant
                </label>
                <input
                  type="text"
                  name="merchant"
                  value={formData.merchant}
                  onChange={handleInputChange}
                  placeholder="Starbucks, Target, etc."
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Account Type
                </label>
                <select
                  name="account_type"
                  value={formData.account_type}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"
                >
                  <option value="Checking">Checking</option>
                  <option value="Credit Card">Credit Card</option>
                  <option value="Savings">Savings</option>
                  <option value="Cash">Cash</option>
                </select>
              </div>
            </>
          )}

          {type === "goal" && (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Goal Name
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="Emergency Fund, Vacation, etc."
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  placeholder="Brief description of your goal"
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Target Amount
                </label>
                <input
                  type="number"
                  step="0.01"
                  name="target_amount"
                  value={formData.target_amount}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Current Amount
                </label>
                <input
                  type="number"
                  step="0.01"
                  name="current_amount"
                  value={formData.current_amount}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Target Date
                </label>
                <input
                  type="date"
                  name="target_date"
                  value={formData.target_date}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Category
                </label>
                <select
                  name="category"
                  value={formData.category}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"
                >
                  <option value="">Select category</option>
                  {categories.goal.map((cat) => (
                    <option key={cat} value={cat}>
                      {cat}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Monthly Contribution
                </label>
                <input
                  type="number"
                  step="0.01"
                  name="monthly_contribution"
                  value={formData.monthly_contribution}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>
            </>
          )}

          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-sky-600 text-white rounded-md hover:bg-sky-700 disabled:opacity-50"
            >
              {loading
                ? "Adding..."
                : `Add ${type.charAt(0).toUpperCase() + type.slice(1)}`}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default DataEntryModal;
