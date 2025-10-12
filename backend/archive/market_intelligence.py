"""
Market Intelligence Tool - Real-time market data and insights
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from agents.nodes import FinanceAgentState
from tools.data_loader import DataLoader
import random  # For demo purposes - simulating market data


class MarketIntelligenceTool:
    """Market intelligence and analysis tool"""

    def __init__(self):
        self.data_loader = DataLoader()

    def __call__(self, state: FinanceAgentState) -> FinanceAgentState:
        """Main entry point for market intelligence"""
        analysis = self._market_analysis(state.get("user_query", ""))

        state["analysis_results"]["market_intelligence"] = analysis
        state["tools_used"].append("market_intelligence")
        return state

    def _market_analysis(self, query):
        """Comprehensive market analysis"""
        analysis = {
            "market_overview": self._get_market_overview(),
            "sector_analysis": self._get_sector_analysis(),
            "economic_indicators": self._get_economic_indicators(),
            "market_sentiment": self._analyze_market_sentiment(),
            "investment_opportunities": self._identify_opportunities(),
            "risk_alerts": self._generate_risk_alerts(),
            "market_forecast": self._generate_market_forecast(),
        }

        return analysis

    def _get_market_overview(self):
        """Get current market overview"""
        # Simulated market data for demo
        return {
            "major_indices": {
                "S&P 500": {
                    "current": 4521.30,
                    "change": 25.40,
                    "change_percent": 0.56,
                    "trend": "bullish",
                },
                "NASDAQ": {
                    "current": 14823.12,
                    "change": -12.85,
                    "change_percent": -0.09,
                    "trend": "neutral",
                },
                "DOW": {
                    "current": 35467.89,
                    "change": 156.23,
                    "change_percent": 0.44,
                    "trend": "bullish",
                },
            },
            "market_status": "OPEN",
            "volatility_index": 18.45,
            "market_mood": "cautiously optimistic",
        }

    def _get_sector_analysis(self):
        """Analyze sector performance"""
        sectors = [
            "Technology",
            "Healthcare",
            "Financial Services",
            "Energy",
            "Consumer Discretionary",
            "Industrials",
            "Real Estate",
            "Utilities",
        ]

        sector_data = {}
        for sector in sectors:
            # Simulate sector performance
            change = random.uniform(-3.0, 4.0)
            sector_data[sector] = {
                "performance_1d": round(change, 2),
                "performance_1w": round(change * 3.2, 2),
                "performance_1m": round(change * 8.5, 2),
                "outlook": "positive" if change > 0 else "negative",
                "key_drivers": self._get_sector_drivers(sector),
            }

        return sector_data

    def _get_sector_drivers(self, sector):
        """Get key drivers for each sector"""
        drivers = {
            "Technology": ["AI adoption", "Cloud migration", "Semiconductor demand"],
            "Healthcare": ["Aging population", "Drug approvals", "Healthcare spending"],
            "Financial Services": ["Interest rates", "Credit demand", "Regulation"],
            "Energy": ["Oil prices", "Renewable transition", "Geopolitical events"],
            "Consumer Discretionary": [
                "Consumer confidence",
                "Employment",
                "Inflation",
            ],
            "Industrials": [
                "Manufacturing activity",
                "Infrastructure spending",
                "Trade",
            ],
            "Real Estate": ["Interest rates", "Housing demand", "Commercial occupancy"],
            "Utilities": [
                "Energy transition",
                "Interest rates",
                "Regulatory environment",
            ],
        }
        return drivers.get(
            sector, ["Market conditions", "Economic factors", "Industry trends"]
        )

    def _get_economic_indicators(self):
        """Get key economic indicators"""
        return {
            "gdp_growth": {"current": 2.4, "forecast": 2.1, "trend": "stable"},
            "inflation_rate": {"current": 3.2, "target": 2.0, "trend": "declining"},
            "unemployment": {"current": 3.8, "change": -0.1, "trend": "improving"},
            "fed_funds_rate": {
                "current": 5.25,
                "next_meeting": "2025-11-15",
                "expected_change": 0.0,
            },
            "consumer_confidence": {
                "current": 102.3,
                "change": 2.1,
                "trend": "improving",
            },
        }

    def _analyze_market_sentiment(self):
        """Analyze overall market sentiment"""
        return {
            "overall_sentiment": "Neutral to Positive",
            "fear_greed_index": 58,  # 0-100 scale
            "volatility_trend": "decreasing",
            "investor_positioning": {"bullish": 42, "neutral": 38, "bearish": 20},
            "sentiment_drivers": [
                "Economic resilience",
                "Corporate earnings stability",
                "Geopolitical uncertainty",
                "Monetary policy expectations",
            ],
            "market_themes": [
                "AI and Technology Innovation",
                "Energy Transition",
                "Infrastructure Investment",
                "Healthcare Innovation",
            ],
        }

    def _identify_opportunities(self):
        """Identify potential investment opportunities"""
        opportunities = [
            {
                "category": "Technology",
                "theme": "Artificial Intelligence",
                "description": "AI adoption accelerating across industries",
                "risk_level": "Medium-High",
                "time_horizon": "1-3 years",
                "key_beneficiaries": [
                    "Cloud providers",
                    "Semiconductor companies",
                    "AI software",
                ],
            },
            {
                "category": "Healthcare",
                "theme": "Aging Demographics",
                "description": "Growing healthcare needs from aging population",
                "risk_level": "Medium",
                "time_horizon": "3-5 years",
                "key_beneficiaries": [
                    "Medical devices",
                    "Pharmaceuticals",
                    "Healthcare services",
                ],
            },
            {
                "category": "Energy",
                "theme": "Renewable Transition",
                "description": "Shift toward clean energy accelerating",
                "risk_level": "Medium-High",
                "time_horizon": "2-5 years",
                "key_beneficiaries": [
                    "Solar/wind",
                    "Battery storage",
                    "Grid infrastructure",
                ],
            },
            {
                "category": "Infrastructure",
                "theme": "Digital Infrastructure",
                "description": "5G, data centers, and connectivity expansion",
                "risk_level": "Medium",
                "time_horizon": "2-4 years",
                "key_beneficiaries": [
                    "Data centers",
                    "Telecom",
                    "Infrastructure REITs",
                ],
            },
        ]

        return opportunities

    def _generate_risk_alerts(self):
        """Generate market risk alerts"""
        alerts = [
            {
                "type": "Geopolitical Risk",
                "severity": "Medium",
                "description": "Ongoing geopolitical tensions may impact global trade",
                "affected_sectors": ["Energy", "Technology", "Materials"],
                "timeframe": "Near-term",
            },
            {
                "type": "Interest Rate Risk",
                "severity": "Low-Medium",
                "description": "Potential policy changes could affect rate-sensitive sectors",
                "affected_sectors": ["Real Estate", "Utilities", "Financial Services"],
                "timeframe": "3-6 months",
            },
            {
                "type": "Inflation Risk",
                "severity": "Low",
                "description": "Inflation trending down but remains above target",
                "affected_sectors": ["Consumer goods", "Energy", "Materials"],
                "timeframe": "6-12 months",
            },
        ]

        return alerts

    def _generate_market_forecast(self):
        """Generate market forecast"""
        return {
            "short_term_outlook": {
                "timeframe": "1-3 months",
                "direction": "Neutral to Positive",
                "key_factors": [
                    "Corporate earnings season",
                    "Economic data releases",
                    "Central bank communications",
                ],
                "expected_volatility": "Moderate",
            },
            "medium_term_outlook": {
                "timeframe": "3-12 months",
                "direction": "Cautiously Optimistic",
                "key_factors": [
                    "Economic resilience",
                    "Technology innovation",
                    "Policy normalization",
                ],
                "expected_volatility": "Moderate to Low",
            },
            "key_scenarios": [
                {
                    "name": "Base Case (60% probability)",
                    "description": "Continued economic growth with manageable inflation",
                    "market_impact": "Positive for risk assets",
                },
                {
                    "name": "Bull Case (25% probability)",
                    "description": "Stronger growth and rapid productivity gains from AI",
                    "market_impact": "Strong performance, led by technology",
                },
                {
                    "name": "Bear Case (15% probability)",
                    "description": "Economic slowdown or geopolitical shock",
                    "market_impact": "Flight to quality, defensive sectors outperform",
                },
            ],
            "asset_class_preferences": {
                "equities": "Overweight",
                "bonds": "Neutral",
                "commodities": "Underweight",
                "cash": "Underweight",
                "alternatives": "Neutral",
            },
        }
