"""
FastAPI server with Groq-based LangGraph workflow
Clean implementation without HuggingFace dependencies
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our LangGraph implementation
from core.langgraph_workflow import finance_workflow, FinanceState
from core.groq_client import groq_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Dynamic Personal Finance Agent API",
    description="LangGraph-based Personal Finance Agent with Groq Integration",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    user_id: str = "default"
    workflow_stage: str = "Started"

class AuthRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class OnboardingRequest(BaseModel):
    user_data: Dict[str, Any]


@app.get("/")
async def root():
    return {
        "message": "Dynamic Personal Finance Agent API",
        "version": "2.0.0", 
        "description": "Multi-stage LangGraph workflow with Groq API integration",
        "groq_status": "Connected" if groq_client.api_key else "API Key Missing",
        "workflow_stages": {
            "started": "User onboarding and consent",
            "mvp": "Basic budgeting and goal planning",
            "intermediate": "Advanced budgeting with AI insights",
            "advanced": "Sophisticated portfolio management"
        },
        "endpoints": {
            "chat": "/api/v1/chat",
            "dashboard": "/api/v1/dashboard",
            "auth": "/api/v1/auth/*",
            "health": "/health",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health_check():
    groq_status = "healthy" if groq_client.api_key else "missing_api_key"
    return {
        "status": "healthy", 
        "service": "finance-agent-api",
        "groq_integration": groq_status
    }


@app.post("/api/v1/chat")
async def chat_with_agent(request: ChatRequest):
    """Chat with the AI finance agent using LangGraph workflow"""
    try:
        # Create initial state for LangGraph
        state = FinanceState(
            user_id=request.user_id,
            user_query=request.message,
            current_stage=request.workflow_stage.lower(),
            system_stage=request.workflow_stage.lower(),
            intent="",
            context=request.context or {},
            response="",
            analysis_results={},
            next_action="",
            tools_used=[],
            messages=[],
            consent_given=request.workflow_stage != "Started",
            profile_complete=request.workflow_stage in ["intermediate", "advanced"],
            execute_action=False
        )
        
        # Run through LangGraph workflow
        result_state = await finance_workflow.run_async(state)
        
        return {
            "response": result_state["response"],
            "intent": result_state["intent"],
            "workflow_stage": result_state["current_stage"],
            "tools_used": result_state["tools_used"],
            "analysis_results": result_state["analysis_results"],
            "next_action": result_state["next_action"]
        }
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@app.post("/api/v1/auth/login")
async def login(request: AuthRequest):
    """User login endpoint"""
    # Simple demo authentication
    if request.email == "demo@example.com" and request.password == "demo123":
        return {
            "message": "Login successful",
            "user": {
                "id": "demo_user",
                "name": "Demo User",
                "email": request.email
            },
            "token": "demo_token_123",
            "workflow_stage": "Started"
        }
    else:
        # For demo purposes, accept any login
        return {
            "message": "Login successful",
            "user": {
                "id": "user_" + request.email.split("@")[0],
                "name": request.email.split("@")[0].title(),
                "email": request.email
            },
            "token": "token_" + request.email.split("@")[0],
            "workflow_stage": "Started"
        }


@app.post("/api/v1/auth/register")
async def register(request: AuthRequest):
    """User registration endpoint"""
    return {
        "message": "Registration successful",
        "user": {
            "id": "user_" + request.email.split("@")[0],
            "name": request.name or request.email.split("@")[0].title(),
            "email": request.email
        },
        "token": "token_" + request.email.split("@")[0],
        "workflow_stage": "Started"
    }


@app.get("/api/v1/auth/verify")
async def verify_token():
    """Token verification endpoint"""
    return {
        "user": {
            "id": "demo_user",
            "name": "Demo User",
            "email": "demo@example.com"
        },
        "workflow_stage": "Started"
    }


@app.get("/api/v1/dashboard")
async def get_dashboard():
    """Dashboard data endpoint with sample financial data"""
    return {
        "accountBalance": 12450.50,
        "monthlyIncome": 5000,
        "monthlyExpenses": 3200,
        "savingsRate": 36,
        "budgetCategories": [
            {"name": "Food & Dining", "budgeted": 600, "spent": 485, "percentage": 81},
            {"name": "Transportation", "budgeted": 400, "spent": 320, "percentage": 80},
            {"name": "Entertainment", "budgeted": 200, "spent": 150, "percentage": 75},
            {"name": "Shopping", "budgeted": 300, "spent": 380, "percentage": 127}
        ],
        "recentTransactions": [
            {"description": "Coffee Shop", "amount": -4.50, "date": "2025-10-11", "category": "Food & Dining"},
            {"description": "Salary Deposit", "amount": 2500, "date": "2025-10-10", "category": "Income"},
            {"description": "Gas Station", "amount": -45.00, "date": "2025-10-09", "category": "Transportation"},
            {"description": "Online Purchase", "amount": -89.99, "date": "2025-10-08", "category": "Shopping"},
            {"description": "Restaurant", "amount": -67.50, "date": "2025-10-07", "category": "Food & Dining"}
        ],
        "goals": [
            {"name": "Emergency Fund", "target": 10000, "current": 6500, "deadline": "2025-12-31"},
            {"name": "Vacation Fund", "target": 3000, "current": 1200, "deadline": "2025-07-01"},
            {"name": "New Car", "target": 25000, "current": 8500, "deadline": "2026-06-01"}
        ],
        "insights": [
            {"title": "Great Job!", "description": "You stayed under budget in 3 out of 4 categories this month.", "type": "success"},
            {"title": "Shopping Alert", "description": "You've exceeded your shopping budget by 27%. Consider reducing discretionary purchases.", "type": "warning"},
            {"title": "Savings Tip", "description": "Your emergency fund is 65% complete. You're on track to reach your goal by December.", "type": "tip"}
        ]
    }


@app.post("/api/v1/onboarding")
async def complete_onboarding(request: OnboardingRequest):
    """Complete user onboarding"""
    return {
        "message": "Onboarding completed successfully",
        "userProfile": request.user_data,
        "workflow_stage": "MVP",
        "next_steps": [
            "Set up your first budget",
            "Connect your bank account",
            "Define your financial goals"
        ]
    }


if __name__ == "__main__":
    # Check for Groq API key
    if not os.getenv("GROQ_API_KEY"):
        logger.warning("GROQ_API_KEY not found in environment variables")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )