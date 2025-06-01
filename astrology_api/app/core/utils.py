"""
Módulo de utilitários para a aplicação AstroAPI.

Este módulo contém funções auxiliares e utilitários gerais para a aplicação.
"""
import base64
from typing import Dict, Any, Optional
import pytz
from datetime import datetime

def validate_timezone(tz_str: str) -> bool:
    """
    Valida se a string de fuso horário é válida.
    
    Args:
        tz_str (str): String de fuso horário a ser validada.
        
    Returns:
        bool: True se a string de fuso horário for válida, False caso contrário.
    """
    try:
        pytz.timezone(tz_str)
        return True
    except pytz.exceptions.UnknownTimeZoneError:
        return False

def validate_date(year: int, month: int, day: int) -> bool:
    """
    Valida se a data é válida.
    
    Args:
        year (int): Ano.
        month (int): Mês.
        day (int): Dia.
        
    Returns:
        bool: True se a data for válida, False caso contrário.
    """
    try:
        datetime(year, month, day)
        return True
    except ValueError:
        return False

def validate_time(hour: int, minute: int) -> bool:
    """
    Valida se a hora é válida.
    
    Args:
        hour (int): Hora (0-23).
        minute (int): Minuto (0-59).
        
    Returns:
        bool: True se a hora for válida, False caso contrário.
    """
    return 0 <= hour <= 23 and 0 <= minute <= 59

def svg_to_base64(svg_content: str) -> Dict[str, str]:
    """
    Converte o conteúdo SVG para Base64.
    
    Args:
        svg_content (str): Conteúdo SVG.
        
    Returns:
        Dict[str, str]: Dicionário com o conteúdo SVG em Base64 e o URI de dados.
    """
    # Codificar o conteúdo SVG em Base64
    svg_bytes = svg_content.encode("utf-8")
    svg_base64 = base64.b64encode(svg_bytes).decode("utf-8")
    
    # Criar o URI de dados
    data_uri = f"data:image/svg+xml;base64,{svg_base64}"
    
    return {
        "svg_base64": svg_base64,
        "data_uri": data_uri
    }

def format_interpretation_result(result: Dict[str, Any], language: str = "pt") -> Dict[str, Any]:
    """
    Formata o resultado da interpretação.
    
    Args:
        result (Dict[str, Any]): Resultado da interpretação.
        language (str, opcional): Idioma para os textos. Padrão é "pt".
        
    Returns:
        Dict[str, Any]: Resultado da interpretação formatado.
    """
    # Aqui pode-se implementar lógica específica para formatação
    # Por enquanto, apenas retornamos o resultado sem modificação
    return result
