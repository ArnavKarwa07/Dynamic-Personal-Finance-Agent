from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import models as dbm
from typing import Dict, Any
from core.langgraph_workflow import finance_workflow

router = APIRouter()

@router.get("/workflow/status/{user_id}")
async def get_workflow_status(user_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    user = db.query(dbm.User).filter(dbm.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    has_goals = db.query(dbm.Goal).filter(dbm.Goal.user_id == user_id).count() > 0
    has_budgets = db.query(dbm.Budget).filter(dbm.Budget.user_id == user_id).count() > 0
    has_transactions = db.query(dbm.Transaction).filter(dbm.Transaction.user_id == user_id).count() > 0

    if not (has_goals or has_budgets or has_transactions):
        current_stage = "started"
        next_steps = ["Provide consent", "Set a budget", "Add your first goal"]
    elif not (has_goals and has_budgets):
        current_stage = "mvp"
        next_steps = ["Complete budgets and goals", "Review spending patterns"]
    else:
        current_stage = "intermediate"
        next_steps = ["Explore AI insights", "Plan next actions"]

    return {"user_id": user_id, "current_stage": current_stage, "next_steps": next_steps}

@router.get("/workflow/visualization")
async def get_workflow_visualization():
    # Keep endpoint but return a minimal structure (non-dummy content is not DB-driven here)
    return {"workflow_structure": {"stages": ["started", "mvp", "intermediate", "advanced"]}}

@router.get("/tools")
async def get_available_tools(db: Session = Depends(get_db)):
    # Derive available tools from DB presence rather than static list
    # If there is data, we expose relevant capabilities
    has_transactions = db.query(dbm.Transaction).count() > 0
    has_budgets = db.query(dbm.Budget).count() > 0
    has_goals = db.query(dbm.Goal).count() > 0
    tools = []
    if has_transactions:
        tools.append("statement_parser")
        tools.append("budget_analyzer")
    if has_budgets:
        tools.append("budget_alerts")
    if has_goals:
        tools.append("goal_planner")
    return {"tools": tools}

@router.get("/examples")
async def get_example_queries(db: Session = Depends(get_db)):
    # Return example prompts conditioned on presence of user data
    has_transactions = db.query(dbm.Transaction).count() > 0
    has_budgets = db.query(dbm.Budget).count() > 0
    has_goals = db.query(dbm.Goal).count() > 0
    examples = []
    if has_transactions:
        examples.append("Summarize my spending over the last month")
        examples.append("Which categories did I overspend in this month?")
    if has_budgets:
        examples.append("How am I tracking against my budgets this month?")
    if has_goals:
        examples.append("Am I on track for my Emergency Fund goal?")
    if not examples:
        examples.append("Help me get started with budgeting and goals")
    return {"examples": examples}
