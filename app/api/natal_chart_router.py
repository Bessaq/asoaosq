from fastapi import APIRouter, HTTPException, Depends
from app.models import NatalChartRequest, NatalChartResponse, HOUSE_SYSTEM_MAP
from kerykeion import AstrologicalSubject
from app.security import verify_api_key

router = APIRouter(prefix="/api/v1", tags=["natal_chart"])

@router.post("/natal_chart", response_model=NatalChartResponse, dependencies=[Depends(verify_api_key)])
async def calculate_natal_chart(data: NatalChartRequest):
    try:
        # Converter o nome amigável do sistema de casas para o código do Kerykeion
        house_system_code = HOUSE_SYSTEM_MAP.get(data.house_system, "P")  # Default para Placidus
        
        # Criar o objeto AstrologicalSubject com o sistema de casas especificado
        subject = AstrologicalSubject(
            name=data.name or "Subject",
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
        
        # Extrair dados das casas
        houses = {}
        for i, house in enumerate(subject._houses_list, 1):
            houses[f"house_{i}"] = {
                "number": i,
                "sign": house.sign,
                "sign_num": house.sign_num,
                "longitude": house.longitude
            }
        
        # Extrair dados do ascendente e meio do céu
        ascendant = {
            "longitude": subject.asc.longitude,
            "sign": subject.asc.sign,
            "sign_num": subject.asc.sign_num
        }
        
        midheaven = {
            "longitude": subject.mc.longitude,
            "sign": subject.mc.sign,
            "sign_num": subject.mc.sign_num
        }
        
        # Construir resposta
        response = {
            "input_data": data.dict(),
            "planets": planets,
            "houses": houses,
            "ascendant": ascendant,
            "midheaven": midheaven,
            "house_system": data.house_system  # Incluir o sistema de casas usado na resposta
        }
        
        return response
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular mapa natal: {str(e)}")

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
