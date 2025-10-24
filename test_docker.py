#!/usr/bin/env python3
"""
Script para testar se a API FastAPI está funcionando.
"""
import requests
import time

def test_api():
    """Testa os endpoints da API."""
    base_url = "http://localhost:8000"

    print("Testando API FastAPI do Agente IA...")
    print("=" * 50)

    # Teste 1: Health check
    try:
        print("1. Testando endpoint /health...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("[OK] Health check: OK")
            print(f"   Status: {response.json()}")
        else:
            print(f"[ERRO] Health check falhou: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Erro na conexao: {e}")
        print("Dica: Certifique-se que o Docker Compose esta rodando com: docker-compose up")
        return

    print()

    # Teste 2: Endpoint raiz
    try:
        print("2. Testando endpoint /...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("[OK] Endpoint raiz: OK")
        else:
            print(f"[ERRO] Endpoint raiz falhou: {response.status_code}")
    except Exception as e:
        print(f"[ERRO] Erro no endpoint raiz: {e}")

    print()

    # Teste 3: Pergunta ao agente
    try:
        print("3. Testando pergunta ao agente...")
        question = "Quanto custa GPU V100 na AWS?"
        response = requests.post(
            f"{base_url}/ask",
            json={"question": question},
            timeout=30  # Mais tempo para resposta da IA
        )

        if response.status_code == 200:
            data = response.json()
            print("[OK] Pergunta processada: OK")
            print(f"   Pergunta: {data['question']}")
            print(f"   Resposta: {data['answer'][:200]}...")
        else:
            print(f"[ERRO] Pergunta falhou: {response.status_code}")
            print(f"   Detalhes: {response.text}")

    except Exception as e:
        print(f"[ERRO] Erro na pergunta: {e}")

    print()
    print("Testes concluidos!")

if __name__ == "__main__":
    test_api()

