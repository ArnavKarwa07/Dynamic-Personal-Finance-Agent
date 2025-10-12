from sqlalchemy.orm import Session
from datetime import date, timedelta
from .models import User, Transaction, Goal, Budget, RecurringTransaction
from .database import SessionLocal, engine, Base
from passlib.context import CryptContext

pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def seed_demo():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        # idempotent: check existing demo user
        demo = db.query(User).filter(User.email == "demo@example.com").first()
        if not demo:
            demo = User(
                email="demo@example.com",
                name="Demo User",
                password_hash=pwd.hash("demo123"),
            )
            db.add(demo)
            db.commit()
            db.refresh(demo)

        uid = demo.id

        # Seed budgets (current & last month)
        budgets = [
            Budget(user_id=uid, category="Food & Dining", budgeted=600, month="2025-10"),
            Budget(user_id=uid, category="Transportation", budgeted=400, month="2025-10"),
            Budget(user_id=uid, category="Entertainment", budgeted=200, month="2025-10"),
            Budget(user_id=uid, category="Shopping", budgeted=300, month="2025-10"),
            Budget(user_id=uid, category="Food & Dining", budgeted=550, month="2025-09"),
        ]
        for b in budgets:
            if not db.query(Budget).filter(Budget.user_id==uid, Budget.month==b.month, Budget.category==b.category).first():
                db.add(b)

        # Seed goals
        goals = [
            Goal(user_id=uid, name="Emergency Fund", target=10000, current=6500, deadline=date(2025,12,31)),
            Goal(user_id=uid, name="Vacation Fund", target=3000, current=1200, deadline=date(2025,7,1)),
        ]
        for g in goals:
            if not db.query(Goal).filter(Goal.user_id==uid, Goal.name==g.name).first():
                db.add(g)

        # Seed recurring (monthly rent and subscription)
        recur = [
            RecurringTransaction(user_id=uid, description="Rent", amount=-1500, category="Housing", start_date=date(2025,1,1), frequency="monthly", interval=1, next_date=date(2025,10,1)),
            RecurringTransaction(user_id=uid, description="Music Subscription", amount=-9.99, category="Entertainment", start_date=date(2025,8,1), frequency="monthly", interval=1, next_date=date(2025,10,1)),
        ]
        for r in recur:
            if not db.query(RecurringTransaction).filter(RecurringTransaction.user_id==uid, RecurringTransaction.description==r.description).first():
                db.add(r)

        # Seed a few recent transactions
        today = date.today()
        txs = [
            Transaction(user_id=uid, description="Coffee Shop", amount=-4.50, date=today - timedelta(days=1), category="Food & Dining"),
            Transaction(user_id=uid, description="Salary Deposit", amount=2500, date=today - timedelta(days=2), category="Income"),
            Transaction(user_id=uid, description="Gas Station", amount=-45.00, date=today - timedelta(days=3), category="Transportation"),
        ]
        for t in txs:
            exists = db.query(Transaction).filter(Transaction.user_id==uid, Transaction.description==t.description, Transaction.date==t.date).first()
            if not exists:
                db.add(t)

        db.commit()
        return {"status":"ok","user_id": uid}
    finally:
        db.close()

if __name__ == "__main__":
    print(seed_demo())
