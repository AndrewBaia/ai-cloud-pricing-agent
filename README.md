# Agente IA de Precificação em Nuvem

## O Que É

Um agente de IA autônomo que ajuda usuários a entenderem e compararem preços de GPUs nos principais provedores de nuvem: AWS, Azure e Google Cloud Platform (GCP).

## Como Funciona

O agente usa inteligência artificial para:
- **Buscar preços** de GPUs em diferentes provedores
- **Comparar custos** entre plataformas
- **Dar recomendações** sobre qual opção é mais econômica
- **Explicar diferenças** técnicas entre instâncias

## Ferramentas Usadas

1. **Framework Agno** - Para criar o agente inteligente
2. **ChromaDB** - Base de dados vetorial para conhecimento
3. **GPT-4 da OpenAI** - Cérebro do agente
4. **Python** - Linguagem de programação

## Arquitetura Simples

```
Usuário → Agente Agno → 3 Ferramentas
                      ↓
               Resposta Estruturada
```

**As 3 ferramentas:**
- 🔍 **Busca Local**: Procura preços em dados JSON
- 🧠 **Base de Conhecimento**: ChromaDB com dicas de otimização
- 🌐 **API Externa**: Simula comparações de mercado

## Instalação Rápida

1. **Instale Python** (versão 3.11 ou superior)

2. **Clone e instale**:
   ```bash
   git clone <repository-url>
   cd ai-cloud-pricing-agent
   pip install -r requirements.txt
   ```

3. **Configure API key**:
   ```bash
   # Crie arquivo .env
   echo "OPENAI_API_KEY=sua-chave-aqui" > .env
   ```

## Como Executar

### Opção 1: Docker Compose com API FastAPI (Recomendado)
```bash
# Construir e executar a API FastAPI
docker-compose up --build

# A API ficará disponível em: http://localhost:8000
# Documentação automática: http://localhost:8000/docs

# Para rebuild quando fizer mudanças
docker-compose up --build
```

#### Como usar a API FastAPI:
```bash
# 1. Verificar se a API está funcionando
curl http://localhost:8000/health

# 2. Ver documentação interativa da API
# Abra no navegador: http://localhost:8000/docs

# 3. Fazer uma pergunta (via POST)
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "Quanto custa GPU V100 na AWS?"}'

# 4. Ou usar o script de teste Python
python test_docker.py

# 5. Ou via linha de comando (exemplo antigo)
docker-compose run --rm ai-agent python src/main.py "Qual é o preço da GPU V100 na Azure?"
```

### 🔧 Troubleshooting (Resolução de Problemas)

#### Docker não conecta:
```bash
# 1. Verificar se Docker Desktop está rodando
# Abra o Docker Desktop manualmente

# 2. Verificar status do Docker
docker info

# 3. Reiniciar Docker Desktop se necessário
```

#### Porta 8000 ocupada:
```yaml
# Modifique no docker-compose.yml:
ports:
  - "8001:8000"  # Muda para porta 8001 local
```

#### Erro de permissão nos logs:
- Os diretórios `logs/` e `data/chromadb/` são criados automaticamente no container
- Não há necessidade de criar manualmente

#### API retorna erro 503:
- Aguardar alguns segundos para o agente inicializar completamente
- Verificar logs: `docker-compose logs ai-agent`

### Opção 2: Docker Direto
```bash
# Construir a imagem
docker build -t ai-agent .

# Executar com arquivo .env
docker run --rm --env-file test.env ai-agent python src/main.py "Quanto custa GPU na AWS?"
```

### Opção 3: Localmente
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar
python src/main.py "Qual é o preço da GPU V100 na AWS?"
```

## Como Usar

### Exemplo Básico
```bash
python src/main.py "Quanto custa uma GPU V100 na AWS?"
```

### Exemplos de Perguntas
- "Compare preços de GPU entre AWS e Azure"
- "Qual é a opção mais barata para machine learning?"
- "Explique as diferenças entre instâncias P3 e NC6"

## Arquivos Importantes

- `src/main.py` - Ponto de entrada
- `src/agents/cloud_pricing_agent.py` - O agente principal
- `src/tools/` - As 3 ferramentas
- `data/pricing_data.json` - Dados de preços mock
- `docs/architecture.md` - Documentação técnica completa

## Resultado de Teste

Exemplo de saída do agente:

```
==================================================
RESPOSTA DO AGENTE:
==================================================
Baseado nos dados disponíveis, uma GPU V100 na AWS custa $3.06 por hora na instância P3.2xlarge.

Para comparar com Azure, uma instância similar (NC6s_v3) custa $2.80 por hora, representando uma economia de 8.5%.

Recomendação: Considere Azure para workloads que não exigem a performance máxima da AWS.
==================================================
```

## Para Desenvolvedores

### Estrutura do Projeto
```
src/
├── main.py                 # CLI principal
├── agents/
│   └── cloud_pricing_agent.py  # Agente Agno
└── tools/                  # As 3 ferramentas
    ├── search_tool.py      # Busca local
    ├── vector_store.py     # ChromaDB
    └── external_api.py     # API externa mock
```

### Principais Componentes

**Agente Principal:**
```python
class CloudPricingAgent:
    def __init__(self):
        self.search_tool = MockSearchTool()
        self.vector_store = VectorStoreTool()
        self.external_api = ExternalAPITool()
        self.agent = self._create_agent()
```

**Ferramentas Disponíveis:**
- `search_gpu_pricing()` - Busca preços
- `compare_cloud_prices()` - Compara provedores
- `get_market_trends()` - Tendências de mercado
- `search_knowledge_base()` - Dicas de otimização

## Próximos Passos

- [ ] Integrar com APIs reais dos provedores
- [ ] Adicionar mais provedores de nuvem
- [ ] Implementar cache inteligente
- [ ] Criar interface web
- [ ] Adicionar testes automatizados completos
