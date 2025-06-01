from typing import Optional, Dict, Any, Literal, List
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

class HouseCuspData(BaseModel):
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

class NatalChartResponse(BaseModel):
    input_data: NatalChartRequest
    planets: Dict[str, PlanetData]
    houses: Dict[str, HouseCuspData]
    ascendant: HouseCuspData
    midheaven: HouseCuspData
    aspects: List[AspectData] = Field(default_factory=list, description="Aspects between planets")
    house_system: Optional[HouseSystemType] = Field(default="Placidus", description="Sistema de casas utilizado")
    interpretations: Optional[Dict[str, Any]] = None

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
    language: Optional[Literal["en", "pt"]] = Field(default="pt", description="Idioma para os textos na resposta")
    include_interpretations: bool = Field(default=False, description="Se deve incluir interpretações textuais na resposta")

class TransitResponse(BaseModel):
    input_data: TransitRequest
    planets: Dict[str, PlanetData]
    house_system: Optional[HouseSystemType] = Field(default="Placidus", description="Sistema de casas utilizado")
    interpretations: Optional[Dict[str, Any]] = None

class TransitsToNatalRequest(BaseModel):
    natal: NatalChartRequest
    transit: TransitRequest
    include_interpretations: bool = Field(default=False, description="Se deve incluir interpretações textuais na resposta")

class TransitsToNatalResponse(BaseModel):
    input_data: TransitsToNatalRequest
    natal_planets: Dict[str, PlanetData]
    transit_planets: Dict[str, PlanetData]
    aspects: List[AspectData] = Field(default_factory=list, description="Aspects between transit and natal planets")
    natal_house_system: Optional[HouseSystemType] = Field(default="Placidus", description="Sistema de casas utilizado para o mapa natal")
    transit_house_system: Optional[HouseSystemType] = Field(default="Placidus", description="Sistema de casas utilizado para os trânsitos")
    interpretations: Optional[Dict[str, Any]] = None

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

class InterpretationResponse(BaseModel):
    interpretations: Dict[str, Any]
