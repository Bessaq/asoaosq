"""
Módulo de segurança para a aplicação AstroAPI.

Este módulo contém funcionalidades para autenticação e autorização.
"""
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da chave de API
API_KEY = os.getenv("API_KEY_ASTROLOGIA")
API_KEY_NAME = "X-API-KEY"

# Se não houver chave definida, usar uma padrão para desenvolvimento
if not API_KEY:
    API_KEY = "dev_key"
    print("AVISO: Usando chave de API padrão para desenvolvimento. Defina API_KEY_ASTROLOGIA no .env para produção.")

# Configurar o cabeçalho de chave de API
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Verifica se a chave de API é válida.
    
    Args:
        api_key (str): Chave de API fornecida no cabeçalho da requisição.
        
    Returns:
        str: A chave de API se for válida.
        
    Raises:
        HTTPException: Se a chave de API for inválida.
    """
    if api_key == API_KEY:
        return api_key
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Chave de API inválida",
        headers={"WWW-Authenticate": API_KEY_NAME},
    )
