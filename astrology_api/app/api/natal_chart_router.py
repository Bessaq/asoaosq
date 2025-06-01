"""
Router para os endpoints de mapa natal.

Este módulo contém os endpoints relacionados ao cálculo de mapas natais.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

from ..schemas.models import NatalChartRequest, NatalChartResponse
from ..core.calculations import (
    create_astrological_subject,
    get_planet_data,
    get_houses_data,
    get_aspects_data
)
from ..core.utils import validate_date, validate_timezone, validate_time
from ..security import verify_api_key

# Criar o router
router = APIRouter(
    prefix="/api/v1",
    tags=["Natal Chart"],
    dependencies=[Depends(verify_api_key)],
)

@router.post("/natal_chart", response_model=NatalChartResponse)
async def calculate_natal_chart(request: NatalChartRequest):
    """
    Calcula um mapa natal com base nos dados fornecidos.
    
    Args:
        request (NatalChartRequest): Dados para o cálculo do mapa natal.
        
    Returns:
        NatalChartResponse: Dados do mapa natal calculado.
        
    Raises:
        HTTPException: Se ocorrer um erro durante o cálculo.
    """
    try:
        # Validar os dados de entrada
        if not validate_date(request.year, request.month, request.day):
            raise HTTPException(status_code=400, detail="Data inválida")
        
        if not validate_time(request.hour, request.minute):
            raise HTTPException(status_code=400, detail="Hora inválida")
        
        if not validate_timezone(request.tz_str):
            raise HTTPException(status_code=400, detail="Fuso horário inválido")
        
        # Criar o objeto AstrologicalSubject
        subject = create_astrological_subject(
            name=request.name if request.name else "NatalChart",
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            longitude=request.longitude,
            latitude=request.latitude,
            tz_str=request.tz_str,
            house_system=request.house_system
        )
        
        # Obter os dados dos planetas
        planets = get_planet_data(subject, request.language)
        
        # Obter os dados das casas
        houses = get_houses_data(subject, request.language)
        
        # Obter os dados dos aspectos
        aspects = get_aspects_data(subject, request.language)
        
        # Criar a resposta
        response = NatalChartResponse(
            input_data=request,
            planets=planets,
            houses=houses,
            ascendant=houses["1"],
            midheaven=houses["10"],
            aspects=aspects,
            house_system=request.house_system,
            interpretations=None  # Implementação futura
        )
        
        return response
        
    except Exception as e:
        # Logar o erro
        print(f"Erro ao calcular mapa natal: {str(e)}")
        
        # Retornar erro ao cliente
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao calcular mapa natal: {str(e)}"
        )
