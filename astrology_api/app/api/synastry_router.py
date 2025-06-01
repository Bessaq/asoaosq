"""
Router para os endpoints de sinastria (comparação de mapas natais).

Este módulo contém os endpoints relacionados ao cálculo de sinastria entre dois mapas natais.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional

from ..schemas.models import SynastryRequest, SynastryResponse, HouseSystemType, LanguageType
from ..core.calculations import (
    create_astrological_subject,
    get_planet_data,
    get_synastry_aspects_data
)
from ..core.utils import validate_date, validate_timezone, validate_time
from ..interpretations.text_search import get_aspect_interpretation
from ..security import verify_api_key

# Criar o router
router = APIRouter(
    prefix="/api/v1",
    tags=["Synastry"],
    dependencies=[Depends(verify_api_key)],
)

@router.post("/synastry", response_model=SynastryResponse)
async def calculate_synastry(request: SynastryRequest):
    """
    Calcula a sinastria (comparação) entre dois mapas natais.
    
    Args:
        request (SynastryRequest): Dados para o cálculo da sinastria.
        
    Returns:
        SynastryResponse: Dados da sinastria calculada.
        
    Raises:
        HTTPException: Se ocorrer um erro durante o cálculo.
    """
    try:
        # Validar os dados de entrada do primeiro mapa
        chart1 = request.chart1
        if not validate_date(chart1.year, chart1.month, chart1.day):
            raise HTTPException(status_code=400, detail="Data do primeiro mapa inválida")
        
        if not validate_time(chart1.hour, chart1.minute):
            raise HTTPException(status_code=400, detail="Hora do primeiro mapa inválida")
        
        if not validate_timezone(chart1.tz_str):
            raise HTTPException(status_code=400, detail="Fuso horário do primeiro mapa inválido")
        
        # Validar os dados de entrada do segundo mapa
        chart2 = request.chart2
        if not validate_date(chart2.year, chart2.month, chart2.day):
            raise HTTPException(status_code=400, detail="Data do segundo mapa inválida")
        
        if not validate_time(chart2.hour, chart2.minute):
            raise HTTPException(status_code=400, detail="Hora do segundo mapa inválida")
        
        if not validate_timezone(chart2.tz_str):
            raise HTTPException(status_code=400, detail="Fuso horário do segundo mapa inválido")
        
        # Usar valores padrão se não fornecidos
        house_system1: HouseSystemType = chart1.house_system or "Placidus"
        house_system2: HouseSystemType = chart2.house_system or "Placidus"
        language: LanguageType = request.language or "pt"
        
        # Criar os objetos AstrologicalSubject
        subject1 = create_astrological_subject(
            name=chart1.name if chart1.name else "Chart1",
            year=chart1.year,
            month=chart1.month,
            day=chart1.day,
            hour=chart1.hour,
            minute=chart1.minute,
            longitude=chart1.longitude,
            latitude=chart1.latitude,
            tz_str=chart1.tz_str,
            house_system=house_system1
        )
        
        subject2 = create_astrological_subject(
            name=chart2.name if chart2.name else "Chart2",
            year=chart2.year,
            month=chart2.month,
            day=chart2.day,
            hour=chart2.hour,
            minute=chart2.minute,
            longitude=chart2.longitude,
            latitude=chart2.latitude,
            tz_str=chart2.tz_str,
            house_system=house_system2
        )
        
        # Obter os dados dos planetas para ambos os mapas
        planets1 = get_planet_data(subject1, language)
        planets2 = get_planet_data(subject2, language)
        
        # Obter os aspectos entre os planetas dos dois mapas
        aspects = get_synastry_aspects_data(subject1, subject2, language)
        
        # Obter interpretações dos aspectos, se solicitado
        interpretations = None
        if request.include_interpretations:
            interpretations = {
                "aspects": []
            }
            
            for aspect in aspects:
                p1_name = aspect.p1_name
                p2_name = aspect.p2_name
                aspect_name = aspect.aspect
                
                interp = get_aspect_interpretation(p1_name, p2_name, aspect_name, request.language)
                if interp:
                    interpretations["aspects"].append({
                        "p1": p1_name,
                        "p2": p2_name,
                        "aspect": aspect_name,
                        "interpretation": interp
                    })
        
        # Criar a resposta
        response = SynastryResponse(
            input_data=request,
            chart1_planets=planets1,
            chart2_planets=planets2,
            aspects=aspects,
            chart1_house_system=chart1.house_system,
            chart2_house_system=chart2.house_system,
            interpretations=interpretations
        )
        
        return response
        
    except Exception as e:
        # Logar o erro
        print(f"Erro ao calcular sinastria: {str(e)}")
        
        # Retornar erro ao cliente
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao calcular sinastria: {str(e)}"
        )
