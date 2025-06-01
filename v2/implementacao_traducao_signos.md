# Implementação da Tradução de Signos para Português

Vamos implementar a tradução dos nomes dos signos para português em todas as respostas da API, conforme a estratégia definida anteriormente.

## 1. Criação do Módulo de Tradução

Primeiro, vamos criar um módulo dedicado para as traduções:

```python
# Em app/utils/translations.py

# Mapeamento de abreviações em inglês para nomes completos em português
SIGN_TRANSLATIONS = {
    "Ari": "Áries",
    "Tau": "Touro",
    "Gem": "Gêmeos",
    "Can": "Câncer",
    "Leo": "Leão",
    "Vir": "Virgem",
    "Lib": "Libra",
    "Sco": "Escorpião",
    "Sag": "Sagitário",
    "Cap": "Capricórnio",
    "Aqu": "Aquário",
    "Pis": "Peixes"
}

# Mapeamento de nomes completos em inglês para português (para uso nos gráficos SVG)
FULL_SIGN_TRANSLATIONS = {
    "Aries": "Áries",
    "Taurus": "Touro",
    "Gemini": "Gêmeos",
    "Cancer": "Câncer",
    "Leo": "Leão",
    "Virgo": "Virgem",
    "Libra": "Libra",
    "Scorpio": "Escorpião",
    "Sagittarius": "Sagitário",
    "Capricorn": "Capricórnio",
    "Aquarius": "Aquário",
    "Pisces": "Peixes"
}

# Mapeamento de nomes de planetas em inglês para português
PLANET_TRANSLATIONS = {
    "Sun": "Sol",
    "Moon": "Lua",
    "Mercury": "Mercúrio",
    "Venus": "Vênus",
    "Mars": "Marte",
    "Jupiter": "Júpiter",
    "Saturn": "Saturno",
    "Uranus": "Urano",
    "Neptune": "Netuno",
    "Pluto": "Plutão",
    "North Node": "Nodo Norte",
    "Mean Node": "Nodo Norte Médio",
    "True Node": "Nodo Norte Verdadeiro",
    "South Node": "Nodo Sul",
    "Mean South Node": "Nodo Sul Médio",
    "True South Node": "Nodo Sul Verdadeiro",
    "Chiron": "Quíron",
    "Lilith": "Lilith",
    "Mean Lilith": "Lilith Média",
    "True Lilith": "Lilith Verdadeira",
    "Ascendant": "Ascendente",
    "Midheaven": "Meio do Céu"
}

# Mapeamento de aspectos em inglês para português
ASPECT_TRANSLATIONS = {
    "Conjunction": "Conjunção",
    "Opposition": "Oposição",
    "Trine": "Trígono",
    "Square": "Quadratura",
    "Sextile": "Sextil",
    "Quincunx": "Quincúncio",
    "Semisextile": "Semisextil",
    "Semisquare": "Semiquadratura",
    "Sesquisquare": "Sesquiquadratura",
    "Quintile": "Quintil",
    "Biquintile": "Biquintil"
}

def translate_sign(sign_abbr):
    """Traduz a abreviação do signo em inglês para o nome completo em português."""
    return SIGN_TRANSLATIONS.get(sign_abbr, sign_abbr)

def translate_full_sign(sign_name):
    """Traduz o nome completo do signo em inglês para português."""
    return FULL_SIGN_TRANSLATIONS.get(sign_name, sign_name)

def translate_planet(planet_name):
    """Traduz o nome do planeta em inglês para português."""
    return PLANET_TRANSLATIONS.get(planet_name, planet_name)

def translate_aspect(aspect_name):
    """Traduz o nome do aspecto em inglês para português."""
    return ASPECT_TRANSLATIONS.get(aspect_name, aspect_name)
```

## 2. Criação do Middleware de Processamento de Resposta

Agora, vamos criar um middleware para processar as respostas da API e traduzir os signos:

```python
# Em app/utils/response_processor.py
from app.utils.translations import translate_sign, translate_planet, translate_aspect

def process_planet_data(planet_data):
    """Processa os dados de um planeta para incluir tradução."""
    if not planet_data:
        return None
    
    result = planet_data.copy()
    
    # Traduzir signo
    if "sign" in result:
        # Preservar o signo original em um novo campo
        result["sign_original"] = result["sign"]
        # Traduzir o signo
        result["sign"] = translate_sign(result["sign"])
    
    # Traduzir nome do planeta
    if "name" in result:
        # Preservar o nome original em um novo campo
        result["name_original"] = result["name"]
        # Traduzir o nome
        result["name"] = translate_planet(result["name"])
    
    return result

def process_house_data(house_data):
    """Processa os dados de uma casa para incluir tradução."""
    if not house_data:
        return None
    
    result = house_data.copy()
    
    # Traduzir signo
    if "sign" in result:
        # Preservar o signo original em um novo campo
        result["sign_original"] = result["sign"]
        # Traduzir o signo
        result["sign"] = translate_sign(result["sign"])
    
    return result

def process_aspect_data(aspect_data):
    """Processa os dados de um aspecto para incluir tradução."""
    if not aspect_data:
        return None
    
    result = aspect_data.copy()
    
    # Traduzir tipo de aspecto
    if "aspect" in result:
        # Preservar o aspecto original em um novo campo
        result["aspect_original"] = result["aspect"]
        # Traduzir o aspecto
        result["aspect"] = translate_aspect(result["aspect"])
    
    # Traduzir nomes dos planetas
    if "p1_name" in result:
        result["p1_name_original"] = result["p1_name"]
        result["p1_name"] = translate_planet(result["p1_name"])
    
    if "p2_name" in result:
        result["p2_name_original"] = result["p2_name"]
        result["p2_name"] = translate_planet(result["p2_name"])
    
    return result

def process_natal_chart_response(response_data):
    """Processa a resposta completa do mapa natal para incluir traduções."""
    if not response_data:
        return response_data
    
    result = response_data.copy()
    
    # Processar planetas
    if "planets" in result:
        for planet_key, planet_data in result["planets"].items():
            result["planets"][planet_key] = process_planet_data(planet_data)
    
    # Processar casas
    if "houses" in result:
        for house_key, house_data in result["houses"].items():
            result["houses"][house_key] = process_house_data(house_data)
    
    # Processar ascendente e meio do céu
    if "ascendant" in result:
        result["ascendant"] = process_house_data(result["ascendant"])
    if "midheaven" in result:
        result["midheaven"] = process_house_data(result["midheaven"])
    
    # Processar aspectos
    if "aspects" in result:
        result["aspects"] = [process_aspect_data(aspect) for aspect in result["aspects"]]
    
    return result

def process_transits_response(response_data):
    """Processa a resposta de trânsitos para incluir traduções."""
    if not response_data:
        return response_data
    
    result = response_data.copy()
    
    # Processar planetas em trânsito
    if "planets" in result:
        for planet_key, planet_data in result["planets"].items():
            result["planets"][planet_key] = process_planet_data(planet_data)
    
    return result

def process_transits_to_natal_response(response_data):
    """Processa a resposta de trânsitos para mapa natal para incluir traduções."""
    if not response_data:
        return response_data
    
    result = response_data.copy()
    
    # Processar planetas natais
    if "natal_planets" in result:
        for planet_key, planet_data in result["natal_planets"].items():
            result["natal_planets"][planet_key] = process_planet_data(planet_data)
    
    # Processar planetas em trânsito
    if "transit_planets" in result:
        for planet_key, planet_data in result["transit_planets"].items():
            result["transit_planets"][planet_key] = process_planet_data(planet_data)
    
    # Processar aspectos
    if "aspects" in result:
        result["aspects"] = [process_aspect_data(aspect) for aspect in result["aspects"]]
    
    return result
```

## 3. Atualização dos Routers para Usar o Processador de Resposta

Agora, vamos modificar os routers para aplicar o processador de resposta:

```python
# Em app/routers/natal_chart_router.py
from app.utils.response_processor import process_natal_chart_response

@router.post("/natal_chart", response_model=NatalChartResponse)
async def calculate_natal_chart(data: NatalChartRequest):
    try:
        # Código existente para calcular o mapa natal...
        
        # Antes de retornar, aplicar tradução
        response = process_natal_chart_response(response)
        
        return response
    except Exception as e:
        # Tratamento de erro existente...
```

```python
# Em app/routers/transit_router.py
from app.utils.response_processor import process_transits_response, process_transits_to_natal_response

@router.post("/current_transits", response_model=Dict[str, Any])
async def calculate_current_transits(data: TransitRequest):
    try:
        # Código existente para calcular os trânsitos...
        
        # Antes de retornar, aplicar tradução
        response = process_transits_response(response)
        
        return response
    except Exception as e:
        # Tratamento de erro existente...

@router.post("/transits_to_natal", response_model=TransitsToNatalResponse)
async def calculate_transits_to_natal(data: TransitsToNatalRequest):
    try:
        # Código existente para calcular os trânsitos para o mapa natal...
        
        # Antes de retornar, aplicar tradução
        response = process_transits_to_natal_response(response)
        
        return response
    except Exception as e:
        # Tratamento de erro existente...
```

## 4. Atualização do Router de SVG para Usar Traduções

Vamos atualizar o router de SVG para usar as traduções:

```python
# Em app/routers/svg_chart_router.py
from app.utils.translations import FULL_SIGN_TRANSLATIONS, PLANET_TRANSLATIONS, ASPECT_TRANSLATIONS

@router.post("/svg_chart", response_class=Response)
async def generate_svg_chart(data: SVGChartRequest):
    try:
        # Código existente para gerar o gráfico SVG...
        
        # Aplicar idioma
        if data.language == "pt":
            # Criar um dicionário completo de traduções
            translations = {}
            translations.update(FULL_SIGN_TRANSLATIONS)
            translations.update(PLANET_TRANSLATIONS)
            translations.update(ASPECT_TRANSLATIONS)
            
            # Adicionar traduções para casas
            for i in range(1, 13):
                translations[f"House {i}"] = f"Casa {i}"
            
            # Aplicar traduções ao gráfico
            chart.set_language_labels(translations)
        
        # Resto do código existente...
    except Exception as e:
        # Tratamento de erro existente...
```

## 5. Atualização dos Modelos de Resposta

Vamos atualizar os modelos de resposta para incluir os campos originais:

```python
# Em models.py
class PlanetData(BaseModel):
    name: str
    name_original: Optional[str] = None
    longitude: float
    latitude: float
    sign: str
    sign_original: Optional[str] = None
    sign_num: int
    house: int
    retrograde: bool

class HouseData(BaseModel):
    number: int
    sign: str
    sign_original: Optional[str] = None
    sign_num: int
    longitude: float

class AspectData(BaseModel):
    p1_name: str
    p1_name_original: Optional[str] = None
    p1_owner: str
    p2_name: str
    p2_name_original: Optional[str] = None
    p2_owner: str
    aspect: str
    aspect_original: Optional[str] = None
    orbit: float
    aspect_degrees: float
    diff: float
    applying: bool
```

## 6. Adição de Parâmetro de Idioma nas Requisições

Para permitir que os usuários escolham o idioma, vamos adicionar um parâmetro opcional nas requisições:

```python
# Em models.py
class NatalChartRequest(BaseModel):
    # Campos existentes...
    language: Optional[Literal["en", "pt"]] = Field(default="pt", description="Idioma para os textos na resposta")

class TransitRequest(BaseModel):
    # Campos existentes...
    language: Optional[Literal["en", "pt"]] = Field(default="pt", description="Idioma para os textos na resposta")

class TransitsToNatalRequest(BaseModel):
    natal: NatalChartRequest
    transit: TransitRequest
```

E atualizar os routers para respeitar esse parâmetro:

```python
# Em app/routers/natal_chart_router.py
@router.post("/natal_chart", response_model=NatalChartResponse)
async def calculate_natal_chart(data: NatalChartRequest):
    try:
        # Código existente...
        
        # Aplicar tradução apenas se o idioma for português
        if data.language == "pt":
            response = process_natal_chart_response(response)
        
        return response
    except Exception as e:
        # Tratamento de erro existente...
```

Aplicar a mesma lógica nos outros routers.

## 7. Testes e Validação

Para testar a implementação, vamos criar um script que faz requisições com diferentes idiomas e verifica as traduções:

```python
# Em tests/test_translations.py
import requests
import json

def test_translations():
    # Dados de teste
    data = {
        "name": "Albert Einstein",
        "year": 1879,
        "month": 3,
        "day": 14,
        "hour": 11,
        "minute": 30,
        "longitude": 10.0,
        "latitude": 48.4,
        "tz_str": "Europe/Berlin",
        "house_system": "Placidus"
    }
    
    # Testar com idioma inglês
    data_en = data.copy()
    data_en["language"] = "en"
    
    response_en = requests.post("http://localhost:8000/api/v1/natal_chart", json=data_en)
    
    assert response_en.status_code == 200
    result_en = response_en.json()
    
    # Testar com idioma português
    data_pt = data.copy()
    data_pt["language"] = "pt"
    
    response_pt = requests.post("http://localhost:8000/api/v1/natal_chart", json=data_pt)
    
    assert response_pt.status_code == 200
    result_pt = response_pt.json()
    
    # Verificar traduções
    # Sol em inglês vs português
    sun_en = result_en["planets"]["sun"]["sign"]
    sun_pt = result_pt["planets"]["sun"]["sign"]
    sun_pt_original = result_pt["planets"]["sun"]["sign_original"]
    
    print(f"Sol em inglês: {sun_en}")
    print(f"Sol em português: {sun_pt}")
    print(f"Original preservado: {sun_pt_original}")
    
    assert sun_en == sun_pt_original  # O original em português deve ser igual ao inglês
    assert sun_en != sun_pt  # A tradução deve ser diferente do inglês
    
    # Verificar se todos os signos foram traduzidos
    for planet_key, planet_data in result_pt["planets"].items():
        if planet_data:
            assert "sign" in planet_data
            assert "sign_original" in planet_data
            assert planet_data["sign"] != planet_data["sign_original"]
            print(f"{planet_key}: {planet_data['sign_original']} -> {planet_data['sign']}")
    
    # Verificar tradução nos gráficos SVG
    svg_data = {
        "natal_chart": data_pt,
        "chart_type": "natal",
        "language": "pt"
    }
    
    response_svg = requests.post(
        "http://localhost:8000/api/v1/svg_chart_base64",
        json=svg_data
    )
    
    assert response_svg.status_code == 200
    
    print("\nTeste concluído com sucesso!")

if __name__ == "__main__":
    test_translations()
```

## 8. Atualização da Documentação

Vamos atualizar a documentação para incluir informações sobre o suporte a idiomas:

```python
# Em main.py
app = FastAPI(
    title="API de Astrologia",
    description="""
    API para cálculos astrológicos, incluindo mapas natais, trânsitos, aspectos e geração de gráficos SVG.
    
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
    
    ## Suporte a Idiomas
    
    A API suporta os seguintes idiomas:
    
    - **Inglês (en)**: Nomes de signos, planetas e aspectos em inglês.
    - **Português (pt)** (padrão): Nomes de signos, planetas e aspectos traduzidos para português.
    
    Para especificar o idioma, inclua o parâmetro `language` na requisição.
    """,
    version="1.0.0"
)
```

## 9. Considerações Adicionais

1. **Extensibilidade**: A estrutura proposta permite adicionar facilmente suporte para outros idiomas no futuro.

2. **Preservação dos Dados Originais**: Mantemos os valores originais em inglês para compatibilidade com sistemas externos.

3. **Consistência**: Garantimos que as traduções sejam aplicadas de forma consistente em toda a API.

4. **Desempenho**: O processamento de tradução é leve e não deve impactar significativamente o desempenho da API.

5. **Testes**: É importante testar todas as combinações de parâmetros para garantir que as traduções funcionem corretamente em todos os cenários.

Esta implementação fornece uma solução completa para a tradução dos nomes dos signos, planetas e aspectos para português em todas as respostas da API, mantendo a compatibilidade com sistemas existentes e permitindo que os usuários escolham o idioma de sua preferência.
