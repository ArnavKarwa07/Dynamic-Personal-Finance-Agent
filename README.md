# 🚀 LangGraph Personal Finance Agent

A comprehensive **LangGraph-based Personal Finance Agent** demonstrating advanced Agentic AI capabilities with intelligent financial analysis, tool orchestration, and real-time chat interface.

## ✨ Key Features

- **🧠 LangGraph Workflow**: Advanced multi-node workflow orchestration
- **🛠️ Financial Tools**: 5 specialized analysis tools (transactions, budget, investments, goals, insights)
- **💬 Real-time Chat**: Interactive AI assistant with intent classification
- **📊 Rich Dashboard**: Comprehensive financial overview with live data
- **🔄 Full-Stack**: React frontend + FastAPI backend integration
- **📈 Mock Data**: Realistic financial datasets for demonstration

## 🚀 Quick Start

**Backend** (Terminal 1):

```bash
cd backend
python simple_server.py
```

**Frontend** (Terminal 2):

```bash
cd frontend
npm run dev
```

**Access**: http://localhost:5173

## 🎯 Demo Queries

Try these in the chat interface:

- "What did I spend on dining this month?"
- "How is my budget looking?"
- "Show me my investment portfolio performance"
- "How close am I to my savings goals?"

## 🏗️ Architecture

- **LangGraph Engine**: StateGraph with intent classification and tool routing
- **Financial Tools**: TransactionAnalyzer, BudgetManager, InvestmentAnalyzer, GoalTracker, FinancialInsights
- **API Layer**: FastAPI with comprehensive endpoints and real-time data
- **Frontend**: React with Tailwind CSS, real-time chat, and dashboard

## 📚 Documentation

See `PROJECT_SUMMARY.md` for complete technical details, API documentation, and implementation guide.
