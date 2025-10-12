"""
Direct Groq API integration for the Finance Agent
Clean implementation without HuggingFace dependencies
Async-compatible for LangGraph workflow
"""
import os
import json
import asyncio
import httpx
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass


@dataclass
class GroqResponse:
    """Response object from Groq API"""
    content: str
    role: str = "assistant"


class GroqClient:
    """Direct Groq API client without LangChain dependencies"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def chat(self, 
                   messages: Union[str, List[Dict[str, str]]], 
                   model: str = "llama3-8b-8192", 
                   temperature: float = 0.1) -> str:
        """Send chat request to Groq API (async)"""
        
        # Handle both string and message list inputs
        if isinstance(messages, str):
            formatted_messages = [{"role": "user", "content": messages}]
        else:
            formatted_messages = messages
        
        payload = {
            "messages": formatted_messages,
            "model": model,
            "temperature": temperature,
            "max_tokens": 1024,
            "top_p": 1,
            "stream": False
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                return content
                
        except httpx.RequestError as e:
            print(f"Groq API error: {e}")
            return "I'm sorry, I encountered an error processing your request."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "I'm sorry, I encountered an unexpected error."
    
    def chat_sync(self, 
                  messages: Union[str, List[Dict[str, str]]], 
                  model: str = "llama3-8b-8192", 
                  temperature: float = 0.1) -> str:
        """Send chat request to Groq API (synchronous)"""
        return asyncio.run(self.chat(messages, model, temperature))
    
    async def analyze_financial_query(self, user_query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze financial query and provide response (async)"""
        
        system_prompt = """You are an expert financial advisor AI assistant. You help users with:
- Budget analysis and spending recommendations
- Investment advice and portfolio optimization
- Financial goal planning and tracking
- Expense categorization and insights
- Risk assessment and financial health analysis
- Market analysis and economic insights
- Tax planning and optimization
- Retirement and estate planning

Provide clear, actionable financial advice based on the user's query. Be specific and practical in your recommendations."""

        # Build context string
        context_str = ""
        if context:
            context_str = f"\nUser Context: {json.dumps(context, indent=2)}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_query}{context_str}"}
        ]
        
        response = await self.chat(messages)
        
        # Simple intent classification based on keywords
        intent = self._classify_intent(user_query)
        
        return {
            "response": response,
            "intent": intent,
            "model_used": "groq-llama3-8b",
            "context_used": bool(context)
        }
    
    def analyze_financial_query_sync(self, user_query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze financial query and provide response (synchronous)"""
        return asyncio.run(self.analyze_financial_query(user_query, context))
    
    def _classify_intent(self, query: str) -> str:
        """Simple keyword-based intent classification"""
        query_lower = query.lower()
        
        # Budget and expense analysis
        if any(word in query_lower for word in ['budget', 'spending', 'expense', 'cost', 'allocat']):
            return "budget_analysis"
        
        # Investment and portfolio management
        elif any(word in query_lower for word in ['invest', 'portfolio', 'stock', 'bond', 'fund', 'asset', 'diversif']):
            return "investment_advice"
        
        # Goal setting and savings
        elif any(word in query_lower for word in ['goal', 'save', 'saving', 'target', 'plan', 'objective']):
            return "goal_planning"
        
        # Transaction analysis
        elif any(word in query_lower for word in ['transaction', 'payment', 'purchase', 'bill', 'receipt']):
            return "transaction_analysis"
        
        # Risk and insurance
        elif any(word in query_lower for word in ['risk', 'insurance', 'emergency', 'protect', 'coverage']):
            return "risk_assessment"
        
        # Market and economic analysis
        elif any(word in query_lower for word in ['market', 'economic', 'trend', 'forecast', 'outlook']):
            return "market_analysis"
        
        # Tax planning
        elif any(word in query_lower for word in ['tax', 'deduction', 'ira', 'retirement', '401k']):
            return "tax_planning"
        
        # Debt management
        elif any(word in query_lower for word in ['debt', 'loan', 'credit', 'mortgage', 'refinanc']):
            return "debt_management"
        
        else:
            return "general_inquiry"


# Create global instance
groq_client = GroqClient()