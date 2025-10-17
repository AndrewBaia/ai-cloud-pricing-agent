"""
Cloud Pricing Analysis Agent using Agno framework.
This agent can analyze cloud GPU pricing across multiple providers and provide recommendations.
"""
import os
from typing import Dict, List, Any, Optional
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.tools import Function
from loguru import logger

from ..tools.search_tool import MockSearchTool
from ..tools.vector_store import VectorStoreTool
from ..tools.external_api import ExternalAPITool


class CloudPricingAgent:
    """AI Agent specialized in cloud pricing analysis and recommendations."""

    def __init__(self,
                 model_name: str = "gpt-4",
                 chroma_db_path: str = "./data/chromadb",
                 external_api_url: str = "http://localhost:8001",
                 external_api_key: str = "demo_key"):

        self.model_name = model_name
        self.chroma_db_path = chroma_db_path

        # Initialize tools
        self.search_tool = MockSearchTool()
        self.vector_store = VectorStoreTool(chroma_db_path)
        self.external_api = ExternalAPITool(external_api_url, external_api_key)

        # Initialize the Agno agent
        self.agent = self._create_agent()

        logger.info(f"Cloud Pricing Agent initialized with model: {model_name}")

    def _create_agent(self) -> Agent:
        """Create and configure the Agno agent with tools."""

        # Determine model provider
        if "gpt" in self.model_name.lower():
            model = OpenAIChat(id=self.model_name)
        elif "claude" in self.model_name.lower():
            model = Claude(id=self.model_name)
        else:
            # Default to OpenAI GPT-4
            model = OpenAIChat(id="gpt-4")
            logger.warning(f"Unknown model {self.model_name}, defaulting to gpt-4")

        # Define tool functions for the agent
        search_gpu_pricing_tool = Function(
            fn=self.search_gpu_pricing,
            name="search_gpu_pricing",
            description="Search for GPU instance pricing across cloud providers. Use this to find current prices, instance types, and specifications."
        )

        compare_prices_tool = Function(
            fn=self.compare_cloud_prices,
            name="compare_cloud_prices",
            description="Compare prices between two cloud providers for specific instance types. Returns detailed comparison with recommendations."
        )

        get_market_trends_tool = Function(
            fn=self.get_market_trends,
            name="get_market_trends",
            description="Get current market trends and pricing analysis for cloud providers."
        )

        search_knowledge_base_tool = Function(
            fn=self.search_knowledge_base,
            name="search_knowledge_base",
            description="Search the knowledge base for cloud computing information, best practices, and cost optimization strategies."
        )

        # Create the agent
        agent = Agent(
            model=model,
            tools=[
                search_gpu_pricing_tool,
                compare_prices_tool,
                get_market_trends_tool,
                search_knowledge_base_tool
            ],
            instructions=self._get_agent_instructions()
        )

        return agent

    def _get_agent_instructions(self) -> str:
        """Get the system instructions for the agent."""
        return """
        You are an expert Cloud Pricing Analyst AI agent specializing in cloud computing costs and optimization.

        Your capabilities:
        1. Analyze GPU pricing across AWS, Azure, and GCP
        2. Compare pricing between different cloud providers
        3. Provide cost optimization recommendations
        4. Explain technical specifications of cloud instances
        5. Identify market trends and pricing patterns

        When analyzing queries:
        1. Always use the available tools to gather comprehensive data
        2. Provide structured, easy-to-understand responses
        3. Include specific numbers, comparisons, and recommendations
        4. Explain your reasoning step by step
        5. Suggest cost-saving strategies when applicable

        Response format:
        - Use clear sections with descriptive headers
        - Include tables for price comparisons
        - Provide actionable recommendations
        - Mention any assumptions or limitations

        Always aim to provide the most cost-effective solutions while considering performance requirements.
        """

    def search_gpu_pricing(self, provider: Optional[str] = None,
                          gpu_type: Optional[str] = None,
                          min_gpu_count: Optional[int] = None,
                          max_price: Optional[float] = None) -> str:
        """
        Search for GPU pricing information.

        Args:
            provider: Cloud provider filter (AWS, Azure, GCP)
            gpu_type: GPU type filter (V100, K80, etc.)
            min_gpu_count: Minimum GPU count
            max_price: Maximum hourly price

        Returns:
            Formatted string with pricing information
        """
        logger.info(f"Agent calling search_gpu_pricing: provider={provider}, gpu_type={gpu_type}")

        results = self.search_tool.search_gpu_pricing(
            provider=provider,
            gpu_type=gpu_type,
            min_gpu_count=min_gpu_count,
            max_price=max_price
        )

        if not results:
            return "No GPU instances found matching the specified criteria."

        # Format results as readable text
        response = f"Found {len(results)} GPU instances:\n\n"

        for result in results[:10]:  # Limit to top 10 results
            response += f"**{result['provider']} {result['instance_type']}**\n"
            response += f"- GPU: {result['gpu_type']} ({result['gpu_count']} GPUs)\n"
            response += f"- CPU: {result['vcpus']} vCPUs\n"
            response += f"- Memory: {result['memory_gb']} GB\n"
            response += f"- Price: ${result['price_per_hour']:.2f}/hour\n"
            response += f"- Region: {result['region']}\n\n"

        if len(results) > 10:
            response += f"... and {len(results) - 10} more results.\n"

        return response

    def compare_cloud_prices(self, provider1: str, provider2: str,
                           instance_type: str) -> str:
        """
        Compare prices between two cloud providers.

        Args:
            provider1: First cloud provider
            provider2: Second cloud provider
            instance_type: Instance type to compare

        Returns:
            Formatted comparison string
        """
        logger.info(f"Agent calling compare_prices: {provider1} vs {provider2} for {instance_type}")

        result = self.external_api.compare_prices(provider1, provider2, instance_type)

        if result.get("status") == "error":
            return f"Unable to compare prices: {result.get('comparison', {}).get('error', 'Unknown error')}"

        comparison = result.get("comparison", {})

        response = f"**Price Comparison: {provider1} vs {provider2} - {instance_type}**\n\n"

        p1_price = comparison.get(f"{provider1.lower()}_price")
        p2_price = comparison.get(f"{provider2.lower()}_price")

        if p1_price is not None and p2_price is not None:
            response += f"{provider1}: ${p1_price:.2f}/hour\n"
            response += f"{provider2}: ${p2_price:.2f}/hour\n\n"

            cheaper_provider = comparison.get("recommendation", provider1)
            savings = comparison.get("savings_percent", 0)

            response += f"**Recommendation: {cheaper_provider}**\n"
            if savings > 0:
                response += f"Potential savings: {savings:.1f}%\n"

        return response

    def get_market_trends(self, provider: Optional[str] = None) -> str:
        """
        Get market trends for cloud pricing.

        Args:
            provider: Optional provider filter

        Returns:
            Formatted trends string
        """
        logger.info(f"Agent calling get_market_trends: provider={provider}")

        result = self.external_api.get_market_trends(provider)

        if result.get("status") == "error":
            return f"Unable to fetch market trends: {result.get('market_trends', {}).get('error', 'Unknown error')}"

        if provider:
            # Single provider response
            trend_data = result
            response = f"**Market Trends for {provider}**\n\n"
            response += f"Trend: {trend_data.get('trend', 'unknown').replace('_', ' ').title()}\n"
            response += f"Price Change: {trend_data.get('change_percent', 0):.1f}%\n"
        else:
            # All providers response
            trends = result.get("market_trends", {})
            response = "**Cloud Market Trends**\n\n"
            response += f"Overall Trend: {trends.get('overall_trend', 'unknown').replace('_', ' ').title()}\n"
            response += f"Average Change: {trends.get('average_change_percent', 0):.1f}%\n\n"

            response += "**Provider Breakdown:**\n"
            for prov, data in trends.get("providers", {}).items():
                response += f"- {prov}: {data.get('trend', 'unknown').replace('_', ' ').title()} ({data.get('change_percent', 0):.1f}%)\n"

        return response

    def search_knowledge_base(self, query: str, n_results: int = 3) -> str:
        """
        Search the knowledge base for relevant information.

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            Formatted search results
        """
        logger.info(f"Agent calling search_knowledge_base: '{query}'")

        result = self.vector_store.search_similar(query, n_results)

        if not result.get("results", {}).get("documents"):
            return f"No relevant information found for: {query}"

        documents = result["results"]["documents"][0]
        metadatas = result["results"]["metadatas"][0]

        response = f"**Knowledge Base Results for: '{query}'**\n\n"

        for i, (doc, metadata) in enumerate(zip(documents, metadatas), 1):
            response += f"**Result {i}:**\n"
            response += f"{doc}\n"

            # Add relevant metadata
            if "provider" in metadata:
                response += f"*Provider: {metadata['provider']}*\n"
            if "use_case" in metadata:
                response += f"*Use Case: {metadata['use_case']}*\n"

            response += "\n"

        return response

    def analyze_query(self, user_query: str) -> str:
        """
        Main method to analyze user queries about cloud pricing.

        Args:
            user_query: User's question or request

        Returns:
            Agent's response with analysis and recommendations
        """
        logger.info(f"Processing user query: {user_query}")

        try:
            # Use Agno agent to process the query
            response = self.agent.run(user_query)

            # Extract the final answer
            if hasattr(response, 'content'):
                final_answer = response.content
            else:
                final_answer = str(response)

            logger.info("Query processed successfully")
            return final_answer

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return f"I apologize, but I encountered an error while processing your query: {str(e)}. Please try again."

    def get_agent_stats(self) -> Dict[str, Any]:
        """Get statistics about the agent and its tools."""
        return {
            "model": self.model_name,
            "vector_store_stats": self.vector_store.get_collection_stats(),
            "tools_available": [
                "search_gpu_pricing",
                "compare_cloud_prices",
                "get_market_trends",
                "search_knowledge_base"
            ]
        }
