"""
Configuração simples de logging.
"""
import os
from loguru import logger

from .config import Config


def setup_logging():
    """Configura logging básico."""
    # Cria diretório de logs se não existir
    os.makedirs("logs", exist_ok=True)

    # Remove logger padrão
    logger.remove()

    # Adiciona logger no console
    logger.add(
        "logs/agent.log",
        level=Config.LOG_LEVEL,
        rotation="10 MB"
    )

    logger.info("Logging configurado")


def get_logger():
    """Retorna instância do logger."""
    return logger
