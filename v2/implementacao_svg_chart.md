# Implementação do Endpoint de Geração de SVG

Vamos implementar o endpoint para geração de gráficos SVG de mapas astrológicos, utilizando as funcionalidades do Kerykeion.

## 1. Análise das Capacidades do Kerykeion para SVG

O Kerykeion possui funcionalidades para geração de gráficos SVG através do módulo `charts`. Vamos utilizar essas capacidades para criar um endpoint que gere representações visuais de mapas natais e trânsitos.

## 2. Atualização dos Modelos de Dados

Primeiro, vamos criar modelos para as requisições de geração de SVG:

```python
# Em models.py
from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

class SVGChartRequest(BaseModel):
    natal_chart: NatalChartRequest
    transit_chart: Optional[TransitRequest] = None
    chart_type: Literal["natal", "transit", "combined"] = Field(
        default="natal", 
        description="Tipo de gráfico: 'natal' para apenas mapa natal, 'transit' para apenas trânsitos, 'combined' para mapa natal com trânsitos"
    )
    show_aspects: bool = Field(
        default=True,
        description="Se deve mostrar linhas de aspectos no gráfico"
    )
    language: Literal["en", "pt"] = Field(
        default="pt",
        description="Idioma para os textos no gráfico"
    )
    theme: Literal["light", "dark"] = Field(
        default="light",
        description="Tema de cores para o gráfico"
    )
```

## 3. Implementação do Router para SVG

Agora, vamos criar um novo router para o endpoint de geração de SVG:

```python
# Em app/routers/svg_chart_router.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.models import SVGChartRequest, HOUSE_SYSTEM_MAP
from kerykeion import AstrologicalSubject
from kerykeion.charts import MakeSvgChart
import io
import base64

router = APIRouter(prefix="/api/v1", tags=["svg_charts"])

@router.post("/svg_chart", response_class=Response)
async def generate_svg_chart(data: SVGChartRequest):
    try:
        # Converter o nome amigável do sistema de casas para o código do Kerykeion
        natal_house_system_code = HOUSE_SYSTEM_MAP.get(data.natal_chart.house_system, "P")
        
        # Criar objeto natal
        natal_subject = AstrologicalSubject(
            name=data.natal_chart.name or "Natal Chart",
            year=data.natal_chart.year,
            month=data.natal_chart.month,
            day=data.natal_chart.day,
            hour=data.natal_chart.hour,
            minute=data.natal_chart.minute,
            lng=data.natal_chart.longitude,
            lat=data.natal_chart.latitude,
            tz_str=data.natal_chart.tz_str,
            houses_system_identifier=natal_house_system_code
        )
        
        # Configurar parâmetros para o gráfico
        chart_params = {
            "chart_type": data.chart_type,
            "show_aspects": data.show_aspects,
            "language": data.language,
            "theme": data.theme
        }
        
        # Criar objeto de trânsito se necessário
        transit_subject = None
        if data.transit_chart and (data.chart_type == "transit" or data.chart_type == "combined"):
            transit_house_system_code = HOUSE_SYSTEM_MAP.get(data.transit_chart.house_system, "P")
            
            transit_subject = AstrologicalSubject(
                name="Transit",
                year=data.transit_chart.year,
                month=data.transit_chart.month,
                day=data.transit_chart.day,
                hour=data.transit_chart.hour,
                minute=data.transit_chart.minute,
                lng=data.transit_chart.longitude,
                lat=data.transit_chart.latitude,
                tz_str=data.transit_chart.tz_str,
                houses_system_identifier=transit_house_system_code
            )
        
        # Gerar o gráfico SVG
        if data.chart_type == "natal":
            chart = MakeSvgChart(natal_subject, chart_type="Natal")
        elif data.chart_type == "transit" and transit_subject:
            chart = MakeSvgChart(transit_subject, chart_type="Transit")
        elif data.chart_type == "combined" and transit_subject:
            chart = MakeSvgChart(natal_subject, chart_type="Synastry", second_obj=transit_subject)
        else:
            raise ValueError("Configuração de gráfico inválida")
        
        # Aplicar tema
        if data.theme == "dark":
            chart.set_theme("dark")
        
        # Aplicar idioma
        if data.language == "pt":
            # Substituir textos em inglês por português
            # Isso é uma simplificação, idealmente teríamos um sistema completo de tradução
            chart.set_language_labels({
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
                "South Node": "Nodo Sul",
                "Chiron": "Quíron",
                "Ascendant": "Ascendente",
                "Midheaven": "Meio do Céu",
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
                "Pisces": "Peixes",
                "House": "Casa",
                "Conjunction": "Conjunção",
                "Opposition": "Oposição",
                "Trine": "Trígono",
                "Square": "Quadratura",
                "Sextile": "Sextil"
            })
        
        # Configurar aspectos
        if not data.show_aspects:
            chart.set_show_aspects(False)
        
        # Gerar o SVG
        svg_content = chart.get_svg_string()
        
        # Retornar o SVG como resposta
        return Response(
            content=svg_content,
            media_type="image/svg+xml",
            headers={"Content-Disposition": f"attachment; filename=chart_{data.natal_chart.name or 'natal'}.svg"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico SVG: {str(e)}")

@router.post("/svg_chart_base64", response_model=Dict[str, str])
async def generate_svg_chart_base64(data: SVGChartRequest):
    """
    Gera um gráfico SVG e retorna como string base64.
    Útil para incorporação em aplicações web.
    """
    try:
        # Reutilizar a lógica do endpoint anterior
        svg_response = await generate_svg_chart(data)
        svg_content = svg_response.body
        
        # Converter para base64
        base64_svg = base64.b64encode(svg_content).decode("utf-8")
        
        # Retornar como JSON
        return {
            "svg_base64": base64_svg,
            "data_uri": f"data:image/svg+xml;base64,{base64_svg}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico SVG em base64: {str(e)}")
```

## 4. Atualização do Arquivo Principal

Vamos atualizar o arquivo principal para incluir o novo router:

```python
# Em main.py
from fastapi import FastAPI
from app.routers import natal_chart_router, transit_router, svg_chart_router
import uvicorn

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
    
    ## Geração de Gráficos SVG
    
    A API suporta a geração de gráficos SVG para mapas natais, trânsitos e combinações.
    Os gráficos podem ser personalizados com diferentes temas, idiomas e configurações.
    """,
    version="1.0.0"
)

app.include_router(natal_chart_router.router)
app.include_router(transit_router.router)
app.include_router(svg_chart_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 5. Adaptações para o Kerykeion

Dependendo da versão do Kerykeion, pode ser necessário fazer algumas adaptações na classe `MakeSvgChart`. Se a classe não tiver métodos como `set_theme`, `set_language_labels` ou `set_show_aspects`, precisaremos criar uma classe personalizada que estenda a funcionalidade original:

```python
# Em app/utils/svg_chart_utils.py
from kerykeion.charts import MakeSvgChart as OriginalMakeSvgChart
import re

class EnhancedSvgChart(OriginalMakeSvgChart):
    """
    Versão estendida da classe MakeSvgChart do Kerykeion com suporte adicional
    para personalização de tema, idioma e aspectos.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language_labels = {}
        self.theme = "light"
        self.show_aspects = True
    
    def set_theme(self, theme):
        """Define o tema do gráfico (light ou dark)."""
        self.theme = theme
        
        if theme == "dark":
            # Substituir cores no SVG para tema escuro
            self.svg_string = self.svg_string.replace("#FFFFFF", "#121212")  # Fundo
            self.svg_string = self.svg_string.replace("#000000", "#FFFFFF")  # Texto
            # Outras substituições de cores conforme necessário
    
    def set_language_labels(self, labels_dict):
        """Define rótulos traduzidos para o gráfico."""
        self.language_labels = labels_dict
        
        # Aplicar traduções ao SVG
        svg = self.svg_string
        for en_label, pt_label in labels_dict.items():
            # Substituir textos preservando case-sensitivity
            pattern = re.compile(re.escape(en_label), re.IGNORECASE)
            svg = pattern.sub(pt_label, svg)
        
        self.svg_string = svg
    
    def set_show_aspects(self, show):
        """Define se os aspectos devem ser mostrados no gráfico."""
        self.show_aspects = show
        
        if not show:
            # Remover linhas de aspectos do SVG
            # Isso é uma simplificação, a implementação real dependeria da estrutura do SVG
            pattern = re.compile(r'<line.*?class="aspect-line".*?/>', re.DOTALL)
            self.svg_string = pattern.sub('', self.svg_string)
    
    def get_svg_string(self):
        """Retorna a string SVG com todas as personalizações aplicadas."""
        return self.svg_string
```

Se necessário, podemos substituir a importação no router:

```python
# Em app/routers/svg_chart_router.py
from app.utils.svg_chart_utils import EnhancedSvgChart as MakeSvgChart
```

## 6. Testes e Validação

Para testar a implementação, podemos criar um script que faz uma requisição ao endpoint e salva o SVG gerado:

```python
# Em tests/test_svg_chart.py
import requests
import base64
import json

def test_svg_chart():
    # Dados de teste
    data = {
        "natal_chart": {
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
        },
        "chart_type": "natal",
        "show_aspects": True,
        "language": "pt",
        "theme": "light"
    }
    
    # Testar endpoint SVG direto
    response = requests.post(
        "http://localhost:8000/api/v1/svg_chart",
        json=data,
        headers={"Accept": "image/svg+xml"}
    )
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/svg+xml"
    
    # Salvar o SVG em um arquivo
    with open("test_chart.svg", "wb") as f:
        f.write(response.content)
    
    print("SVG salvo em test_chart.svg")
    
    # Testar endpoint base64
    response = requests.post(
        "http://localhost:8000/api/v1/svg_chart_base64",
        json=data
    )
    
    assert response.status_code == 200
    result = response.json()
    
    assert "svg_base64" in result
    assert "data_uri" in result
    
    # Decodificar e salvar o SVG
    svg_content = base64.b64decode(result["svg_base64"])
    with open("test_chart_base64.svg", "wb") as f:
        f.write(svg_content)
    
    print("SVG de base64 salvo em test_chart_base64.svg")
    
    # Testar com trânsitos
    data["transit_chart"] = {
        "year": 2025,
        "month": 5,
        "day": 28,
        "hour": 12,
        "minute": 0,
        "longitude": 10.0,
        "latitude": 48.4,
        "tz_str": "Europe/Berlin",
        "house_system": "Placidus"
    }
    data["chart_type"] = "combined"
    
    response = requests.post(
        "http://localhost:8000/api/v1/svg_chart",
        json=data,
        headers={"Accept": "image/svg+xml"}
    )
    
    assert response.status_code == 200
    
    # Salvar o SVG combinado em um arquivo
    with open("test_combined_chart.svg", "wb") as f:
        f.write(response.content)
    
    print("SVG combinado salvo em test_combined_chart.svg")
    
    print("Teste concluído com sucesso!")

if __name__ == "__main__":
    test_svg_chart()
```

## 7. Considerações Adicionais

1. **Personalização Avançada**: Podemos expandir a API para permitir personalização mais avançada dos gráficos, como cores específicas, tamanho, fontes, etc.

2. **Caching**: Implementar cache para gráficos frequentemente solicitados para melhorar o desempenho.

3. **Formatos Alternativos**: Além de SVG, podemos oferecer outros formatos como PNG ou PDF.

4. **Integração com Frontend**: Fornecer exemplos de como integrar os gráficos SVG em aplicações frontend.

5. **Acessibilidade**: Garantir que os gráficos SVG gerados sejam acessíveis, incluindo textos alternativos e outras práticas recomendadas.

Esta implementação fornece um endpoint robusto para geração de gráficos SVG de mapas astrológicos, com suporte para personalização de tema, idioma e configurações. A API pode ser facilmente estendida para suportar mais opções de personalização no futuro.
