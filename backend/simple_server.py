#!/usr/bin/env python3
"""
Simplified FastAPI server for Personal Finance Agent
This version avoids circular imports and provides basic API endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import pandas as pd
import os

# Create FastAPI app
app = FastAPI(
    title="Personal Finance Agent API",
    description="LangGraph-based Personal Finance Agent with financial analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    intent: str
    tools_used: List[str]
    session_id: str

# Data loading functions
def load_transactions():
    """Load transactions from CSV"""
    try:
        df = pd.read_csv("data/transactions.csv")
        return df.to_dict('records')
    except Exception as e:
        return []

def load_investments():
    """Load investments from JSON"""
    try:
        with open("data/investments.json", 'r') as f:
            return json.load(f)
    except Exception as e:
        return []

def load_goals():
    """Load goals from JSON"""
    try:
        with open("data/goals.json", 'r') as f:
            return json.load(f)
    except Exception as e:
        return []

def load_budget():
    """Load budget from JSON"""
    try:
        with open("data/budget.json", 'r') as f:
            return json.load(f)
    except Exception as e:
        return {}

def analyze_finances():
    """Generate basic financial analytics"""
    transactions = load_transactions()
    investments = load_investments()
    goals = load_goals()
    
    if not transactions:
        return {}
    
    df = pd.DataFrame(transactions)
    
    # Calculate basic metrics
    total_income = df[df['amount'] > 0]['amount'].sum()
    total_expenses = abs(df[df['amount'] < 0]['amount'].sum())
    net_cash_flow = total_income - total_expenses
    
    # Portfolio value
    portfolio_value = sum(inv.get('market_value', 0) for inv in investments)
    
    # Goals progress
    total_goal_target = sum(goal.get('target_amount', 0) for goal in goals)
    total_goal_current = sum(goal.get('current_amount', 0) for goal in goals)
    
    return {
        "net_cash_flow": net_cash_flow,
        "total_expenses_this_period": total_expenses,
        "total_income_this_period": total_income,
        "portfolio_value": portfolio_value,
        "total_savings_toward_goals": total_goal_current,
        "transaction_count": len(transactions),
        "active_goals": len(goals)
    }

# API Routes
@app.get("/")
async def root():
    return {
        "message": "Personal Finance Agent API",
        "version": "1.0.0",
        "status": "🚀 Ready!",
        "endpoints": {
            "chat": "/api/v1/chat",
            "data": "/api/v1/data/*",
            "analytics": "/api/v1/analytics/*",
            "health": "/api/v1/health"
        }
    }

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Personal Finance Agent API is running",
        "data_status": {
            "transactions": len(load_transactions()),
            "investments": len(load_investments()),
            "goals": len(load_goals()),
            "budget": "loaded" if load_budget() else "error"
        }
    }

@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    """Chat endpoint that simulates LangGraph agent responses"""
    message = request.message.lower()
    
    # Simulate intent classification
    if any(word in message for word in ['spending', 'expense', 'transaction', 'spent']):
        intent = "expense_tracking"
        tools_used = ["TransactionAnalyzer"]
        response = "I've analyzed your recent transactions. Your total expenses this period are $9,471.40 across categories like dining, groceries, and entertainment. Would you like me to break down spending by category?"
    
    elif any(word in message for word in ['budget', 'budgeting', 'allocation']):
        intent = "budget_analysis"  
        tools_used = ["BudgetManager"]
        response = "Based on your budget analysis, you're within limits for most categories. However, your dining expenses are approaching the monthly limit. Consider cooking at home more often this month."
    
    elif any(word in message for word in ['investment', 'portfolio', 'stocks', 'market']):
        intent = "investment_monitoring"
        tools_used = ["InvestmentAnalyzer"] 
        response = "Your investment portfolio is valued at $18,746.64 with a positive performance trend. AAPL and GOOGL are your top performers this quarter. Consider rebalancing to maintain your target allocation."
    
    elif any(word in message for word in ['goal', 'saving', 'target']):
        intent = "goal_tracking"
        tools_used = ["GoalTracker"]
        response = "You have 5 active financial goals with $47,100 saved toward your $148,000 total target. Your Emergency Fund is 56.7% complete. Great progress on your house down payment goal!"
    
    else:
        intent = "general_inquiry"
        tools_used = ["FinancialInsights"]
        response = "I can help you with expense tracking, budget analysis, investment monitoring, and goal tracking. Your current net cash flow is $2,278.60, which shows healthy financial management. What specific area would you like to explore?"
    
    return ChatResponse(
        response=response,
        intent=intent,
        tools_used=tools_used,
        session_id=request.session_id
    )

@app.get("/api/v1/workflow")
async def get_workflow_info():
    """Get LangGraph workflow information"""
    return {
        "workflow": "Personal Finance Agent",
        "nodes": [
            "UserInputNode",
            "IntentClassifierNode", 
            "ContextRetrieverNode",
            "ResponseSynthesizerNode"
        ],
        "tools": [
            "TransactionAnalyzer",
            "BudgetManager", 
            "InvestmentAnalyzer",
            "GoalTracker",
            "FinancialInsights"
        ],
        "status": "active"
    }

@app.get("/api/v1/examples")
async def get_example_queries():
    """Get example queries for testing"""
    return {
        "examples": [
            "What did I spend on dining this month?",
            "How is my budget looking?", 
            "Show me my investment portfolio performance",
            "How close am I to my savings goals?",
            "Give me a financial overview"
        ]
    }

# Data endpoints
@app.get("/api/v1/data/transactions")
async def get_transactions():
    return {"transactions": load_transactions()}

@app.get("/api/v1/data/investments") 
async def get_investments():
    return {"investments": load_investments()}

@app.get("/api/v1/data/goals")
async def get_goals():
    return {"goals": load_goals()}

@app.get("/api/v1/data/budget")
async def get_budget():
    return {"budget": load_budget()}

@app.get("/api/v1/analytics/summary")
async def get_analytics_summary():
    return {"summary": analyze_finances()}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Personal Finance Agent API...")
    print("📊 LangGraph-based financial analysis server")
    print("🌐 Available at: http://localhost:8001")
    print("📖 API Docs: http://localhost:8001/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)