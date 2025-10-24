"""
Agente IA de Precificação em Nuvem - Classe Principal (CloudPricingAgent)

Esta é a classe central do sistema. Ela coordena todas as operações do agente autônomo,
integrando o modelo de linguagem (GPT-4) com as 3 ferramentas especializadas.

O agente funciona como um "orquestrador inteligente" que:
1. Recebe queries do usuário em linguagem natural
2. Decide automaticamente quais ferramentas usar
3. Coordena chamadas para ferramentas
4. Sintetiza resultados em respostas estruturadas
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import Function
from loguru import logger

from tools.search_tool import MockSearchTool
from tools.vector_store import VectorStoreTool
from tools.external_api import ExternalAPITool


class CloudPricingAgent:
    """
    Agente IA especializado em análise de preços de GPU na nuvem.

    Esta classe representa o "cérebro" do sistema. Ela usa o framework Agno
    para criar um agente autônomo que pode raciocinar e tomar decisões.

    O agente possui 3 ferramentas especializadas:
    1. MockSearchTool - Busca dados de preços locais
    2. VectorStoreTool - Base de conhecimento vetorial
    3. ExternalAPITool - API externa para comparações

    Atributos:
        search_tool: Ferramenta de busca em dados locais
        vector_store: Base de conhecimento vetorial
        external_api: API externa simulada
        agent: Instância do agente Agno
    """

    def __init__(self):
        """
        Inicializa o agente com suas 3 ferramentas essenciais.

        Este método configura todo o ecossistema do agente:
        1. Cria instâncias das 3 ferramentas
        2. Inicializa o agente Agno com GPT-4
        3. Registra todas as funções como ferramentas disponíveis
        """
        # Inicializa as 3 ferramentas do agente
        # Cada ferramenta representa uma fonte diferente de conhecimento
        self.search_tool = MockSearchTool()     # Busca em dados JSON locais
        self.vector_store = VectorStoreTool()   # Busca semântica na base vetorial
        self.external_api = ExternalAPITool()   # API externa para comparações

        # Cria o agente Agno com modelo e ferramentas
        self.agent = self._create_agent()

        logger.info("Agente de precificação inicializado com sucesso")

    def _create_agent(self) -> Agent:
        """
        Cria e configura o agente Agno com GPT-4 e ferramentas.

        Este método é o "coração" da configuração do agente. Ele:
        1. Define o modelo de linguagem (GPT-4)
        2. Registra cada ferramenta como uma função que o LLM pode chamar
        3. Define as instruções do sistema
        4. Cria a instância final do agente

        Returns:
            Agent: Instância configurada do agente Agno
        """
        # Define o modelo de linguagem (sempre GPT-4 para consistência)
        model = OpenAIChat(id="gpt-4")

        # Registra as ferramentas como funções que o LLM pode chamar
        # Cada Function representa uma "habilidade" que o agente pode usar

        search_tool = Function(
            fn=self.search_gpu_pricing,           # Função Python a ser chamada
            name="search_gpu_pricing",            # Nome que o LLM vê
            description="Busca preços de GPU nos provedores AWS, Azure e GCP"  # Descrição para o LLM
        )

        compare_tool = Function(
            fn=self.compare_cloud_prices,
            name="compare_cloud_prices",
            description="Compara preços entre dois provedores de nuvem"
        )

        trends_tool = Function(
            fn=self.get_market_trends,
            name="get_market_trends",
            description="Obtém tendências de mercado e análise de preços"
        )

        knowledge_tool = Function(
            fn=self.search_knowledge_base,
            name="search_knowledge_base",
            description="Busca informações sobre otimização de custos na nuvem"
        )

        # Cria o agente Agno com todas as configurações
        agent = Agent(
            model=model,                          # Modelo LLM (GPT-4)
            tools=[search_tool, compare_tool, trends_tool, knowledge_tool],  # Ferramentas disponíveis
            instructions=self._get_instructions() # Instruções do sistema
        )

        return agent

    def _get_instructions(self) -> str:
        """Instruções claras para o agente."""
        return """
        Você é um especialista em preços de nuvem focado em GPUs.

        SUAS FERRAMENTAS:
        - search_gpu_pricing: Busca preços de GPU nos provedores AWS, Azure, GCP
        - compare_cloud_prices: Compara preços entre dois provedores
        - get_market_trends: Obtém tendências de mercado
        - search_knowledge_base: Busca dicas de otimização de custos

        SEMPRE:
        1. Use as ferramentas disponíveis para obter dados
        2. Forneça respostas estruturadas e claras
        3. Compare preços quando possível
        4. Sugira a opção mais econômica
        5. Explique seu raciocínio passo a passo
        """

    def search_gpu_pricing(self, query: str) -> str:
        """
        Wrapper para busca de preços - chamado automaticamente pelo LLM.

        Quando o agente decide que precisa buscar dados de preços,
        ele chama esta função, que delega para a ferramenta MockSearchTool.

        Args:
            query: Termo de busca fornecido pelo LLM

        Returns:
            str: Resultados da busca em JSON
        """
        logger.info(f"Executando busca de preços: '{query}'")
        # Delega para a ferramenta especializada
        return self.search_tool.search_gpu_pricing(query)

    def compare_cloud_prices(self, provider1: str, provider2: str, gpu_type: str = "") -> str:
        """
        Wrapper para comparação de preços - chamado automaticamente pelo LLM.

        Quando o agente precisa comparar custos entre provedores,
        ele chama esta função, que delega para a ferramenta ExternalAPITool.

        Args:
            provider1: Primeiro provedor para comparar
            provider2: Segundo provedor para comparar
            gpu_type: Tipo de GPU para comparar

        Returns:
            str: Resultados da comparação em JSON
        """
        logger.info(f"Executando comparação: {provider1} vs {provider2} para {gpu_type}")
        # Delega para a ferramenta especializada
        return self.external_api.compare_prices(provider1, provider2, gpu_type)

    def get_market_trends(self, provider: str = "all") -> str:
        """
        Wrapper para tendências de mercado - chamado automaticamente pelo LLM.

        Quando o agente precisa de insights sobre tendências,
        ele chama esta função, que delega para a ferramenta ExternalAPITool.

        Args:
            provider: Provedor específico ou "all" para todos

        Returns:
            str: Tendências de mercado em JSON
        """
        logger.info(f"Consultando tendências para: {provider}")
        # Delega para a ferramenta especializada
        return self.external_api.get_market_trends(provider)

    def search_knowledge_base(self, query: str) -> str:
        """
        Wrapper para busca na base de conhecimento - chamado automaticamente pelo LLM.

        Quando o agente precisa de conhecimento geral ou dicas,
        ele chama esta função, que delega para a ferramenta VectorStoreTool.

        Args:
            query: Pergunta ou termo para buscar conhecimento

        Returns:
            str: Documentos relevantes encontrados em JSON
        """
        logger.info(f"Buscando conhecimento sobre: '{query}'")
        # Delega para a ferramenta especializada
        return self.vector_store.search_similar(query)

    def analyze_query(self, user_query: str) -> str:
        """
        MÉTODO PRINCIPAL: Processa queries do usuário usando o agente Agno.

        Este é o ponto de entrada principal da aplicação. O agente:
        1. Recebe a query do usuário em linguagem natural
        2. Decide automaticamente quais ferramentas usar (chain-of-thought)
        3. Coordena chamadas para as ferramentas na ordem correta
        4. Sintetiza todos os resultados em uma resposta estruturada
        5. Retorna resposta final para o usuário

        Este método representa a "mágica" do agente autônomo - ele pensa,
        planeja e executa sem intervenção manual.

        Args:
            user_query: Pergunta do usuário (ex: "Quanto custa GPU na AWS?")

        Returns:
            str: Resposta estruturada do agente
        """
        logger.info(f"Iniciando análise da query: '{user_query}'")

        try:
            # O agente Agno processa a query e usa ferramentas automaticamente
            # Esta é a chamada principal que dispara todo o chain-of-thought
            response = self.agent.run(user_query)

            # Extrai o conteúdo da resposta
            final_response = response.content if hasattr(response, 'content') else str(response)

            logger.info("Análise da query concluída com sucesso")
            return final_response

        except Exception as e:
            # Tratamento robusto de erros
            logger.error(f"Erro durante análise da query: {e}")
            return f"Erro ao processar query: {str(e)}"
