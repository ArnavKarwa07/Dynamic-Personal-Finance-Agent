"""
Risk Assessment Tool - Comprehensive risk analysis for financial portfolios
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from agents.nodes import FinanceAgentState
from tools.data_loader import DataLoader
import numpy as np


class RiskAssessmentTool:
    """Comprehensive risk assessment and management tool"""

    def __init__(self):
        self.data_loader = DataLoader()

    def __call__(self, state: FinanceAgentState) -> FinanceAgentState:
        """Main entry point for risk assessment"""
        context = state.get("context", {})

        analysis = self._comprehensive_risk_analysis(
            context.get("transactions"),
            context.get("budget"),
            context.get("investments"),
            context.get("goals"),
            state.get("user_query", ""),
        )

        state["analysis_results"]["risk_assessment"] = analysis
        state["tools_used"].append("risk_assessment")
        return state

    def _comprehensive_risk_analysis(
        self, transactions, budget, investments, goals, query
    ):
        """Perform comprehensive risk analysis"""
        analysis = {
            "overall_risk_score": 0,
            "risk_categories": {},
            "vulnerability_assessment": {},
            "stress_test_results": {},
            "risk_mitigation_strategies": [],
            "insurance_recommendations": [],
            "diversification_analysis": {},
        }

        try:
            # Overall risk scoring
            analysis["overall_risk_score"] = self._calculate_overall_risk_score(
                transactions, budget, investments, goals
            )

            # Category-wise risk analysis
            analysis["risk_categories"] = self._analyze_risk_categories(
                transactions, budget, investments
            )

            # Vulnerability assessment
            analysis["vulnerability_assessment"] = self._assess_vulnerabilities(
                transactions, investments
            )

            # Stress testing
            analysis["stress_test_results"] = self._perform_stress_tests(
                transactions, investments
            )

            # Risk mitigation strategies
            analysis["risk_mitigation_strategies"] = (
                self._generate_risk_mitigation_strategies(
                    transactions, budget, investments
                )
            )

            # Insurance gap analysis
            analysis["insurance_recommendations"] = self._analyze_insurance_needs(
                transactions, investments
            )

            # Portfolio diversification analysis
            if investments:
                analysis["diversification_analysis"] = (
                    self._analyze_portfolio_diversification(investments)
                )

        except Exception as e:
            analysis["error"] = f"Risk analysis error: {str(e)}"

        return analysis

    def _calculate_overall_risk_score(self, transactions, budget, investments, goals):
        """Calculate overall risk score (0-100, higher = more risky)"""
        risk_score = 0

        # Income volatility risk (0-25 points)
        if transactions is not None and not transactions.empty:
            income_volatility = self._calculate_income_volatility(transactions)
            risk_score += min(25, income_volatility * 100)

        # Liquidity risk (0-25 points)
        liquidity_risk = self._calculate_liquidity_risk(transactions, investments)
        risk_score += min(25, liquidity_risk * 25)

        # Concentration risk (0-25 points)
        if investments:
            concentration_risk = self._calculate_concentration_risk(investments)
            risk_score += min(25, concentration_risk * 25)

        # Budget overrun risk (0-25 points)
        if budget and transactions is not None:
            budget_risk = self._calculate_budget_risk(transactions, budget)
            risk_score += min(25, budget_risk * 25)

        return min(100, risk_score)

    def _analyze_risk_categories(self, transactions, budget, investments):
        """Analyze different categories of financial risk"""
        categories = {
            "market_risk": {"score": 0, "description": ""},
            "credit_risk": {"score": 0, "description": ""},
            "liquidity_risk": {"score": 0, "description": ""},
            "operational_risk": {"score": 0, "description": ""},
            "inflation_risk": {"score": 0, "description": ""},
        }

        # Market risk (investment volatility)
        if investments and investments.get("investments"):
            market_risk_score = 0
            for investment in investments["investments"]:
                gain_loss_pct = investment.get("gain_loss_percentage", 0)
                if abs(gain_loss_pct) > 20:  # High volatility
                    market_risk_score += 20
                elif abs(gain_loss_pct) > 10:
                    market_risk_score += 10

            categories["market_risk"]["score"] = min(100, market_risk_score)
            categories["market_risk"][
                "description"
            ] = "Risk from market price fluctuations"

        # Liquidity risk
        liquidity_score = (
            self._calculate_liquidity_risk(transactions, investments) * 100
        )
        categories["liquidity_risk"]["score"] = liquidity_score
        categories["liquidity_risk"][
            "description"
        ] = "Risk of not having enough cash for emergencies"

        # Credit risk (simplified - based on spending patterns)
        if transactions is not None and not transactions.empty:
            expenses = abs(transactions[transactions["amount"] < 0]["amount"].sum())
            income = transactions[transactions["amount"] > 0]["amount"].sum()

            if income > 0:
                expense_ratio = expenses / income
                if expense_ratio > 0.9:  # Spending >90% of income
                    categories["credit_risk"]["score"] = 80
                elif expense_ratio > 0.8:
                    categories["credit_risk"]["score"] = 60
                else:
                    categories["credit_risk"]["score"] = 20

        # Inflation risk (simplified assessment)
        cash_heavy = True
        if investments and investments.get("investments"):
            equity_exposure = sum(
                1
                for inv in investments["investments"]
                if "stock" in inv.get("symbol", "").lower()
            )
            if equity_exposure > len(investments["investments"]) * 0.4:
                cash_heavy = False

        categories["inflation_risk"]["score"] = 70 if cash_heavy else 30
        categories["inflation_risk"]["description"] = "Risk of purchasing power erosion"

        return categories

    def _assess_vulnerabilities(self, transactions, investments):
        """Assess specific financial vulnerabilities"""
        vulnerabilities = []

        # Single income source vulnerability
        if transactions is not None and not transactions.empty:
            income_sources = len(
                transactions[transactions["amount"] > 0]["description"].unique()
            )
            if income_sources <= 1:
                vulnerabilities.append(
                    {
                        "type": "single_income_source",
                        "severity": "high",
                        "description": "Dependence on single income source increases financial risk",
                    }
                )

        # Lack of emergency fund
        emergency_months = self._calculate_emergency_fund_months(
            transactions, investments
        )
        if emergency_months < 3:
            vulnerabilities.append(
                {
                    "type": "insufficient_emergency_fund",
                    "severity": "high" if emergency_months < 1 else "medium",
                    "description": f"Only {emergency_months:.1f} months of expenses in emergency fund",
                }
            )

        # Over-concentration in investments
        if investments and investments.get("investments"):
            concentration = self._calculate_concentration_risk(investments)
            if concentration > 0.4:
                vulnerabilities.append(
                    {
                        "type": "investment_concentration",
                        "severity": "medium",
                        "description": "High concentration in single investment increases risk",
                    }
                )

        return {"vulnerabilities": vulnerabilities, "total_count": len(vulnerabilities)}

    def _perform_stress_tests(self, transactions, investments):
        """Perform financial stress tests"""
        stress_tests = {}

        # Income loss stress test
        if transactions is not None and not transactions.empty:
            monthly_income = transactions[transactions["amount"] > 0][
                "amount"
            ].sum() / max(1, len(transactions["date"].dt.to_period("M").unique()))
            monthly_expenses = abs(
                transactions[transactions["amount"] < 0]["amount"].sum()
            ) / max(1, len(transactions["date"].dt.to_period("M").unique()))

            emergency_months = self._calculate_emergency_fund_months(
                transactions, investments
            )

            stress_tests["income_loss"] = {
                "scenario": "Complete income loss",
                "survival_months": emergency_months,
                "monthly_burn_rate": monthly_expenses,
                "assessment": "critical" if emergency_months < 3 else "manageable",
            }

        # Market crash stress test
        if investments and investments.get("investments"):
            current_portfolio_value = sum(
                inv.get("current_value", 0) for inv in investments["investments"]
            )
            crash_scenario_value = current_portfolio_value * 0.7  # 30% market decline

            stress_tests["market_crash"] = {
                "scenario": "30% market decline",
                "current_value": current_portfolio_value,
                "stressed_value": crash_scenario_value,
                "loss_amount": current_portfolio_value - crash_scenario_value,
                "loss_percentage": 30,
            }

        # High inflation stress test
        if transactions is not None and not transactions.empty:
            current_expenses = abs(
                transactions[transactions["amount"] < 0]["amount"].sum()
            )
            high_inflation_expenses = current_expenses * 1.1  # 10% inflation

            stress_tests["high_inflation"] = {
                "scenario": "10% inflation increase",
                "current_expenses": current_expenses,
                "inflated_expenses": high_inflation_expenses,
                "additional_cost": high_inflation_expenses - current_expenses,
            }

        return stress_tests

    def _generate_risk_mitigation_strategies(self, transactions, budget, investments):
        """Generate risk mitigation strategies"""
        strategies = []

        # Emergency fund strategy
        emergency_months = self._calculate_emergency_fund_months(
            transactions, investments
        )
        if emergency_months < 6:
            strategies.append(
                {
                    "category": "liquidity",
                    "priority": "high",
                    "strategy": "Build Emergency Fund",
                    "description": f"Increase emergency fund from {emergency_months:.1f} to 6 months of expenses",
                    "action_items": [
                        "Set up automatic savings for emergency fund",
                        "Consider high-yield savings account",
                        "Target $500-1000 monthly contributions",
                    ],
                }
            )

        # Diversification strategy
        if investments and investments.get("investments"):
            if len(investments["investments"]) < 5:
                strategies.append(
                    {
                        "category": "diversification",
                        "priority": "medium",
                        "strategy": "Increase Portfolio Diversification",
                        "description": "Add more asset classes to reduce concentration risk",
                        "action_items": [
                            "Consider index funds for broad market exposure",
                            "Add international investments",
                            "Include bonds for stability",
                        ],
                    }
                )

        # Income diversification
        if transactions is not None and not transactions.empty:
            income_sources = len(
                transactions[transactions["amount"] > 0]["description"].unique()
            )
            if income_sources <= 1:
                strategies.append(
                    {
                        "category": "income",
                        "priority": "medium",
                        "strategy": "Diversify Income Sources",
                        "description": "Reduce dependence on single income source",
                        "action_items": [
                            "Develop side income streams",
                            "Build marketable skills",
                            "Consider passive income investments",
                        ],
                    }
                )

        # Budget management strategy
        if budget and transactions is not None:
            budget_risk = self._calculate_budget_risk(transactions, budget)
            if budget_risk > 0.3:
                strategies.append(
                    {
                        "category": "budgeting",
                        "priority": "medium",
                        "strategy": "Improve Budget Control",
                        "description": "Better manage spending to reduce financial stress",
                        "action_items": [
                            "Review and adjust budget categories",
                            "Set up spending alerts",
                            "Track expenses weekly",
                        ],
                    }
                )

        return strategies

    def _analyze_insurance_needs(self, transactions, investments):
        """Analyze insurance gap and recommendations"""
        recommendations = []

        # Estimate insurance needs based on income and assets
        if transactions is not None and not transactions.empty:
            annual_income = (
                transactions[transactions["amount"] > 0]["amount"].sum()
                * 12
                / max(1, len(transactions["date"].dt.to_period("M").unique()))
            )

            # Life insurance need (simplified calculation)
            life_insurance_need = annual_income * 10  # 10x annual income rule
            recommendations.append(
                {
                    "type": "life_insurance",
                    "estimated_need": life_insurance_need,
                    "description": f"Consider ${life_insurance_need:,.0f} in life insurance coverage",
                }
            )

            # Disability insurance
            monthly_income = annual_income / 12
            disability_benefit = monthly_income * 0.6  # 60% income replacement
            recommendations.append(
                {
                    "type": "disability_insurance",
                    "estimated_benefit": disability_benefit,
                    "description": f"Consider ${disability_benefit:,.0f}/month disability insurance",
                }
            )

        # Property insurance (basic recommendation)
        total_assets = 0
        if investments and investments.get("investments"):
            total_assets = sum(
                inv.get("current_value", 0) for inv in investments["investments"]
            )

        if total_assets > 100000:  # If significant assets
            recommendations.append(
                {
                    "type": "umbrella_insurance",
                    "estimated_need": min(total_assets, 1000000),
                    "description": "Consider umbrella insurance for asset protection",
                }
            )

        return recommendations

    def _analyze_portfolio_diversification(self, investments):
        """Analyze portfolio diversification"""
        if not investments.get("investments"):
            return {"error": "No investment data"}

        total_value = sum(
            inv.get("current_value", 0) for inv in investments["investments"]
        )

        # Asset allocation analysis
        asset_types = {}
        for investment in investments["investments"]:
            symbol = investment.get("symbol", "").lower()
            value = investment.get("current_value", 0)

            # Simple classification
            if "bond" in symbol or "treasury" in symbol:
                asset_types["bonds"] = asset_types.get("bonds", 0) + value
            elif any(term in symbol for term in ["stock", "equity", "etf"]):
                asset_types["stocks"] = asset_types.get("stocks", 0) + value
            else:
                asset_types["other"] = asset_types.get("other", 0) + value

        # Calculate percentages
        allocation = {}
        for asset_type, value in asset_types.items():
            allocation[asset_type] = (
                (value / total_value * 100) if total_value > 0 else 0
            )

        # Diversification score
        num_holdings = len(investments["investments"])
        max_position_pct = (
            max(
                (inv.get("current_value", 0) / total_value * 100)
                for inv in investments["investments"]
            )
            if total_value > 0
            else 0
        )

        diversification_score = 100
        if max_position_pct > 40:
            diversification_score -= 30
        elif max_position_pct > 25:
            diversification_score -= 15

        if num_holdings < 5:
            diversification_score -= 20
        elif num_holdings < 10:
            diversification_score -= 10

        return {
            "asset_allocation": allocation,
            "total_holdings": num_holdings,
            "largest_position_pct": max_position_pct,
            "diversification_score": max(0, diversification_score),
            "recommendations": self._get_diversification_recommendations(
                allocation, num_holdings
            ),
        }

    def _get_diversification_recommendations(self, allocation, num_holdings):
        """Get diversification recommendations"""
        recommendations = []

        stocks_pct = allocation.get("stocks", 0)
        bonds_pct = allocation.get("bonds", 0)

        if stocks_pct > 80:
            recommendations.append(
                "Consider adding bonds for stability (target 10-30%)"
            )

        if bonds_pct > 50:
            recommendations.append(
                "Consider reducing bond allocation for growth (target 20-40%)"
            )

        if num_holdings < 5:
            recommendations.append(
                "Increase number of holdings for better diversification"
            )

        if not allocation.get("other", 0):
            recommendations.append(
                "Consider alternative investments (REITs, commodities)"
            )

        return recommendations

    def _calculate_income_volatility(self, transactions):
        """Calculate income volatility"""
        if transactions is None or transactions.empty:
            return 0

        monthly_income = (
            transactions[transactions["amount"] > 0]
            .groupby(transactions["date"].dt.to_period("M"))["amount"]
            .sum()
        )

        if len(monthly_income) < 2:
            return 0

        return (
            monthly_income.std() / monthly_income.mean()
            if monthly_income.mean() > 0
            else 0
        )

    def _calculate_liquidity_risk(self, transactions, investments):
        """Calculate liquidity risk (0-1, higher = more risky)"""
        emergency_months = self._calculate_emergency_fund_months(
            transactions, investments
        )

        if emergency_months >= 6:
            return 0.1  # Low risk
        elif emergency_months >= 3:
            return 0.3  # Medium risk
        elif emergency_months >= 1:
            return 0.6  # High risk
        else:
            return 1.0  # Very high risk

    def _calculate_concentration_risk(self, investments):
        """Calculate investment concentration risk (0-1)"""
        if not investments.get("investments"):
            return 0

        total_value = sum(
            inv.get("current_value", 0) for inv in investments["investments"]
        )
        if total_value <= 0:
            return 0

        max_position = max(
            inv.get("current_value", 0) for inv in investments["investments"]
        )
        return max_position / total_value

    def _calculate_budget_risk(self, transactions, budget):
        """Calculate budget adherence risk (0-1)"""
        if not budget or not budget.get("monthly_budgets"):
            return 0

        current_month = datetime.now().strftime("%Y-%m")
        current_budget = budget["monthly_budgets"].get(current_month, {})

        if not current_budget.get("categories"):
            return 0

        overrun_count = 0
        total_categories = len(current_budget["categories"])

        for category, data in current_budget["categories"].items():
            if data.get("percentage_used", 0) > 100:
                overrun_count += 1

        return overrun_count / total_categories if total_categories > 0 else 0

    def _calculate_emergency_fund_months(self, transactions, investments):
        """Calculate months of expenses covered by emergency fund"""
        if transactions is None or transactions.empty:
            return 0

        monthly_expenses = abs(
            transactions[transactions["amount"] < 0]["amount"].sum()
        ) / max(1, len(transactions["date"].dt.to_period("M").unique()))

        # Estimate liquid assets
        liquid_assets = 0
        if investments and investments.get("investments"):
            # Conservative estimate: 30% of investments are liquid
            total_investments = sum(
                inv.get("current_value", 0) for inv in investments["investments"]
            )
            liquid_assets = total_investments * 0.3

        return liquid_assets / monthly_expenses if monthly_expenses > 0 else 0
