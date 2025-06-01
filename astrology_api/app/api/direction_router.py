"""
Router para os endpoints de direções astrológicas.

Este módulo contém os endpoints relacionados ao cálculo de direções de arco solar e primárias.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from ..schemas.models import DirectionRequest, DirectionResponse, HouseSystemType, LanguageType
from ..core.calculations import (
    create_astrological_subject,
    get_planet_data,
    get_houses_data,
    calculate_solar_arc_directions,
    get_aspects_data
)
from ..core.utils import validate_date, validate_timezone, validate_time
from ..interpretations.text_search import get_planet_interpretation
from ..interpretations.translations import translate_sign, translate_aspect, translate_planet
from ..security import verify_api_key

# Criar o router
router = APIRouter(
    prefix="/api/v1",
    tags=["Directions"],
    dependencies=[Depends(verify_api_key)],
)

# Lista de signos em ordem
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def get_sign_name(sign_num: int) -> str:
    """Retorna o nome do signo baseado no número (1-12)"""
    if 1 <= sign_num <= 12:
        return ZODIAC_SIGNS[sign_num - 1]
    return "Unknown"

def calculate_house_position(longitude: float, house_cusps: List[float]) -> int:
    """
    Calcula a casa astrológica para uma dada longitude.
    
    Args:
        longitude (float): Longitude eclíptica
        house_cusps (List[float]): Lista de cúspides das casas
        
    Returns:
        int: Número da casa (1-12)
    """
    # Normalizar longitude para 0-360
    while longitude < 0:
        longitude += 360
    while longitude >= 360:
        longitude -= 360
    
    # Verificar cada casa
    for i in range(1, 13):
        cusp_start = house_cusps[i-1]
        cusp_end = house_cusps[i % 12]
        
        # Lidar com casas que cruzam 0°
        if cusp_end < cusp_start:
            if longitude >= cusp_start or longitude < cusp_end:
                return i
        else:
            if cusp_start <= longitude < cusp_end:
                return i
    
    return 1  # Default para a primeira casa se algo der errado

@router.post("/solar-arc", response_model=DirectionResponse)
async def calculate_solar_arc(request: DirectionRequest):
    """
    Calcula as direções de arco solar para um mapa natal.
    
    Args:
        request (DirectionRequest): Dados para o cálculo das direções.
        
    Returns:
        DirectionResponse: Dados das direções calculadas.
        
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
        
        # Validar os dados da data de direção
        direction_date = request.direction_date
        if not validate_date(direction_date.year, direction_date.month, direction_date.day):
            raise HTTPException(status_code=400, detail="Data de direção inválida")
            
        # Usar valores padrão para house_system e language se não fornecidos
        house_system: HouseSystemType = natal.house_system or "Placidus"
        language: LanguageType = request.language or "pt"
        
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
            house_system=house_system
        )
        
        # Calcular as direções de arco solar
        direction_date_obj = datetime(
            direction_date.year,
            direction_date.month,
            direction_date.day
        )
        
        solar_arc, directed_positions = calculate_solar_arc_directions(natal_subject, direction_date_obj)
        
        # Obter dados das casas natais
        houses = get_houses_data(natal_subject, language)
        
        # Criar um mapa com as posições direcionadas
        directed_planets = {}
        
        for planet_name, planet_data in get_planet_data(natal_subject, language).items():
            # Copiar os dados do planeta natal
            directed_planet = planet_data.copy()
            
            # Atualizar a longitude com a posição direcionada
            if planet_name in directed_positions:
                longitude = directed_positions[planet_name]
                directed_planet.longitude = longitude
                
                # Calcular o novo signo
                sign_num = int(longitude / 30) + 1
                sign = get_sign_name(sign_num)
                directed_planet.sign = translate_sign(sign, language)
                directed_planet.sign_original = sign
                directed_planet.sign_num = sign_num
                
                # Atualizar a casa
                house_cusps = [float(h.longitude) for h in houses.values()]
                directed_planet.house = calculate_house_position(longitude, house_cusps)
            
            directed_planets[planet_name] = directed_planet
        
        # Calcular aspectos entre planetas direcionados e natais
        natal_planets = get_planet_data(natal_subject, language)
        all_aspects = []
        
        for d_planet, d_data in directed_planets.items():
            for n_planet, n_data in natal_planets.items():
                # Calcular aspecto (simplificado)
                diff = abs(d_data.longitude - n_data.longitude) % 360
                for aspect_angle, aspect_name in [(0, "Conjunction"), (60, "Sextile"), 
                                              (90, "Square"), (120, "Trine"), (180, "Opposition")]:
                    if abs(diff - aspect_angle) <= 8:  # Orbe de 8 graus
                        all_aspects.append({
                            "p1_name": translate_planet(d_planet, language),
                            "p1_name_original": d_planet,
                            "p1_owner": "directed",
                            "p2_name": translate_planet(n_planet, language),
                            "p2_name_original": n_planet,
                            "p2_owner": "natal",
                            "aspect": translate_aspect(aspect_name, language),
                            "aspect_original": aspect_name,
                            "orbit": abs(diff - aspect_angle)
                        })
        
        # Gerar interpretações se solicitado
        interpretations = None
        if request.include_interpretations:
            interpretations = {
                "planets": {},
                "aspects": []
            }
            
            # Interpretações dos planetas
            for planet_name, planet_data in directed_planets.items():
                # Usar a função get_planet_interpretation com valores não-nulos
                interp = get_planet_interpretation(planet_name, planet_data.sign, planet_data.house, language)
                if interp:
                    interpretations["planets"][planet_name] = interp
            
            # Interpretações dos aspectos
            for aspect in all_aspects:
                p1_name = aspect["p1_name_original"]
                p2_name = aspect["p2_name_original"]
                aspect_name = aspect["aspect_original"]
                # Usar a função get_aspect_interpretation com valores não-nulos
                interp = get_planet_interpretation(f"{p1_name} {aspect_name} {p2_name}", "", 0, language)
                if interp:
                    interpretations["aspects"].append({
                        "p1": p1_name,
                        "p2": p2_name,
                        "aspect": aspect_name,
                        "text": interp
                    })
        
        # Construir resposta
        return DirectionResponse(
            input_data=request,
            directed_planets=directed_planets,
            natal_houses=houses,
            direction_value=solar_arc,
            aspects=all_aspects,
            house_system=house_system,
            interpretations=interpretations
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
