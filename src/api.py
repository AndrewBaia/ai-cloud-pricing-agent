#!/usr/bin/env python3
"""
API FastAPI para o Agente IA de Precificação em Nuvem.

Esta API fornece endpoints HTTP para interagir com o agente de IA,
permitindo fazer perguntas sobre preços de GPU via interface web.
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger

# Importar o agente principal
from agents import CloudPricingAgent
from utils import setup_logging, Config

# Modelo para requisições
class QueryRequest(BaseModel):
    question: str

# Configurar FastAPI
app = FastAPI(
    title="Agente IA de Precificação em Nuvem",
    description="API para consultar preços de GPU nos provedores de nuvem AWS, Azure e GCP",
    version="1.0.0"
)

# Configurar CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instância global do agente (inicializada na startup)
agent = None

@app.on_event("startup")
async def startup_event():
    """Inicializa o agente quando a API inicia."""
    global agent

    # Validar configuração
    if not Config.validar():
        logger.error("Configuração inválida - abortando inicialização")
        raise RuntimeError("OPENAI_API_KEY não configurada")

    # Configurar logging
    setup_logging()

    # Inicializar agente
    try:
        agent = CloudPricingAgent()
        logger.info("Agente IA inicializado com sucesso na API")
    except Exception as e:
        logger.error(f"Erro ao inicializar agente: {e}")
        raise RuntimeError(f"Falha na inicialização do agente: {e}")

@app.get("/")
async def root():
    """Endpoint raiz com informações da API."""
    return {
        "message": "Agente IA de Precificação em Nuvem",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "Esta documentação",
            "POST /ask": "Fazer pergunta ao agente",
            "GET /health": "Verificar saúde da API"
        },
        "exemplos": [
            "Quanto custa uma GPU V100 na AWS?",
            "Qual é mais barato: AWS ou Azure para GPU K80?",
            "Como otimizar custos de GPU na nuvem?"
        ]
    }

@app.get("/health")
async def health_check():
    """Verifica se a API está funcionando."""
    return {
        "status": "healthy",
        "agent_ready": agent is not None,
        "timestamp": "2025-01-20T13:15:00Z"  # Em produção, use datetime.utcnow()
    }

@app.post("/ask")
async def ask_agent(request: QueryRequest):
    """
    Faz uma pergunta ao agente IA.

    Args:
        request: Objeto contendo a pergunta do usuário

    Returns:
        dict: Resposta estruturada do agente
    """
    if not agent:
        raise HTTPException(status_code=503, detail="Agente não inicializado")

    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Pergunta não pode estar vazia")

    try:
        logger.info(f"Pergunta recebida via API: '{request.question}'")

        # Processar pergunta com o agente
        resposta = agent.analyze_query(request.question.strip())

        logger.info("Pergunta processada com sucesso via API")

        return {
            "success": True,
            "question": request.question,
            "answer": resposta,
            "timestamp": "2025-01-20T13:15:00Z"  # Em produção, use datetime.utcnow()
        }

    except Exception as e:
        logger.error(f"Erro ao processar pergunta via API: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
