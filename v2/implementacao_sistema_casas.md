# Implementação do Suporte para Sistema de Casas Personalizado

Vamos implementar o suporte para personalização do sistema de casas na API, seguindo a estratégia definida anteriormente.

## 1. Atualização dos Modelos de Dados

Primeiro, vamos atualizar os modelos para incluir o parâmetro de sistema de casas:

```python
# Em models.py
from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

# Definir os sistemas de casas suportados
HouseSystemType = Literal[
    "Placidus", "Koch", "Porphyrius", "Regiomontanus", "Campanus", 
    "Equal", "Whole Sign", "Alcabitus", "Morinus", "Horizontal", 
    "Topocentric", "Vehlow"
]

# Mapeamento de nomes amigáveis para os códigos do Kerykeion
HOUSE_SYSTEM_MAP = {
    "Placidus": "P",
    "Koch": "K",
    "Porphyrius": "O",
    "Regiomontanus": "R",
    "Campanus": "C",
    "Equal": "A",  # ou "E"
    "Whole Sign": "W",
    "Alcabitus": "B",
    "Morinus": "M",
    "Horizontal": "H",
    "Topocentric": "T",
    "Vehlow": "V"
}

class NatalChartRequest(BaseModel):
    name: Optional[str] = None
    year: int
    month: int
    day: int
    hour: int
    minute: int
    longitude: float
    latitude: float
    tz_str: str
    house_system: Optional[HouseSystemType] = Field(default="Placidus", description="Sistema de casas a ser utilizado")

class TransitRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    longitude: float
    latitude: float
    tz_str: str
    house_system: Optional[HouseSystemType] = Field(default="Placidus", description="Sistema de casas a ser utilizado")

class TransitsToNatalRequest(BaseModel):
    natal: NatalChartRequest
    transit: TransitRequest
```

## 2. Atualização do Router de Mapa Natal

Agora, vamos modificar o router de mapa natal para usar o sistema de casas especificado:

```python
# Em app/routers/natal_chart_router.py
from fastapi import APIRouter, HTTPException
from app.models import NatalChartRequest, NatalChartResponse, HOUSE_SYSTEM_MAP
from kerykeion import AstrologicalSubject

router = APIRouter(prefix="/api/v1", tags=["natal_chart"])

@router.post("/natal_chart", response_model=NatalChartResponse)
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular mapa natal: {str(e)}")

def _extract_planet_data(planet_point):
    """Extrai dados relevantes de um ponto planetário."""
    if not planet_point:
        return None
    
    return {
        "name": planet_point.name,
        "longitude": planet_point.longitude,
        "latitude": planet_point.latitude,
        "sign": planet_point.sign,
        "sign_num": planet_point.sign_num,
        "house": planet_point.house,
        "retrograde": planet_point.retrograde
    }
```

## 3. Atualização do Router de Trânsitos

Vamos modificar o router de trânsitos para também usar o sistema de casas especificado:

```python
# Em app/routers/transit_router.py
from fastapi import APIRouter, HTTPException
from app.models import TransitRequest, TransitsToNatalRequest, TransitsToNatalResponse, HOUSE_SYSTEM_MAP
from kerykeion import AstrologicalSubject
from kerykeion.aspects import SynastryAspects

router = APIRouter(prefix="/api/v1", tags=["transits"])

@router.post("/current_transits", response_model=Dict[str, Any])
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

@router.post("/transits_to_natal", response_model=TransitsToNatalResponse)
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
        "longitude": planet_point.longitude,
        "latitude": planet_point.latitude,
        "sign": planet_point.sign,
        "sign_num": planet_point.sign_num,
        "house": planet_point.house,
        "retrograde": planet_point.retrograde
    }
```

## 4. Atualização da Documentação

Vamos adicionar informações sobre o sistema de casas na documentação da API:

```python
# Em main.py
from fastapi import FastAPI
from app.routers import natal_chart_router, transit_router
import uvicorn

app = FastAPI(
    title="API de Astrologia",
    description="""
    API para cálculos astrológicos, incluindo mapas natais, trânsitos e aspectos.
    
    ## Sistemas de Casas Suportados
    
    A API suporta os seguintes sistemas de casas:
    
    - **Placidus** (padrão): Sistema mais comum, baseado na divisão do tempo que leva para um ponto da eclíptica passar do horizonte ao meio-céu.
    - **Koch**: Baseado na divisão do tempo que leva para um ponto da eclíptica passar do horizonte ao meridiano.
    - **Porphyrius**: Sistema antigo que divide o espaço entre os quatro ângulos.
    - **Regiomontanus**: Baseado na divisão do equador celeste.
    - **Campanus**: Baseado na divisão do primeiro vertical.
    - **Equal**: Casas de tamanho igual (30°) a partir do Ascendente.
    - **Whole Sign**: Cada casa corresponde a um signo inteiro.
    - **Alcabitus**: Sistema medieval baseado na divisão do equador celeste.
    - **Morinus**: Sistema que ignora a rotação da Terra.
    - **Horizontal**: Baseado no horizonte local.
    - **Topocentric**: Variação do sistema Placidus.
    - **Vehlow**: Variação do sistema Equal com deslocamento de 5°.
    
    Para especificar um sistema de casas, inclua o parâmetro `house_system` na requisição.
    """,
    version="1.0.0"
)

app.include_router(natal_chart_router.router)
app.include_router(transit_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 5. Testes e Validação

Para testar a implementação, podemos criar um script que faz requisições com diferentes sistemas de casas e verifica se os resultados são diferentes:

```python
# Em tests/test_house_systems.py
import requests
import json

def test_house_systems():
    # Dados de teste
    base_data = {
        "name": "Albert Einstein",
        "year": 1879,
        "month": 3,
        "day": 14,
        "hour": 11,
        "minute": 30,
        "longitude": 10.0,
        "latitude": 48.4,
        "tz_str": "Europe/Berlin"
    }
    
    # Sistemas de casas a testar
    house_systems = ["Placidus", "Koch", "Whole Sign", "Equal", "Campanus"]
    
    results = {}
    
    # Fazer requisições para cada sistema de casas
    for system in house_systems:
        data = base_data.copy()
        data["house_system"] = system
        
        response = requests.post("http://localhost:8000/api/v1/natal_chart", json=data)
        
        assert response.status_code == 200
        result = response.json()
        
        # Guardar as posições das cúspides das casas
        house_cusps = {}
        for house_key, house_data in result["houses"].items():
            house_cusps[house_key] = {
                "longitude": house_data["longitude"],
                "sign": house_data["sign"]
            }
        
        results[system] = house_cusps
    
    # Verificar se há diferenças entre os sistemas
    # Comparar Placidus com cada um dos outros sistemas
    placidus_cusps = results["Placidus"]
    
    for system in house_systems[1:]:
        system_cusps = results[system]
        
        # Verificar se há pelo menos uma diferença
        differences = False
        for house_key in placidus_cusps:
            if placidus_cusps[house_key]["longitude"] != system_cusps[house_key]["longitude"]:
                differences = True
                break
        
        assert differences, f"Não há diferenças entre Placidus e {system}"
        print(f"Verificado: {system} é diferente de Placidus")
    
    # Imprimir resultados para inspeção
    print("\nResultados detalhados:")
    for system, cusps in results.items():
        print(f"\n{system}:")
        for house_key, house_data in cusps.items():
            print(f"  {house_key}: {house_data['longitude']}° ({house_data['sign']})")
    
    print("\nTeste concluído com sucesso!")

if __name__ == "__main__":
    test_house_systems()
```

Esta implementação fornece suporte completo para personalização do sistema de casas em todos os endpoints relevantes da API, mantendo a compatibilidade com requisições existentes e seguindo as melhores práticas RESTful. A documentação foi atualizada para incluir informações sobre os sistemas de casas suportados, e testes foram criados para validar a implementação.

Nas próximas etapas, podemos integrar esta funcionalidade com o sistema de tradução de signos e a geração de SVG.
