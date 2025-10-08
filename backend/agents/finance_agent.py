from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from agents.nodes import (
    FinanceAgentState, 
    UserInputNode, 
    IntentClassifierNode, 
    ContextRetrieverNode, 
    ResponseSynthesizerNode,
    route_by_intent,
    should_continue
)
from tools.transaction_analyzer import TransactionAnalyzerTool
from tools.budget_manager import BudgetManagerTool
from tools.investment_analyzer import InvestmentAnalyzerTool
from tools.goal_tracker import GoalTrackerTool
from tools.financial_insights import FinancialInsightsTool

class FinanceAgent:
    """Main LangGraph-based Personal Finance Agent"""
    
    def __init__(self):
        self.setup_tools()
        self.setup_graph()
    
    def setup_tools(self):
        """Initialize all financial analysis tools"""
        self.transaction_analyzer = TransactionAnalyzerTool()
        self.budget_manager = BudgetManagerTool()
        self.investment_analyzer = InvestmentAnalyzerTool()
        self.goal_tracker = GoalTrackerTool()
        self.financial_insights = FinancialInsightsTool()
    
    def setup_graph(self):
        """Setup the LangGraph workflow"""
        # Initialize nodes
        self.user_input_node = UserInputNode()
        self.intent_classifier_node = IntentClassifierNode()
        self.context_retriever_node = ContextRetrieverNode()
        self.response_synthesizer_node = ResponseSynthesizerNode()
        
        # Create the state graph
        workflow = StateGraph(FinanceAgentState)
        
        # Add nodes to the graph
        workflow.add_node("user_input", self.user_input_node)
        workflow.add_node("intent_classifier", self.intent_classifier_node)
        workflow.add_node("context_retriever", self.context_retriever_node)
        workflow.add_node("transaction_analyzer", self.transaction_analyzer)
        workflow.add_node("budget_manager", self.budget_manager)
        workflow.add_node("investment_analyzer", self.investment_analyzer)
        workflow.add_node("goal_tracker", self.goal_tracker)
        workflow.add_node("financial_insights", self.financial_insights)
        workflow.add_node("response_synthesizer", self.response_synthesizer_node)
        
        # Define the workflow edges
        workflow.set_entry_point("user_input")
        
        # Sequential flow through core processing
        workflow.add_edge("user_input", "intent_classifier")
        workflow.add_edge("intent_classifier", "context_retriever")
        
        # Conditional routing based on intent
        workflow.add_conditional_edges(
            "context_retriever",
            route_by_intent,
            {
                "transaction_analyzer": "transaction_analyzer",
                "budget_manager": "budget_manager",
                "investment_analyzer": "investment_analyzer", 
                "goal_tracker": "goal_tracker",
                "financial_insights": "financial_insights",
                "response_synthesizer": "response_synthesizer"
            }
        )
        
        # All tools route to response synthesizer
        workflow.add_edge("transaction_analyzer", "response_synthesizer")
        workflow.add_edge("budget_manager", "response_synthesizer")
        workflow.add_edge("investment_analyzer", "response_synthesizer")
        workflow.add_edge("goal_tracker", "response_synthesizer")
        workflow.add_edge("financial_insights", "response_synthesizer")
        
        # Response synthesizer ends the workflow
        workflow.add_edge("response_synthesizer", END)
        
        # Compile the graph
        self.app = workflow.compile()
    
    async def process_query(self, user_query: str, conversation_history: list = None) -> dict:
        """Process a user financial query through the LangGraph workflow"""
        
        # Initialize state
        initial_state = FinanceAgentState(
            messages=conversation_history or [],
            user_query=user_query,
            intent="",
            context={},
            tools_used=[],
            analysis_results={},
            response=""
        )
        
        # Add user message to conversation
        initial_state["messages"].append(HumanMessage(content=user_query))
        
        try:
            # Run the workflow
            final_state = await self.app.ainvoke(initial_state)
            
            return {
                "response": final_state.get("response", "I'm sorry, I couldn't process your request."),
                "intent": final_state.get("intent", ""),
                "tools_used": final_state.get("tools_used", []),
                "analysis_results": final_state.get("analysis_results", {}),
                "conversation_history": final_state.get("messages", [])
            }
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                "response": f"I encountered an error processing your request: {str(e)}",
                "intent": "ERROR", 
                "tools_used": [],
                "analysis_results": {},
                "conversation_history": initial_state["messages"]
            }
    
    def process_query_sync(self, user_query: str, conversation_history: list = None) -> dict:
        """Synchronous version of process_query"""
        
        # Initialize state
        initial_state = FinanceAgentState(
            messages=conversation_history or [],
            user_query=user_query,
            intent="",
            context={},
            tools_used=[],
            analysis_results={},
            response=""
        )
        
        # Add user message to conversation
        initial_state["messages"].append(HumanMessage(content=user_query))
        
        try:
            # Run the workflow synchronously
            final_state = self.app.invoke(initial_state)
            
            return {
                "response": final_state.get("response", "I'm sorry, I couldn't process your request."),
                "intent": final_state.get("intent", ""),
                "tools_used": final_state.get("tools_used", []),
                "analysis_results": final_state.get("analysis_results", {}),
                "conversation_history": final_state.get("messages", [])
            }
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                "response": f"I encountered an error processing your request: {str(e)}",
                "intent": "ERROR",
                "tools_used": [],
                "analysis_results": {},
                "conversation_history": initial_state["messages"]
            }
    
    def get_workflow_visualization(self) -> str:
        """Get a text representation of the workflow"""
        return """
        Personal Finance Agent Workflow:
        
        1. User Input Node
           ↓
        2. Intent Classifier Node (LLM-based)
           ↓
        3. Context Retriever Node
           ↓
        4. Route by Intent:
           ├── EXPENSE_TRACKING → Transaction Analyzer Tool
           ├── BUDGET_ANALYSIS → Budget Manager Tool
           ├── INVESTMENT_INQUIRY → Investment Analyzer Tool
           ├── GOAL_TRACKING → Goal Tracker Tool
           ├── FINANCIAL_INSIGHTS → Financial Insights Tool
           └── GENERAL_INQUIRY → Response Synthesizer
           ↓
        5. Response Synthesizer Node (LLM-based)
           ↓
        6. END
        
        Tools Available:
        - Transaction Analyzer: Analyzes spending patterns, categories, merchant data
        - Budget Manager: Tracks budget performance, overspending, remaining amounts
        - Investment Analyzer: Portfolio performance, gains/losses, allocation
        - Goal Tracker: Progress toward financial goals, timeline analysis
        - Financial Insights: Comprehensive reports, health scores, recommendations
        """

# Factory function to create the agent
def create_finance_agent() -> FinanceAgent:
    """Create and return a configured finance agent"""
    return FinanceAgent()