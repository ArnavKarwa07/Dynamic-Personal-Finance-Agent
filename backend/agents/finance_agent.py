from typing import Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from agents.nodes import (
    FinanceAgentState,
    UserInputNode,
    IntentClassifierNode,
    ContextRetrieverNode,
    ResponseSynthesizerNode,
    route_by_intent,
    should_continue,
)
from tools.transaction_analyzer import TransactionAnalyzerTool
from tools.budget_manager import BudgetManagerTool
from tools.investment_analyzer import InvestmentAnalyzerTool
from tools.goal_tracker import GoalTrackerTool
from tools.financial_insights import FinancialInsightsTool
from tools.advanced_financial_planner import AdvancedFinancialPlannerTool
from tools.risk_assessment import RiskAssessmentTool
from tools.market_intelligence import MarketIntelligenceTool
from tools.graph_visualization import GraphVisualizationTool


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
        self.advanced_financial_planner = AdvancedFinancialPlannerTool()
        self.risk_assessment = RiskAssessmentTool()
        self.market_intelligence = MarketIntelligenceTool()
        self.graph_visualization = GraphVisualizationTool()

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
        workflow.add_node("advanced_financial_planner", self.advanced_financial_planner)
        workflow.add_node("risk_assessment", self.risk_assessment)
        workflow.add_node("market_intelligence", self.market_intelligence)
        workflow.add_node("graph_visualization", self.graph_visualization)
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
                "advanced_financial_planner": "advanced_financial_planner",
                "risk_assessment": "risk_assessment",
                "market_intelligence": "market_intelligence",
                "graph_visualization": "graph_visualization",
                "response_synthesizer": "response_synthesizer",
            },
        )

        # All tools route to response synthesizer
        workflow.add_edge("transaction_analyzer", "response_synthesizer")
        workflow.add_edge("budget_manager", "response_synthesizer")
        workflow.add_edge("investment_analyzer", "response_synthesizer")
        workflow.add_edge("goal_tracker", "response_synthesizer")
        workflow.add_edge("financial_insights", "response_synthesizer")
        workflow.add_edge("advanced_financial_planner", "response_synthesizer")
        workflow.add_edge("risk_assessment", "response_synthesizer")
        workflow.add_edge("market_intelligence", "response_synthesizer")
        workflow.add_edge("graph_visualization", "response_synthesizer")

        # Response synthesizer ends the workflow
        workflow.add_edge("response_synthesizer", END)

        # Compile the graph
        self.app = workflow.compile()

    async def process_query(
        self, user_query: str, conversation_history: Optional[list] = None
    ) -> dict:
        """Process a user financial query through the LangGraph workflow"""

        # Initialize state
        initial_state = {
            "messages": conversation_history or [],
            "user_query": user_query,
            "intent": "",
            "context": {},
            "tools_used": [],
            "analysis_results": {},
            "response": "",
        }

        # Add user message to conversation
        initial_state["messages"].append(HumanMessage(content=user_query))

        try:
            # Run the workflow
            final_state = await self.app.ainvoke(initial_state)

            return {
                "response": final_state.get(
                    "response", "I'm sorry, I couldn't process your request."
                ),
                "intent": final_state.get("intent", ""),
                "tools_used": final_state.get("tools_used", []),
                "analysis_results": final_state.get("analysis_results", {}),
                "conversation_history": final_state.get("messages", []),
            }

        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                "response": f"I encountered an error processing your request: {str(e)}",
                "intent": "ERROR",
                "tools_used": [],
                "analysis_results": {},
                "conversation_history": initial_state["messages"],
            }

    def process_query_sync(
        self, user_query: str, conversation_history: Optional[list] = None
    ) -> dict:
        """Synchronous version of process_query"""

        # Initialize state
        initial_state = {
            "messages": conversation_history or [],
            "user_query": user_query,
            "intent": "",
            "context": {},
            "tools_used": [],
            "analysis_results": {},
            "response": "",
        }

        # Add user message to conversation
        initial_state["messages"].append(HumanMessage(content=user_query))

        try:
            # Run the workflow synchronously
            final_state = self.app.invoke(initial_state)

            return {
                "response": final_state.get(
                    "response", "I'm sorry, I couldn't process your request."
                ),
                "intent": final_state.get("intent", ""),
                "tools_used": final_state.get("tools_used", []),
                "analysis_results": final_state.get("analysis_results", {}),
                "conversation_history": final_state.get("messages", []),
            }

        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                "response": f"I encountered an error processing your request: {str(e)}",
                "intent": "ERROR",
                "tools_used": [],
                "analysis_results": {},
                "conversation_history": initial_state["messages"],
            }

    def get_workflow_visualization(self) -> str:
        """Get a text representation of the workflow"""
        return """
        🤖 Advanced Personal Finance Agent Workflow (LangGraph):
        
        ┌─────────────────┐
        │  User Input     │ ← Captures user query
        └─────────┬───────┘
                  │
        ┌─────────▼───────┐
        │ Intent Classifier│ ← LLM-based intent detection
        └─────────┬───────┘
                  │
        ┌─────────▼───────┐
        │Context Retriever│ ← Loads relevant financial data
        └─────────┬───────┘
                  │
        ┌─────────▼───────┐
        │  Route by Intent │ ← Smart routing based on keywords & intent
        └─────────┬───────┘
                  │
        ┌─────────▼───────┐
        │    Tool Layer   │
        ├─────────────────┤
        │ 📊 Transaction  │ ← Spending patterns & analysis
        │ 💰 Budget Mgmt  │ ← Budget tracking & alerts
        │ 📈 Investments  │ ← Portfolio performance
        │ 🎯 Goal Tracker │ ← Progress monitoring
        │ 🔍 Insights     │ ← Financial health reports
        │ 🧠 AI Planner   │ ← Strategic planning & optimization
        │ ⚠️  Risk Assess │ ← Risk analysis & mitigation
        │ 📰 Market Intel │ ← Market data & forecasts
        └─────────┬───────┘
                  │
        ┌─────────▼───────┐
        │Response Synth.  │ ← LLM generates natural language
        └─────────┬───────┘
                  │
        ┌─────────▼───────┐
        │      END        │
        └─────────────────┘
        
        🔧 Specialized Financial Tools:
        
        Core Analysis:
        • Transaction Analyzer: Spending patterns, categories, merchant insights
        • Budget Manager: Performance tracking, overspending alerts, remaining funds
        • Investment Analyzer: Portfolio performance, gains/losses, asset allocation
        • Goal Tracker: Progress monitoring, timeline analysis, milestone tracking
        • Financial Insights: Health scores, trends, basic recommendations
        
        Advanced Intelligence:
        • AI Financial Planner: Strategic planning, retirement readiness, optimization
        • Risk Assessment: Vulnerability analysis, stress testing, mitigation strategies
        • Market Intelligence: Real-time market data, sector analysis, economic forecasts
        
        🎯 Intelligent Routing:
        The system uses both intent classification and keyword analysis to route
        queries to the most appropriate specialized tool, ensuring comprehensive
        and accurate financial analysis.
        
        🔄 State Management:
        LangGraph maintains conversation state, tool usage tracking, and analysis
        results throughout the workflow for context-aware responses.
        """


# Factory function to create the agent
def create_finance_agent() -> FinanceAgent:
    """Create and return a configured finance agent"""
    return FinanceAgent()
