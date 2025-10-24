"""
Configuração simples para o agente IA.
"""
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class Config:
    """Configuração básica da aplicação."""

    # Chave da OpenAI (obrigatória)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Configurações básicas
    CHROMA_DB_PATH: str = "./data/chromadb"
    LOG_LEVEL: str = "INFO"
    EXTERNAL_API_URL: str = "http://localhost:8001"

    @classmethod
    def validar(cls) -> bool:
        """Verifica se a configuração essencial está presente."""
        if not cls.OPENAI_API_KEY:
            print("ERRO: OPENAI_API_KEY não encontrada!")
            print("Configure no arquivo .env")
            return False
        return True
