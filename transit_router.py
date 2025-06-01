from fastapi import APIRouter, HTTPException
from kerykeion import AstrologicalSubject
from ..models import (
    TransitRequest, CurrentTransitsResponse, 
    TransitsToNatalRequest, TransitsToNatalResponse, 
    PlanetPosition, TransitAspect, NatalChartRequest
)
from typing import List, Optional

router = APIRouter(
    prefix="/api/v1",
    tags=["Transits"],
)

def get_transit_planet_data(subject: AstrologicalSubject, planet_name_kerykeion: str, api_planet_name: str) -> Optional[PlanetPosition]:
    try:
        p = getattr(subject, planet_name_kerykeion.lower())
        if p and p.name:
            return PlanetPosition(
                name=api_planet_name,
                sign=p.sign,
                sign_num=p.sign_num,
                position=round(p.position, 4),
                abs_pos=round(p.abs_pos, 4),
                house_name=p.house_name if hasattr(p, 'house_name') else "N/A",
                speed=round(p.speed, 4) if hasattr(p, 'speed') else 0.0,
                retrograde=p.retrograde if hasattr(p, 'retrograde') else False
            )
    except AttributeError:
        pass
    return None

@router.post("/current_transits", response_model=CurrentTransitsResponse)
async def get_current_transits(request: TransitRequest):
    try:
        # Removido o argumento house_system da instanciação
        transit_subject = AstrologicalSubject(
            name="CurrentTransits",
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            city="CustomLocation",
            nation="",
            lng=request.longitude,
            lat=request.latitude,
            tz_str=request.tz_str
        )

        planets_map = {
            "sun": "Sun", "moon": "Moon", "mercury": "Mercury", "venus": "Venus",
            "mars": "Mars", "jupiter": "Jupiter", "saturn": "Saturn",
            "uranus": "Uranus", "neptune": "Neptune", "pluto": "Pluto",
            "mean_node": "Mean_Node", "true_node": "True_Node",
        }
        
        transit_planets: List[PlanetPosition] = []
        for k_name, api_name in planets_map.items():
            planet_data = get_transit_planet_data(transit_subject, k_name, api_name)
            if planet_data:
                transit_planets.append(planet_data)
        
        if hasattr(transit_subject, 'chiron') and transit_subject.chiron:
            chiron_data = get_transit_planet_data(transit_subject, 'chiron', 'Chiron')
            if chiron_data: transit_planets.append(chiron_data)

        if hasattr(transit_subject, 'lilith') and transit_subject.lilith and transit_subject.lilith.name:
            lilith_data = PlanetPosition(
                name="Lilith", sign=transit_subject.lilith.sign, sign_num=transit_subject.lilith.sign_num,
                position=round(transit_subject.lilith.position,4), abs_pos=round(transit_subject.lilith.abs_pos,4),
                house_name=transit_subject.lilith.house_name, speed=0.0, retrograde=False
            )
            transit_planets.append(lilith_data)

        return CurrentTransitsResponse(input_data=request, planets=transit_planets)

    except Exception as e:
        print(f"Erro de cálculo astrológico em current_transits (Kerykeion ou outro): {type(e).__name__} - {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Erro de cálculo astrológico (Kerykeion): {str(e)}")

@router.post("/transits_to_natal", response_model=TransitsToNatalResponse)
async def get_transits_to_natal(request: TransitsToNatalRequest):
    try:
        natal_req = request.natal_data
        # Removido o argumento house_system da instanciação
        natal_subject = AstrologicalSubject(
            name=natal_req.name if natal_req.name else "NatalChart",
            year=natal_req.year, month=natal_req.month, day=natal_req.day,
            hour=natal_req.hour, minute=natal_req.minute,
            city="CustomLocation", nation="",
            lng=natal_req.longitude, lat=natal_req.latitude, tz_str=natal_req.tz_str
        )

        transit_req = request.transit_data
        # Removido o argumento house_system da instanciação
        transit_subject = AstrologicalSubject(
            name="TransitChart",
            year=transit_req.year, month=transit_req.month, day=transit_req.day,
            hour=transit_req.hour, minute=transit_req.minute,
            city="CustomLocation", nation="",
            lng=transit_req.longitude, lat=transit_req.latitude, tz_str=transit_req.tz_str
        )

        planets_map = {
            "sun": "Sun", "moon": "Moon", "mercury": "Mercury", "venus": "Venus",
            "mars": "Mars", "jupiter": "Jupiter", "saturn": "Saturn",
            "uranus": "Uranus", "neptune": "Neptune", "pluto": "Pluto",
            "mean_node": "Mean_Node", "true_node": "True_Node"
        }
        transit_planets_positions: List[PlanetPosition] = []
        for k_name, api_name in planets_map.items():
            planet_data = get_transit_planet_data(transit_subject, k_name, api_name)
            if planet_data:
                transit_planets_positions.append(planet_data)
        
        if hasattr(transit_subject, 'chiron') and transit_subject.chiron:
            chiron_data = get_transit_planet_data(transit_subject, 'chiron', 'Chiron')
            if chiron_data: transit_planets_positions.append(chiron_data)
        
        aspects_to_natal: List[TransitAspect] = []
        raw_aspects = natal_subject.get_aspects_to(transit_subject)
        for asp_obj in raw_aspects:
            aspects_to_natal.append(TransitAspect(
                transit_planet=asp_obj.p2_name,
                natal_planet_or_point=asp_obj.p1_name,
                aspect_name=asp_obj.aspect_name,
                orbit=round(asp_obj.orbit, 4)
            ))

        return TransitsToNatalResponse(
            natal_input=request.natal_data,
            transit_input=request.transit_data,
            transit_planets_positions=transit_planets_positions,
            aspects_to_natal=aspects_to_natal
        )

    except Exception as e:
        print(f"Erro de cálculo astrológico em transits_to_natal (Kerykeion ou outro): {type(e).__name__} - {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Erro de cálculo astrológico (Kerykeion): {str(e)}")

