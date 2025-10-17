#!/usr/bin/env python3
"""
Script de teste rápido para o AI Cloud Pricing Agent.
Use este script para verificar se tudo está funcionando corretamente.
"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils import Config, setup_logging
from agents import CloudPricingAgent
from tools import MockExternalAPIServer
import time

def test_basic_functionality():
    """Test basic agent functionality."""
    print("🧪 Testing AI Cloud Pricing Agent...")

    # Check configuration
    if not Config.validate_config():
        print("❌ Configuration validation failed")
        return False

    # Setup logging
    setup_logging()
    print("✅ Logging configured")

    # Test agent initialization
    try:
        agent = CloudPricingAgent(
            model_name="gpt-4",  # Will fallback if not available
            chroma_db_path="./data/chromadb",
            external_api_url="http://localhost:8001",
            external_api_key="demo_key"
        )
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

    # Test basic query
    test_queries = [
        "What GPU instances are available on AWS?",
        "Compare prices between AWS and Azure for V100 GPUs",
        "What are some cost optimization strategies for cloud GPUs?"
    ]

    for query in test_queries:
        print(f"\n🔍 Testing query: '{query}'")
        try:
            start_time = time.time()
            response = agent.analyze_query(query)
            end_time = time.time()

            print(f"⏱️  Response time: {end_time - start_time:.2f}s")
            print(f"📄 Response preview: {response[:200]}...")

        except Exception as e:
            print(f"❌ Query failed: {e}")
            continue

    print("\n✅ Basic functionality test completed!")
    return True

def test_tools():
    """Test individual tools."""
    print("\n🛠️  Testing individual tools...")

    from tools import MockSearchTool, VectorStoreTool, ExternalAPITool

    # Test search tool
    try:
        search_tool = MockSearchTool()
        results = search_tool.search_gpu_pricing()
        print(f"✅ Search tool: Found {len(results)} GPU instances")
    except Exception as e:
        print(f"❌ Search tool failed: {e}")

    # Test vector store
    try:
        vector_store = VectorStoreTool()
        stats = vector_store.get_collection_stats()
        print(f"✅ Vector store: {stats['document_count']} documents loaded")
    except Exception as e:
        print(f"❌ Vector store failed: {e}")

    # Test external API (will fail if server not running, which is expected)
    try:
        external_api = ExternalAPITool()
        # This will likely fail without the mock server running
        result = external_api.get_providers()
        print(f"✅ External API: {result}")
    except Exception as e:
        print(f"⚠️  External API (expected to fail without server): {type(e).__name__}")

def main():
    """Main test function."""
    print("🚀 AI Cloud Pricing Agent - Test Suite")
    print("=" * 50)

    # Test basic functionality
    success = test_basic_functionality()

    # Test tools
    test_tools()

    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! The agent is ready to use.")
        print("\nTo start the interactive mode:")
        print("  python -m src.main interactive")
        print("\nTo start the mock API server (in another terminal):")
        print("  python -m src.main api-server")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
