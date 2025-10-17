# AI Cloud Pricing Agent

Um agente de IA autônomo especializado em análise de custos de computação em nuvem, utilizando o framework Agno e ChromaDB para fornecer recomendações inteligentes sobre preços de GPU entre provedores AWS, Azure e GCP.

## 🚀 Visão Geral

Este projeto implementa um agente de IA complexo que pode:
- Analisar preços de GPU em múltiplos provedores de nuvem
- Comparar custos entre diferentes plataformas
- Fornecer recomendações de otimização de custos
- Pesquisar em base de conhecimento vetorial
- Integrar com APIs externas simuladas

## 🏗️ Arquitetura

O sistema é composto por:

- **Agente Principal**: Implementado com Agno, coordena todas as operações
- **Ferramentas**:
  - `MockSearchTool`: Busca simulada de preços (JSON/local)
  - `VectorStoreTool`: Base vetorial com ChromaDB
  - `ExternalAPITool`: API externa fictícia para comparações
- **Interface CLI**: Interface de linha de comando rica
- **Servidor Mock API**: Simula serviços externos

## 📋 Pré-requisitos

- Python 3.11+
- Chave API do OpenAI ou Anthropic
- (Opcional) Docker para execução containerizada

## 🛠️ Instalação

### Opção 1: Instalação Direta

1. **Clone o repositório**:
   ```bash
   git clone <repository-url>
   cd ai-cloud-pricing-agent
   ```

2. **Crie ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure variáveis de ambiente**:
   ```bash
   cp env.example .env
   # Edite .env com suas chaves API
   ```

### Opção 2: Docker

```bash
docker build -t ai-cloud-agent .
docker run -it --env-file .env ai-cloud-agent
```

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```bash
# APIs (pelo menos uma é necessária)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Modelo padrão
DEFAULT_MODEL=gpt-4

# ChromaDB
CHROMA_DB_PATH=./data/chromadb

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/agent.log

# API Externa (Mock)
EXTERNAL_API_BASE_URL=http://localhost:8001
EXTERNAL_API_KEY=demo_key
```

### Modelos Suportados

- **OpenAI**: `gpt-4`, `gpt-3.5-turbo`
- **Anthropic**: `claude-3-5-sonnet-20241022`, `claude-3-haiku-20240307`

## 🚀 Uso

### 1. Iniciar Servidor Mock API

Em um terminal separado:
```bash
python -m src.main api-server
```

### 2. Modo Interativo

```bash
python -m src.main interactive
```

Exemplos de consultas:
- "Monte um relatório que mostre o preço médio de GPUs na AWS, Azure e GCP, e sugira a opção mais barata por hora de uso"
- "Compare preços de instâncias P3 da AWS com equivalentes no Azure"
- "Quais estratégias de otimização de custos você recomenda para workloads de ML?"

### 3. Consulta Única

```bash
python -m src.main query "Qual é o preço da instância p3.2xlarge na AWS?"
```

### 4. Salvar Resultado

```bash
python -m src.main query "Compare GPUs V100 entre provedores" --output resultado.txt
```

### 5. Verificar Configuração

```bash
python -m src.main config
```

### 6. Ver Estatísticas

```bash
python -m src.main stats
```

## 🔧 Desenvolvimento

### Estrutura do Projeto

```
src/
├── agents/
│   ├── cloud_pricing_agent.py  # Agente principal
│   └── __init__.py
├── tools/
│   ├── search_tool.py          # Busca simulada
│   ├── vector_store.py         # ChromaDB
│   ├── external_api.py         # API mock
│   └── __init__.py
├── utils/
│   ├── config.py              # Configurações
│   ├── logging_config.py      # Logging
│   └── __init__.py
├── main.py                    # CLI principal
└── __init__.py

data/
├── pricing_data.json          # Dados mock
└── chromadb/                  # Base vetorial

docs/
└── architecture.md            # Documentação técnica

tests/
└── (testes futuros)
```

### Adicionando Novas Ferramentas

1. Crie uma nova classe em `src/tools/`
2. Implemente os métodos necessários
3. Registre no agente em `cloud_pricing_agent.py`
4. Atualize o `__init__.py`

## 🧪 Testes

```bash
# Executar testes (quando implementados)
pytest tests/

# Teste manual das ferramentas
python -c "from src.tools import MockSearchTool; tool = MockSearchTool(); print(tool.search_gpu_pricing())"
```

## 📊 Decisões Técnicas

### Framework Agno
- **Razão**: Framework moderno para agentes de IA, suporta múltiplos modelos e ferramentas
- **Alternativas consideradas**: LangChain, LlamaIndex
- **Vantagem**: API limpa, boa integração com ferramentas customizadas

### ChromaDB para Vetorial
- **Razão**: Base vetorial leve, open-source, fácil integração
- **Alternativas**: FAISS, Pinecone, Weaviate
- **Vantagem**: Não requer API externa, persistência local

### Mock APIs
- **Razão**: Simula cenário real sem dependências externas
- **Implementação**: FastAPI para servidor mock, requests para cliente
- **Benefício**: Desenvolvimento independente, testes controlados

### Logging Estruturado
- **Framework**: Loguru para logging moderno
- **Níveis**: INFO para operações normais, ERROR para problemas
- **Formato**: Estruturado com timestamps, níveis e contexto

## 🔒 Segurança

### Considerações Implementadas
- Validação de configuração antes da inicialização
- Logs não expõem chaves API
- Isolamento de ferramentas via funções wrapper
- Tratamento de erros graceful

### Riscos Mitigados
- **Prompt Injection**: Validação de inputs no agente
- **Data Leakage**: Logs sanitizados, dados mock
- **API Abuse**: Rate limiting nas ferramentas simuladas
- **Dependências**: Versões fixadas no requirements.txt

## 📈 Performance

### Otimizações
- **Cache vetorial**: ChromaDB mantém índices em memória
- **Lazy loading**: Ferramentas inicializadas sob demanda
- **Async operations**: APIs simuladas com delays realistas
- **Memory management**: Limitação de resultados de busca

### Métricas Monitoradas
- Tempo de resposta por consulta
- Taxa de sucesso das ferramentas
- Uso de tokens (via logging do Agno)
- Latência da API externa

## 🔄 Escalabilidade

Ver documento completo em `docs/architecture.md` para estratégias detalhadas de escalabilidade.

### Principais Estratégias
- **Horizontal scaling**: Múltiplas instâncias do agente
- **Cache distribuído**: Redis para resultados frequentes
- **Database sharding**: Para grande volume de dados vetoriais
- **API Gateway**: Para rate limiting e load balancing

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-ferramenta`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova ferramenta'`)
4. Push para a branch (`git push origin feature/nova-ferramenta`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é distribuído sob a licença MIT. Ver arquivo LICENSE para detalhes.

## 🙏 Agradecimentos

- Agno framework por facilitar a criação de agentes
- ChromaDB pela base vetorial eficiente
- Comunidade open-source pelas bibliotecas utilizadas

## 📞 Suporte

Para questões ou problemas:
1. Verifique os logs em `logs/agent.log`
2. Valide sua configuração com `python -m src.main config`
3. Abra uma issue no repositório

---

**Nota**: Este é um projeto de demonstração técnica. Os preços mostrados são simulados e não refletem valores reais de mercado.
