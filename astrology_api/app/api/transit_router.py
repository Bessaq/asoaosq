"""
Router para os endpoints de trânsitos.

Este módulo contém os endpoints relacionados ao cálculo de trânsitos planetários.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

from ..schemas.models import (
    TransitRequest, TransitResponse,
    TransitsToNatalRequest, TransitsToNatalResponse
)
from ..core.calculations import (
    create_astrological_subject,
    get_planet_data,
    get_houses_data,
    get_aspects_data,
    get_aspects_between_subjects
)
from ..core.utils import validate_date, validate_timezone, validate_time
from ..security import verify_api_key

# Criar o router
router = APIRouter(
    prefix="/api/v1",
    tags=["Transits"],
    dependencies=[Depends(verify_api_key)],
)

@router.post("/transit_chart", response_model=TransitResponse)
async def calculate_transit_chart(request: TransitRequest):
    """
    Calcula um mapa de trânsito com base nos dados fornecidos.
    
    Args:
        request (TransitRequest): Dados para o cálculo do mapa de trânsito.
        
    Returns:
        TransitResponse: Dados do mapa de trânsito calculado.
        
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
            name="TransitChart",
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
        
        # Criar a resposta
        response = TransitResponse(
            input_data=request,
            planets=planets,
            house_system=request.house_system,
            interpretations=None  # Implementação futura
        )
        
        return response
        
    except Exception as e:
        # Logar o erro
        print(f"Erro ao calcular mapa de trânsito: {str(e)}")
        
        # Retornar erro ao cliente
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao calcular mapa de trânsito: {str(e)}"
        )

@router.post("/transits_to_natal", response_model=TransitsToNatalResponse)
async def calculate_transits_to_natal(request: TransitsToNatalRequest):
    """
    Calcula os trânsitos sobre um mapa natal.
    
    Args:
        request (TransitsToNatalRequest): Dados para o cálculo dos trânsitos sobre o mapa natal.
        
    Returns:
        TransitsToNatalResponse: Dados dos trânsitos sobre o mapa natal.
        
    Raises:
        HTTPException: Se ocorrer um erro durante o cálculo.
    """
    try:
        # Validar os dados de entrada do mapa natal
        natal_req = request.natal
        if not validate_date(natal_req.year, natal_req.month, natal_req.day):
            raise HTTPException(status_code=400, detail="Data natal inválida")
        
        if not validate_time(natal_req.hour, natal_req.minute):
            raise HTTPException(status_code=400, detail="Hora natal inválida")
        
        if not validate_timezone(natal_req.tz_str):
            raise HTTPException(status_code=400, detail="Fuso horário natal inválido")
        
        # Validar os dados de entrada do mapa de trânsito
        transit_req = request.transit
        if not validate_date(transit_req.year, transit_req.month, transit_req.day):
            raise HTTPException(status_code=400, detail="Data de trânsito inválida")
        
        if not validate_time(transit_req.hour, transit_req.minute):
            raise HTTPException(status_code=400, detail="Hora de trânsito inválida")
        
        if not validate_timezone(transit_req.tz_str):
            raise HTTPException(status_code=400, detail="Fuso horário de trânsito inválido")
        
        # Criar o objeto AstrologicalSubject para o mapa natal
        natal_subject = create_astrological_subject(
            name=natal_req.name if natal_req.name else "NatalChart",
            year=natal_req.year,
            month=natal_req.month,
            day=natal_req.day,
            hour=natal_req.hour,
            minute=natal_req.minute,
            longitude=natal_req.longitude,
            latitude=natal_req.latitude,
            tz_str=natal_req.tz_str,
            house_system=natal_req.house_system
        )
        
        # Criar o objeto AstrologicalSubject para o mapa de trânsito
        transit_subject = create_astrological_subject(
            name="TransitChart",
            year=transit_req.year,
            month=transit_req.month,
            day=transit_req.day,
            hour=transit_req.hour,
            minute=transit_req.minute,
            longitude=transit_req.longitude,
            latitude=transit_req.latitude,
            tz_str=transit_req.tz_str,
            house_system=transit_req.house_system
        )
        
        # Obter os dados dos planetas natais
        natal_planets = get_planet_data(natal_subject, natal_req.language)
        
        # Obter os dados dos planetas de trânsito
        transit_planets = get_planet_data(transit_subject, transit_req.language)
        
        # Obter os aspectos entre os planetas natais e de trânsito
        aspects = get_aspects_between_subjects(
            natal_subject,
            transit_subject,
            "natal",
            "transit",
            transit_req.language
        )
        
        # Criar a resposta
        response = TransitsToNatalResponse(
            input_data=request,
            natal_planets=natal_planets,
            transit_planets=transit_planets,
            aspects=aspects,
            natal_house_system=natal_req.house_system,
            transit_house_system=transit_req.house_system,
            interpretations=None  # Implementação futura
        )
        
        return response
        
    except Exception as e:
        # Logar o erro
        print(f"Erro ao calcular trânsitos sobre mapa natal: {str(e)}")
        
        # Retornar erro ao cliente
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao calcular trânsitos sobre mapa natal: {str(e)}"
        )
