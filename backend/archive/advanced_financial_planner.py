"""
Advanced Financial Planning Tool - Strategic analysis and recommendations
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from agents.nodes import FinanceAgentState
from tools.data_loader import DataLoader
import numpy as np


class AdvancedFinancialPlannerTool:
    """Advanced financial planning and strategic analysis tool"""

    def __init__(self):
        self.data_loader = DataLoader()

    def __call__(self, state: FinanceAgentState) -> FinanceAgentState:
        """Main entry point for advanced financial planning"""
        context = state.get("context", {})

        analysis = self._comprehensive_financial_analysis(
            context.get("transactions"),
            context.get("budget"),
            context.get("investments"),
            context.get("goals"),
            state.get("user_query", ""),
        )

        state["analysis_results"]["advanced_financial_planner"] = analysis
        state["tools_used"].append("advanced_financial_planner")
        return state

    def _comprehensive_financial_analysis(
        self, transactions, budget, investments, goals, query
    ):
        """Perform comprehensive financial analysis"""
        analysis = {
            "financial_health_score": 0,
            "risk_assessment": {},
            "optimization_recommendations": [],
            "cash_flow_analysis": {},
            "debt_analysis": {},
            "savings_rate": 0,
            "emergency_fund_months": 0,
            "retirement_readiness": {},
        }

        try:
            # Calculate financial health score
            analysis["financial_health_score"] = self._calculate_financial_health_score(
                transactions, budget, investments, goals
            )

            # Risk assessment
            analysis["risk_assessment"] = self._assess_financial_risks(
                transactions, budget, investments
            )

            # Cash flow analysis
            analysis["cash_flow_analysis"] = self._analyze_cash_flow(transactions)

            # Savings rate calculation
            analysis["savings_rate"] = self._calculate_savings_rate(transactions)

            # Emergency fund assessment
            analysis["emergency_fund_months"] = self._assess_emergency_fund(
                transactions, investments
            )

            # Generate optimization recommendations
            analysis["optimization_recommendations"] = self._generate_recommendations(
                transactions, budget, investments, goals
            )

            # Retirement readiness (basic calculation)
            analysis["retirement_readiness"] = self._assess_retirement_readiness(
                transactions, investments
            )

        except Exception as e:
            analysis["error"] = f"Analysis error: {str(e)}"

        return analysis

    def _calculate_financial_health_score(
        self, transactions, budget, investments, goals
    ):
        """Calculate overall financial health score (0-100)"""
        score = 0
        max_score = 100

        # Emergency fund score (25 points)
        emergency_months = self._assess_emergency_fund(transactions, investments)
        if emergency_months >= 6:
            score += 25
        elif emergency_months >= 3:
            score += 15
        elif emergency_months >= 1:
            score += 10

        # Savings rate score (25 points)
        savings_rate = self._calculate_savings_rate(transactions)
        if savings_rate >= 0.20:  # 20% or more
            score += 25
        elif savings_rate >= 0.15:
            score += 20
        elif savings_rate >= 0.10:
            score += 15
        elif savings_rate >= 0.05:
            score += 10

        # Budget adherence score (25 points)
        if budget and transactions is not None and not transactions.empty:
            budget_score = self._calculate_budget_adherence_score(transactions, budget)
            score += min(25, budget_score)

        # Investment diversification score (25 points)
        if investments and investments.get("investments"):
            diversification_score = self._calculate_diversification_score(investments)
            score += min(25, diversification_score)
        else:
            score += 5  # Bonus for having any investments

        return min(max_score, score)

    def _assess_financial_risks(self, transactions, budget, investments):
        """Assess various financial risks"""
        risks = {
            "high_spending_volatility": False,
            "budget_overruns": [],
            "concentration_risk": False,
            "liquidity_risk": False,
            "inflation_risk": False,
        }

        if transactions is not None and not transactions.empty:
            # Check spending volatility
            monthly_spending = (
                transactions.groupby(transactions["date"].dt.to_period("M"))["amount"]
                .sum()
                .abs()
            )

            if len(monthly_spending) > 1:
                volatility = monthly_spending.std() / monthly_spending.mean()
                risks["high_spending_volatility"] = volatility > 0.3

        if budget and budget.get("monthly_budgets"):
            # Check budget overruns
            current_month = datetime.now().strftime("%Y-%m")
            current_budget = budget["monthly_budgets"].get(current_month, {})

            for category, data in current_budget.get("categories", {}).items():
                if data.get("percentage_used", 0) > 100:
                    risks["budget_overruns"].append(
                        {
                            "category": category,
                            "overrun_percentage": data.get("percentage_used", 0) - 100,
                        }
                    )

        if investments and investments.get("investments"):
            # Check concentration risk
            total_value = sum(
                inv.get("current_value", 0) for inv in investments["investments"]
            )
            if total_value > 0:
                max_position = max(
                    inv.get("current_value", 0) / total_value
                    for inv in investments["investments"]
                )
                risks["concentration_risk"] = (
                    max_position > 0.4
                )  # More than 40% in one asset

        return risks

    def _analyze_cash_flow(self, transactions):
        """Analyze cash flow patterns"""
        if transactions is None or transactions.empty:
            return {"error": "No transaction data"}

        # Separate income and expenses
        income = transactions[transactions["amount"] > 0]["amount"].sum()
        expenses = transactions[transactions["amount"] < 0]["amount"].sum()

        # Monthly cash flow
        monthly_data = (
            transactions.groupby(transactions["date"].dt.to_period("M"))
            .agg({"amount": ["sum", "count"]})
            .round(2)
        )

        return {
            "total_income": income,
            "total_expenses": abs(expenses),
            "net_cash_flow": income + expenses,
            "monthly_average_income": income / max(1, len(monthly_data)),
            "monthly_average_expenses": abs(expenses) / max(1, len(monthly_data)),
            "cash_flow_trend": "positive" if (income + expenses) > 0 else "negative",
        }

    def _calculate_savings_rate(self, transactions):
        """Calculate savings rate"""
        if transactions is None or transactions.empty:
            return 0

        income = transactions[transactions["amount"] > 0]["amount"].sum()
        expenses = abs(transactions[transactions["amount"] < 0]["amount"].sum())

        if income <= 0:
            return 0

        savings = income - expenses
        return max(0, savings / income)

    def _assess_emergency_fund(self, transactions, investments):
        """Assess emergency fund adequacy in months of expenses"""
        if transactions is None or transactions.empty:
            return 0

        # Calculate average monthly expenses
        monthly_expenses = abs(
            transactions[transactions["amount"] < 0]["amount"].sum()
        ) / max(1, len(transactions["date"].dt.to_period("M").unique()))

        # Estimate liquid assets (simplified - using investment data)
        liquid_assets = 0
        if investments and investments.get("investments"):
            # Assume 50% of investments are liquid (conservative estimate)
            total_investments = sum(
                inv.get("current_value", 0) for inv in investments["investments"]
            )
            liquid_assets = total_investments * 0.5

        if monthly_expenses <= 0:
            return 0

        return liquid_assets / monthly_expenses

    def _generate_recommendations(self, transactions, budget, investments, goals):
        """Generate personalized financial recommendations"""
        recommendations = []

        # Savings rate recommendation
        savings_rate = self._calculate_savings_rate(transactions)
        if savings_rate < 0.10:
            recommendations.append(
                {
                    "category": "savings",
                    "priority": "high",
                    "title": "Increase Savings Rate",
                    "description": f"Your current savings rate is {savings_rate*100:.1f}%. Consider targeting at least 10-15% of income for savings.",
                }
            )

        # Emergency fund recommendation
        emergency_months = self._assess_emergency_fund(transactions, investments)
        if emergency_months < 3:
            recommendations.append(
                {
                    "category": "emergency_fund",
                    "priority": "high",
                    "title": "Build Emergency Fund",
                    "description": f"You have {emergency_months:.1f} months of expenses saved. Target 3-6 months for financial security.",
                }
            )

        # Budget optimization
        if budget and transactions is not None and not transactions.empty:
            high_spending_categories = self._identify_high_spending_categories(
                transactions
            )
            if high_spending_categories:
                recommendations.append(
                    {
                        "category": "budgeting",
                        "priority": "medium",
                        "title": "Optimize Spending",
                        "description": f"Consider reviewing spending in: {', '.join(high_spending_categories[:3])}",
                    }
                )

        # Investment diversification
        if investments and investments.get("investments"):
            if len(investments["investments"]) < 3:
                recommendations.append(
                    {
                        "category": "investment",
                        "priority": "medium",
                        "title": "Diversify Investments",
                        "description": "Consider diversifying across more asset classes to reduce risk.",
                    }
                )

        return recommendations

    def _identify_high_spending_categories(self, transactions):
        """Identify categories with high spending"""
        if transactions is None or transactions.empty:
            return []

        category_spending = (
            transactions[transactions["amount"] < 0]
            .groupby("category")["amount"]
            .sum()
            .abs()
        )
        total_spending = category_spending.sum()

        # Categories that account for more than 25% of spending
        high_spending = category_spending[category_spending / total_spending > 0.25]
        return high_spending.index.tolist()

    def _calculate_budget_adherence_score(self, transactions, budget):
        """Calculate budget adherence score"""
        current_month = datetime.now().strftime("%Y-%m")
        current_budget = budget.get("monthly_budgets", {}).get(current_month, {})

        if not current_budget.get("categories"):
            return 0

        total_score = 0
        category_count = 0

        for category, data in current_budget["categories"].items():
            percentage_used = data.get("percentage_used", 0)
            if percentage_used <= 100:
                total_score += min(
                    100, 110 - percentage_used
                )  # Reward staying under budget
            else:
                total_score += max(
                    0, 50 - (percentage_used - 100)
                )  # Penalty for overspending
            category_count += 1

        return (total_score / max(1, category_count)) / 4  # Scale to 25 points max

    def _calculate_diversification_score(self, investments):
        """Calculate investment diversification score"""
        if not investments.get("investments"):
            return 0

        # Simple diversification score based on number of holdings
        num_investments = len(investments["investments"])
        if num_investments >= 10:
            return 25
        elif num_investments >= 5:
            return 20
        elif num_investments >= 3:
            return 15
        else:
            return 10

    def _assess_retirement_readiness(self, transactions, investments):
        """Basic retirement readiness assessment"""
        current_age = 35  # Assumed age for demo
        retirement_age = 65
        years_to_retirement = retirement_age - current_age

        # Estimate current retirement savings
        retirement_savings = 0
        if investments and investments.get("investments"):
            retirement_savings = sum(
                inv.get("current_value", 0) for inv in investments["investments"]
            )

        # Calculate required retirement corpus (simplified)
        annual_expenses = 0
        if transactions is not None and not transactions.empty:
            annual_expenses = (
                abs(transactions[transactions["amount"] < 0]["amount"].sum())
                * 12
                / len(transactions["date"].dt.to_period("M").unique())
            )

        required_corpus = annual_expenses * 25  # 4% rule

        return {
            "current_savings": retirement_savings,
            "required_corpus": required_corpus,
            "years_to_retirement": years_to_retirement,
            "monthly_savings_needed": (
                max(
                    0,
                    (required_corpus - retirement_savings) / (years_to_retirement * 12),
                )
                if years_to_retirement > 0
                else 0
            ),
            "on_track": (
                retirement_savings
                >= (
                    required_corpus
                    * (retirement_age - years_to_retirement)
                    / retirement_age
                )
                if years_to_retirement > 0
                else False
            ),
        }
