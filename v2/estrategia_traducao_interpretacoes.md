# Estratégia para Tradução de Signos e Integração de Interpretações

## Análise da Situação Atual

Após analisar o código do projeto, identifiquei que os nomes dos signos são retornados em formato abreviado em inglês (ex: "Gem" para Gêmeos) diretamente do Kerykeion. Além disso, a API atualmente não fornece interpretações textuais para os elementos astrológicos.

## Estratégia para Tradução de Signos

### 1. Criação de Mapeamento de Tradução

Vamos criar um mapeamento completo dos signos em inglês para português:

```python
# Em um novo arquivo: app/utils/translations.py

SIGN_TRANSLATIONS = {
    # Abreviações em inglês para nomes completos em português
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

# Mapeamento inverso para uso interno se necessário
PORTUGUESE_TO_ENGLISH = {v: k for k, v in SIGN_TRANSLATIONS.items()}

def translate_sign(sign_abbr):
    """Traduz a abreviação do signo em inglês para o nome completo em português."""
    return SIGN_TRANSLATIONS.get(sign_abbr, sign_abbr)
```

### 2. Implementação de Middleware de Tradução

Criar uma função que processa os resultados do Kerykeion antes de retorná-los ao cliente:

```python
# Em app/utils/response_processor.py

from app.utils.translations import translate_sign

def process_planet_data(planet_data):
    """Processa os dados de um planeta para incluir tradução."""
    if planet_data and "sign" in planet_data:
        # Preservar o signo original em um novo campo
        planet_data["sign_original"] = planet_data["sign"]
        # Traduzir o signo
        planet_data["sign"] = translate_sign(planet_data["sign"])
    return planet_data

def process_house_data(house_data):
    """Processa os dados de uma casa para incluir tradução."""
    if house_data and "sign" in house_data:
        # Preservar o signo original em um novo campo
        house_data["sign_original"] = house_data["sign"]
        # Traduzir o signo
        house_data["sign"] = translate_sign(house_data["sign"])
    return house_data

def process_natal_chart_response(response_data):
    """Processa a resposta completa do mapa natal para incluir traduções."""
    # Processar planetas
    for planet_key in ["sun", "moon", "mercury", "venus", "mars", "jupiter", 
                      "saturn", "uranus", "neptune", "pluto", "north_node", 
                      "south_node", "chiron"]:
        if planet_key in response_data:
            response_data[planet_key] = process_planet_data(response_data[planet_key])
    
    # Processar casas
    if "houses" in response_data:
        for house_key, house_data in response_data["houses"].items():
            response_data["houses"][house_key] = process_house_data(house_data)
    
    # Processar ascendente e meio do céu
    if "ascendant" in response_data:
        response_data["ascendant"] = process_house_data(response_data["ascendant"])
    if "midheaven" in response_data:
        response_data["midheaven"] = process_house_data(response_data["midheaven"])
    
    return response_data
```

### 3. Integração nos Routers

Modificar os routers para aplicar a tradução:

```python
# Em natal_chart_router.py
@router.post("/natal_chart", response_model=NatalChartResponse)
async def calculate_natal_chart(data: NatalChartRequest):
    try:
        # Código existente para calcular o mapa natal...
        
        # Antes de retornar, aplicar tradução
        response_data = process_natal_chart_response(response_data)
        
        return response_data
    except Exception as e:
        # Tratamento de erro existente...
```

Aplicar o mesmo padrão nos outros routers relevantes.

## Estratégia para Integração de Interpretações Textuais

### 1. Criação de Banco de Interpretações

Criar um arquivo JSON com interpretações básicas para diferentes elementos astrológicos:

```json
// Em app/data/interpretations.json
{
  "planets_in_signs": {
    "sun": {
      "Áries": "O Sol em Áries confere uma personalidade dinâmica, corajosa e pioneira. Há uma forte necessidade de autoafirmação e independência. Pessoas com Sol em Áries tendem a ser diretas, entusiasmadas e possuem iniciativa para começar novos projetos.",
      "Touro": "O Sol em Touro indica uma personalidade estável, prática e determinada. Há uma forte conexão com o mundo material e valorização da segurança. Pessoas com Sol em Touro tendem a ser pacientes, confiáveis e apreciam conforto e beleza.",
      // Continuar para todos os signos
    },
    "moon": {
      // Interpretações para Lua em cada signo
    },
    // Continuar para todos os planetas
  },
  "planets_in_houses": {
    "sun": {
      "1": "O Sol na primeira casa confere forte vitalidade e autoexpressão. A personalidade tende a ser marcante, com necessidade de se destacar e ser reconhecido. Há uma forte identificação com a aparência física e a maneira como se apresenta ao mundo.",
      // Continuar para todas as casas
    },
    // Continuar para todos os planetas
  },
  "aspects": {
    "sun_conjunct_moon": "A conjunção entre Sol e Lua indica uma forte integração entre a consciência e as emoções. Há harmonia entre os princípios masculino e feminino internos, resultando em uma personalidade coesa e autoconfiante.",
    "sun_square_moon": "A quadratura entre Sol e Lua indica tensão entre a vontade consciente e as necessidades emocionais. Pode haver conflito interno entre o que se deseja fazer e o que se sente, resultando em períodos de indecisão ou mudanças de humor.",
    // Continuar para todos os aspectos principais
  }
}
```

### 2. Criação de Serviço de Interpretação

Implementar um serviço que busca interpretações com base nos dados astrológicos:

```python
# Em app/services/interpretation_service.py

import json
import os

class InterpretationService:
    def __init__(self):
        # Carregar o arquivo de interpretações
        file_path = os.path.join(os.path.dirname(__file__), '../data/interpretations.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            self.interpretations = json.load(f)
    
    def get_planet_in_sign_interpretation(self, planet, sign):
        """Retorna a interpretação para um planeta em um signo."""
        try:
            return self.interpretations["planets_in_signs"][planet][sign]
        except KeyError:
            return f"Interpretação não disponível para {planet} em {sign}."
    
    def get_planet_in_house_interpretation(self, planet, house):
        """Retorna a interpretação para um planeta em uma casa."""
        try:
            house_num = str(house).replace("House_", "")
            return self.interpretations["planets_in_houses"][planet][house_num]
        except KeyError:
            return f"Interpretação não disponível para {planet} na casa {house}."
    
    def get_aspect_interpretation(self, aspect_key):
        """Retorna a interpretação para um aspecto."""
        try:
            return self.interpretations["aspects"][aspect_key]
        except KeyError:
            return f"Interpretação não disponível para {aspect_key}."
    
    def generate_basic_interpretation(self, natal_chart_data):
        """Gera uma interpretação básica para um mapa natal."""
        interpretations = {
            "sun_sign": self.get_planet_in_sign_interpretation("sun", natal_chart_data["sun"]["sign"]),
            "moon_sign": self.get_planet_in_sign_interpretation("moon", natal_chart_data["moon"]["sign"]),
            "ascendant": self.get_planet_in_sign_interpretation("ascendant", natal_chart_data["ascendant"]["sign"]),
            # Adicionar mais elementos conforme necessário
        }
        
        # Adicionar interpretações de aspectos
        aspect_interpretations = {}
        for aspect in natal_chart_data.get("aspects", []):
            aspect_key = f"{aspect['planet1'].lower()}_{aspect['aspect_type'].lower()}_{aspect['planet2'].lower()}"
            aspect_interpretations[aspect_key] = self.get_aspect_interpretation(aspect_key)
        
        interpretations["aspects"] = aspect_interpretations
        
        return interpretations
```

### 3. Integração no Endpoint

Criar um novo endpoint para fornecer interpretações:

```python
# Em app/routers/interpretation_router.py

from fastapi import APIRouter, HTTPException
from app.models import NatalChartRequest, InterpretationResponse
from app.services.interpretation_service import InterpretationService

router = APIRouter(prefix="/api/v1", tags=["interpretations"])
interpretation_service = InterpretationService()

@router.post("/interpret_natal_chart", response_model=InterpretationResponse)
async def interpret_natal_chart(natal_chart_data: dict):
    """Gera interpretações textuais para um mapa natal."""
    try:
        interpretations = interpretation_service.generate_basic_interpretation(natal_chart_data)
        return {"interpretations": interpretations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar interpretações: {str(e)}")
```

### 4. Atualização dos Modelos

Adicionar novos modelos para suportar as interpretações:

```python
# Em models.py
class InterpretationResponse(BaseModel):
    interpretations: Dict[str, str]
```

## Considerações Adicionais

1. **Extensibilidade**: A estrutura proposta permite adicionar facilmente mais interpretações no futuro.

2. **Internacionalização**: O sistema pode ser expandido para suportar múltiplos idiomas além do português.

3. **Qualidade das Interpretações**: As interpretações devem ser baseadas em fontes astrológicas confiáveis e revisadas por especialistas.

4. **Personalização**: Considerar permitir que os usuários forneçam suas próprias interpretações ou escolham entre diferentes estilos de interpretação.

5. **Caching**: Implementar cache para interpretações frequentemente solicitadas para melhorar o desempenho.

Esta estratégia fornece uma base sólida para a tradução de signos e a integração de interpretações textuais, mantendo a flexibilidade para expansões futuras e garantindo uma experiência consistente para os usuários da API.
