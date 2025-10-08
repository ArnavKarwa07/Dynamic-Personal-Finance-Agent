from datetime import datetime
from typing import Dict, List, Any, Optional
import yfinance as yf
from agents.nodes import FinanceAgentState
from tools.data_loader import DataLoader

class InvestmentAnalyzerTool:
    """Analyzes investment portfolio and market data"""
    
    def __init__(self):
        self.data_loader = DataLoader()
    
    def __call__(self, state: FinanceAgentState) -> FinanceAgentState:
        """Main entry point for investment analysis"""
        investments = state.get("context", {}).get("investments")
        
        if not investments:
            state["analysis_results"]["investment_analyzer"] = {
                "error": "No investment data available"
            }
            return state
        
        query = state.get("user_query", "").lower()
        
        if any(word in query for word in ["performance", "how are", "doing"]):
            analysis = self._analyze_portfolio_performance(investments)
        elif any(word in query for word in ["gains", "losses", "profit"]):
            analysis = self._analyze_gains_losses(investments)
        elif any(word in query for word in ["diversification", "allocation", "breakdown"]):
            analysis = self._analyze_portfolio_allocation(investments)
        elif any(word in query for word in ["best", "worst", "top", "bottom"]):
            analysis = self._analyze_best_worst_performers(investments)
        else:
            analysis = self._analyze_portfolio_summary(investments)
        
        state["analysis_results"]["investment_analyzer"] = analysis
        state["tools_used"].append("investment_analyzer")
        return state
    
    def _analyze_portfolio_performance(self, investments: List[Dict]) -> Dict[str, Any]:
        """Comprehensive portfolio performance analysis"""
        total_market_value = sum(inv.get("market_value", 0) for inv in investments)
        total_cost = sum(inv.get("total_cost", 0) for inv in investments)
        total_gain_loss = total_market_value - total_cost
        overall_return = (total_gain_loss / total_cost * 100) if total_cost > 0 else 0
        
        # Performance by holding
        performance_details = []
        for inv in investments:
            performance_details.append({
                "symbol": inv.get("symbol", ""),
                "company": inv.get("company", ""),
                "market_value": inv.get("market_value", 0),
                "cost_basis": inv.get("total_cost", 0),
                "gain_loss": inv.get("unrealized_gain_loss", 0),
                "return_percentage": inv.get("percentage_change", 0),
                "current_price": inv.get("current_price", 0),
                "shares": inv.get("shares", 0)
            })
        
        # Sort by return percentage
        performance_details.sort(key=lambda x: x["return_percentage"], reverse=True)
        
        # Market data enhancement (get current market info)
        enhanced_performance = self._enhance_with_market_data(performance_details)
        
        return {
            "analysis_type": "Portfolio Performance",
            "portfolio_summary": {
                "total_market_value": round(total_market_value, 2),
                "total_cost_basis": round(total_cost, 2),
                "total_gain_loss": round(total_gain_loss, 2),
                "overall_return_percentage": round(overall_return, 2),
                "number_of_holdings": len(investments)
            },
            "individual_performance": enhanced_performance,
            "best_performer": enhanced_performance[0] if enhanced_performance else None,
            "worst_performer": enhanced_performance[-1] if enhanced_performance else None,
            "analysis_date": datetime.now().isoformat()
        }
    
    def _analyze_gains_losses(self, investments: List[Dict]) -> Dict[str, Any]:
        """Focus on gains and losses analysis"""
        winners = []
        losers = []
        
        for inv in investments:
            gain_loss = inv.get("unrealized_gain_loss", 0)
            position_data = {
                "symbol": inv.get("symbol", ""),
                "company": inv.get("company", ""),
                "gain_loss": gain_loss,
                "percentage_change": inv.get("percentage_change", 0),
                "market_value": inv.get("market_value", 0)
            }
            
            if gain_loss >= 0:
                winners.append(position_data)
            else:
                losers.append(position_data)
        
        # Sort winners by gain (descending) and losers by loss (ascending, most loss first)
        winners.sort(key=lambda x: x["gain_loss"], reverse=True)
        losers.sort(key=lambda x: x["gain_loss"])
        
        total_gains = sum(w["gain_loss"] for w in winners)
        total_losses = sum(abs(l["gain_loss"]) for l in losers)
        
        return {
            "analysis_type": "Gains & Losses",
            "summary": {
                "total_unrealized_gains": round(total_gains, 2),
                "total_unrealized_losses": round(total_losses, 2),
                "net_unrealized": round(total_gains - total_losses, 2),
                "winning_positions": len(winners),
                "losing_positions": len(losers),
                "win_rate": round((len(winners) / len(investments)) * 100, 1) if investments else 0
            },
            "winners": winners,
            "losers": losers,
            "biggest_winner": winners[0] if winners else None,
            "biggest_loser": losers[0] if losers else None
        }
    
    def _analyze_portfolio_allocation(self, investments: List[Dict]) -> Dict[str, Any]:
        """Analyze portfolio allocation and diversification"""
        total_value = sum(inv.get("market_value", 0) for inv in investments)
        
        # Calculate allocation percentages
        allocations = []
        for inv in investments:
            market_value = inv.get("market_value", 0)
            allocation_percentage = (market_value / total_value * 100) if total_value > 0 else 0
            
            allocations.append({
                "symbol": inv.get("symbol", ""),
                "company": inv.get("company", ""),
                "market_value": market_value,
                "allocation_percentage": round(allocation_percentage, 2),
                "shares": inv.get("shares", 0)
            })
        
        # Sort by allocation percentage
        allocations.sort(key=lambda x: x["allocation_percentage"], reverse=True)
        
        # Diversification analysis
        largest_position = max(allocations, key=lambda x: x["allocation_percentage"]) if allocations else None
        concentration_risk = largest_position["allocation_percentage"] if largest_position else 0
        
        # Simple sector analysis (based on known companies)
        sector_mapping = {
            "AAPL": "Technology",
            "GOOGL": "Technology", 
            "MSFT": "Technology",
            "TSLA": "Automotive/Technology",
            "SPY": "Diversified ETF"
        }
        
        sector_allocation = {}
        for alloc in allocations:
            sector = sector_mapping.get(alloc["symbol"], "Other")
            if sector not in sector_allocation:
                sector_allocation[sector] = 0
            sector_allocation[sector] += alloc["allocation_percentage"]
        
        return {
            "analysis_type": "Portfolio Allocation",
            "total_portfolio_value": round(total_value, 2),
            "individual_allocations": allocations,
            "sector_breakdown": {k: round(v, 2) for k, v in sector_allocation.items()},
            "diversification_metrics": {
                "number_of_positions": len(allocations),
                "largest_position_percentage": round(concentration_risk, 2),
                "concentration_risk": "High" if concentration_risk > 25 else "Medium" if concentration_risk > 15 else "Low",
                "top_3_concentration": round(sum(a["allocation_percentage"] for a in allocations[:3]), 2)
            },
            "recommendations": self._generate_allocation_recommendations(allocations, concentration_risk)
        }
    
    def _analyze_best_worst_performers(self, investments: List[Dict]) -> Dict[str, Any]:
        """Identify best and worst performing investments"""
        sorted_by_performance = sorted(
            investments, 
            key=lambda x: x.get("percentage_change", 0), 
            reverse=True
        )
        
        best_performers = sorted_by_performance[:3]
        worst_performers = sorted_by_performance[-3:]
        
        return {
            "analysis_type": "Best & Worst Performers",
            "best_performers": [
                {
                    "symbol": inv.get("symbol", ""),
                    "company": inv.get("company", ""),
                    "return_percentage": inv.get("percentage_change", 0),
                    "gain_loss": inv.get("unrealized_gain_loss", 0),
                    "market_value": inv.get("market_value", 0)
                }
                for inv in best_performers
            ],
            "worst_performers": [
                {
                    "symbol": inv.get("symbol", ""),
                    "company": inv.get("company", ""),
                    "return_percentage": inv.get("percentage_change", 0),
                    "gain_loss": inv.get("unrealized_gain_loss", 0),
                    "market_value": inv.get("market_value", 0)
                }
                for inv in worst_performers
            ],
            "performance_spread": round(
                sorted_by_performance[0].get("percentage_change", 0) - 
                sorted_by_performance[-1].get("percentage_change", 0), 2
            )
        }
    
    def _analyze_portfolio_summary(self, investments: List[Dict]) -> Dict[str, Any]:
        """General portfolio overview"""
        total_market_value = sum(inv.get("market_value", 0) for inv in investments)
        total_cost = sum(inv.get("total_cost", 0) for inv in investments)
        total_gain_loss = sum(inv.get("unrealized_gain_loss", 0) for inv in investments)
        
        positive_positions = sum(1 for inv in investments if inv.get("unrealized_gain_loss", 0) >= 0)
        
        return {
            "analysis_type": "Portfolio Summary",
            "portfolio_overview": {
                "total_positions": len(investments),
                "total_market_value": round(total_market_value, 2),
                "total_cost_basis": round(total_cost, 2),
                "total_unrealized_gain_loss": round(total_gain_loss, 2),
                "overall_return_percentage": round((total_gain_loss / total_cost * 100), 2) if total_cost > 0 else 0,
                "winning_positions": positive_positions,
                "losing_positions": len(investments) - positive_positions
            },
            "top_holdings": sorted(
                [
                    {
                        "symbol": inv.get("symbol", ""),
                        "company": inv.get("company", ""),
                        "market_value": inv.get("market_value", 0),
                        "percentage_of_portfolio": round((inv.get("market_value", 0) / total_market_value * 100), 2) if total_market_value > 0 else 0
                    }
                    for inv in investments
                ],
                key=lambda x: x["market_value"],
                reverse=True
            )[:3],
            "last_updated": datetime.now().isoformat()
        }
    
    def _enhance_with_market_data(self, performance_details: List[Dict]) -> List[Dict]:
        """Enhance performance data with real-time market information"""
        # Note: In a production environment, you'd want to cache this data
        # and implement rate limiting for API calls
        
        enhanced = []
        for detail in performance_details:
            symbol = detail.get("symbol", "")
            enhanced_detail = detail.copy()
            
            try:
                # Get real-time data from yfinance
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                # Add additional market metrics
                enhanced_detail.update({
                    "market_cap": info.get("marketCap", "N/A"),
                    "pe_ratio": info.get("trailingPE", "N/A"),
                    "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
                    "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
                    "volume": info.get("volume", "N/A"),
                    "sector": info.get("sector", "N/A")
                })
                
            except Exception as e:
                # If real-time data fails, continue with existing data
                print(f"Could not fetch real-time data for {symbol}: {e}")
            
            enhanced.append(enhanced_detail)
        
        return enhanced
    
    def _generate_allocation_recommendations(self, allocations: List[Dict], concentration_risk: float) -> List[str]:
        """Generate portfolio allocation recommendations"""
        recommendations = []
        
        if concentration_risk > 25:
            recommendations.append(
                f"Your largest position represents {concentration_risk:.1f}% of your portfolio. "
                "Consider reducing concentration risk by diversifying."
            )
        
        if len(allocations) < 5:
            recommendations.append(
                "Consider adding more positions to improve diversification."
            )
        
        # Check for sector concentration
        tech_allocation = sum(
            alloc["allocation_percentage"] 
            for alloc in allocations 
            if alloc["symbol"] in ["AAPL", "GOOGL", "MSFT"]
        )
        
        if tech_allocation > 50:
            recommendations.append(
                f"You have {tech_allocation:.1f}% in technology stocks. "
                "Consider diversifying across other sectors."
            )
        
        if not recommendations:
            recommendations.append("Your portfolio allocation looks well balanced.")
        
        return recommendations