from typing import Optional, Dict, Any
from pydantic import BaseModel

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

class PlanetData(BaseModel):
    name: str
    sign: str
    sign_num: int
    position: float
    abs_pos: float
    house_name: str
    speed: float
    retrograde: bool

class HouseCuspData(BaseModel):
    name: str
    sign: str
    position: float

class AspectData(BaseModel):
    planet1: str
    planet2: str
    aspect_type: str
    orbit: float

class NatalChartResponse(BaseModel):
    input_data: NatalChartRequest
    sun: PlanetData
    moon: PlanetData
    mercury: PlanetData
    venus: PlanetData
    mars: PlanetData
    jupiter: PlanetData
    saturn: PlanetData
    uranus: PlanetData
    neptune: PlanetData
    pluto: PlanetData
    north_node: Optional[PlanetData] = None
    south_node: Optional[PlanetData] = None
    chiron: Optional[PlanetData] = None
    houses: Dict[str, HouseCuspData]
    ascendant: HouseCuspData
    midheaven: HouseCuspData
    aspects: list[AspectData]

class TransitRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    longitude: float
    latitude: float
    tz_str: str

class TransitResponse(BaseModel):
    planets: list[PlanetData]

class TransitsToNatalRequest(BaseModel):
    natal_data: NatalChartRequest
    transit_data: TransitRequest

class TransitsToNatalResponse(BaseModel):
    transit_positions: list[PlanetData]
    aspects_to_natal: list[AspectData]
