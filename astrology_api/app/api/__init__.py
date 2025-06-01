"""
Inicializador do pacote de API.

Este módulo exporta os routers para serem incluídos na aplicação principal.
"""
from .natal_chart_router import router as natal_chart_router
from .transit_router import router as transit_router
from .svg_chart_router_fixed import router as svg_chart_router  # Usando o router fixado
from .synastry_router import router as synastry_router
from .progression_router import router as progression_router
from .return_router import router as return_router
from .direction_router import router as direction_router
