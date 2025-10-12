from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import models as dbm
from typing import Dict, Any
from core.langgraph_workflow import finance_workflow, FinanceState
from api.schemas import ChatRequest

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

@router.post("/workflow/run")
async def run_workflow_on_demand(req: ChatRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Run the LangGraph workflow only when user asks. Returns explainable steps."""
    try:
        # Optional: load context from DB similar to chat
        ctx = req.context or {}
        uid = None
        try:
            if req.user_id and req.user_id != "default":
                uid = int(req.user_id)
        except Exception:
            uid = None
        if uid:
            user = db.query(dbm.User).filter(dbm.User.id == uid).first()
            if user:
                tx = (
                    db.query(dbm.Transaction)
                    .filter(dbm.Transaction.user_id == uid)
                    .order_by(dbm.Transaction.date.desc())
                    .limit(25)
                    .all()
                )
                ctx.update({
                    "user": {"id": user.id, "email": user.email, "name": user.name},
                    "transactions_count": len(tx),
                })

        state: FinanceState = {
            "user_id": req.user_id,
            "user_query": req.message,
            "current_stage": req.workflow_stage.lower(),
            "system_stage": req.workflow_stage.lower(),
            "intent": "",
            "context": ctx,
            "response": "",
            "analysis_results": {},
            "next_action": "",
            "tools_used": [],
            "messages": [],
            "consent_given": req.workflow_stage != "Started",
            "profile_complete": req.workflow_stage in ["intermediate", "advanced"],
            "execute_action": False,
            "explanations": [],
        }

        result = await finance_workflow.run_async(state)
        return {
            "response": result.get("response", ""),
            "intent": result.get("intent", ""),
            "workflow_stage": result.get("current_stage", "started"),
            "tools_used": result.get("tools_used", []),
            "explanations": result.get("explanations", []),
            "analysis_results": result.get("analysis_results", {}),
            "next_action": result.get("next_action", ""),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow error: {e}")
