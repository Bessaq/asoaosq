from fastapi import APIRouter, HTTPException, Depends
from app.models import TransitRequest, TransitsToNatalRequest, TransitsToNatalResponse, HOUSE_SYSTEM_MAP
from kerykeion import AstrologicalSubject
from kerykeion.aspects import SynastryAspects
from app.security import verify_api_key
from typing import Dict, Any, List

router = APIRouter(prefix="/api/v1", tags=["transits"])

@router.post("/current_transits", response_model=Dict[str, Any], dependencies=[Depends(verify_api_key)])
async def calculate_current_transits(data: TransitRequest):
    try:
        # Converter o nome amigável do sistema de casas para o código do Kerykeion
        house_system_code = HOUSE_SYSTEM_MAP.get(data.house_system, "P")  # Default para Placidus
        
        # Criar o objeto AstrologicalSubject com o sistema de casas especificado
        subject = AstrologicalSubject(
            name="Transit",
            year=data.year,
            month=data.month,
            day=data.day,
            hour=data.hour,
            minute=data.minute,
            lng=data.longitude,
            lat=data.latitude,
            tz_str=data.tz_str,
            houses_system_identifier=house_system_code
        )
        
        # Extrair dados dos planetas
        planets = {
            "sun": _extract_planet_data(subject.sun),
            "moon": _extract_planet_data(subject.moon),
            "mercury": _extract_planet_data(subject.mercury),
            "venus": _extract_planet_data(subject.venus),
            "mars": _extract_planet_data(subject.mars),
            "jupiter": _extract_planet_data(subject.jupiter),
            "saturn": _extract_planet_data(subject.saturn),
            "uranus": _extract_planet_data(subject.uranus),
            "neptune": _extract_planet_data(subject.neptune),
            "pluto": _extract_planet_data(subject.pluto),
            "north_node": _extract_planet_data(subject.mean_node),
            "south_node": _extract_planet_data(subject.mean_south_node),
            "chiron": _extract_planet_data(subject.chiron) if subject.chiron else None
        }
        
        # Construir resposta
        response = {
            "input_data": data.dict(),
            "planets": planets,
            "house_system": data.house_system  # Incluir o sistema de casas usado na resposta
        }
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular trânsitos: {str(e)}")

@router.post("/transits_to_natal", response_model=TransitsToNatalResponse, dependencies=[Depends(verify_api_key)])
async def calculate_transits_to_natal(data: TransitsToNatalRequest):
    try:
        # Converter o nome amigável do sistema de casas para o código do Kerykeion
        natal_house_system_code = HOUSE_SYSTEM_MAP.get(data.natal.house_system, "P")
        transit_house_system_code = HOUSE_SYSTEM_MAP.get(data.transit.house_system, "P")
        
        # Criar objeto natal
        natal_subject = AstrologicalSubject(
            name=data.natal.name or "Natal Chart",
            year=data.natal.year,
            month=data.natal.month,
            day=data.natal.day,
            hour=data.natal.hour,
            minute=data.natal.minute,
            lng=data.natal.longitude,
            lat=data.natal.latitude,
            tz_str=data.natal.tz_str,
            houses_system_identifier=natal_house_system_code
        )
        
        # Criar objeto de trânsito
        transit_subject = AstrologicalSubject(
            name="Transit",
            year=data.transit.year,
            month=data.transit.month,
            day=data.transit.day,
            hour=data.transit.hour,
            minute=data.transit.minute,
            lng=data.transit.longitude,
            lat=data.transit.latitude,
            tz_str=data.transit.tz_str,
            houses_system_identifier=transit_house_system_code
        )
        
        # Calcular aspectos entre trânsito e natal
        synastry = SynastryAspects(transit_subject, natal_subject)
        
        # Extrair dados dos planetas natais
        natal_planets = {
            "sun": _extract_planet_data(natal_subject.sun),
            "moon": _extract_planet_data(natal_subject.moon),
            "mercury": _extract_planet_data(natal_subject.mercury),
            "venus": _extract_planet_data(natal_subject.venus),
            "mars": _extract_planet_data(natal_subject.mars),
            "jupiter": _extract_planet_data(natal_subject.jupiter),
            "saturn": _extract_planet_data(natal_subject.saturn),
            "uranus": _extract_planet_data(natal_subject.uranus),
            "neptune": _extract_planet_data(natal_subject.neptune),
            "pluto": _extract_planet_data(natal_subject.pluto),
            "north_node": _extract_planet_data(natal_subject.mean_node),
            "south_node": _extract_planet_data(natal_subject.mean_south_node),
            "chiron": _extract_planet_data(natal_subject.chiron) if natal_subject.chiron else None
        }
        
        # Extrair dados dos planetas em trânsito
        transit_planets = {
            "sun": _extract_planet_data(transit_subject.sun),
            "moon": _extract_planet_data(transit_subject.moon),
            "mercury": _extract_planet_data(transit_subject.mercury),
            "venus": _extract_planet_data(transit_subject.venus),
            "mars": _extract_planet_data(transit_subject.mars),
            "jupiter": _extract_planet_data(transit_subject.jupiter),
            "saturn": _extract_planet_data(transit_subject.saturn),
            "uranus": _extract_planet_data(transit_subject.uranus),
            "neptune": _extract_planet_data(transit_subject.neptune),
            "pluto": _extract_planet_data(transit_subject.pluto),
            "north_node": _extract_planet_data(transit_subject.mean_node),
            "south_node": _extract_planet_data(transit_subject.mean_south_node),
            "chiron": _extract_planet_data(transit_subject.chiron) if transit_subject.chiron else None
        }
        
        # Processar aspectos
        aspects = []
        for aspect in synastry.all_aspects:
            # Verificar se o aspecto é entre um planeta em trânsito e um natal
            if aspect.p1_owner == "Transit" and aspect.p2_owner == "Natal Chart":
                # Obter os objetos dos planetas
                transit_planet = getattr(transit_subject, aspect.p1_name.lower(), None)
                natal_planet = getattr(natal_subject, aspect.p2_name.lower(), None)
                
                # Determinar se o aspecto está se aplicando
                applying = is_aspect_applying(transit_planet, natal_planet, aspect.diff)
                
                aspects.append({
                    "p1_name": aspect.p1_name,
                    "p1_owner": "Trânsito",
                    "p2_name": aspect.p2_name,
                    "p2_owner": "Natal",
                    "aspect": aspect.aspect,
                    "orbit": aspect.orbit,
                    "aspect_degrees": aspect.aspect_degrees,
                    "diff": aspect.diff,
                    "applying": applying
                })
        
        # Construir resposta
        response = {
            "input_data": data.dict(),
            "natal_planets": natal_planets,
            "transit_planets": transit_planets,
            "aspects": aspects,
            "natal_house_system": data.natal.house_system,
            "transit_house_system": data.transit.house_system
        }
        
        return response
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular trânsitos: {str(e)}")

def is_aspect_applying(transit_planet, natal_planet, aspect_diff):
    """
    Determina se um aspecto está se aplicando ou separando.
    
    Args:
        transit_planet: Objeto do planeta em trânsito
        natal_planet: Objeto do planeta natal
        aspect_diff: Diferença atual do aspecto em graus
    
    Returns:
        bool: True se o aspecto está se aplicando, False se está separando
    """
    # Os planetas natais são fixos, então apenas a velocidade do planeta em trânsito importa
    # Se o planeta em trânsito está retrógrado, a lógica se inverte
    
    # Simplificação: se o planeta em trânsito está retrógrado e a diferença é positiva,
        # ou se não está retrógrado e a diferença é negativa, então está se aplicando
    return (transit_planet.retrograde and aspect_diff > 0) or (not transit_planet.retrograde and aspect_diff < 0)

def _extract_planet_data(planet_point):
    """Extrai dados relevantes de um ponto planetário."""
    if not planet_point:
        return None
    
    return {
        "name": planet_point.name,
        "position": planet_point.longitude,
        "abs_pos": planet_point.latitude,
        "sign": planet_point.sign,
        "sign_num": planet_point.sign_num,
        "house": planet_point.house,
        "retrograde": planet_point.retrograde
    }
