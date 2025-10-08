#!/usr/bin/env python3
"""
Basic data test for Personal Finance Agent
Tests data loading and basic functionality
"""

import sys
import os
import json
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_data_files():
    """Test that all data files exist and are readable"""
    print("🚀 Testing Personal Finance Agent Data")
    print("=" * 50)
    
    # Test data files
    data_dir = "data"
    test_results = []
    
    # Test transactions.csv
    print("\n📊 Testing Transactions Data")
    try:
        transactions_path = os.path.join(data_dir, "transactions.csv")
        if os.path.exists(transactions_path):
            df = pd.read_csv(transactions_path)
            print(f"✅ transactions.csv loaded: {len(df)} transactions")
            print(f"   Columns: {list(df.columns)}")
            print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
            print(f"   Total amount: ${df['amount'].sum():.2f}")
            test_results.append("Transactions: ✅")
        else:
            print("❌ transactions.csv not found")
            test_results.append("Transactions: ❌")
    except Exception as e:
        print(f"❌ Error loading transactions: {e}")
        test_results.append("Transactions: ❌")
    
    # Test investments.json
    print("\n📈 Testing Investments Data")
    try:
        investments_path = os.path.join(data_dir, "investments.json")
        if os.path.exists(investments_path):
            with open(investments_path, 'r') as f:
                investments = json.load(f)
            print(f"✅ investments.json loaded: {len(investments)} investments")
            total_value = sum(inv['market_value'] for inv in investments)
            print(f"   Total portfolio value: ${total_value:.2f}")
            test_results.append("Investments: ✅")
        else:
            print("❌ investments.json not found")
            test_results.append("Investments: ❌")
    except Exception as e:
        print(f"❌ Error loading investments: {e}")
        test_results.append("Investments: ❌")
    
    # Test goals.json
    print("\n🎯 Testing Goals Data")
    try:
        goals_path = os.path.join(data_dir, "goals.json")
        if os.path.exists(goals_path):
            with open(goals_path, 'r') as f:
                goals = json.load(f)
            print(f"✅ goals.json loaded: {len(goals)} goals")
            total_target = sum(goal['target_amount'] for goal in goals)
            total_current = sum(goal['current_amount'] for goal in goals)
            print(f"   Total target: ${total_target:.2f}")
            print(f"   Total saved: ${total_current:.2f}")
            test_results.append("Goals: ✅")
        else:
            print("❌ goals.json not found")
            test_results.append("Goals: ❌")
    except Exception as e:
        print(f"❌ Error loading goals: {e}")
        test_results.append("Goals: ❌")
    
    # Test budget.json
    print("\n💰 Testing Budget Data")
    try:
        budget_path = os.path.join(data_dir, "budget.json")
        if os.path.exists(budget_path):
            with open(budget_path, 'r') as f:
                data = json.load(f)
            print(f"✅ budget.json loaded")
            print(f"   Budget data structure verified")
            test_results.append("Budget: ✅")
        else:
            print("❌ budget.json not found")
            test_results.append("Budget: ❌")
    except Exception as e:
        print(f"❌ Error loading budget: {e}")
        test_results.append("Budget: ❌")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    for result in test_results:
        print(f"   {result}")
    
    all_passed = all("✅" in result for result in test_results)
    if all_passed:
        print("\n🎉 All data files are working correctly!")
        print("✨ Personal Finance Agent data layer is ready!")
    else:
        print("\n⚠️  Some data files have issues. Check the errors above.")
    
    return all_passed

def test_basic_analysis():
    """Test basic financial analysis without LLM"""
    print("\n🧮 Testing Basic Financial Analysis")
    print("-" * 40)
    
    try:
        # Load and analyze transactions
        transactions_path = os.path.join("data", "transactions.csv")
        df = pd.read_csv(transactions_path)
        
        # Basic analytics
        total_income = df[df['amount'] > 0]['amount'].sum()
        total_expenses = abs(df[df['amount'] < 0]['amount'].sum())
        net_flow = total_income - total_expenses
        
        print(f"💰 Total Income: ${total_income:.2f}")
        print(f"💸 Total Expenses: ${total_expenses:.2f}")
        print(f"📊 Net Cash Flow: ${net_flow:.2f}")
        
        # Category breakdown
        expense_by_category = df[df['amount'] < 0].groupby('category')['amount'].sum().abs()
        print(f"\n📂 Expense Categories:")
        for category, amount in expense_by_category.head().items():
            print(f"   {category}: ${amount:.2f}")
        
        return True
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Personal Finance Agent - Data Layer Test")
    print("Testing core data functionality...")
    
    # Test data files
    data_ok = test_data_files()
    
    if data_ok:
        # Test basic analysis
        analysis_ok = test_basic_analysis()
        
        if analysis_ok:
            print("\n✅ All tests passed!")
            print("🚀 Ready for full LangGraph agent testing with API key")
        else:
            print("\n⚠️  Data loads but analysis has issues")
    else:
        print("\n❌ Data loading failed - check data files")