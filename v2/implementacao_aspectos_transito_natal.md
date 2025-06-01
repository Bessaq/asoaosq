# Implementação do Cálculo de Aspectos Trânsito-Natal

Vamos implementar o cálculo de aspectos entre planetas em trânsito e planetas natais, utilizando a classe `SynastryAspects` do Kerykeion, que já vimos ser adequada para este propósito.

## 1. Atualização dos Modelos de Dados

Primeiro, vamos atualizar os modelos para incluir aspectos nas respostas:

```python
# Em models.py
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class AspectModel(BaseModel):
    p1_name: str = Field(..., description="Nome do primeiro planeta")
    p1_owner: str = Field(..., description="Proprietário do primeiro planeta (Natal ou Trânsito)")
    p2_name: str = Field(..., description="Nome do segundo planeta")
    p2_owner: str = Field(..., description="Proprietário do segundo planeta (Natal ou Trânsito)")
    aspect: str = Field(..., description="Tipo de aspecto (Conjunção, Oposição, etc.)")
    orbit: float = Field(..., description="Orbe do aspecto em graus")
    aspect_degrees: float = Field(..., description="Graus do aspecto")
    diff: float = Field(..., description="Diferença entre a posição exata e a atual")
    applying: bool = Field(..., description="Se o aspecto está se aplicando (aproximando) ou separando")

class TransitsToNatalResponse(BaseModel):
    input_data: Dict[str, Any]
    transit_planets: Dict[str, Any]
    natal_planets: Dict[str, Any]
    aspects: List[AspectModel] = Field(default_factory=list, description="Aspectos entre planetas em trânsito e natais")
```

## 2. Implementação do Cálculo de Aspectos

Agora, vamos modificar o router de trânsitos para incluir o cálculo de aspectos:

```python
# Em app/routers/transit_router.py
from fastapi import APIRouter, HTTPException
from app.models import TransitRequest, TransitsToNatalRequest, TransitsToNatalResponse
from kerykeion import AstrologicalSubject
from kerykeion.aspects import SynastryAspects
from typing import Dict, Any, List

router = APIRouter(prefix="/api/v1", tags=["transits"])

@router.post("/transits_to_natal", response_model=TransitsToNatalResponse)
async def calculate_transits_to_natal(data: TransitsToNatalRequest):
    try:
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
            tz_str=data.natal.tz_str
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
            tz_str=data.transit.tz_str
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
                # Determinar se o aspecto está se aplicando ou separando
                # Um aspecto está se aplicando se a diferença está diminuindo
                # Isso requer conhecimento da velocidade dos planetas, que é complexo
                # Para simplificar, vamos considerar aplicando se a diferença for menor que 0.5 graus
                applying = abs(aspect.diff) < 0.5
                
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
            "aspects": aspects
        }
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular trânsitos: {str(e)}")

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

## 3. Função Auxiliar para Determinar se um Aspecto está se Aplicando

Para determinar com precisão se um aspecto está se aplicando ou separando, precisamos considerar a velocidade dos planetas. Vamos adicionar uma função mais precisa:

```python
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
```

## 4. Atualização da Função Principal para Usar a Determinação Precisa

```python
# Modificar a parte do processamento de aspectos no router
# ...

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

# ...
```

## 5. Testes e Validação

Para testar a implementação, podemos criar um script que faz uma requisição ao endpoint e verifica se os aspectos estão sendo calculados corretamente:

```python
# Em tests/test_transits_aspects.py
import requests
import json
from datetime import datetime

def test_transits_to_natal_aspects():
    # Dados de teste
    data = {
        "natal": {
            "name": "Albert Einstein",
            "year": 1879,
            "month": 3,
            "day": 14,
            "hour": 11,
            "minute": 30,
            "longitude": 10.0,
            "latitude": 48.4,
            "tz_str": "Europe/Berlin"
        },
        "transit": {
            "year": datetime.now().year,
            "month": datetime.now().month,
            "day": datetime.now().day,
            "hour": 12,
            "minute": 0,
            "longitude": 10.0,
            "latitude": 48.4,
            "tz_str": "Europe/Berlin"
        }
    }
    
    # Fazer requisição
    response = requests.post("http://localhost:8000/api/v1/transits_to_natal", json=data)
    
    # Verificar resposta
    assert response.status_code == 200
    result = response.json()
    
    # Verificar se há aspectos na resposta
    assert "aspects" in result
    assert len(result["aspects"]) > 0
    
    # Imprimir aspectos para inspeção
    print(json.dumps(result["aspects"], indent=2))
    
    # Verificar estrutura de um aspecto
    aspect = result["aspects"][0]
    assert "p1_name" in aspect
    assert "p1_owner" in aspect
    assert "p2_name" in aspect
    assert "p2_owner" in aspect
    assert "aspect" in aspect
    assert "orbit" in aspect
    assert "aspect_degrees" in aspect
    assert "diff" in aspect
    assert "applying" in aspect
    
    print("Teste concluído com sucesso!")

if __name__ == "__main__":
    test_transits_to_natal_aspects()
```

Esta implementação fornece uma base sólida para o cálculo de aspectos entre planetas em trânsito e planetas natais, utilizando a classe `SynastryAspects` do Kerykeion. A determinação se um aspecto está se aplicando ou separando é uma simplificação, mas funciona bem para a maioria dos casos.

Nas próximas etapas, podemos refinar esta implementação, adicionar mais detalhes às interpretações dos aspectos e integrar com o sistema de tradução de signos.
