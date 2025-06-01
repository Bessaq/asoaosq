# Estratégia para Personalização do Sistema de Casas

## Análise da Situação Atual

Após analisar o código do Kerykeion e a estrutura atual da API, identifiquei que o Kerykeion suporta diferentes sistemas de casas através do parâmetro `houses_system_identifier` na classe `AstrologicalSubject`. Este parâmetro aceita valores definidos no tipo `HousesSystemIdentifier`, que inclui opções como:

- "P" (Placidus) - Sistema padrão
- "K" (Koch)
- "O" (Porphyrius)
- "R" (Regiomontanus)
- "C" (Campanus)
- "A" ou "E" (Equal)
- "W" (Whole Sign)
- "B" (Alcabitus)
- "M" (Morinus)
- "H" (Horizontal)
- "T" (Topocentric)
- "V" (Vehlow)

Atualmente, a API não expõe esta funcionalidade aos usuários, utilizando apenas o sistema Placidus como padrão.

## Estratégia de Implementação

### 1. Modificação dos Modelos de Dados

Vamos atualizar os modelos de requisição para incluir um parâmetro opcional para o sistema de casas:

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
```

### 2. Atualização dos Routers

Modificar os routers para processar o novo parâmetro:

```python
# Em natal_chart_router.py
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
        
        # Resto do código permanece o mesmo...
```

Aplicar a mesma modificação nos outros routers relevantes (transit_router.py, etc.).

### 3. Atualização da Resposta

Incluir o sistema de casas utilizado na resposta para maior transparência:

```python
# Em models.py
class NatalChartResponse(BaseModel):
    input_data: NatalChartRequest
    # Outros campos permanecem os mesmos...
```

Isso garantirá que o sistema de casas escolhido seja incluído no campo `input_data` da resposta.

### 4. Documentação

Atualizar a documentação para incluir informações sobre o novo parâmetro:

```python
# Em main.py ou em um arquivo de documentação
"""
## Sistemas de Casas Suportados

A API suporta os seguintes sistemas de casas:

- Placidus (padrão): Sistema mais comum, baseado na divisão do tempo que leva para um ponto da eclíptica passar do horizonte ao meio-céu.
- Koch: Baseado na divisão do tempo que leva para um ponto da eclíptica passar do horizonte ao meridiano.
- Porphyrius: Sistema antigo que divide o espaço entre os quatro ângulos.
- Regiomontanus: Baseado na divisão do equador celeste.
- Campanus: Baseado na divisão do primeiro vertical.
- Equal: Casas de tamanho igual (30°) a partir do Ascendente.
- Whole Sign: Cada casa corresponde a um signo inteiro.
- Alcabitus: Sistema medieval baseado na divisão do equador celeste.
- Morinus: Sistema que ignora a rotação da Terra.
- Horizontal: Baseado no horizonte local.
- Topocentric: Variação do sistema Placidus.
- Vehlow: Variação do sistema Equal com deslocamento de 5°.

Para especificar um sistema de casas, inclua o parâmetro `house_system` na requisição.
"""
```

## Considerações Adicionais

1. **Validação**: Garantir que valores inválidos para `house_system` sejam tratados adequadamente, retornando para o padrão (Placidus) com um aviso no log.

2. **Desempenho**: O cálculo com diferentes sistemas de casas não deve impactar significativamente o desempenho, pois o Kerykeion já implementa essa funcionalidade internamente.

3. **Compatibilidade**: Manter compatibilidade com requisições existentes que não especificam o sistema de casas.

4. **Testes**: Implementar testes para verificar se os diferentes sistemas de casas estão sendo calculados corretamente.

Esta estratégia permite uma implementação limpa e modular da personalização do sistema de casas, mantendo a compatibilidade com a arquitetura existente e seguindo as melhores práticas RESTful.
