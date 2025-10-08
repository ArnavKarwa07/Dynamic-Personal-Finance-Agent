"""
Test script to verify the finance agent functionality
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from agents.finance_agent import create_finance_agent

def test_finance_agent():
    """Test the finance agent with various queries"""
    
    # Create the agent
    print("🤖 Creating Personal Finance Agent...")
    agent = create_finance_agent()
    print("✅ Agent created successfully!")
    
    # Test queries
    test_queries = [
        "How much did I spend on food this month?",
        "Am I over budget?", 
        "How are my investments performing?",
        "How close am I to my emergency fund goal?",
        "Give me a financial summary"
    ]
    
    print("\n🧪 Testing Finance Agent with various queries...\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"{'='*60}")
        print(f"Test {i}: {query}")
        print(f"{'='*60}")
        
        try:
            result = agent.process_query_sync(query)
            
            print(f"Intent: {result['intent']}")
            print(f"Tools Used: {', '.join(result['tools_used'])}")
            print(f"Response: {result['response']}")
            
            if result['analysis_results']:
                print(f"Analysis Available: {list(result['analysis_results'].keys())}")
            
            print("✅ Query processed successfully!\n")
            
        except Exception as e:
            print(f"❌ Error processing query: {e}\n")
    
    print("🎉 Finance Agent testing completed!")

if __name__ == "__main__":
    test_finance_agent()