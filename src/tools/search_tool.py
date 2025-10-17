"""
Simulated search tool that returns mock data for cloud pricing information.
"""
import json
import random
from typing import Dict, List, Any
from loguru import logger


class MockSearchTool:
    """Simulated search tool with predefined cloud pricing data."""

    def __init__(self, data_file: str = "data/pricing_data.json"):
        self.data_file = data_file
        self._load_mock_data()

    def _load_mock_data(self):
        """Load mock pricing data."""
        try:
            with open(self.data_file, 'r') as f:
                self.pricing_data = json.load(f)
        except FileNotFoundError:
            # Create default mock data if file doesn't exist
            self.pricing_data = self._create_default_data()

    def _create_default_data(self) -> Dict[str, Any]:
        """Create default mock pricing data."""
        return {
            "cloud_providers": {
                "AWS": {
                    "gpus": {
                        "p3.2xlarge": {
                            "name": "P3.2xlarge",
                            "gpu_type": "V100",
                            "gpu_count": 1,
                            "vcpus": 8,
                            "memory_gb": 61,
                            "price_per_hour": 3.06,
                            "region": "us-east-1"
                        },
                        "p3.8xlarge": {
                            "name": "P3.8xlarge",
                            "gpu_type": "V100",
                            "gpu_count": 4,
                            "vcpus": 32,
                            "memory_gb": 244,
                            "price_per_hour": 12.24,
                            "region": "us-east-1"
                        },
                        "p3.16xlarge": {
                            "name": "P3.16xlarge",
                            "gpu_type": "V100",
                            "gpu_count": 8,
                            "vcpus": 64,
                            "memory_gb": 488,
                            "price_per_hour": 24.48,
                            "region": "us-east-1"
                        }
                    }
                },
                "Azure": {
                    "gpus": {
                        "NC6": {
                            "name": "NC6",
                            "gpu_type": "K80",
                            "gpu_count": 1,
                            "vcpus": 6,
                            "memory_gb": 56,
                            "price_per_hour": 0.90,
                            "region": "East US"
                        },
                        "NC12": {
                            "name": "NC12",
                            "gpu_type": "K80",
                            "gpu_count": 2,
                            "vcpus": 12,
                            "memory_gb": 112,
                            "price_per_hour": 1.80,
                            "region": "East US"
                        },
                        "NC24": {
                            "name": "NC24",
                            "gpu_type": "K80",
                            "gpu_count": 4,
                            "vcpus": 24,
                            "memory_gb": 224,
                            "price_per_hour": 3.60,
                            "region": "East US"
                        }
                    }
                },
                "GCP": {
                    "gpus": {
                        "n1-standard-8": {
                            "name": "n1-standard-8 with Tesla K80",
                            "gpu_type": "K80",
                            "gpu_count": 1,
                            "vcpus": 8,
                            "memory_gb": 30,
                            "price_per_hour": 0.70,
                            "region": "us-central1"
                        },
                        "n1-standard-16": {
                            "name": "n1-standard-16 with Tesla K80",
                            "gpu_type": "K80",
                            "gpu_count": 2,
                            "vcpus": 16,
                            "memory_gb": 60,
                            "price_per_hour": 1.40,
                            "region": "us-central1"
                        },
                        "n1-standard-32": {
                            "name": "n1-standard-32 with Tesla K80",
                            "gpu_type": "K80",
                            "gpu_count": 4,
                            "vcpus": 32,
                            "memory_gb": 120,
                            "price_per_hour": 2.80,
                            "region": "us-central1"
                        }
                    }
                }
            }
        }

    def search_gpu_pricing(self, provider: str = None, gpu_type: str = None,
                          min_gpu_count: int = None, max_price: float = None) -> List[Dict[str, Any]]:
        """
        Search for GPU pricing information.

        Args:
            provider: Filter by cloud provider (AWS, Azure, GCP)
            gpu_type: Filter by GPU type (V100, K80, etc.)
            min_gpu_count: Minimum number of GPUs
            max_price: Maximum price per hour

        Returns:
            List of matching GPU instances
        """
        logger.info(f"Searching GPU pricing - Provider: {provider}, GPU Type: {gpu_type}, "
                   f"Min GPUs: {min_gpu_count}, Max Price: {max_price}")

        results = []

        providers_to_search = [provider] if provider else self.pricing_data["cloud_providers"].keys()

        for prov in providers_to_search:
            if prov not in self.pricing_data["cloud_providers"]:
                continue

            for instance_type, instance_data in self.pricing_data["cloud_providers"][prov]["gpus"].items():
                # Apply filters
                if gpu_type and instance_data["gpu_type"] != gpu_type:
                    continue
                if min_gpu_count and instance_data["gpu_count"] < min_gpu_count:
                    continue
                if max_price and instance_data["price_per_hour"] > max_price:
                    continue

                results.append({
                    "provider": prov,
                    "instance_type": instance_type,
                    **instance_data
                })

        # Add some randomness to simulate real search variability
        random.shuffle(results)

        logger.info(f"Found {len(results)} matching GPU instances")
        return results

    def search_general(self, query: str) -> Dict[str, Any]:
        """
        General search function that can handle various queries.

        Args:
            query: Search query string

        Returns:
            Search results
        """
        logger.info(f"Performing general search for: {query}")

        # Simulate search latency
        import time
        time.sleep(random.uniform(0.1, 0.5))

        query_lower = query.lower()

        if "gpu" in query_lower and ("price" in query_lower or "cost" in query_lower):
            return {
                "type": "gpu_pricing",
                "results": self.search_gpu_pricing(),
                "query": query
            }
        elif "cloud" in query_lower and "provider" in query_lower:
            return {
                "type": "cloud_providers",
                "results": list(self.pricing_data["cloud_providers"].keys()),
                "query": query
            }
        else:
            return {
                "type": "general",
                "results": f"Mock search results for: {query}",
                "query": query
            }
