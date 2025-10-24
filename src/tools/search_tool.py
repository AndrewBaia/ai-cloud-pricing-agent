"""
Ferramenta de Busca Simulada (MockSearchTool)

Esta ferramenta simula uma busca em dados de preços de nuvem.
Ela representa a primeira ferramenta do agente: uma "busca local" em dados JSON.

Responsabilidades:
- Carregar dados mock de preços de GPU de provedores de nuvem
- Realizar buscas textuais simples nos dados
- Retornar resultados formatados em JSON
"""
import json
from loguru import logger


class MockSearchTool:
    """
    Ferramenta de busca simulada que representa uma "API de busca local".

    Esta classe simula como seria buscar dados em uma API externa ou banco de dados.
    No cenário real, isso seria substituído por chamadas reais para APIs de preços.

    Atributos:
        data_file: Caminho para o arquivo JSON com dados mock
        data: Dados carregados em memória
    """

    def __init__(self, data_file: str = "data/pricing_data.json"):
        """
        Inicializa a ferramenta de busca.

        Args:
            data_file: Caminho para arquivo JSON com dados de preços
        """
        self.data_file = data_file
        # Carrega dados uma vez na inicialização para performance
        self.data = self._load_data()

    def _load_data(self):
        """
        Carrega dados mock do arquivo JSON.

        Este método representa como seria conectar com uma fonte de dados real.
        Em produção, isso seria uma chamada para API ou banco de dados.

        Returns:
            dict: Dados carregados ou dict vazio se arquivo não existir
        """
        try:
            # Abre arquivo com encoding UTF-8 para suportar caracteres especiais
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Log de warning se arquivo não existir (desenvolvimento)
            logger.warning(f"Arquivo {self.data_file} não encontrado, usando dados vazios")
            return {}

    def search_gpu_pricing(self, query: str) -> str:
        """
        Método principal: realiza busca por preços de GPU.

        Esta é a função que o agente IA chama quando precisa buscar dados de preços.
        Representa uma "ferramenta externa" que o LLM pode invocar.

        Algoritmo de busca:
        1. Converte query para minúsculas
        2. Itera sobre todos os dados (provedores -> categorias -> itens)
        3. Verifica se query aparece em qualquer campo do item
        4. Retorna até 5 resultados mais relevantes

        Args:
            query: String de busca (ex: "AWS V100", "GPU pricing", etc.)

        Returns:
            str: JSON com resultados da busca ou mensagem de erro
        """
        logger.info(f"Iniciando busca por: '{query}'")
        results = []

        # Normaliza query para busca case-insensitive
        query_lower = query.lower()

        # Itera sobre estrutura de dados: provider -> category -> items
        # Exemplo: AWS -> GPU_Instances -> [lista de instâncias]
        for provider, categories in self.data.items():
            for category, items in categories.items():
                for item in items:
                    # Converte item completo para string e busca
                    # Isso permite buscar por qualquer campo (nome, tipo, preço, etc.)
                    item_str = json.dumps(item, ensure_ascii=False).lower()
                    if query_lower in item_str:
                        # Adiciona resultado com contexto
                        results.append({
                            "provider": provider,      # AWS, Azure, GCP
                            "category": category,      # GPU_Instances, etc.
                            "data": item              # Dados completos da instância
                        })

        # Verifica se encontrou resultados
        if not results:
            logger.info(f"Nenhum resultado encontrado para: {query}")
            return json.dumps({
                "mensagem": f"Nenhum resultado encontrado para: {query}",
                "query": query
            })

        # Limita a 5 resultados para não sobrecarregar o LLM
        limited_results = results[:5]
        logger.info(f"Encontrados {len(limited_results)} resultados para: {query}")

        # Retorna JSON formatado para o agente
        return json.dumps(limited_results, ensure_ascii=False, indent=2)
