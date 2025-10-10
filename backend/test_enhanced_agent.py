"""
Test script to verify the enhanced LangGraph agent functionality
"""

import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from agents.finance_agent import create_finance_agent
import json


def test_agent_capabilities():
    """Test the enhanced agent with various query types"""

    # Create the agent
    agent = create_finance_agent()

    # Test queries for different tools
    test_queries = [
        {
            "query": "Show me the agent workflow and architecture",
            "expected_tool": "graph_visualization",
        },
        {"query": "What are my financial risks?", "expected_tool": "risk_assessment"},
        {
            "query": "How is the market performing today?",
            "expected_tool": "market_intelligence",
        },
        {
            "query": "Create a comprehensive financial plan",
            "expected_tool": "advanced_financial_planner",
        },
        {
            "query": "How much did I spend on food?",
            "expected_tool": "transaction_analyzer",
        },
    ]

    print("🤖 Testing Enhanced LangGraph Finance Agent")
    print("=" * 50)

    for i, test in enumerate(test_queries, 1):
        print(f"\nTest {i}: {test['query']}")
        print("-" * 40)

        try:
            result = agent.process_query_sync(test["query"])

            print(f"✅ Intent: {result['intent']}")
            print(f"🔧 Tools Used: {', '.join(result['tools_used'])}")
            print(f"📊 Analysis Results: {len(result['analysis_results'])} modules")

            # Check if expected tool was used
            if test["expected_tool"] in result["tools_used"]:
                print(f"✅ Expected tool '{test['expected_tool']}' was used")
            else:
                print(
                    f"⚠️  Expected tool '{test['expected_tool']}' not found in: {result['tools_used']}"
                )

            # Show sample of response
            response_preview = (
                result["response"][:150] + "..."
                if len(result["response"]) > 150
                else result["response"]
            )
            print(f"💬 Response Preview: {response_preview}")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

    print("\n" + "=" * 50)
    print("🎯 Agent Workflow Visualization:")
    print(agent.get_workflow_visualization())


if __name__ == "__main__":
    test_agent_capabilities()
