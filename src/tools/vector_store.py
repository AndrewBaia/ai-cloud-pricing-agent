"""
Ferramenta de Base de Conhecimento Vetorial (VectorStoreTool)

Esta ferramenta representa a segunda ferramenta do agente: uma "base de conhecimento inteligente".
Usa ChromaDB para armazenar e buscar informações usando similaridade vetorial.

Responsabilidades:
- Armazenar documentos de conhecimento sobre nuvem e otimização
- Realizar buscas semânticas (não apenas texto exato)
- Fornecer dicas de otimização de custos
- Manter histórico de informações relevantes
"""
import chromadb
from chromadb.config import Settings
import json
import uuid
from loguru import logger


class VectorStoreTool:
    """
    Base de conhecimento vetorial usando ChromaDB.

    Esta classe representa uma "memória inteligente" do agente.
    Em produção, seria populada com documentação real de provedores de nuvem,
    melhores práticas, e conhecimento específico do domínio.

    Atributos:
        persist_directory: Diretório onde ChromaDB salva dados
        client: Cliente ChromaDB para operações
        collection_name: Nome da coleção de documentos
        collection: Objeto da coleção ChromaDB
    """

    def __init__(self, persist_directory: str = "./data/chromadb"):
        """
        Inicializa a base de conhecimento vetorial.

        Args:
            persist_directory: Caminho onde dados serão persistidos
        """
        self.persist_directory = persist_directory

        # Cria cliente ChromaDB com persistência local
        # Desabilita telemetria para privacidade
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )

        # Nome da coleção que armazenará nossos documentos
        self.collection_name = "cloud_pricing_docs"

        # Inicializa ou carrega coleção existente
        self._initialize_collection()

    def _initialize_collection(self):
        """
        Inicializa ou carrega a coleção ChromaDB.

        Este método verifica se já existe uma coleção com dados.
        Se não existir, cria uma nova e popula com dados iniciais.

        Processo:
        1. Tenta carregar coleção existente
        2. Se não existir, cria nova coleção
        3. Popula com documentos de conhecimento básico
        """
        try:
            # Tenta carregar coleção existente
            self.collection = self.client.get_collection(self.collection_name)
            logger.info("Coleção existente de conhecimento carregada")
        except:
            # Coleção não existe, criar nova
            self.collection = self.client.create_collection(self.collection_name)
            # Popula com dados iniciais de conhecimento
            self._populate_initial_data()
            logger.info("Nova coleção de conhecimento criada")

    def _populate_initial_data(self):
        """
        Popula a coleção com documentos iniciais de conhecimento.

        Estes documentos representam o "conhecimento base" do agente sobre:
        - Preços de diferentes provedores
        - Estratégias de otimização
        - Informações técnicas relevantes

        Em produção, isso seria feito com dados reais de documentação,
        blogs técnicos, e melhores práticas dos provedores.
        """
        documents = [
            {
                "id": str(uuid.uuid4()),
                "content": "AWS P3 instances com V100 GPUs para machine learning. Preços: P3.2xlarge $3.06/h, P3.8xlarge $12.24/h.",
                "metadata": {"provider": "AWS", "gpu_type": "V100"}
            },
            {
                "id": str(uuid.uuid4()),
                "content": "Azure NC series com K80 GPUs. Preços: NC6 $0.90/h, NC12 $1.80/h, NC24 $3.60/h.",
                "metadata": {"provider": "Azure", "gpu_type": "K80"}
            },
            {
                "id": str(uuid.uuid4()),
                "content": "GCP com K80 GPUs. Preços: n1-standard-8 $0.70/h, n1-standard-16 $1.40/h.",
                "metadata": {"provider": "GCP", "gpu_type": "K80"}
            },
            {
                "id": str(uuid.uuid4()),
                "content": "Dicas de economia: Use spot instances, escolha tamanho correto, considere reserved instances.",
                "metadata": {"topic": "cost_optimization"}
            }
        ]

        # Extrai dados para o formato esperado pelo ChromaDB
        ids = [doc["id"] for doc in documents]
        contents = [doc["content"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]

        # Adiciona documentos à coleção
        # ChromaDB criará embeddings automaticamente
        self.collection.add(documents=contents, metadatas=metadatas, ids=ids)
        logger.info(f"Base de conhecimento populada com {len(documents)} documentos")

    def search_similar(self, query: str) -> str:
        """
        Método principal: realiza busca semântica na base de conhecimento.

        Esta é a função que o agente IA chama quando precisa de conhecimento
        geral sobre nuvem, melhores práticas, ou dicas de otimização.

        Como funciona a busca vetorial:
        1. A query é convertida em embedding vetorial
        2. Busca documentos similares no espaço vetorial
        3. Retorna os mais relevantes (não apenas matches exatos)

        Args:
            query: Pergunta ou termo de busca (ex: "otimização de custos")

        Returns:
            str: JSON com documentos relevantes encontrados
        """
        logger.info(f"Busca semântica por: '{query}'")

        # Realiza busca vetorial - retorna 2 resultados mais similares
        results = self.collection.query(query_texts=[query], n_results=2)

        # Verifica se encontrou documentos
        if not results.get("documents") or not results["documents"][0]:
            logger.info(f"Nenhum documento relevante encontrado para: {query}")
            return json.dumps({
                "mensagem": f"Nenhum documento relevante encontrado para: {query}",
                "query": query
            })

        # Formatar resposta para o agente
        docs = results["documents"][0]      # Lista de conteúdos
        metadatas = results["metadatas"][0] # Lista de metadados

        # Combina conteúdo + metadados em formato estruturado
        formatted_results = []
        for doc, meta in zip(docs, metadatas):
            formatted_results.append({
                "conteudo": doc,    # Texto completo do documento
                "metadata": meta    # Informações contextuais
            })

        logger.info(f"Encontrados {len(formatted_results)} documentos relevantes")
        # Retorna JSON formatado para o agente
        return json.dumps(formatted_results, ensure_ascii=False, indent=2)
