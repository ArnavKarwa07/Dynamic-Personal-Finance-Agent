"""
Simple test script to verify backend functionality
"""

import sys
import os

sys.path.append(os.path.dirname(__file__))

from agents.finance_agent import create_finance_agent
from tools.data_loader import DataLoader


def test_data_loader():
    """Test data loading functionality"""
    print("Testing data loader...")
    loader = DataLoader()

    # Test loading transactions
    transactions = loader.load_transactions()
    print(f"✓ Loaded {len(transactions)} transactions")

    # Test loading investments
    investments = loader.load_investments()
    print(f"✓ Loaded {len(investments)} investments")

    # Test loading goals
    goals = loader.load_goals()
    print(f"✓ Loaded {len(goals)} goals")

    # Test loading budget
    budget = loader.load_budget()
    print(
        f"✓ Loaded budget data with {len(budget.get('monthly_budgets', {}))} monthly budgets"
    )

    return True


def test_finance_agent():
    """Test finance agent creation and basic functionality"""
    print("\nTesting finance agent...")

    try:
        # Create agent
        agent = create_finance_agent()
        print("✓ Finance agent created successfully")

        # Test basic query (synchronous version)
        print("Testing sample query...")
        result = agent.process_query_sync("How much did I spend on food this month?")

        print(f"✓ Query processed successfully")
        print(f"  Response: {result['response'][:100]}...")
        print(f"  Intent: {result['intent']}")
        print(f"  Tools used: {result['tools_used']}")

        return True

    except Exception as e:
        print(f"✗ Error testing finance agent: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Testing Backend Functionality\n")

    try:
        # Test data loading
        if not test_data_loader():
            print("❌ Data loader tests failed")
            return False

        # Test finance agent
        if not test_finance_agent():
            print("❌ Finance agent tests failed")
            return False

        print("\n✅ All backend tests passed!")
        print("Backend is ready for frontend integration.")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    main()
