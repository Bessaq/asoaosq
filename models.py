from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal

class PlanetPosition(BaseModel):
    name: str
    sign: str
    sign_num: int
    position: float = Field(..., description="Grau decimal no signo")
    abs_pos: float = Field(..., description="Longitude eclíptica absoluta em graus decimais")
    house_name: str
    speed: float
    retrograde: bool

class HouseCusp(BaseModel):
    name: str
    sign: str
    position: float = Field(..., description="Grau decimal no signo")

class AscMc(BaseModel):
    sign: str
    position: float = Field(..., description="Grau decimal no signo")

class Aspect(BaseModel):
    planet1: str
    planet2: str
    aspect_name: str
    orbit: float

class NatalChartRequest(BaseModel):
    name: Optional[str] = "NatalChart"
    year: int
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    tz_str: str = Field(..., description="Ex: America/Sao_Paulo")
    house_system: Optional[str] = "Placidus"

class NatalChartResponse(BaseModel):
    input_data: NatalChartRequest
    sun: PlanetPosition
    moon: PlanetPosition
    mercury: PlanetPosition
    venus: PlanetPosition
    mars: PlanetPosition
    jupiter: PlanetPosition
    saturn: PlanetPosition
    uranus: PlanetPosition
    neptune: PlanetPosition
    pluto: PlanetPosition
    mean_node: Optional[PlanetPosition] = None # Nodo Norte Médio
    true_node: Optional[PlanetPosition] = None # Nodo Norte Verdadeiro (Kerykeion pode fornecer um ou ambos)
    chiron: Optional[PlanetPosition] = None
    lilith: Optional[PlanetPosition] = None # Lilith Média (Mean Apogee)
    houses: List[HouseCusp]
    ascendant: AscMc
    mc: AscMc
    aspects: List[Aspect]
    # Opcional: distribuição por elemento e qualidade
    # element_distribution: Optional[dict] = None
    # quality_distribution: Optional[dict] = None

class TransitRequest(BaseModel):
    year: int
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    tz_str: str

class CurrentTransitsResponse(BaseModel):
    input_data: TransitRequest
    planets: List[PlanetPosition]

class TransitsToNatalRequest(BaseModel):
    natal_data: NatalChartRequest
    transit_data: TransitRequest

class TransitAspect(BaseModel):
    transit_planet: str
    natal_planet_or_point: str
    aspect_name: str
    orbit: float

class TransitsToNatalResponse(BaseModel):
    natal_input: NatalChartRequest
    transit_input: TransitRequest
    transit_planets_positions: List[PlanetPosition]
    aspects_to_natal: List[TransitAspect]

class NatalChartSVGRequest(NatalChartRequest):
    pass

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
