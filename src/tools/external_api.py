"""
Mock external API tool that simulates an external service for additional data.
"""
import requests
import json
import time
import random
from typing import Dict, Any, Optional
from loguru import logger
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class PriceComparisonRequest(BaseModel):
    provider1: str
    provider2: str
    instance_type: str


class MockExternalAPIServer:
    """Mock external API server for demonstration."""

    def __init__(self):
        self.app = FastAPI(title="Mock External API", version="1.0.0")
        self._setup_routes()

    def _setup_routes(self):
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "service": "mock_external_api"}

        @self.app.get("/providers")
        async def get_providers():
            """Get list of supported cloud providers."""
            return {
                "providers": ["AWS", "Azure", "GCP", "IBM", "Oracle"],
                "status": "success"
            }

        @self.app.post("/compare-prices")
        async def compare_prices(request: PriceComparisonRequest):
            """Compare prices between two providers for a specific instance type."""
            # Simulate processing time
            time.sleep(random.uniform(0.2, 0.8))

            provider1 = request.provider1.upper()
            provider2 = request.provider2.upper()
            instance_type = request.instance_type

            # Mock comparison data
            mock_comparisons = {
                ("AWS", "AZURE"): {
                    "p3.2xlarge": {
                        "aws_price": 3.06,
                        "azure_price": 2.80,
                        "recommendation": "Azure",
                        "savings_percent": 8.5
                    },
                    "p3.8xlarge": {
                        "aws_price": 12.24,
                        "azure_price": 11.20,
                        "recommendation": "Azure",
                        "savings_percent": 8.5
                    }
                },
                ("AWS", "GCP"): {
                    "p3.2xlarge": {
                        "aws_price": 3.06,
                        "gcp_price": 2.90,
                        "recommendation": "GCP",
                        "savings_percent": 5.2
                    }
                },
                ("AZURE", "GCP"): {
                    "NC6": {
                        "azure_price": 0.90,
                        "gcp_price": 0.70,
                        "recommendation": "GCP",
                        "savings_percent": 22.2
                    }
                }
            }

            key = (provider1, provider2)
            reverse_key = (provider2, provider1)

            if key in mock_comparisons and instance_type in mock_comparisons[key]:
                data = mock_comparisons[key][instance_type]
                return {
                    "comparison": {
                        "instance_type": instance_type,
                        f"{provider1.lower()}_price": data[f"{provider1.lower()}_price"],
                        f"{provider2.lower()}_price": data[f"{provider2.lower()}_price"],
                        "recommendation": data["recommendation"],
                        "savings_percent": data["savings_percent"]
                    },
                    "status": "success"
                }
            elif reverse_key in mock_comparisons and instance_type in mock_comparisons[reverse_key]:
                data = mock_comparisons[reverse_key][instance_type]
                return {
                    "comparison": {
                        "instance_type": instance_type,
                        f"{provider1.lower()}_price": data[f"{reverse_key[0].lower()}_price"],
                        f"{provider2.lower()}_price": data[f"{reverse_key[1].lower()}_price"],
                        "recommendation": data["recommendation"],
                        "savings_percent": data["savings_percent"]
                    },
                    "status": "success"
                }
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"No comparison data available for {provider1} vs {provider2} - {instance_type}"
                )

        @self.app.get("/market-trends")
        async def get_market_trends(provider: Optional[str] = None):
            """Get market trends for cloud pricing."""
            trends = {
                "overall_trend": "prices_decreasing",
                "average_change_percent": -5.2,
                "providers": {
                    "AWS": {"trend": "stable", "change_percent": -2.1},
                    "Azure": {"trend": "decreasing", "change_percent": -8.5},
                    "GCP": {"trend": "decreasing", "change_percent": -6.3}
                }
            }

            if provider:
                provider = provider.upper()
                if provider in trends["providers"]:
                    return {
                        "provider": provider,
                        **trends["providers"][provider],
                        "status": "success"
                    }
                else:
                    raise HTTPException(status_code=404, detail=f"Provider {provider} not found")

            return {"market_trends": trends, "status": "success"}


class ExternalAPITool:
    """Client tool for interacting with the mock external API."""

    def __init__(self, base_url: str = "http://localhost:8001", api_key: str = "demo_key"):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def get_providers(self) -> Dict[str, Any]:
        """Get list of supported providers from external API."""
        logger.info("Fetching providers from external API")

        try:
            response = self.session.get(f"{self.base_url}/providers")
            response.raise_for_status()
            result = response.json()
            logger.info(f"Retrieved {len(result.get('providers', []))} providers")
            return result
        except requests.RequestException as e:
            logger.error(f"Failed to fetch providers: {e}")
            return {"providers": ["AWS", "Azure", "GCP"], "status": "fallback"}

    def compare_prices(self, provider1: str, provider2: str, instance_type: str) -> Dict[str, Any]:
        """
        Compare prices between two providers for a specific instance type.

        Args:
            provider1: First cloud provider
            provider2: Second cloud provider
            instance_type: Instance type to compare

        Returns:
            Comparison results
        """
        logger.info(f"Comparing prices: {provider1} vs {provider2} for {instance_type}")

        payload = {
            "provider1": provider1,
            "provider2": provider2,
            "instance_type": instance_type
        }

        try:
            response = self.session.post(f"{self.base_url}/compare-prices", json=payload)
            response.raise_for_status()
            result = response.json()
            logger.info(f"Price comparison successful: {result.get('comparison', {}).get('recommendation', 'N/A')}")
            return result
        except requests.RequestException as e:
            logger.error(f"Failed to compare prices: {e}")
            return {
                "comparison": {
                    "error": f"API request failed: {str(e)}",
                    "provider1": provider1,
                    "provider2": provider2,
                    "instance_type": instance_type
                },
                "status": "error"
            }

    def get_market_trends(self, provider: Optional[str] = None) -> Dict[str, Any]:
        """
        Get market trends data.

        Args:
            provider: Optional provider filter

        Returns:
            Market trends data
        """
        logger.info(f"Fetching market trends for provider: {provider}")

        params = {"provider": provider} if provider else {}

        try:
            response = self.session.get(f"{self.base_url}/market-trends", params=params)
            response.raise_for_status()
            result = response.json()
            logger.info("Market trends retrieved successfully")
            return result
        except requests.RequestException as e:
            logger.error(f"Failed to fetch market trends: {e}")
            return {
                "market_trends": {
                    "error": f"API request failed: {str(e)}",
                    "overall_trend": "unknown"
                },
                "status": "error"
            }
