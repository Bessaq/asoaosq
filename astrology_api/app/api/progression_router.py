"""
Router para os endpoints de progressões astrológicas.

Este módulo contém os endpoints relacionados ao cálculo de progressões secundárias.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional, Any

from ..schemas.models import ProgressionRequest, ProgressionResponse
from ..core.calculations import (
    create_astrological_subject,
    get_planet_data,
    get_houses_data,
    get_progressed_chart,
    get_aspects_data
)
from ..core.utils import validate_date, validate_timezone, validate_time
from ..interpretations.text_search import get_planet_interpretation
from ..security import verify_api_key

# Criar o router
router = APIRouter(
    prefix="/api/v1",
    tags=["Progressions"],
    dependencies=[Depends(verify_api_key)],
)

@router.post("/progressions", response_model=ProgressionResponse)
async def calculate_progressions(request: ProgressionRequest):
    """
    Calcula as progressões secundárias para um mapa natal.
    
    Args:
        request (ProgressionRequest): Dados para o cálculo das progressões.
        
    Returns:
        ProgressionResponse: Dados das progressões calculadas.
        
    Raises:
        HTTPException: Se ocorrer um erro durante o cálculo.
    """
    try:
        # Validar os dados de entrada do mapa natal
        natal = request.natal_chart
        if not validate_date(natal.year, natal.month, natal.day):
            raise HTTPException(status_code=400, detail="Data natal inválida")
        
        if not validate_time(natal.hour, natal.minute):
            raise HTTPException(status_code=400, detail="Hora natal inválida")
        
        if not validate_timezone(natal.tz_str):
            raise HTTPException(status_code=400, detail="Fuso horário natal inválido")
        
        # Validar os dados da data de progressão
        prog_date = request.progression_date
        if not validate_date(prog_date.year, prog_date.month, prog_date.day):
            raise HTTPException(status_code=400, detail="Data de progressão inválida")
        
        # Criar o objeto AstrologicalSubject para o mapa natal
        natal_subject = create_astrological_subject(
            name=natal.name if natal.name else "NatalChart",
            year=natal.year,
            month=natal.month,
            day=natal.day,
            hour=natal.hour,
            minute=natal.minute,
            longitude=natal.longitude,
            latitude=natal.latitude,
            tz_str=natal.tz_str,
            house_system=natal.house_system
        )
        
        # Calcular as progressões
        progressed_subject = get_progressed_chart(
            natal_subject, 
            prog_date.year, 
            prog_date.month, 
            prog_date.day
        )
        
        # Obter os dados dos planetas progressados
        progressed_planets = get_planet_data(progressed_subject, request.language)
        
        # Obter os dados das casas (usando o mapa natal como referência)
        houses = get_houses_data(natal_subject, request.language)
        
        # Obter os aspectos entre planetas natais e progressados
        aspects = []
        if request.include_natal_comparison:
            # Obter os dados dos planetas natais
            natal_planets = get_planet_data(natal_subject, request.language)
            
            # Calcular aspectos entre planetas natais e progressados
            # (Esta função precisa ser implementada no módulo calculations.py)
            aspects = get_aspects_data(
                progressed_subject, 
                natal_subject, 
                request.language, 
                cross_aspects=True
            )
        
        # Obter interpretações, se solicitado
        interpretations = None
        if request.include_interpretations:
            interpretations = {
                "planets": {},
                "aspects": []
            }
            
            # Interpretações dos planetas progressados
            for planet_key, planet_data in progressed_planets.items():
                planet_name = planet_data.name
                sign = planet_data.sign
                house = planet_data.house
                
                interp = get_planet_interpretation(planet_name, sign, house, request.language)
                if interp:
                    interpretations["planets"][planet_key] = interp
            
            # Interpretações dos aspectos
            for aspect in aspects:
                p1_name = aspect.p1_name
                p2_name = aspect.p2_name
                aspect_name = aspect.aspect
                
                interp = get_planet_interpretation(f"{p1_name} {aspect_name} {p2_name}", "", 0, request.language)
                if interp:
                    interpretations["aspects"].append({
                        "p1": p1_name,
                        "p2": p2_name,
                        "aspect": aspect_name,
                        "interpretation": interp
                    })
        
        # Criar a resposta
        response = ProgressionResponse(
            input_data=request,
            progressed_planets=progressed_planets,
            natal_houses=houses,
            aspects=aspects,
            house_system=natal.house_system,
            interpretations=interpretations
        )
        
        return response
        
    except Exception as e:
        # Logar o erro
        print(f"Erro ao calcular progressões: {str(e)}")
        
        # Retornar erro ao cliente
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao calcular progressões: {str(e)}"
        )
