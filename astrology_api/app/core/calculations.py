"""
Módulo de cálculos astrológicos para a aplicação AstroAPI.
"""
from kerykeion import AstrologicalSubject
from typing import Dict, List, Optional, Union, Literal, cast
from datetime import datetime, timedelta
import logging
import math

from ..schemas.models import (
    PlanetData, HouseCuspData, AspectData, 
    HouseSystemType, HOUSE_SYSTEM_MAP,
    LanguageType
)
from ..interpretations.translations import (
    translate_planet, translate_sign, translate_aspect, translate_house
)
from ..core.cache import get_cache_key, get_from_cache, save_to_cache

logger = logging.getLogger(__name__)

def get_kerykeion_house_system_code(house_system: HouseSystemType) -> str:
    """Converte o nome do sistema de casas para o código usado pelo Kerykeion."""
    return HOUSE_SYSTEM_MAP.get(house_system, "P")

def create_astrological_subject(
    name: str,
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    longitude: float,
    latitude: float,
    tz_str: str,
    house_system: HouseSystemType = "Placidus"
) -> AstrologicalSubject:
    """Cria um objeto AstrologicalSubject do Kerykeion."""
    try:
        # Garantir que house_system não é None
        house_system_code = HOUSE_SYSTEM_MAP.get(house_system or "Placidus", "P")
        
        subject = AstrologicalSubject(
            name=str(name),
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour),
            minute=int(minute),
            city="CustomLocation",
            nation="",
            lng=float(longitude),
            lat=float(latitude),
            tz_str=str(tz_str),
            houses_system_identifier=house_system_code
        )
        
        return subject
        
    except Exception as e:
        logger.error(f"Erro ao criar objeto AstrologicalSubject: {str(e)}")
        raise ValueError(f"Erro ao criar objeto AstrologicalSubject: {str(e)}")

def get_planet_data(subject: AstrologicalSubject, language: LanguageType = "pt") -> Dict[str, PlanetData]:
    """
    Obtém dados dos planetas de um AstrologicalSubject.
    
    Args:
        subject (AstrologicalSubject): Sujeito astrológico
        language (LanguageType): Idioma para nomes traduzidos. Defaults to "pt".
        
    Returns:
        Dict[str, PlanetData]: Dicionário com dados dos planetas
    """
    planets_data = {}
    
    # Garantir que language não é None
    language = language or "pt"
    
    for planet in subject.planets:
        name = planet.name
        translated_name = translate_planet(name, language)
        sign = planet.sign
        translated_sign = translate_sign(sign, language)
        
        planets_data[name] = PlanetData(
            name=translated_name,
            name_original=name,
            longitude=planet.longitude,
            latitude=planet.latitude,
            sign=translated_sign,
            sign_original=sign,
            sign_num=planet.sign_num,
            house=planet.house,
            retrograde=planet.retrograde,
            speed=planet.speed
        )
    
    return planets_data

def get_houses_data(subject: AstrologicalSubject, language: LanguageType = "pt") -> Dict[str, HouseCuspData]:
    """
    Obtém dados das casas de um AstrologicalSubject.
    
    Args:
        subject (AstrologicalSubject): Sujeito astrológico
        language (LanguageType): Idioma para nomes traduzidos. Defaults to "pt".
        
    Returns:
        Dict[str, HouseCuspData]: Dicionário com dados das casas
    """
    houses_data = {}
    
    # Garantir que language não é None
    language = language or "pt"
    
    for i, house in enumerate(subject.houses, start=1):
        sign = house.sign
        translated_sign = translate_sign(sign, language)
        
        houses_data[str(i)] = HouseCuspData(
            number=i,
            sign=translated_sign,
            sign_original=sign,
            sign_num=house.sign_num,
            longitude=house.longitude
        )
    
    return houses_data

def calculate_aspect(point1_long: float, point2_long: float) -> Optional[Dict[str, Union[str, float]]]:
    """Calcula o aspecto entre dois pontos baseado em suas longitudes."""
    # Diferença entre as longitudes
    diff = abs(point1_long - point2_long)
    if diff > 180:
        diff = 360 - diff
        
    # Definição dos aspectos e seus orbes
    aspects = {
        "Conjunction": {"angle": 0, "orb": 8},
        "Opposition": {"angle": 180, "orb": 8},
        "Trine": {"angle": 120, "orb": 6},
        "Square": {"angle": 90, "orb": 6},
        "Sextile": {"angle": 60, "orb": 4}
    }
    
    # Verificar cada aspecto possível
    for aspect_name, aspect_data in aspects.items():
        orbit = abs(diff - aspect_data["angle"])
        if orbit <= aspect_data["orb"]:
            return {
                "aspect": aspect_name,
                "orbit": orbit,
                "angle": aspect_data["angle"],
                "diff": diff
            }
            
    return None

def get_aspects_data(subject: AstrologicalSubject, language: LanguageType = "pt") -> List[AspectData]:
    """Calcula os aspectos entre planetas em um mapa."""
    result = []
    processed = set()
    
    try:
        # Lista de planetas principais para aspectos
        planet_attrs = [
            'sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn',
            'uranus', 'neptune', 'pluto'
        ]
        
        # Calcular aspectos entre todos os pares de planetas
        for i, p1_attr in enumerate(planet_attrs):
            if not hasattr(subject, p1_attr):
                continue
                
            planet1 = getattr(subject, p1_attr)
            if not planet1 or not hasattr(planet1, 'longitude'):
                continue
                
            for p2_attr in planet_attrs[i+1:]:
                if not hasattr(subject, p2_attr):
                    continue
                    
                planet2 = getattr(subject, p2_attr)
                if not planet2 or not hasattr(planet2, 'longitude'):
                    continue
                    
                # Calcular o aspecto
                aspect_info = calculate_aspect(planet1.longitude, planet2.longitude)
                if not aspect_info:
                    continue
                
                # Criar chave única para o aspecto
                aspect_key = tuple(sorted([p1_attr, p2_attr]))
                if aspect_key in processed:
                    continue
                
                processed.add(aspect_key)
                
                # Determinar se o aspecto está se aplicando
                applying = False
                if hasattr(planet1, 'motion') and hasattr(planet2, 'motion'):
                    if hasattr(planet1.motion, 'speed') and hasattr(planet2.motion, 'speed'):
                        applying = planet1.motion.speed > planet2.motion.speed
                
                # Criar o objeto AspectData
                aspect_data = AspectData(
                    p1_name=translate_planet(planet1.name, language),
                    p1_name_original=planet1.name,
                    p1_owner="natal",
                    p2_name=translate_planet(planet2.name, language),
                    p2_name_original=planet2.name,
                    p2_owner="natal",
                    aspect=translate_aspect(aspect_info["aspect"], language),
                    aspect_original=aspect_info["aspect"],
                    orbit=round(float(aspect_info["orbit"]), 4),
                    aspect_degrees=round(float(aspect_info["angle"]), 4),
                    diff=round(float(aspect_info["diff"]), 4),
                    applying=applying
                )
                
                result.append(aspect_data)
                
    except Exception as e:
        logger.error(f"Erro ao calcular aspectos: {str(e)}")
        
    return result

def get_aspects_between_charts(
    subject1: AstrologicalSubject, 
    subject2: AstrologicalSubject,
    language: LanguageType = "pt"
) -> List[AspectData]:
    """Calcula aspectos entre dois mapas astrológicos."""
    result = []
    
    try:
        # Usar o método de aspectos entre mapas se disponível
        if hasattr(subject1, 'get_aspects_between'):
            aspects = subject1.get_aspects_between(subject2)
        else:
            # Implementação alternativa se o método não existir
            aspects = calculate_aspects_between(subject1, subject2)
            
        for aspect in aspects:
            if not aspect:
                continue
                
            p1_name = aspect.p1.name if hasattr(aspect, 'p1') and hasattr(aspect.p1, 'name') else ''
            p2_name = aspect.p2.name if hasattr(aspect, 'p2') and hasattr(aspect.p2, 'name') else ''
            aspect_name = aspect.aspect if hasattr(aspect, 'aspect') else ''
            
            aspect_data = AspectData(
                p1_name=translate_planet(p1_name, language),
                p1_name_original=p1_name,
                p1_owner="natal",
                p2_name=translate_planet(p2_name, language),
                p2_name_original=p2_name,
                p2_owner="transit",
                aspect=translate_aspect(aspect_name, language),
                aspect_original=aspect_name,
                orbit=float(aspect.orbit) if hasattr(aspect, 'orbit') else 0.0,
                aspect_degrees=float(aspect.aspect_degrees) if hasattr(aspect, 'aspect_degrees') else 0.0,
                diff=float(aspect.diff) if hasattr(aspect, 'diff') else 0.0,
                applying=False  # Implementar lógica de applying/separating se necessário
            )
            
            result.append(aspect_data)
            
    except Exception as e:
        logger.error(f"Erro ao calcular aspectos entre mapas: {str(e)}")
        
    return result

def calculate_aspects_between(subject1: AstrologicalSubject, subject2: AstrologicalSubject) -> List[Any]:
    """Implementação alternativa para cálculo de aspectos entre mapas."""
    result = []
    
    # Definir aspectos principais e seus orbes
    aspects = {
        "Conjunction": {"angle": 0, "orb": 8},
        "Opposition": {"angle": 180, "orb": 8},
        "Trine": {"angle": 120, "orb": 6},
        "Square": {"angle": 90, "orb": 6},
        "Sextile": {"angle": 60, "orb": 4}
    }
    
    try:
        # Iterar sobre os planetas do primeiro mapa
        for p1 in subject1.planets_list:
            if not p1:
                continue
                
            # Iterar sobre os planetas do segundo mapa
            for p2 in subject2.planets_list:
                if not p2:
                    continue
                    
                # Calcular a diferença de longitude
                diff = abs(p1.longitude - p2.longitude)
                if diff > 180:
                    diff = 360 - diff
                    
                # Verificar aspectos
                for aspect_name, aspect_data in aspects.items():
                    orbit = abs(diff - aspect_data["angle"])
                    
                    if orbit <= aspect_data["orb"]:
                        # Criar um objeto de aspecto simples
                        aspect = type("Aspect", (), {
                            "p1": p1,
                            "p2": p2,
                            "aspect": aspect_name,
                            "orbit": orbit,
                            "aspect_degrees": aspect_data["angle"],
                            "diff": diff
                        })
                        
                        result.append(aspect)
                        
    except Exception as e:
        logger.error(f"Erro ao calcular aspectos manualmente: {str(e)}")
        
    return result

# Removed duplicate definition of get_aspects_data to avoid confusion and maintenance issues.

def get_aspects_between_subjects(
    subject1: AstrologicalSubject, 
    subject2: AstrologicalSubject,
    subject1_owner: str = "natal",
    subject2_owner: str = "transit",
    language: str = "pt"
) -> List[AspectData]:
    """
    Extrai os dados dos aspectos entre dois objetos AstrologicalSubject.
    
    Args:
        subject1 (AstrologicalSubject): Primeiro objeto AstrologicalSubject (geralmente o mapa natal).
        subject2 (AstrologicalSubject): Segundo objeto AstrologicalSubject (geralmente o mapa de trânsito).
        subject1_owner (str, opcional): Identificador do proprietário do primeiro objeto. Padrão é "natal".
        subject2_owner (str, opcional): Identificador do proprietário do segundo objeto. Padrão é "transit".
        language (str, opcional): Idioma para os textos. Padrão é "pt".
        
    Returns:
        List[AspectData]: Lista com os dados dos aspectos entre os dois objetos.
    """
    result = []
    
    # Obter os aspectos entre os dois objetos
    raw_aspects = subject1.get_aspects_to(subject2)
    
    # Mapeamento de nomes de aspectos em português
    aspect_names_pt = {
        "Conjunction": "Conjunção",
        "Opposition": "Oposição",
        "Trine": "Trígono",
        "Square": "Quadratura",
        "Sextile": "Sextil",
        "Quincunx": "Quincúncio",
        "Semisextile": "Semisextil",
        "Semisquare": "Semiquadratura",
        "Sesquiquadrate": "Sesquiquadratura",
        "Quintile": "Quintil",
        "Biquintile": "Biquintil"
    }
    
    for asp in raw_aspects:
        # Obter o nome do aspecto no idioma selecionado
        aspect_name = asp.aspect_name
        if language == "pt":
            aspect_name = aspect_names_pt.get(asp.aspect_name, asp.aspect_name)
        
        # Determinar se o aspecto está se aplicando
        applying = False
        if hasattr(asp, 'applying'):
            applying = asp.applying
        
        # Criar o objeto AspectData
        aspect_data = AspectData(
            p1_name=asp.p1_name if language == "pt" else asp.p1_name,
            p1_name_original=asp.p1_name,
            p1_owner=subject1_owner,
            p2_name=asp.p2_name if language == "pt" else asp.p2_name,
            p2_name_original=asp.p2_name,
            p2_owner=subject2_owner,
            aspect=aspect_name,
            aspect_original=asp.aspect_name,
            orbit=round(asp.orbit, 4),
            aspect_degrees=round(asp.aspect_degrees, 4) if hasattr(asp, 'aspect_degrees') else 0.0,
            diff=round(asp.diff, 4) if hasattr(asp, 'diff') else 0.0,
            applying=applying
        )
        
        result.append(aspect_data)
    
    return result

def get_synastry_aspects_data(subject1: AstrologicalSubject, subject2: AstrologicalSubject, language: str = "pt") -> List[AspectData]:
    """
    Calcula os aspectos entre os planetas de dois mapas natais (sinastria).
    
    Args:
        subject1 (AstrologicalSubject): Primeiro objeto AstrologicalSubject.
        subject2 (AstrologicalSubject): Segundo objeto AstrologicalSubject.
        language (str, opcional): Idioma para os textos. Padrão é "pt".
        
    Returns:
        List[AspectData]: Lista de aspectos entre os planetas dos dois mapas.
    """
    aspects = []
    
    # Dicionário para mapear nomes de planetas em inglês para os do Kerykeion
    planet_to_kerykeion = {
        "Sun": "sun", "Moon": "moon", "Mercury": "mercury", "Venus": "venus",
        "Mars": "mars", "Jupiter": "jupiter", "Saturn": "saturn",
        "Uranus": "uranus", "Neptune": "neptune", "Pluto": "pluto",
        "Mean_Node": "mean_node", "True_Node": "true_node", "Chiron": "chiron"
    }
    
    # Obter planetas do primeiro mapa
    planets1 = subject1.planets
    
    # Obter planetas do segundo mapa
    planets2 = subject2.planets
    
    # Aspectos aceitos pelo Kerykeion
    aspects_to_check = ["conjunction", "opposition", "trine", "square", "sextile"]
    
    # Orbes para cada tipo de aspecto
    orbs = {
        "conjunction": 8, "opposition": 8, "trine": 6,
        "square": 6, "sextile": 4
    }
    
    # Mapear aspectos
    aspect_map = {
        "conjunction": "Conjunction", "opposition": "Opposition",
        "trine": "Trine", "square": "Square", "sextile": "Sextile"
    }
    
    # Calcular aspectos entre os planetas dos dois mapas
    for p1_en, p1_key in planet_to_kerykeion.items():
        if p1_key not in planets1:
            continue
        
        p1_lon = planets1[p1_key]['position']['longitude']
        
        for p2_en, p2_key in planet_to_kerykeion.items():
            if p2_key not in planets2:
                continue
            
            p2_lon = planets2[p2_key]['position']['longitude']
            
            # Calcular a diferença em graus
            diff = abs(p1_lon - p2_lon)
            if diff > 180:
                diff = 360 - diff
            
            # Verificar se há algum aspecto
            for aspect_key, aspect_en in aspect_map.items():
                aspect_degree = 0
                if aspect_key == "conjunction":
                    aspect_degree = 0
                elif aspect_key == "opposition":
                    aspect_degree = 180
                elif aspect_key == "trine":
                    aspect_degree = 120
                elif aspect_key == "square":
                    aspect_degree = 90
                elif aspect_key == "sextile":
                    aspect_degree = 60
                
                # Verificar se está dentro do orbe
                orbit = abs(diff - aspect_degree)
                if orbit <= orbs[aspect_key]:
                    # Determinar se o aspecto está se aplicando ou separando
                    applying = False
                    if p1_lon < p2_lon:
                        applying = planets1[p1_key]['position']['speed'] > planets2[p2_key]['position']['speed']
                    else:
                        applying = planets1[p1_key]['position']['speed'] < planets2[p2_key]['position']['speed']
                    
                    # Traduzir nomes
                    p1_name = translate_planet(p1_en, language)
                    p2_name = translate_planet(p2_en, language)
                    aspect_name = translate_aspect(aspect_en, language)
                    
                    # Adicionar aspecto
                    aspects.append(AspectData(
                        p1_name=p1_name,
                        p1_name_original=p1_en,
                        p1_owner="chart1",
                        p2_name=p2_name,
                        p2_name_original=p2_en,
                        p2_owner="chart2",
                        aspect=aspect_name,
                        aspect_original=aspect_en,
                        orbit=orbit,
                        aspect_degrees=aspect_degree,
                        diff=diff,
                        applying=applying
                    ))
    
    return aspects

def get_progressed_chart(natal_subject: AstrologicalSubject, prog_year: int, prog_month: int, prog_day: int) -> AstrologicalSubject:
    """
    Calcula o mapa progressado secundário para uma data específica.
    A progressão secundária segue o princípio de "um dia = um ano".
    
    Args:
        natal_subject (AstrologicalSubject): Objeto AstrologicalSubject do mapa natal.
        prog_year (int): Ano para o qual calcular a progressão.
        prog_month (int): Mês para o qual calcular a progressão.
        prog_day (int): Dia para o qual calcular a progressão.
        
    Returns:
        AstrologicalSubject: Objeto AstrologicalSubject do mapa progressado.
    """
    # Calcular a diferença em anos entre a data natal e a data de progressão
    # Data natal
    natal_date = datetime(
        natal_subject.year, 
        natal_subject.month, 
        natal_subject.day, 
        natal_subject.hour, 
        natal_subject.minute
    )
    
    # Data para a qual queremos a progressão
    prog_date = datetime(prog_year, prog_month, prog_day)
    
    # Calcular a diferença em dias (1 dia = 1 ano na progressão secundária)
    days_diff = (prog_date.year - natal_date.year) + (prog_date.month - natal_date.month) / 12 + (prog_date.day - natal_date.day) / 365.25
    
    # Calcular a data progressada
    progressed_date = natal_date + timedelta(days=days_diff)
    
    # Criar um novo objeto AstrologicalSubject com a data progressada
    progressed_subject = AstrologicalSubject(
        name=f"{natal_subject.name}_Progressed",
        year=progressed_date.year,
        month=progressed_date.month,
        day=progressed_date.day,
        hour=progressed_date.hour,
        minute=progressed_date.minute,
        city=natal_subject.city,
        lng=natal_subject.lng,
        lat=natal_subject.lat,
        tz_str=natal_subject.tz_str,
        house_system=natal_subject.house_system
    )
    
    return progressed_subject

def get_return_chart(
    natal_subject: AstrologicalSubject, 
    return_year: int, 
    return_month: Optional[int] = None,
    return_type: Literal["solar", "lunar"] = "solar",
    location_longitude: Optional[float] = None,
    location_latitude: Optional[float] = None,
    location_tz_str: Optional[str] = None
) -> AstrologicalSubject:
    """
    Calcula um mapa de retorno solar ou lunar.
    
    Args:
        natal_subject (AstrologicalSubject): Objeto AstrologicalSubject do mapa natal.
        return_year (int): Ano para o qual calcular o retorno.
        return_month (Optional[int]): Mês para o qual calcular o retorno (apenas para retorno lunar).
        return_type (str): Tipo de retorno, "solar" ou "lunar".
        location_longitude (Optional[float]): Longitude do local do retorno.
        location_latitude (Optional[float]): Latitude do local do retorno.
        location_tz_str (Optional[str]): Fuso horário do local do retorno.
        
    Returns:
        AstrologicalSubject: Objeto AstrologicalSubject do mapa de retorno.
    """
    # Definir a localização para o retorno
    location_lng = location_longitude if location_longitude is not None else natal_subject.lng
    location_lat = location_latitude if location_latitude is not None else natal_subject.lat
    location_tz = location_tz_str if location_tz_str is not None else natal_subject.tz_str
    
    if return_type == "solar":
        # Para retorno solar, precisamos encontrar o momento exato em que o Sol retorna
        # à mesma posição zodiacal do mapa natal
        
        # Obter a posição do Sol no mapa natal
        natal_sun_position = natal_subject.planets["sun"]["position"]["longitude"]
        
        # Criar uma data aproximada para o retorno solar (próximo ao aniversário)
        natal_month = natal_subject.month
        natal_day = natal_subject.day
        
        # Data inicial para a busca
        start_date = datetime(return_year, natal_month, natal_day)
        
        # Ajustar para 5 dias antes do aniversário
        start_date = start_date - timedelta(days=5)
        
        # Criar um mapa para esta data inicial
        temp_subject = AstrologicalSubject(
            name=f"{natal_subject.name}_SolarReturn",
            year=start_date.year,
            month=start_date.month,
            day=start_date.day,
            hour=12,  # Meio-dia como hora inicial
            minute=0,
            city="",
            lng=location_lng,
            lat=location_lat,
            tz_str=location_tz
        )
        
        # Buscar iterativamente a data do retorno solar
        for i in range(12):  # Verificar até 12 dias a partir da data inicial
            temp_date = start_date + timedelta(days=i)
            temp_subject = AstrologicalSubject(
                name=f"{natal_subject.name}_SolarReturn",
                year=temp_date.year,
                month=temp_date.month,
                day=temp_date.day,
                hour=12,  # Meio-dia como hora inicial
                minute=0,
                city="",
                lng=location_lng,
                lat=location_lat,
                tz_str=location_tz
            )
            
            # Verificar a posição do Sol
            current_sun_position = temp_subject.planets["sun"]["position"]["longitude"]
            
            # Se a posição atual é maior que a natal, significa que o retorno ocorreu
            # entre este dia e o anterior
            if current_sun_position > natal_sun_position and i > 0:
                break
        
        # Refinar a hora exata do retorno
        for hour in range(24):
            temp_subject = AstrologicalSubject(
                name=f"{natal_subject.name}_SolarReturn",
                year=temp_date.year,
                month=temp_date.month,
                day=temp_date.day,
                hour=hour,
                minute=0,
                city="",
                lng=location_lng,
                lat=location_lat,
                tz_str=location_tz
            )
            
            current_sun_position = temp_subject.planets["sun"]["position"]["longitude"]
            
            # Se a posição atual é maior ou igual à natal, encontramos a hora aproximada
            if abs(current_sun_position - natal_sun_position) < 1.0:
                # Refinar os minutos
                for minute in range(0, 60, 5):
                    temp_subject = AstrologicalSubject(
                        name=f"{natal_subject.name}_SolarReturn",
                        year=temp_date.year,
                        month=temp_date.month,
                        day=temp_date.day,
                        hour=hour,
                        minute=minute,
                        city="",
                        lng=location_lng,
                        lat=location_lat,
                        tz_str=location_tz
                    )
                    
                    current_sun_position = temp_subject.planets["sun"]["position"]["longitude"]
                    
                    # Verificar se encontramos a posição exata
                    if abs(current_sun_position - natal_sun_position) < 0.1:
                        return temp_subject
                
                # Se não encontrou a posição exata, retorna a mais próxima
                return temp_subject
        
        # Se não encontrou nas horas, retorna o mapa do meio-dia
        return temp_subject
    
    elif return_type == "lunar":
        # Para retorno lunar, precisamos encontrar o momento exato em que a Lua retorna
        # à mesma posição zodiacal do mapa natal
        
        # Obter a posição da Lua no mapa natal
        natal_moon_position = natal_subject.planets["moon"]["position"]["longitude"]
        
        # Se o mês não foi especificado, usar o mês atual
        if return_month is None:
            return_month = datetime.now().month
        
        # Data inicial para a busca (primeiro dia do mês)
        start_date = datetime(return_year, return_month, 1)
        
        # Calcular cada dia do mês até encontrar o retorno lunar
        for day in range(1, 29):  # A Lua completa um ciclo em aproximadamente 27.3 dias
            temp_date = start_date + timedelta(days=day)
            
            temp_subject = AstrologicalSubject(
                name=f"{natal_subject.name}_LunarReturn",
                year=temp_date.year,
                month=temp_date.month,
                day=temp_date.day,
                hour=12,  # Meio-dia como hora inicial
                minute=0,
                city="",
                lng=location_lng,
                lat=location_lat,
                tz_str=location_tz
            )
            
            # Verificar a posição da Lua
            current_moon_position = temp_subject.planets["moon"]["position"]["longitude"]
            
            # Se a posição atual está próxima da natal, refinar a hora
            if abs(current_moon_position - natal_moon_position) < 15:
                # Refinar a hora exata do retorno
                for hour in range(24):
                    temp_subject = AstrologicalSubject(
                        name=f"{natal_subject.name}_LunarReturn",
                        year=temp_date.year,
                        month=temp_date.month,
                        day=temp_date.day,
                        hour=hour,
                        minute=0,
                        city="",
                        lng=location_lng,
                        lat=location_lat,
                        tz_str=location_tz
                    )
                    
                    current_moon_position = temp_subject.planets["moon"]["position"]["longitude"]
                    
                    # Se a posição atual está mais próxima da natal, refinar os minutos
                    if abs(current_moon_position - natal_moon_position) < 5:
                        # Refinar os minutos
                        for minute in range(0, 60, 5):
                            temp_subject = AstrologicalSubject(
                                name=f"{natal_subject.name}_LunarReturn",
                                year=temp_date.year,
                                month=temp_date.month,
                                day=temp_date.day,
                                hour=hour,
                                minute=minute,
                                city="",
                                lng=location_lng,
                                lat=location_lat,
                                tz_str=location_tz
                            )
                            
                            current_moon_position = temp_subject.planets["moon"]["position"]["longitude"]
                            
                            # Verificar se encontramos a posição exata
                            if abs(current_moon_position - natal_moon_position) < 0.5:
                                return temp_subject
                        
                        # Se não encontrou a posição exata, retorna a mais próxima
                        return temp_subject
                
                # Se não encontrou nas horas, retorna o mapa do meio-dia
                return temp_subject
        
        # Se não encontrou o retorno lunar no mês especificado, usar o primeiro dia do mês
        return AstrologicalSubject(
            name=f"{natal_subject.name}_LunarReturn",
            year=return_year,
            month=return_month,
            day=1,
            hour=12,
            minute=0,
            city="",
            lng=location_lng,
            lat=location_lat,
            tz_str=location_tz
        )
    
    else:
        raise ValueError(f"Tipo de retorno não suportado: {return_type}")

def get_return_chart_cached(
    natal_subject: AstrologicalSubject, 
    return_year: int, 
    return_month: Optional[int] = None,
    return_type: Literal["solar", "lunar"] = "solar",
    location_longitude: Optional[float] = None,
    location_latitude: Optional[float] = None,
    location_tz_str: Optional[str] = None
) -> AstrologicalSubject:
    """
    Calcula um mapa de retorno solar ou lunar com cache.
    
    Args:
        natal_subject (AstrologicalSubject): Objeto AstrologicalSubject do mapa natal.
        return_year (int): Ano para o qual calcular o retorno.
        return_month (Optional[int]): Mês para o qual calcular o retorno (apenas para retorno lunar).
        return_type (str): Tipo de retorno, "solar" ou "lunar".
        location_longitude (Optional[float]): Longitude do local do retorno.
        location_latitude (Optional[float]): Latitude do local do retorno.
        location_tz_str (Optional[str]): Fuso horário do local do retorno.
        
    Returns:
        AstrologicalSubject: Objeto AstrologicalSubject do mapa de retorno.
    """
    # Gerar a chave de cache
    cache_key = get_cache_key(
        f"{return_type}_return",
        natal_name=natal_subject.name,
        natal_year=natal_subject.year,
        natal_month=natal_subject.month,
        natal_day=natal_subject.day,
        natal_hour=natal_subject.hour,
        natal_minute=natal_subject.minute,
        return_year=return_year,
        return_month=return_month,
        location_longitude=location_longitude or natal_subject.lng,
        location_latitude=location_latitude or natal_subject.lat,
        location_tz_str=location_tz_str or natal_subject.tz_str
    )
    
    # Verificar se existe no cache
    cached_subject = get_from_cache(cache_key)
    if cached_subject is not None:
        return cached_subject
    
    # Se não estiver no cache, calcular
    subject = get_return_chart(
        natal_subject=natal_subject,
        return_year=return_year,
        return_month=return_month,
        return_type=return_type,
        location_longitude=location_longitude,
        location_latitude=location_latitude,
        location_tz_str=location_tz_str
    )
    
    # Salvar no cache
    save_to_cache(cache_key, subject)
    
    return subject

def get_progressed_chart_cached(
    natal_subject: AstrologicalSubject, 
    prog_year: int, 
    prog_month: int, 
    prog_day: int
) -> AstrologicalSubject:
    """
    Calcula o mapa progressado secundário com cache.
    
    Args:
        natal_subject (AstrologicalSubject): Objeto AstrologicalSubject do mapa natal.
        prog_year (int): Ano para o qual calcular a progressão.
        prog_month (int): Mês para o qual calcular a progressão.
        prog_day (int): Dia para o qual calcular a progressão.
        
    Returns:
        AstrologicalSubject: Objeto AstrologicalSubject do mapa progressado.
    """
    # Gerar a chave de cache
    cache_key = get_cache_key(
        "progressed_chart",
        natal_name=natal_subject.name,
        natal_year=natal_subject.year,
        natal_month=natal_subject.month,
        natal_day=natal_subject.day,
        natal_hour=natal_subject.hour,
        natal_minute=natal_subject.minute,
        prog_year=prog_year,
        prog_month=prog_month,
        prog_day=prog_day
    )
    
    # Verificar se existe no cache
    cached_subject = get_from_cache(cache_key)
    if cached_subject is not None:
        return cached_subject
    
    # Se não estiver no cache, calcular
    subject = get_progressed_chart(
        natal_subject=natal_subject,
        prog_year=prog_year,
        prog_month=prog_month,
        prog_day=prog_day
    )
    
    # Salvar no cache
    save_to_cache(cache_key, subject)
    
    return subject

def calculate_solar_arc_directions(
    natal_subject: AstrologicalSubject, 
    direction_date: datetime
) -> Tuple[float, Dict[str, float]]:
    """
    Calcula as direções de arco solar.
    
    Args:
        natal_subject (AstrologicalSubject): Objeto AstrologicalSubject do mapa natal.
        direction_date (datetime): Data para a qual calcular as direções.
        
    Returns:
        Tuple[float, Dict[str, float]]: Valor do arco em graus e posições dos planetas direcionados.
    """
    # Data natal
    natal_date = datetime(
        natal_subject.year, 
        natal_subject.month, 
        natal_subject.day, 
        natal_subject.hour, 
        natal_subject.minute
    )
    
    # Calcular a diferença em anos decimais
    years_diff = (direction_date.year - natal_date.year) + \
                 (direction_date.month - natal_date.month) / 12 + \
                 (direction_date.day - natal_date.day) / 365.25
    
    # Calcular o arco solar (aproximadamente 1 grau por ano)
    solar_arc = years_diff
    
    # Obter as posições dos planetas natais
    natal_positions = {}
    for planet_key, planet_data in natal_subject.planets.items():
        natal_positions[planet_key] = planet_data['position']['longitude']
    
    # Calcular as posições direcionadas (adicionar o arco solar)
    directed_positions = {}
    for planet_key, position in natal_positions.items():
        directed_positions[planet_key] = (position + solar_arc) % 360
    
    return solar_arc, directed_positions
