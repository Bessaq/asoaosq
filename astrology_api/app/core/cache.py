"""
Módulo para cache de cálculos astrológicos.

Este módulo implementa um sistema de cache para cálculos astrológicos frequentes,
reduzindo o tempo de resposta para requisições repetidas.
"""
from typing import Dict, Any, Optional, Tuple
import time
import pickle
import os
import hashlib
import json

# Diretório para armazenar o cache
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "cache")

# Verificar se o diretório de cache existe, caso contrário, criá-lo
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Cache em memória para acesso rápido
MEMORY_CACHE = {}

# Tempo de expiração do cache em segundos (24 horas)
CACHE_EXPIRATION = 24 * 60 * 60

def get_cache_key(prefix: str, **kwargs) -> str:
    """
    Gera uma chave de cache baseada nos parâmetros.
    
    Args:
        prefix (str): Prefixo para a chave (ex: 'natal', 'transit').
        **kwargs: Parâmetros para gerar a chave.
        
    Returns:
        str: Chave de cache.
    """
    # Criar uma string representando os parâmetros
    param_str = json.dumps(kwargs, sort_keys=True)
    
    # Gerar um hash SHA-256 da string
    hash_obj = hashlib.sha256(param_str.encode())
    hash_str = hash_obj.hexdigest()
    
    # Retornar a chave no formato prefix_hash
    return f"{prefix}_{hash_str}"

def get_from_cache(key: str) -> Optional[Any]:
    """
    Recupera um valor do cache.
    
    Args:
        key (str): Chave do cache.
        
    Returns:
        Optional[Any]: Valor do cache ou None se não encontrado ou expirado.
    """
    # Verificar primeiro no cache em memória
    if key in MEMORY_CACHE:
        timestamp, value = MEMORY_CACHE[key]
        
        # Verificar se o cache expirou
        if time.time() - timestamp < CACHE_EXPIRATION:
            return value
        else:
            # Remover do cache em memória se expirou
            del MEMORY_CACHE[key]
    
    # Verificar no cache em disco
    cache_file = os.path.join(CACHE_DIR, f"{key}.pickle")
    if os.path.exists(cache_file):
        # Verificar a data de modificação do arquivo
        mod_time = os.path.getmtime(cache_file)
        
        # Verificar se o cache expirou
        if time.time() - mod_time < CACHE_EXPIRATION:
            try:
                with open(cache_file, 'rb') as f:
                    value = pickle.load(f)
                
                # Atualizar o cache em memória
                MEMORY_CACHE[key] = (time.time(), value)
                
                return value
            except:
                # Em caso de erro ao carregar o cache, remover o arquivo
                os.remove(cache_file)
        else:
            # Remover o arquivo se expirou
            os.remove(cache_file)
    
    return None

def save_to_cache(key: str, value: Any) -> None:
    """
    Salva um valor no cache.
    
    Args:
        key (str): Chave do cache.
        value (Any): Valor a ser armazenado.
    """
    # Salvar no cache em memória
    MEMORY_CACHE[key] = (time.time(), value)
    
    # Salvar no cache em disco
    cache_file = os.path.join(CACHE_DIR, f"{key}.pickle")
    try:
        with open(cache_file, 'wb') as f:
            pickle.dump(value, f)
    except:
        # Em caso de erro ao salvar, apenas ignorar
        pass

def clear_cache() -> None:
    """
    Limpa todo o cache.
    """
    # Limpar cache em memória
    MEMORY_CACHE.clear()
    
    # Limpar cache em disco
    for filename in os.listdir(CACHE_DIR):
        file_path = os.path.join(CACHE_DIR, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except:
            pass

def clear_expired_cache() -> None:
    """
    Limpa apenas o cache expirado.
    """
    current_time = time.time()
    
    # Limpar cache em memória
    keys_to_remove = []
    for key, (timestamp, _) in MEMORY_CACHE.items():
        if current_time - timestamp >= CACHE_EXPIRATION:
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        del MEMORY_CACHE[key]
    
    # Limpar cache em disco
    for filename in os.listdir(CACHE_DIR):
        file_path = os.path.join(CACHE_DIR, filename)
        try:
            if os.path.isfile(file_path):
                mod_time = os.path.getmtime(file_path)
                if current_time - mod_time >= CACHE_EXPIRATION:
                    os.remove(file_path)
        except:
            pass
