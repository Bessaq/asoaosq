from fastapi import APIRouter, HTTPException, Depends
from kerykeion import AstrologicalSubject
from ..models import NatalChartRequest, NatalChartResponse, PlanetPosition, HouseCusp, AscMc, Aspect
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/api/v1",
    tags=["Natal Chart"],
)

_HOUSE_NUMBER_TO_NAME_BASE = {
    1: "first", 2: "second", 3: "third", 4: "fourth",
    5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth",
    9: "ninth", 10: "tenth", 11: "eleventh", 12: "twelfth"
}

def get_planet_data(subject: AstrologicalSubject, planet_name_kerykeion: str, api_planet_name: str) -> Optional[PlanetPosition]:
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

@router.post("/natal_chart", response_model=NatalChartResponse)
async def create_natal_chart(request: NatalChartRequest):
    try:
        # Removido o argumento house_system da instanciação
        subject = AstrologicalSubject(
            name=request.name if request.name else "NatalChart",
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
        # Se Kerykeion permitir definir o sistema de casas após a instanciação, seria aqui.
        # Ex: if request.house_system: subject.set_house_system(request.house_system)
        # Por agora, Kerykeion usará seu padrão (provavelmente Placidus).

        planets_map = {
            "sun": "Sun", "moon": "Moon", "mercury": "Mercury", "venus": "Venus",
            "mars": "Mars", "jupiter": "Jupiter", "saturn": "Saturn",
            "uranus": "Uranus", "neptune": "Neptune", "pluto": "Pluto",
            "mean_node": "Mean_Node",
            "true_node": "True_Node",
        }
        
        response_planets = {}
        for k_name, api_name in planets_map.items():
            planet_data = get_planet_data(subject, k_name, api_name)
            if planet_data:
                response_planets[k_name] = planet_data
        
        if hasattr(subject, 'chiron') and subject.chiron:
            chiron_data = get_planet_data(subject, 'chiron', 'Chiron')
            if chiron_data: response_planets['chiron'] = chiron_data
        
        if hasattr(subject, 'lilith') and subject.lilith and subject.lilith.name:
             response_planets['lilith'] = PlanetPosition(
                name="Lilith", sign=subject.lilith.sign, sign_num=subject.lilith.sign_num,
                position=round(subject.lilith.position,4), abs_pos=round(subject.lilith.abs_pos,4),
                house_name=subject.lilith.house_name, speed=0.0, retrograde=False
            )

        houses: List[HouseCusp] = []
        for i in range(1, 13):
            house_name_base = _HOUSE_NUMBER_TO_NAME_BASE.get(i)
            if not house_name_base:
                continue
            
            house_obj_attr_name = f"{house_name_base}_house"
            house_obj = getattr(subject, house_obj_attr_name)
            houses.append(HouseCusp(
                name=house_obj.name,
                sign=house_obj.sign,
                position=round(house_obj.position, 4)
            ))

        ascendant = AscMc(sign=subject.first_house.sign, position=round(subject.first_house.position, 4))
        mc = AscMc(sign=subject.tenth_house.sign, position=round(subject.tenth_house.position, 4))

        aspects_list: List[Aspect] = []
        main_planets_for_aspects = [
            subject.sun, subject.moon, subject.mercury, subject.venus, subject.mars,
            subject.jupiter, subject.saturn, subject.uranus, subject.neptune, subject.pluto
        ]

        processed_aspects = set()
        for p1 in main_planets_for_aspects:
            if not p1 or not hasattr(p1, 'aspects'): continue
            for asp in p1.aspects:
                p2_name = asp.p2_name
                pair = tuple(sorted((p1.name, p2_name)) + (asp.aspect_name,))
                if pair not in processed_aspects:
                    aspects_list.append(Aspect(
                        planet1=p1.name,
                        planet2=p2_name,
                        aspect_name=asp.aspect_name,
                        orbit=round(asp.orbit, 4)
                    ))
                    processed_aspects.add(pair)
        
        final_response_data = {
            "input_data": request,
            "sun": response_planets.get('sun'),
            "moon": response_planets.get('moon'),
            "mercury": response_planets.get('mercury'),
            "venus": response_planets.get('venus'),
            "mars": response_planets.get('mars'),
            "jupiter": response_planets.get('jupiter'),
            "saturn": response_planets.get('saturn'),
            "uranus": response_planets.get('uranus'),
            "neptune": response_planets.get('neptune'),
            "pluto": response_planets.get('pluto'),
            "mean_node": response_planets.get('mean_node'),
            "true_node": response_planets.get('true_node'),
            "chiron": response_planets.get('chiron'),
            "lilith": response_planets.get('lilith'),
            "houses": houses,
            "ascendant": ascendant,
            "mc": mc,
            "aspects": aspects_list
        }
        
        return NatalChartResponse(**final_response_data)

    except Exception as e:
        print(f"Erro de cálculo astrológico em natal_chart (Kerykeion ou outro): {type(e).__name__} - {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Erro de cálculo astrológico (Kerykeion): {str(e)}")

