from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from core.langgraph_workflow import finance_workflow, FinanceState
from core.groq_client import groq_client
from api.schemas import ChatRequest
from sqlalchemy.orm import Session
from db.database import get_db
from db import models as dbm
from datetime import datetime

router = APIRouter()


@router.post("/chat")
async def chat_with_agent(request: ChatRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    try:
        # Build user context from DB for full personalization
        user_ctx: Dict[str, Any] = request.context or {}
        if request.user_id and request.user_id != "default":
            try:
                uid = int(request.user_id)
            except ValueError:
                uid = None
            if uid:
                user = db.query(dbm.User).filter(dbm.User.id == uid).first()
                if user:
                    tx = db.query(dbm.Transaction).filter(dbm.Transaction.user_id == uid).order_by(dbm.Transaction.date.desc()).limit(25).all()
                    goals = db.query(dbm.Goal).filter(dbm.Goal.user_id == uid).all()
                    budgets = db.query(dbm.Budget).filter(dbm.Budget.user_id == uid).all()
                    rec = db.query(dbm.RecurringTransaction).filter(dbm.RecurringTransaction.user_id == uid).all()
                    user_ctx.update({
                        "user": {"id": user.id, "email": user.email, "name": user.name},
                        "transactions": [
                            {
                                "id": t.id,
                                "description": t.description,
                                "amount": float(t.amount),
                                "date": t.date.isoformat() if hasattr(t.date, 'isoformat') else str(t.date),
                                "category": t.category,
                            }
                            for t in tx
                        ],
                        "goals": [
                            {
                                "id": g.id,
                                "name": g.name,
                                "target": float(g.target),
                                "current": float(g.current),
                                "deadline": g.deadline.isoformat() if g.deadline else None,
                            }
                            for g in goals
                        ],
                        "budgets": [
                            {"id": b.id, "category": b.category, "budgeted": float(b.budgeted), "month": b.month}
                            for b in budgets
                        ],
                        "recurring": [
                            {
                                "id": r.id,
                                "description": r.description,
                                "amount": float(r.amount),
                                "category": r.category,
                                "frequency": r.frequency,
                                "interval": r.interval,
                                "start_date": r.start_date.isoformat() if r.start_date else None,
                                "end_date": r.end_date.isoformat() if r.end_date else None,
                                "next_date": r.next_date.isoformat() if r.next_date else None,
                            }
                            for r in rec
                        ],
                    })

        state: FinanceState = {
            "user_id": request.user_id,
            "user_query": request.message,
            "current_stage": request.workflow_stage.lower(),
            "system_stage": request.workflow_stage.lower(),
            "intent": "",
            "context": user_ctx,
            "response": "",
            "analysis_results": {},
            "next_action": "",
            "tools_used": [],
            "messages": [],
            "consent_given": request.workflow_stage != "Started",
            "profile_complete": request.workflow_stage in ["intermediate", "advanced"],
            "execute_action": False,
            "explanations": [],
        }

        result = await finance_workflow.run_async(state)
        # Try to extract and execute a structured action
        action_info = await groq_client.extract_action(request.message)
        action_result = None
        if action_info.get("action") and action_info["action"] != "none":
            try:
                action = action_info["action"]
                p = action_info.get("params", {})
                uid = int(request.user_id) if request.user_id and request.user_id != "default" else None
                if uid:
                    if action == "add_transaction":
                        row = dbm.Transaction(
                            user_id=uid,
                            description=p.get("description"),
                            amount=float(p.get("amount")),
                            date=datetime.strptime(p.get("date"), "%Y-%m-%d").date() if p.get("date") else datetime.utcnow().date(),
                            category=p.get("category") or "Uncategorized",
                        )
                        db.add(row); db.commit(); action_result = {"status": "ok", "id": row.id}
                    elif action == "update_transaction" and p.get("id"):
                        r = db.query(dbm.Transaction).filter(dbm.Transaction.user_id==uid, dbm.Transaction.id==int(p["id"])) .first()
                        if r:
                            if p.get("description") is not None: r.description = p.get("description")
                            if p.get("amount") is not None: r.amount = float(p.get("amount"))
                            if p.get("date"): r.date = datetime.strptime(p.get("date"), "%Y-%m-%d").date()
                            if p.get("category"): r.category = p.get("category")
                            db.commit(); action_result = {"status": "ok", "id": r.id}
                    elif action == "delete_transaction" and p.get("id"):
                        r = db.query(dbm.Transaction).filter(dbm.Transaction.user_id==uid, dbm.Transaction.id==int(p["id"])) .first()
                        if r:
                            db.delete(r); db.commit(); action_result = {"status": "ok", "deleted": int(p["id"]) }
                    elif action == "add_goal":
                        r = dbm.Goal(user_id=uid, name=p.get("name"), target=float(p.get("target")), current=float(p.get("current") or 0), deadline=datetime.strptime(p.get("deadline"), "%Y-%m-%d").date() if p.get("deadline") else None)
                        db.add(r); db.commit(); action_result = {"status": "ok", "id": r.id}
                    elif action == "update_goal" and p.get("id"):
                        r = db.query(dbm.Goal).filter(dbm.Goal.user_id==uid, dbm.Goal.id==int(p["id"])) .first()
                        if r:
                            if p.get("name") is not None: r.name = p.get("name")
                            if p.get("target") is not None: r.target = float(p.get("target"))
                            if p.get("current") is not None: r.current = float(p.get("current"))
                            if p.get("deadline"): r.deadline = datetime.strptime(p.get("deadline"), "%Y-%m-%d").date()
                            db.commit(); action_result = {"status": "ok", "id": r.id}
                    elif action == "delete_goal" and p.get("id"):
                        r = db.query(dbm.Goal).filter(dbm.Goal.user_id==uid, dbm.Goal.id==int(p["id"])) .first()
                        if r:
                            db.delete(r); db.commit(); action_result = {"status": "ok", "deleted": int(p["id"]) }
                    elif action == "add_budget":
                        r = dbm.Budget(user_id=uid, category=p.get("category"), budgeted=float(p.get("budgeted")), month=p.get("month") or datetime.utcnow().strftime("%Y-%m"))
                        db.add(r); db.commit(); action_result = {"status": "ok", "id": r.id}
                    elif action == "update_budget" and p.get("id"):
                        r = db.query(dbm.Budget).filter(dbm.Budget.user_id==uid, dbm.Budget.id==int(p["id"])) .first()
                        if r:
                            if p.get("category"): r.category = p.get("category")
                            if p.get("budgeted") is not None: r.budgeted = float(p.get("budgeted"))
                            if p.get("month"): r.month = p.get("month")
                            db.commit(); action_result = {"status": "ok", "id": r.id}
                    elif action == "delete_budget" and p.get("id"):
                        r = db.query(dbm.Budget).filter(dbm.Budget.user_id==uid, dbm.Budget.id==int(p["id"])) .first()
                        if r:
                            db.delete(r); db.commit(); action_result = {"status": "ok", "deleted": int(p["id"]) }
                    elif action == "add_recurring":
                        r = dbm.RecurringTransaction(
                            user_id=uid,
                            description=p.get("description"),
                            amount=float(p.get("amount")),
                            category=p.get("category") or "Subscriptions",
                            start_date=datetime.strptime(p.get("start_date"), "%Y-%m-%d").date() if p.get("start_date") else datetime.utcnow().date(),
                            frequency=p.get("frequency") or "monthly",
                            interval=int(p.get("interval") or 1),
                            end_date=datetime.strptime(p.get("end_date"), "%Y-%m-%d").date() if p.get("end_date") else None,
                            next_date=datetime.strptime(p.get("next_date"), "%Y-%m-%d").date() if p.get("next_date") else None,
                        )
                        db.add(r); db.commit(); action_result = {"status": "ok", "id": r.id}
                    elif action == "update_recurring" and p.get("id"):
                        r = db.query(dbm.RecurringTransaction).filter(dbm.RecurringTransaction.user_id==uid, dbm.RecurringTransaction.id==int(p["id"])) .first()
                        if r:
                            if p.get("description") is not None: r.description = p.get("description")
                            if p.get("amount") is not None: r.amount = float(p.get("amount"))
                            if p.get("category"): r.category = p.get("category")
                            if p.get("frequency"): r.frequency = p.get("frequency")
                            if p.get("interval") is not None: r.interval = int(p.get("interval"))
                            if p.get("start_date"): r.start_date = datetime.strptime(p.get("start_date"), "%Y-%m-%d").date()
                            if p.get("end_date"): r.end_date = datetime.strptime(p.get("end_date"), "%Y-%m-%d").date()
                            if p.get("next_date"): r.next_date = datetime.strptime(p.get("next_date"), "%Y-%m-%d").date()
                            db.commit(); action_result = {"status": "ok", "id": r.id}
                    elif action == "delete_recurring" and p.get("id"):
                        r = db.query(dbm.RecurringTransaction).filter(dbm.RecurringTransaction.user_id==uid, dbm.RecurringTransaction.id==int(p["id"])) .first()
                        if r:
                            db.delete(r); db.commit(); action_result = {"status": "ok", "deleted": int(p["id"]) }
                # Append action to explanations for transparency
                if action_result is not None:
                    result.setdefault("explanations", []).append({
                        "step": "action_executor",
                        "what": f"Executed {action_info['action']}",
                        "outcome": action_result,
                    })
                    tools = result.get("tools_used", [])
                    if "action_executor" not in tools:
                        tools.append("action_executor")
                        result["tools_used"] = tools
            except Exception as _:
                # If execution fails, record failure in trace
                result.setdefault("explanations", []).append({
                    "step": "action_executor",
                    "what": f"Attempted {action_info['action']} but failed",
                })

        return {
            "response": result.get("response", ""),
            "intent": result.get("intent", ""),
            "workflow_stage": result.get("current_stage", "started"),
            "stage": result.get("current_stage", "started"),
            "tools_used": result.get("tools_used", []),
            "analysis_results": result.get("analysis_results", {}),
            "next_action": result.get("next_action", ""),
            # Explainable AI trace
            "explanations": result.get("explanations", []),
            # Compat placeholders kept empty (no predefined messages)
            "suggestions": [],
            "visualizations": [],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {e}")


@router.post("/chat/execute")
async def execute_action(payload: Dict[str, Any], db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Execute a structured action coming from the UI suggestions.
    Body: { user_id: int, action: str, params: dict }
    """
    try:
        user_id = payload.get("user_id")
        action = payload.get("action")
        p = payload.get("params", {})
        if not user_id or not action:
            raise HTTPException(status_code=400, detail="Missing user_id or action")
        uid = int(user_id)
        action_result = None

        if action == "add_transaction":
            row = dbm.Transaction(
                user_id=uid,
                description=p.get("description"),
                amount=float(p.get("amount")),
                date=datetime.strptime(p.get("date"), "%Y-%m-%d").date() if p.get("date") else datetime.utcnow().date(),
                category=p.get("category") or "Uncategorized",
            )
            db.add(row); db.commit(); action_result = {"status": "ok", "id": row.id}
        elif action == "update_transaction" and p.get("id"):
            r = db.query(dbm.Transaction).filter(dbm.Transaction.user_id==uid, dbm.Transaction.id==int(p["id"])) .first()
            if r:
                if p.get("description") is not None: r.description = p.get("description")
                if p.get("amount") is not None: r.amount = float(p.get("amount"))
                if p.get("date"): r.date = datetime.strptime(p.get("date"), "%Y-%m-%d").date()
                if p.get("category"): r.category = p.get("category")
                db.commit(); action_result = {"status": "ok", "id": r.id}
        elif action == "delete_transaction" and p.get("id"):
            r = db.query(dbm.Transaction).filter(dbm.Transaction.user_id==uid, dbm.Transaction.id==int(p["id"])) .first()
            if r:
                db.delete(r); db.commit(); action_result = {"status": "ok", "deleted": int(p["id"]) }
        elif action == "add_goal":
            r = dbm.Goal(user_id=uid, name=p.get("name"), target=float(p.get("target")), current=float(p.get("current") or 0), deadline=datetime.strptime(p.get("deadline"), "%Y-%m-%d").date() if p.get("deadline") else None)
            db.add(r); db.commit(); action_result = {"status": "ok", "id": r.id}
        elif action == "update_goal" and p.get("id"):
            r = db.query(dbm.Goal).filter(dbm.Goal.user_id==uid, dbm.Goal.id==int(p["id"])) .first()
            if r:
                if p.get("name") is not None: r.name = p.get("name")
                if p.get("target") is not None: r.target = float(p.get("target"))
                if p.get("current") is not None: r.current = float(p.get("current"))
                if p.get("deadline"): r.deadline = datetime.strptime(p.get("deadline"), "%Y-%m-%d").date()
                db.commit(); action_result = {"status": "ok", "id": r.id}
        elif action == "delete_goal" and p.get("id"):
            r = db.query(dbm.Goal).filter(dbm.Goal.user_id==uid, dbm.Goal.id==int(p["id"])) .first()
            if r:
                db.delete(r); db.commit(); action_result = {"status": "ok", "deleted": int(p["id"]) }
        elif action == "add_budget":
            r = dbm.Budget(user_id=uid, category=p.get("category"), budgeted=float(p.get("budgeted")), month=p.get("month") or datetime.utcnow().strftime("%Y-%m"))
            db.add(r); db.commit(); action_result = {"status": "ok", "id": r.id}
        elif action == "update_budget" and p.get("id"):
            r = db.query(dbm.Budget).filter(dbm.Budget.user_id==uid, dbm.Budget.id==int(p["id"])) .first()
            if r:
                if p.get("category"): r.category = p.get("category")
                if p.get("budgeted") is not None: r.budgeted = float(p.get("budgeted"))
                if p.get("month"): r.month = p.get("month")
                db.commit(); action_result = {"status": "ok", "id": r.id}
        elif action == "delete_budget" and p.get("id"):
            r = db.query(dbm.Budget).filter(dbm.Budget.user_id==uid, dbm.Budget.id==int(p["id"])) .first()
            if r:
                db.delete(r); db.commit(); action_result = {"status": "ok", "deleted": int(p["id"]) }
        elif action == "add_recurring":
            r = dbm.RecurringTransaction(
                user_id=uid,
                description=p.get("description"),
                amount=float(p.get("amount")),
                category=p.get("category") or "Subscriptions",
                start_date=datetime.strptime(p.get("start_date"), "%Y-%m-%d").date() if p.get("start_date") else datetime.utcnow().date(),
                frequency=p.get("frequency") or "monthly",
                interval=int(p.get("interval") or 1),
                end_date=datetime.strptime(p.get("end_date"), "%Y-%m-%d").date() if p.get("end_date") else None,
                next_date=datetime.strptime(p.get("next_date"), "%Y-%m-%d").date() if p.get("next_date") else None,
            )
            db.add(r); db.commit(); action_result = {"status": "ok", "id": r.id}
        elif action == "update_recurring" and p.get("id"):
            r = db.query(dbm.RecurringTransaction).filter(dbm.RecurringTransaction.user_id==uid, dbm.RecurringTransaction.id==int(p["id"])) .first()
            if r:
                if p.get("description") is not None: r.description = p.get("description")
                if p.get("amount") is not None: r.amount = float(p.get("amount"))
                if p.get("category"): r.category = p.get("category")
                if p.get("frequency"): r.frequency = p.get("frequency")
                if p.get("interval") is not None: r.interval = int(p.get("interval"))
                if p.get("start_date"): r.start_date = datetime.strptime(p.get("start_date"), "%Y-%m-%d").date()
                if p.get("end_date"): r.end_date = datetime.strptime(p.get("end_date"), "%Y-%m-%d").date()
                if p.get("next_date"): r.next_date = datetime.strptime(p.get("next_date"), "%Y-%m-%d").date()
                db.commit(); action_result = {"status": "ok", "id": r.id}
        elif action == "delete_recurring" and p.get("id"):
            r = db.query(dbm.RecurringTransaction).filter(dbm.RecurringTransaction.user_id==uid, dbm.RecurringTransaction.id==int(p["id"])) .first()
            if r:
                db.delete(r); db.commit(); action_result = {"status": "ok", "deleted": int(p["id"]) }

        if action_result is None:
            raise HTTPException(status_code=400, detail="Action failed or did nothing")

        return {"status": "ok", "result": action_result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing action: {e}")
