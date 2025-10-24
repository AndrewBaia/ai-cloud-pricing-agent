"""
Ferramenta de API Externa Simulada (ExternalAPITool)

Esta ferramenta representa a terceira ferramenta do agente: uma "API externa de mercado".
Simula chamadas para serviços externos que fornecem dados de tendências e comparações.

Responsabilidades:
- Simular chamadas para APIs de comparação de preços
- Fornecer dados de tendências de mercado
- Calcular economias potenciais entre provedores
- Retornar análises de mercado
"""
import json
from loguru import logger


class ExternalAPITool:
    """
    Ferramenta que simula uma API externa de análise de mercado.

    Esta classe representa como seria integrar com um serviço real de análise
    de preços de nuvem, tendências de mercado, e comparações competitivas.

    Em produção, isso seria substituído por chamadas reais para:
    - APIs de provedores de nuvem
    - Serviços de análise de mercado
    - Ferramentas de comparação de custos

    Atributos:
        base_url: URL base da API simulada
        api_key: Chave de autenticação simulada
    """

    def __init__(self, base_url: str = "http://localhost:8001", api_key: str = "demo"):
        """
        Inicializa a ferramenta de API externa.

        Args:
            base_url: URL base da API (simulada)
            api_key: Chave de API para autenticação (simulada)
        """
        self.base_url = base_url
        self.api_key = api_key

    def compare_prices(self, provider1: str, provider2: str, gpu_type: str = "") -> str:
        """
        Método principal: compara preços entre dois provedores de nuvem.

        Esta é a função que o agente IA chama quando precisa comparar
        custos entre diferentes provedores para o mesmo tipo de GPU.

        Lógica de comparação:
        1. Busca dados de preços simulados para ambos os provedores
        2. Calcula diferenças de preço
        3. Determina qual opção é mais econômica
        4. Calcula percentual de economia

        Args:
            provider1: Primeiro provedor (AWS, Azure, GCP)
            provider2: Segundo provedor para comparação
            gpu_type: Tipo de GPU para comparar (V100, K80, etc.)

        Returns:
            str: JSON com resultados da comparação ou mensagem de erro
        """
        logger.info(f"Iniciando comparação: {provider1} vs {provider2} para GPU {gpu_type}")

        # Base de dados simulada de comparações
        # Em produção, isso viria de uma API real de análise de mercado
        comparisons = {
            ("AWS", "Azure"): {
                "V100": {"aws_price": 3.06, "azure_price": 2.80, "recommendation": "Azure", "savings": "8.5%"},
                "K80": {"aws_price": 0.90, "azure_price": 0.85, "recommendation": "Azure", "savings": "5.6%"}
            },
            ("AWS", "GCP"): {
                "V100": {"aws_price": 3.06, "gcp_price": 2.90, "recommendation": "GCP", "savings": "5.2%"},
                "K80": {"aws_price": 0.90, "gcp_price": 0.70, "recommendation": "GCP", "savings": "22.2%"}
            },
            ("Azure", "GCP"): {
                "K80": {"azure_price": 0.85, "gcp_price": 0.70, "recommendation": "GCP", "savings": "17.6%"}
            }
        }

        # Tenta encontrar comparação direta
        key = (provider1, provider2)
        reverse_key = (provider2, provider1)

        if key in comparisons and gpu_type in comparisons[key]:
            # Comparação direta encontrada
            data = comparisons[key][gpu_type]
            result = {
                "comparacao": {
                    f"{provider1}_preco": data[f"{provider1.lower()}_price"],
                    f"{provider2}_preco": data[f"{provider2.lower()}_price"],
                    "recomendacao": data["recommendation"],
                    "economia": data["savings"]
                }
            }
            logger.info(f"Comparação encontrada: {data['recommendation']} recomendado com {data['savings']} de economia")

        elif reverse_key in comparisons and gpu_type in comparisons[reverse_key]:
            # Comparação reversa encontrada (ex: Azure vs AWS quando pediu AWS vs Azure)
            data = comparisons[reverse_key][gpu_type]
            result = {
                "comparacao": {
                    f"{provider1}_preco": data[f"{provider2.lower()}_price"],  # Inverte os preços
                    f"{provider2}_preco": data[f"{provider1.lower()}_price"],  # Inverte os preços
                    "recomendacao": data["recommendation"],
                    "economia": data["savings"]
                }
            }
            logger.info(f"Comparação reversa encontrada: {data['recommendation']} recomendado")

        else:
            # Nenhuma comparação disponível
            logger.info(f"Comparação não disponível: {provider1} vs {provider2} para {gpu_type}")
            result = {
                "mensagem": f"Comparação não disponível para {provider1} vs {provider2} com GPU {gpu_type}"
            }

        # Retorna resultado em JSON para o agente
        return json.dumps(result, ensure_ascii=False, indent=2)

    def get_market_trends(self, provider: str = "all") -> str:
        """
        Método secundário: obtém tendências de mercado.

        Esta função simula uma chamada para um serviço de análise de tendências
        de mercado, fornecendo insights sobre direção dos preços.

        Args:
            provider: Provedor específico ou "all" para todos

        Returns:
            str: JSON com tendências de mercado
        """
        logger.info(f"Consultando tendências de mercado para: {provider}")

        # Dados simulados de tendências de mercado
        # Em produção, isso viria de análise real de dados históricos
        trends = {
            "AWS": {
                "tendencia": "estavel",
                "analise": "Demanda alta mantém preços estáveis, boa disponibilidade"
            },
            "Azure": {
                "tendencia": "crescendo",
                "analise": "Aumento na demanda por workloads de IA, preços em ascensão"
            },
            "GCP": {
                "tendencia": "estavel",
                "analise": "Preços competitivos, foco em workloads sustentáveis"
            }
        }

        if provider == "all":
            # Retorna tendências para todos os provedores
            result = {"tendencias": trends}
            logger.info("Tendências de todos os provedores retornadas")
        elif provider in trends:
            # Retorna tendência de um provedor específico
            result = {provider: trends[provider]}
            logger.info(f"Tendência de {provider} retornada")
        else:
            # Provedor não encontrado
            result = {
                "mensagem": f"Tendências não disponíveis para o provedor: {provider}"
            }
            logger.info(f"Tendência não encontrada para: {provider}")

        # Retorna resultado em JSON para o agente
        return json.dumps(result, ensure_ascii=False, indent=2)