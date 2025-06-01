"""
Router para os endpoints de retornos solares e lunares.

Este módulo contém os endpoints relacionados ao cálculo de retornos solares e lunares.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional, Any

from ..schemas.models import ReturnRequest, ReturnResponse
from ..core.calculations import (
    create_astrological_subject,
    get_planet_data,
    get_houses_data,
    get_return_chart,
    get_aspects_data
)
from ..core.utils import validate_date, validate_timezone, validate_time
from ..interpretations.text_search import get_planet_interpretation
from ..security import verify_api_key

# Criar o router
router = APIRouter(
    prefix="/api/v1",
    tags=["Returns"],
    dependencies=[Depends(verify_api_key)],
)

@router.post("/solar-return", response_model=ReturnResponse)
async def calculate_solar_return(request: ReturnRequest):
    """
    Calcula o retorno solar para um ano específico.
    
    Args:
        request (ReturnRequest): Dados para o cálculo do retorno solar.
        
    Returns:
        ReturnResponse: Dados do retorno solar calculado.
        
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
        
        # Validar o ano do retorno
        return_year = request.return_year
        if return_year < 1900 or return_year > 2100:
            raise HTTPException(status_code=400, detail="Ano de retorno fora do intervalo válido (1900-2100)")
        
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
        
        # Calcular o retorno solar
        return_subject = get_return_chart(
            natal_subject, 
            return_year,
            return_type="solar",
            location_longitude=request.location_longitude if request.location_longitude is not None else natal.longitude,
            location_latitude=request.location_latitude if request.location_latitude is not None else natal.latitude,
            location_tz_str=request.location_tz_str if request.location_tz_str is not None else natal.tz_str
        )
        
        # Obter os dados dos planetas do retorno
        return_planets = get_planet_data(return_subject, request.language)
        
        # Obter os dados das casas do retorno
        return_houses = get_houses_data(return_subject, request.language)
        
        # Obter os aspectos entre planetas do retorno e natais
        aspects = []
        if request.include_natal_comparison:
            aspects = get_aspects_data(
                return_subject, 
                natal_subject, 
                request.language, 
                cross_aspects=True
            )
        
        # Obter interpretações, se solicitado
        interpretations = None
        if request.include_interpretations:
            interpretations = {
                "planets": {},
                "houses": {},
                "aspects": []
            }
            
            # Interpretações dos planetas do retorno
            for planet_key, planet_data in return_planets.items():
                planet_name = planet_data.name
                sign = planet_data.sign
                house = planet_data.house
                
                interp = get_planet_interpretation(planet_name, sign, house, request.language)
                if interp:
                    interpretations["planets"][planet_key] = interp
            
            # Interpretações das casas
            for house_num, house_data in return_houses.items():
                sign = house_data.sign
                
                interp = get_planet_interpretation(f"Casa {house_num}", sign, 0, request.language)
                if interp:
                    interpretations["houses"][house_num] = interp
            
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
        response = ReturnResponse(
            input_data=request,
            return_planets=return_planets,
            return_houses=return_houses,
            return_date=return_subject.utc_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            aspects=aspects,
            house_system=natal.house_system,
            interpretations=interpretations
        )
        
        return response
        
    except Exception as e:
        # Logar o erro
        print(f"Erro ao calcular retorno solar: {str(e)}")
        
        # Retornar erro ao cliente
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao calcular retorno solar: {str(e)}"
        )

@router.post("/lunar-return", response_model=ReturnResponse)
async def calculate_lunar_return(request: ReturnRequest):
    """
    Calcula o retorno lunar mais próximo de uma data específica.
    
    Args:
        request (ReturnRequest): Dados para o cálculo do retorno lunar.
        
    Returns:
        ReturnResponse: Dados do retorno lunar calculado.
        
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
        
        # Validar o ano e mês do retorno
        return_year = request.return_year
        return_month = request.return_month
        if return_year < 1900 or return_year > 2100:
            raise HTTPException(status_code=400, detail="Ano de retorno fora do intervalo válido (1900-2100)")
        
        if return_month is not None and (return_month < 1 or return_month > 12):
            raise HTTPException(status_code=400, detail="Mês de retorno inválido (1-12)")
        
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
        
        # Calcular o retorno lunar
        return_subject = get_return_chart(
            natal_subject, 
            return_year,
            return_month=return_month,
            return_type="lunar",
            location_longitude=request.location_longitude if request.location_longitude is not None else natal.longitude,
            location_latitude=request.location_latitude if request.location_latitude is not None else natal.latitude,
            location_tz_str=request.location_tz_str if request.location_tz_str is not None else natal.tz_str
        )
        
        # Obter os dados dos planetas do retorno
        return_planets = get_planet_data(return_subject, request.language)
        
        # Obter os dados das casas do retorno
        return_houses = get_houses_data(return_subject, request.language)
        
        # Obter os aspectos entre planetas do retorno e natais
        aspects = []
        if request.include_natal_comparison:
            aspects = get_aspects_data(
                return_subject, 
                natal_subject, 
                request.language, 
                cross_aspects=True
            )
        
        # Obter interpretações, se solicitado
        interpretations = None
        if request.include_interpretations:
            interpretations = {
                "planets": {},
                "houses": {},
                "aspects": []
            }
            
            # Interpretações dos planetas do retorno
            for planet_key, planet_data in return_planets.items():
                planet_name = planet_data.name
                sign = planet_data.sign
                house = planet_data.house
                
                interp = get_planet_interpretation(planet_name, sign, house, request.language)
                if interp:
                    interpretations["planets"][planet_key] = interp
            
            # Interpretações das casas
            for house_num, house_data in return_houses.items():
                sign = house_data.sign
                
                interp = get_planet_interpretation(f"Casa {house_num}", sign, 0, request.language)
                if interp:
                    interpretations["houses"][house_num] = interp
            
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
        response = ReturnResponse(
            input_data=request,
            return_planets=return_planets,
            return_houses=return_houses,
            return_date=return_subject.utc_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            aspects=aspects,
            house_system=natal.house_system,
            interpretations=interpretations
        )
        
        return response
        
    except Exception as e:
        # Logar o erro
        print(f"Erro ao calcular retorno lunar: {str(e)}")
        
        # Retornar erro ao cliente
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao calcular retorno lunar: {str(e)}"
        )
