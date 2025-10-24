#!/usr/bin/env python3
"""
Script de teste direto para o AI Cloud Pricing Agent.
Testa o agente diretamente sem precisar da API FastAPI.
Use este script para verificar se o agente está funcionando.
"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.config import Config
from utils.logging_config import setup_logging
from agents.cloud_pricing_agent import CloudPricingAgent
import time

def test_basic_functionality():
    """Test basic agent functionality."""
    print("Testing AI Cloud Pricing Agent...")

    # Check configuration
    if not Config.validar():
        print("[ERRO] Configuracao invalida")
        return False

    # Setup logging
    setup_logging()
    print("[OK] Logging configurado")

    # Test agent initialization
    try:
        agent = CloudPricingAgent()
        print("[OK] Agente inicializado com sucesso")
    except Exception as e:
        print(f"[ERRO] Agente falhou ao inicializar: {e}")
        return False

    # Test basic query
    test_queries = [
        "Quais instâncias de GPU estão disponíveis na AWS?",
        "Compare preços entre AWS e Azure para GPUs V100",
        "Quais são algumas estratégias de otimização de custos para GPUs na nuvem?"
    ]

    for query in test_queries:
        print(f"\nTestando pergunta: '{query}'")
        try:
            start_time = time.time()
            response = agent.analyze_query(query)
            end_time = time.time()

            print(f"Tempo de resposta: {end_time - start_time:.2f}s")
            print(f"Resposta: {response[:300]}...")

        except Exception as e:
            print(f"[ERRO] Query falhou: {e}")
            continue

    print("\n[OK] Teste basico concluido!")
    return True

def test_tools():
    """Test individual tools."""
    print("\nTestando ferramentas individuais...")

    from tools.search_tool import MockSearchTool
    from tools.vector_store import VectorStoreTool
    from tools.external_api import ExternalAPITool

    # Test search tool
    try:
        search_tool = MockSearchTool()
        results_str = search_tool.search_gpu_pricing("AWS")  # Retorna string JSON
        # Verifica se a string não está vazia e é válida
        if results_str and len(results_str) > 10:  # Mais que apenas "{}" ou "[]"
            print(f"[OK] Ferramenta de busca: Resposta obtida ({len(results_str)} chars)")
        else:
            print(f"[ERRO] Ferramenta de busca: Resposta vazia")
    except Exception as e:
        print(f"[ERRO] Ferramenta de busca falhou: {e}")

    # Test vector store
    try:
        vector_store = VectorStoreTool()
        # Testar busca no conhecimento - metodo correto
        results_str = vector_store.search_similar("GPU pricing")
        if results_str and len(results_str) > 10:
            print(f"[OK] Vector store: Resposta obtida ({len(results_str)} chars)")
        else:
            print(f"[ERRO] Vector store: Resposta vazia")
    except Exception as e:
        print(f"[ERRO] Vector store falhou: {e}")

    # Test external API
    try:
        external_api = ExternalAPITool()
        # Testar comparacao de precos - metodo correto
        result = external_api.get_market_trends()
        print(f"[OK] API externa: Dados obtidos")
    except Exception as e:
        print(f"[ERRO] API externa falhou: {e}")

def main():
    """Main test function."""
    print("AI Cloud Pricing Agent - Suite de Testes")
    print("=" * 50)

    # Test basic functionality
    success = test_basic_functionality()

    # Test tools
    test_tools()

    print("\n" + "=" * 50)
    if success:
        print("Sucesso! O agente esta funcionando.")
        print("\nPara usar a API FastAPI:")
        print("  docker-compose up")
        print("  curl -X POST http://localhost:8000/ask -H 'Content-Type: application/json' -d '{\"question\":\"Quanto custa GPU V100?\"}'")
    else:
        print("Alguns testes falharam. Verifique os erros acima.")
        sys.exit(1)

if __name__ == "__main__":
    main()
