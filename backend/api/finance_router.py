from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from agents.finance_agent import create_finance_agent
from datetime import datetime
import uuid

# Initialize the finance agent
finance_agent = create_finance_agent()

# Pydantic models for API requests/responses
class FinanceQuery(BaseModel):
    query: str
    session_id: Optional[str] = None
    conversation_history: Optional[List[Dict[str, Any]]] = None

class FinanceResponse(BaseModel):
    response: str
    intent: str
    tools_used: List[str]
    analysis_results: Dict[str, Any]
    session_id: str
    timestamp: str
    
class HealthCheck(BaseModel):
    status: str
    timestamp: str
    version: str

class WorkflowInfo(BaseModel):
    description: str
    available_intents: List[str]
    available_tools: List[str]

# Create router
router = APIRouter(prefix="/api/v1", tags=["finance-agent"])

# In-memory session storage (in production, use Redis or database)
conversation_sessions = {}

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@router.post("/chat", response_model=FinanceResponse)
async def chat_with_finance_agent(query_request: FinanceQuery):
    """Main endpoint to chat with the finance agent"""
    
    try:
        # Generate session ID if not provided
        session_id = query_request.session_id or str(uuid.uuid4())
        
        # Get conversation history from session or request
        if session_id in conversation_sessions:
            conversation_history = conversation_sessions[session_id]
        else:
            conversation_history = query_request.conversation_history or []
        
        # Process the query through the LangGraph workflow
        result = finance_agent.process_query_sync(
            user_query=query_request.query,
            conversation_history=conversation_history
        )
        
        # Update session with new conversation history
        conversation_sessions[session_id] = result["conversation_history"]
        
        return FinanceResponse(
            response=result["response"],
            intent=result["intent"], 
            tools_used=result["tools_used"],
            analysis_results=result["analysis_results"],
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get("/workflow", response_model=WorkflowInfo)
async def get_workflow_info():
    """Get information about the agent workflow and capabilities"""
    return WorkflowInfo(
        description="Personal Finance Agent powered by LangGraph",
        available_intents=[
            "EXPENSE_TRACKING",
            "BUDGET_ANALYSIS", 
            "INVESTMENT_INQUIRY",
            "GOAL_TRACKING",
            "FINANCIAL_INSIGHTS",
            "GENERAL_INQUIRY"
        ],
        available_tools=[
            "transaction_analyzer",
            "budget_manager",
            "investment_analyzer", 
            "goal_tracker",
            "financial_insights"
        ]
    )

@router.get("/workflow/visualization")
async def get_workflow_visualization():
    """Get a visual representation of the workflow"""
    return {"visualization": finance_agent.get_workflow_visualization()}

@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear a conversation session"""
    if session_id in conversation_sessions:
        del conversation_sessions[session_id]
        return {"message": f"Session {session_id} cleared successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@router.get("/sessions")
async def list_sessions():
    """List active conversation sessions"""
    sessions = []
    for session_id, history in conversation_sessions.items():
        sessions.append({
            "session_id": session_id,
            "message_count": len(history),
            "last_activity": history[-1].get("timestamp") if history else None
        })
    return {"active_sessions": sessions}

# Example queries endpoint for testing
@router.get("/examples")
async def get_example_queries():
    """Get example queries to test the finance agent"""
    return {
        "example_queries": [
            {
                "category": "Expense Tracking",
                "queries": [
                    "How much did I spend on food this month?",
                    "Show me my spending by category",
                    "What was my largest expense this month?",
                    "How much did I spend at restaurants?"
                ]
            },
            {
                "category": "Budget Analysis", 
                "queries": [
                    "Am I over budget this month?",
                    "How much budget do I have left?",
                    "Which categories am I overspending in?",
                    "What's my budget performance?"
                ]
            },
            {
                "category": "Investment Analysis",
                "queries": [
                    "How are my investments performing?",
                    "What are my biggest gains and losses?",
                    "Show me my portfolio allocation",
                    "Which stocks are my best performers?"
                ]
            },
            {
                "category": "Goal Tracking",
                "queries": [
                    "How close am I to my emergency fund goal?",
                    "Am I on track with my savings goals?",
                    "Show me progress on my vacation fund",
                    "Which goals are behind schedule?"
                ]
            },
            {
                "category": "Financial Insights",
                "queries": [
                    "Give me a financial summary",
                    "What's my financial health score?",
                    "Show me financial trends",
                    "What recommendations do you have?"
                ]
            }
        ]
    }

# Data endpoints for debugging/development
@router.get("/data/transactions")
async def get_transactions_data():
    """Get transaction data (for development/testing)"""
    try:
        from tools.data_loader import DataLoader
        loader = DataLoader()
        transactions = loader.load_transactions()
        return {
            "transactions": transactions.to_dict('records'),
            "count": len(transactions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading transactions: {str(e)}")

@router.get("/data/investments")
async def get_investments_data():
    """Get investment data (for development/testing)"""
    try:
        from tools.data_loader import DataLoader
        loader = DataLoader()
        investments = loader.load_investments()
        return {
            "investments": investments,
            "count": len(investments)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading investments: {str(e)}")

@router.get("/data/goals")
async def get_goals_data():
    """Get goals data (for development/testing)"""
    try:
        from tools.data_loader import DataLoader
        loader = DataLoader()
        goals = loader.load_goals()
        return {
            "goals": goals,
            "count": len(goals)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading goals: {str(e)}")

@router.get("/data/budget")
async def get_budget_data():
    """Get budget data (for development/testing)"""
    try:
        from tools.data_loader import DataLoader
        loader = DataLoader()
        budget = loader.load_budget()
        return {"budget": budget}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading budget: {str(e)}")

# Analytics endpoint
@router.get("/analytics/summary")
async def get_analytics_summary():
    """Get high-level analytics summary"""
    try:
        from tools.data_loader import DataLoader
        loader = DataLoader()
        
        transactions = loader.load_transactions()
        investments = loader.load_investments()
        goals = loader.load_goals()
        budget = loader.load_budget()
        
        # Calculate summary metrics
        total_expenses = abs(transactions[transactions['amount'] < 0]['amount'].sum())
        total_income = transactions[transactions['amount'] > 0]['amount'].sum()
        portfolio_value = sum(inv.get('market_value', 0) for inv in investments)
        total_goal_progress = sum(goal.get('current_amount', 0) for goal in goals)
        
        return {
            "summary": {
                "total_expenses_this_period": round(total_expenses, 2),
                "total_income_this_period": round(total_income, 2),
                "net_cash_flow": round(total_income - total_expenses, 2),
                "portfolio_value": round(portfolio_value, 2),
                "total_savings_toward_goals": round(total_goal_progress, 2),
                "active_goals": len([g for g in goals if g.get('status') == 'active']),
                "transaction_count": len(transactions)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating analytics: {str(e)}")

# Export the router
__all__ = ["router"]