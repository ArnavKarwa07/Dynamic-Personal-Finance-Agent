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
        status="healthy", timestamp=datetime.now().isoformat(), version="1.0.0"
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
            user_query=query_request.query, conversation_history=conversation_history
        )

        # Update session with new conversation history
        conversation_sessions[session_id] = result["conversation_history"]

        return FinanceResponse(
            response=result["response"],
            intent=result["intent"],
            tools_used=result["tools_used"],
            analysis_results=result["analysis_results"],
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
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
            "RISK_ASSESSMENT",
            "MARKET_INTELLIGENCE",
            "ADVANCED_PLANNING",
            "GENERAL_INQUIRY",
        ],
        available_tools=[
            "transaction_analyzer",
            "budget_manager",
            "investment_analyzer",
            "goal_tracker",
            "financial_insights",
            "advanced_financial_planner",
            "risk_assessment",
            "market_intelligence",
            "graph_visualization",
        ],
    )


@router.get("/workflow/visualization")
async def get_workflow_visualization():
    """Get a visual representation of the workflow"""
    return {"visualization": finance_agent.get_workflow_visualization()}


@router.get("/agent/capabilities")
async def get_agent_capabilities():
    """Get comprehensive information about agent capabilities"""
    try:
        # Use the graph visualization tool to get comprehensive agent info
        result = finance_agent.process_query_sync(
            "Show me the agent workflow and capabilities"
        )

        if "graph_visualization" in result.get("analysis_results", {}):
            return {
                "agent_type": "LangGraph-powered Financial AI Agent",
                "version": "2.0.0",
                "capabilities": result["analysis_results"]["graph_visualization"],
                "workflow_summary": finance_agent.get_workflow_visualization(),
                "features": {
                    "multi_tool_analysis": True,
                    "conversational_ai": True,
                    "contextual_routing": True,
                    "state_management": True,
                    "real_time_insights": True,
                    "risk_assessment": True,
                    "market_intelligence": True,
                    "strategic_planning": True,
                },
                "supported_queries": [
                    "How much did I spend on groceries this month?",
                    "Am I on track with my budget?",
                    "How are my investments performing?",
                    "What are my financial risks?",
                    "Show me market intelligence",
                    "Create a comprehensive financial plan",
                    "Analyze my spending patterns",
                    "What's my financial health score?",
                ],
            }
        else:
            # Fallback response
            return {
                "agent_type": "LangGraph-powered Financial AI Agent",
                "version": "2.0.0",
                "description": "Advanced AI agent for comprehensive financial analysis and planning",
                "tools_count": 8,
                "capabilities": "Multi-tool financial analysis with intelligent routing",
            }

    except Exception as e:
        return {
            "error": "Could not retrieve agent capabilities",
            "details": str(e),
            "agent_type": "LangGraph Financial AI Agent",
        }


@router.post("/demo/showcase")
async def demo_showcase():
    """Showcase the agent's capabilities with sample queries"""
    demo_queries = [
        "What's my financial health score?",
        "Show me my biggest spending risks",
        "How is the technology sector performing?",
        "Create a comprehensive retirement plan",
    ]

    results = []

    for query in demo_queries:
        try:
            result = finance_agent.process_query_sync(query)
            results.append(
                {
                    "query": query,
                    "intent": result.get("intent"),
                    "tools_used": result.get("tools_used", []),
                    "response_preview": (
                        result.get("response", "")[:200] + "..."
                        if len(result.get("response", "")) > 200
                        else result.get("response", "")
                    ),
                    "analysis_summary": {
                        tool: f"Analysis completed with {len(str(data))} characters of data"
                        for tool, data in result.get("analysis_results", {}).items()
                    },
                }
            )
        except Exception as e:
            results.append({"query": query, "error": str(e)})

    return {
        "message": "Agent capability showcase",
        "total_queries": len(demo_queries),
        "results": results,
        "agent_info": {
            "workflow_nodes": 12,
            "available_tools": 8,
            "routing_strategies": 3,
            "langgraph_features": [
                "Conditional edge routing",
                "State management",
                "Multi-tool orchestration",
                "Context-aware analysis",
            ],
        },
    }


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
        sessions.append(
            {
                "session_id": session_id,
                "message_count": len(history),
                "last_activity": history[-1].get("timestamp") if history else None,
            }
        )
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
                    "How much did I spend at restaurants?",
                ],
            },
            {
                "category": "Budget Analysis",
                "queries": [
                    "Am I over budget this month?",
                    "How much budget do I have left?",
                    "Which categories am I overspending in?",
                    "What's my budget performance?",
                ],
            },
            {
                "category": "Investment Analysis",
                "queries": [
                    "How are my investments performing?",
                    "What are my biggest gains and losses?",
                    "Show me my portfolio allocation",
                    "Which stocks are my best performers?",
                ],
            },
            {
                "category": "Goal Tracking",
                "queries": [
                    "How close am I to my emergency fund goal?",
                    "Am I on track with my savings goals?",
                    "Show me progress on my vacation fund",
                    "Which goals are behind schedule?",
                ],
            },
            {
                "category": "Financial Insights",
                "queries": [
                    "Give me a financial summary",
                    "What's my financial health score?",
                    "Show me financial trends",
                    "What recommendations do you have?",
                ],
            },
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
            "transactions": transactions.to_dict("records"),
            "count": len(transactions),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading transactions: {str(e)}"
        )


@router.get("/data/investments")
async def get_investments_data():
    """Get investment data (for development/testing)"""
    try:
        from tools.data_loader import DataLoader

        loader = DataLoader()
        investments = loader.load_investments()
        return {"investments": investments, "count": len(investments)}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading investments: {str(e)}"
        )


@router.get("/data/goals")
async def get_goals_data():
    """Get goals data (for development/testing)"""
    try:
        from tools.data_loader import DataLoader

        loader = DataLoader()
        goals = loader.load_goals()
        return {"goals": goals, "count": len(goals)}
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

        # Calculate summary metrics (handle empty data)
        if not transactions.empty:
            total_expenses = abs(
                transactions[transactions["amount"] < 0]["amount"].sum()
            )
            total_income = transactions[transactions["amount"] > 0]["amount"].sum()
            transaction_count = len(transactions)
        else:
            total_expenses = 0.0
            total_income = 0.0
            transaction_count = 0

        portfolio_value = sum(inv.get("market_value", 0) for inv in investments)
        total_goal_progress = sum(goal.get("current_amount", 0) for goal in goals)

        return {
            "summary": {
                "total_expenses_this_period": round(total_expenses, 2),
                "total_income_this_period": round(total_income, 2),
                "net_cash_flow": round(total_income - total_expenses, 2),
                "portfolio_value": round(portfolio_value, 2),
                "total_savings_toward_goals": round(total_goal_progress, 2),
                "active_goals": len([g for g in goals if g.get("status") == "active"]),
                "transaction_count": transaction_count,
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating analytics: {str(e)}"
        )


# Data entry endpoints
class TransactionCreate(BaseModel):
    date: str
    amount: float
    category: str
    description: str
    merchant: str = ""
    account_type: str = "Checking"


class GoalCreate(BaseModel):
    name: str
    description: str = ""
    target_amount: float
    current_amount: float = 0.0
    target_date: str
    category: str
    monthly_contribution: float = 0.0


class BudgetCreate(BaseModel):
    month: str  # YYYY-MM format
    category: str
    budgeted_amount: float


@router.post("/data/transactions")
async def add_transaction(transaction: TransactionCreate):
    """Add a new transaction"""
    try:
        import pandas as pd
        import os
        from config.settings import settings

        # Read existing transactions
        transactions_file = os.path.join(settings.data_dir, "transactions.csv")

        if os.path.exists(transactions_file):
            df = pd.read_csv(transactions_file)
        else:
            df = pd.DataFrame(
                columns=[
                    "date",
                    "amount",
                    "category",
                    "description",
                    "merchant",
                    "account_type",
                ]
            )

        # Add new transaction
        new_transaction = {
            "date": transaction.date,
            "amount": transaction.amount,
            "category": transaction.category,
            "description": transaction.description,
            "merchant": transaction.merchant,
            "account_type": transaction.account_type,
        }

        df = pd.concat([df, pd.DataFrame([new_transaction])], ignore_index=True)

        # Save back to CSV
        df.to_csv(transactions_file, index=False)

        return {
            "message": "Transaction added successfully",
            "transaction": new_transaction,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error adding transaction: {str(e)}"
        )


@router.post("/data/goals")
async def add_goal(goal: GoalCreate):
    """Add a new financial goal"""
    try:
        import json
        import os
        import uuid
        from datetime import datetime
        from config.settings import settings

        # Read existing goals
        goals_file = os.path.join(settings.data_dir, "goals.json")

        if os.path.exists(goals_file):
            with open(goals_file, "r") as f:
                goals = json.load(f)
        else:
            goals = []

        # Calculate progress percentage
        progress_percentage = (
            (goal.current_amount / goal.target_amount * 100)
            if goal.target_amount > 0
            else 0
        )

        # Add new goal
        new_goal = {
            "id": str(uuid.uuid4()),
            "name": goal.name,
            "description": goal.description,
            "target_amount": goal.target_amount,
            "current_amount": goal.current_amount,
            "target_date": goal.target_date,
            "status": "active",
            "category": goal.category,
            "monthly_contribution": goal.monthly_contribution,
            "created_date": datetime.now().isoformat().split("T")[0],
            "progress_percentage": round(progress_percentage, 2),
        }

        goals.append(new_goal)

        # Save back to JSON
        with open(goals_file, "w") as f:
            json.dump(goals, f, indent=2)

        return {"message": "Goal added successfully", "goal": new_goal}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding goal: {str(e)}")


@router.post("/data/budget")
async def add_budget_category(budget: BudgetCreate):
    """Add or update a budget category for a specific month"""
    try:
        import json
        import os
        from config.settings import settings

        # Read existing budget
        budget_file = os.path.join(settings.data_dir, "budget.json")

        if os.path.exists(budget_file):
            with open(budget_file, "r") as f:
                budget_data = json.load(f)
        else:
            budget_data = {
                "monthly_budgets": {},
                "annual_budget": {
                    "total_budgeted": 0.00,
                    "total_spent": 0.00,
                    "remaining": 0.00,
                },
            }

        # Ensure monthly_budgets exists
        if "monthly_budgets" not in budget_data:
            budget_data["monthly_budgets"] = {}

        # Ensure the month exists
        if budget.month not in budget_data["monthly_budgets"]:
            budget_data["monthly_budgets"][budget.month] = {
                "total_budgeted": 0.00,
                "total_spent": 0.00,
                "remaining": 0.00,
                "categories": {},
            }

        # Add/update the category
        budget_data["monthly_budgets"][budget.month]["categories"][budget.category] = {
            "budgeted": budget.budgeted_amount,
            "spent": 0.00,
            "remaining": budget.budgeted_amount,
            "percentage_used": 0.00,
        }

        # Recalculate month totals
        month_data = budget_data["monthly_budgets"][budget.month]
        month_data["total_budgeted"] = sum(
            cat["budgeted"] for cat in month_data["categories"].values()
        )
        month_data["remaining"] = (
            month_data["total_budgeted"] - month_data["total_spent"]
        )

        # Save back to JSON
        with open(budget_file, "w") as f:
            json.dump(budget_data, f, indent=2)

        return {
            "message": "Budget category added successfully",
            "budget": budget_data["monthly_budgets"][budget.month]["categories"][
                budget.category
            ],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error adding budget category: {str(e)}"
        )


# Export the router
__all__ = ["router"]
