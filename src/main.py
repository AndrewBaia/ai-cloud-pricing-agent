#!/usr/bin/env python3
"""
Ponto de entrada principal do Agente IA de Precificação em Nuvem.

Este arquivo é o ponto de entrada CLI da aplicação. Ele:
- Carrega configurações e valida dependências
- Inicializa o agente IA
- Processa queries do usuário via linha de comando
- Exibe respostas estruturadas
"""
import sys
import os

# Adiciona o diretório src ao path para permitir imports relativos
sys.path.insert(0, os.path.dirname(__file__))

# Importa módulos utilitários para configuração e logging
from utils import setup_logging, Config
# Importa o agente principal que coordena todas as operações
from agents import CloudPricingAgent
# Logger para registrar operações e debug
from loguru import logger


def main():
    """
    Função principal da aplicação.

    Fluxo de execução:
    1. Valida configuração (API keys, etc.)
    2. Configura sistema de logging
    3. Inicializa agente IA
    4. Processa query do usuário
    5. Exibe resposta formatada
    """
    # Validação inicial da configuração
    # Verifica se OPENAI_API_KEY está configurada no .env
    if not Config.validar():
        print("ERRO: Configuração inválida. Verifique seu arquivo .env")
        sys.exit(1)

    # Inicializa sistema de logging com rotação automática
    setup_logging()

    # Cria instância do agente IA com suas 3 ferramentas
    agent = CloudPricingAgent()

    # Processamento de argumentos da linha de comando
    # Espera pelo menos uma query como argumento
    if len(sys.argv) < 2:
        print("Uso: python src/main.py 'sua pergunta sobre preços de GPU'")
        print("Exemplo: python src/main.py 'Quanto custa uma GPU V100 na AWS?'")
        sys.exit(1)

    # Junta todos os argumentos em uma única string de query
    query = " ".join(sys.argv[1:])
    logger.info(f"Processando query do usuário: {query}")

    try:
        # Executa a query através do agente IA
        # O agente decide automaticamente quais ferramentas usar
        resposta = agent.analyze_query(query)

        # Formatação e exibição da resposta
        # Usa separadores visuais para destacar a resposta
        print("\n" + "="*50)
        print("RESPOSTA DO AGENTE:")
        print("="*50)
        print(resposta)
        print("="*50 + "\n")

        logger.info("Query processada com sucesso")

    except Exception as e:
        # Tratamento de erros com logging detalhado
        logger.error(f"Erro durante processamento: {e}")
        print(f"Erro ao processar query: {e}")
        print("Verifique os logs em logs/agent.log para mais detalhes")


# Ponto de entrada quando executado diretamente
# Permite tanto execução direta quanto importação como módulo
if __name__ == "__main__":
    main()
