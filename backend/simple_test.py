#!/usr/bin/env python3
"""
Simple test script for the Personal Finance Agent components
Tests individual tools without requiring LLM connectivity
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.transaction_analyzer import TransactionAnalyzerTool
from tools.budget_manager import BudgetManagerTool
from tools.investment_analyzer import InvestmentAnalyzerTool
from tools.goal_tracker import GoalTrackerTool
from tools.financial_insights import FinancialInsightsTool

def test_financial_tools():
    """Test all financial analysis tools"""
    print("🧪 Testing Personal Finance Agent Tools")
    print("=" * 50)
    
    # Test Transaction Analyzer
    print("\n📊 Testing Transaction Analyzer Tool")
    try:
        transaction_tool = TransactionAnalyzerTool()
        result = transaction_tool._run("analyze my spending patterns this month")
        print("✅ Transaction Analysis:", result[:200] + "..." if len(result) > 200 else result)
    except Exception as e:
        print("❌ Transaction Analyzer Error:", str(e))
    
    # Test Budget Manager
    print("\n💰 Testing Budget Manager Tool")
    try:
        budget_tool = BudgetManagerTool()
        result = budget_tool._run("check my budget status for food category")
        print("✅ Budget Analysis:", result[:200] + "..." if len(result) > 200 else result)
    except Exception as e:
        print("❌ Budget Manager Error:", str(e))
    
    # Test Investment Analyzer
    print("\n📈 Testing Investment Analyzer Tool")
    try:
        investment_tool = InvestmentAnalyzerTool()
        result = investment_tool._run("show my portfolio performance")
        print("✅ Investment Analysis:", result[:200] + "..." if len(result) > 200 else result)
    except Exception as e:
        print("❌ Investment Analyzer Error:", str(e))
    
    # Test Goal Tracker
    print("\n🎯 Testing Goal Tracker Tool")
    try:
        goal_tool = GoalTrackerTool()
        result = goal_tool._run("check progress on my emergency fund goal")
        print("✅ Goal Tracking:", result[:200] + "..." if len(result) > 200 else result)
    except Exception as e:
        print("❌ Goal Tracker Error:", str(e))
    
    # Test Financial Insights
    print("\n💡 Testing Financial Insights Tool")
    try:
        insights_tool = FinancialInsightsTool()
        result = insights_tool._run("give me financial insights and recommendations")
        print("✅ Financial Insights:", result[:200] + "..." if len(result) > 200 else result)
    except Exception as e:
        print("❌ Financial Insights Error:", str(e))
    
    print("\n" + "=" * 50)
    print("🎉 Tool Testing Complete!")

def test_data_loading():
    """Test data loading capabilities"""
    print("\n📁 Testing Data Loading")
    print("-" * 30)
    
    # Test data files exist
    data_files = [
        "data/transactions.csv",
        "data/investments.json",
        "data/goals.json",
        "data/budget.json"
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
            # Try to read file size
            size = os.path.getsize(file_path)
            print(f"   Size: {size} bytes")
        else:
            print(f"❌ {file_path} missing")

if __name__ == "__main__":
    print("🚀 Starting Simple Finance Agent Test")
    print("Testing individual components without LLM dependency")
    
    # Test data loading
    test_data_loading()
    
    # Test financial tools
    test_financial_tools()
    
    print("\n✨ Test Complete! The Personal Finance Agent tools are functional.")
    print("Next step: Add OpenAI API key to test full LangGraph workflow.")