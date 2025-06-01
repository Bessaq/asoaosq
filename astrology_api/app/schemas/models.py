"""
Modelos Pydantic para a aplicação AstroAPI.

Este arquivo contém os modelos Pydantic que definem a estrutura
de requisições e respostas da API.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Literal

# Definição de tipos literais para sistemas de casas
HouseSystemType = Literal[
    "Placidus", "Koch", "Porphyrius", "Regiomontanus", "Campanus", 
    "Equal", "Whole Sign", "Alcabitus", "Morinus", "Horizontal", 
    "Topocentric", "Vehlow"
]

# Definição de tipos literais para idiomas suportados
LanguageType = Literal["pt", "en", "es"]

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

# Classes para requisições

class NatalChartRequest(BaseModel):
    """
    Modelo para requisição de mapa natal.
    """
    name: Optional[str] = Field(None, description="Nome da pessoa ou evento")
    year: int = Field(..., description="Ano de nascimento")
    month: int = Field(..., ge=1, le=12, description="Mês de nascimento (1-12)")
    day: int = Field(..., ge=1, le=31, description="Dia de nascimento (1-31)")
    hour: int = Field(..., ge=0, le=23, description="Hora de nascimento (0-23)")
    minute: int = Field(..., ge=0, le=59, description="Minuto de nascimento (0-59)")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude do local de nascimento")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude do local de nascimento")
    tz_str: str = Field(..., description="String de fuso horário (ex: 'America/Sao_Paulo')")
    house_system: Optional[HouseSystemType] = Field("Placidus", description="Sistema de casas a ser utilizado")
    language: Optional[LanguageType] = Field("pt", description="Idioma para textos na resposta")
    include_interpretations: bool = Field(False, description="Se deve incluir interpretações textuais na resposta")

class TransitRequest(BaseModel):
    """
    Modelo para requisição de trânsitos.
    """
    year: int = Field(..., description="Ano do trânsito")
    month: int = Field(..., ge=1, le=12, description="Mês do trânsito (1-12)")
    day: int = Field(..., ge=1, le=31, description="Dia do trânsito (1-31)")
    hour: int = Field(..., ge=0, le=23, description="Hora do trânsito (0-23)")
    minute: int = Field(..., ge=0, le=59, description="Minuto do trânsito (0-59)")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude do local do trânsito")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude do local do trânsito")
    tz_str: str = Field(..., description="String de fuso horário (ex: 'America/Sao_Paulo')")
    house_system: Optional[HouseSystemType] = Field("Placidus", description="Sistema de casas a ser utilizado")
    language: Optional[LanguageType] = Field("pt", description="Idioma para textos na resposta")
    include_interpretations: bool = Field(False, description="Se deve incluir interpretações textuais na resposta")

class TransitsToNatalRequest(BaseModel):
    """
    Modelo para requisição de trânsitos sobre mapa natal.
    """
    natal: NatalChartRequest = Field(..., description="Dados do mapa natal")
    transit: TransitRequest = Field(..., description="Dados do trânsito")
    include_interpretations: bool = Field(False, description="Se deve incluir interpretações textuais na resposta")

class SVGChartRequest(BaseModel):
    """
    Modelo para requisição de gráfico SVG.
    """
    natal_chart: NatalChartRequest = Field(..., description="Dados do mapa natal")
    transit_chart: Optional[TransitRequest] = Field(None, description="Dados do trânsito (opcional)")
    chart_type: Literal["natal", "transit", "combined"] = Field(
        "natal", 
        description="Tipo de gráfico: 'natal' para apenas mapa natal, 'transit' para apenas trânsitos, 'combined' para mapa natal com trânsitos"
    )
    show_aspects: bool = Field(
        True,
        description="Se deve mostrar linhas de aspectos no gráfico"
    )
    language: LanguageType = Field(
        "pt",
        description="Idioma para os textos no gráfico"
    )
    theme: Literal["light", "dark"] = Field(
        "light",
        description="Tema de cores para o gráfico"
    )

# Classes para componentes de resposta

class PlanetData(BaseModel):
    """
    Modelo para dados de um planeta.
    """
    name: str = Field(..., description="Nome do planeta")
    name_original: Optional[str] = Field(None, description="Nome original do planeta em inglês")
    longitude: float = Field(..., description="Longitude eclíptica do planeta")
    latitude: float = Field(..., description="Latitude eclíptica do planeta")
    sign: str = Field(..., description="Signo zodiacal do planeta")
    sign_original: Optional[str] = Field(None, description="Nome original do signo em inglês")
    sign_num: int = Field(..., description="Número do signo (1-12)")
    house: int = Field(..., description="Casa astrológica do planeta (1-12)")
    retrograde: bool = Field(..., description="Se o planeta está retrógrado")
    speed: float = Field(..., description="Velocidade do planeta")

class HouseCuspData(BaseModel):
    """
    Modelo para dados de uma cúspide de casa.
    """
    number: int = Field(..., description="Número da casa (1-12)")
    sign: str = Field(..., description="Signo zodiacal da cúspide")
    sign_original: Optional[str] = Field(None, description="Nome original do signo em inglês")
    sign_num: int = Field(..., description="Número do signo (1-12)")
    longitude: float = Field(..., description="Longitude eclíptica da cúspide")

class AspectData(BaseModel):
    """
    Modelo para dados de um aspecto.
    """
    p1_name: str = Field(..., description="Nome do primeiro planeta/ponto")
    p1_name_original: Optional[str] = Field(None, description="Nome original do primeiro planeta/ponto em inglês")
    p1_owner: str = Field(..., description="Proprietário do primeiro planeta/ponto (natal/trânsito)")
    p2_name: str = Field(..., description="Nome do segundo planeta/ponto")
    p2_name_original: Optional[str] = Field(None, description="Nome original do segundo planeta/ponto em inglês")
    p2_owner: str = Field(..., description="Proprietário do segundo planeta/ponto (natal/trânsito)")
    aspect: str = Field(..., description="Nome do aspecto")
    aspect_original: Optional[str] = Field(None, description="Nome original do aspecto em inglês")
    orbit: float = Field(..., description="Orbe do aspecto")
    aspect_degrees: float = Field(..., description="Graus do aspecto")
    diff: float = Field(..., description="Diferença em graus")
    applying: bool = Field(..., description="Se o aspecto está se aplicando (true) ou separando (false)")

# Classes para respostas

class NatalChartResponse(BaseModel):
    """
    Modelo para resposta de mapa natal.
    """
    input_data: NatalChartRequest = Field(..., description="Dados de entrada da requisição")
    planets: Dict[str, PlanetData] = Field(..., description="Dados dos planetas")
    houses: Dict[str, HouseCuspData] = Field(..., description="Dados das casas")
    ascendant: HouseCuspData = Field(..., description="Dados do Ascendente")
    midheaven: HouseCuspData = Field(..., description="Dados do Meio-do-Céu")
    aspects: List[AspectData] = Field(default_factory=list, description="Aspectos entre planetas")
    house_system: HouseSystemType = Field(..., description="Sistema de casas utilizado")
    interpretations: Optional[Dict[str, Any]] = Field(None, description="Interpretações textuais (opcional)")

class TransitResponse(BaseModel):
    """
    Modelo para resposta de trânsitos.
    """
    input_data: TransitRequest = Field(..., description="Dados de entrada da requisição")
    planets: Dict[str, PlanetData] = Field(..., description="Dados dos planetas em trânsito")
    house_system: HouseSystemType = Field(..., description="Sistema de casas utilizado")
    interpretations: Optional[Dict[str, Any]] = Field(None, description="Interpretações textuais (opcional)")

class TransitsToNatalResponse(BaseModel):
    """
    Modelo para resposta de trânsitos sobre mapa natal.
    """
    input_data: TransitsToNatalRequest = Field(..., description="Dados de entrada da requisição")
    natal_planets: Dict[str, PlanetData] = Field(..., description="Dados dos planetas natais")
    transit_planets: Dict[str, PlanetData] = Field(..., description="Dados dos planetas em trânsito")
    aspects: List[AspectData] = Field(default_factory=list, description="Aspectos entre planetas em trânsito e natais")
    natal_house_system: HouseSystemType = Field(..., description="Sistema de casas utilizado para o mapa natal")
    transit_house_system: HouseSystemType = Field(..., description="Sistema de casas utilizado para os trânsitos")
    interpretations: Optional[Dict[str, Any]] = Field(None, description="Interpretações textuais (opcional)")

class SVGChartResponse(BaseModel):
    """
    Modelo para resposta de gráfico SVG.
    """
    svg_image: str = Field(..., description="Conteúdo SVG do gráfico")

class SVGChartBase64Response(BaseModel):
    """
    Modelo para resposta de gráfico SVG em Base64.
    """
    svg_base64: str = Field(..., description="Conteúdo SVG do gráfico em Base64")
    data_uri: str = Field(..., description="URI de dados do SVG em Base64")

class InterpretationResponse(BaseModel):
    """
    Modelo para resposta de interpretações.
    """
    interpretations: Dict[str, Any] = Field(..., description="Interpretações textuais")

class SynastryRequest(BaseModel):
    """
    Modelo para requisição de sinastria (comparação de mapas natais).
    """
    chart1: NatalChartRequest = Field(..., description="Dados do primeiro mapa natal")
    chart2: NatalChartRequest = Field(..., description="Dados do segundo mapa natal")
    language: Optional[LanguageType] = Field("pt", description="Idioma para textos na resposta")
    include_interpretations: bool = Field(False, description="Se deve incluir interpretações textuais na resposta")

class SynastryResponse(BaseModel):
    """
    Modelo para resposta de sinastria.
    """
    input_data: SynastryRequest = Field(..., description="Dados de entrada da requisição")
    chart1_planets: Dict[str, PlanetData] = Field(..., description="Dados dos planetas do primeiro mapa")
    chart2_planets: Dict[str, PlanetData] = Field(..., description="Dados dos planetas do segundo mapa")
    aspects: List[AspectData] = Field(default_factory=list, description="Aspectos entre planetas dos dois mapas")
    chart1_house_system: HouseSystemType = Field(..., description="Sistema de casas utilizado para o primeiro mapa")
    chart2_house_system: HouseSystemType = Field(..., description="Sistema de casas utilizado para o segundo mapa")
    interpretations: Optional[Dict[str, Any]] = Field(None, description="Interpretações textuais (opcional)")

class ProgressionDateRequest(BaseModel):
    """
    Modelo para dados de data de progressão.
    """
    year: int = Field(..., description="Ano da progressão")
    month: int = Field(..., ge=1, le=12, description="Mês da progressão (1-12)")
    day: int = Field(..., ge=1, le=31, description="Dia da progressão (1-31)")

class ProgressionRequest(BaseModel):
    """
    Modelo para requisição de progressões secundárias.
    """
    natal_chart: NatalChartRequest = Field(..., description="Dados do mapa natal")
    progression_date: ProgressionDateRequest = Field(..., description="Data para a progressão")
    include_natal_comparison: bool = Field(True, description="Se deve incluir comparação com mapa natal")
    language: Optional[LanguageType] = Field("pt", description="Idioma para textos na resposta")
    include_interpretations: bool = Field(False, description="Se deve incluir interpretações textuais na resposta")

class ProgressionResponse(BaseModel):
    """
    Modelo para resposta de progressões secundárias.
    """
    input_data: ProgressionRequest = Field(..., description="Dados de entrada da requisição")
    progressed_planets: Dict[str, PlanetData] = Field(..., description="Dados dos planetas progressados")
    natal_houses: Dict[str, HouseCuspData] = Field(..., description="Dados das casas natais")
    aspects: List[AspectData] = Field(default_factory=list, description="Aspectos entre planetas progressados e natais")
    house_system: HouseSystemType = Field(..., description="Sistema de casas utilizado")
    interpretations: Optional[Dict[str, Any]] = Field(None, description="Interpretações textuais (opcional)")

class ReturnRequest(BaseModel):
    """
    Modelo para requisição de retornos solares ou lunares.
    """
    natal_chart: NatalChartRequest = Field(..., description="Dados do mapa natal")
    return_year: int = Field(..., description="Ano para o retorno")
    return_month: Optional[int] = Field(None, ge=1, le=12, description="Mês para o retorno (usado apenas para retorno lunar)")
    location_longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude do local do retorno (se diferente do local de nascimento)")
    location_latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude do local do retorno (se diferente do local de nascimento)")
    location_tz_str: Optional[str] = Field(None, description="String de fuso horário para o local do retorno (se diferente do local de nascimento)")
    include_natal_comparison: bool = Field(True, description="Se deve incluir comparação com mapa natal")
    language: Optional[LanguageType] = Field("pt", description="Idioma para textos na resposta")
    include_interpretations: bool = Field(False, description="Se deve incluir interpretações textuais na resposta")

class ReturnResponse(BaseModel):
    """
    Modelo para resposta de retornos solares ou lunares.
    """
    input_data: ReturnRequest = Field(..., description="Dados de entrada da requisição")
    return_planets: Dict[str, PlanetData] = Field(..., description="Dados dos planetas do retorno")
    return_houses: Dict[str, HouseCuspData] = Field(..., description="Dados das casas do retorno")
    return_date: str = Field(..., description="Data e hora exata do retorno")
    aspects: List[AspectData] = Field(default_factory=list, description="Aspectos entre planetas do retorno e natais")
    house_system: HouseSystemType = Field(..., description="Sistema de casas utilizado")
    interpretations: Optional[Dict[str, Any]] = Field(None, description="Interpretações textuais (opcional)")

class DirectionRequest(BaseModel):
    """
    Modelo para requisição de direções solares.
    """
    natal_chart: NatalChartRequest = Field(..., description="Dados do mapa natal")
    direction_date: ProgressionDateRequest = Field(..., description="Data para a direção")
    direction_type: Literal["solar_arc", "primary"] = Field("solar_arc", description="Tipo de direção")
    include_natal_comparison: bool = Field(True, description="Se deve incluir comparação com mapa natal")
    language: Optional[LanguageType] = Field("pt", description="Idioma para textos na resposta")
    include_interpretations: bool = Field(False, description="Se deve incluir interpretações textuais na resposta")

class DirectionResponse(BaseModel):
    """
    Modelo para resposta de direções solares.
    """
    input_data: DirectionRequest = Field(..., description="Dados de entrada da requisição")
    directed_planets: Dict[str, PlanetData] = Field(..., description="Dados dos planetas direcionados")
    natal_houses: Dict[str, HouseCuspData] = Field(..., description="Dados das casas natais")
    direction_value: float = Field(..., description="Valor da direção em graus")
    aspects: List[AspectData] = Field(default_factory=list, description="Aspectos entre planetas direcionados e natais")
    house_system: HouseSystemType = Field(..., description="Sistema de casas utilizado")
    interpretations: Optional[Dict[str, Any]] = Field(None, description="Interpretações textuais (opcional)")
